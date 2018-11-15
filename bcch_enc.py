from pyparsing import Literal, CaselessLiteral, Word,delimitedList, Optional, \
    Combine, Group, alphas, nums, alphanums, ParseException, Forward, oneOf, quotedString, \
    ZeroOrMore, restOfLine, Keyword, Regex

def test( str ):
    #print(str,"->")
    try:
        tokens = simpleBCCH.parseString( str )
        print tokens
        #print tokens.asList()
        '''
		print("message = ",        messageToken)
        print("messageValue = ", bcchMsgTypeToken)
        print("dl-Bandwdith = ", tokens.dlBandwidth)
        print("phich-Duration = ", tokens.phichDuration)
        print("phich-Resource = ", tokens.phichResource)
        print("systemFrameNumber = ", tokens.systemFrameNumber)
        print("spare = ", tokens.spare)
        print tokens.asDict()
		'''
    except ParseException as err:
        print(" "*err.loc + "^\n" + err.msg)
        print(err)
    #print()

	
sequenceToken = Keyword("SEQUENCE", caseless=True)
bcchToken = Keyword("BCCH-BCH-Message", caseless=True)
bcchMsgTypeToken = Keyword("BCCH-BCH-MessageType",caseless=True)
masterInfoBlockToken = Keyword("MasterInformationBlock")
messageToken = Keyword("message", caseless=True)

dlBandwidthToken = Keyword("dl-Bandwidth", caseless=True)
PHICHConfigToken = Keyword("PHICH-Config", caseless=True)
systemFrameNumberToken = Keyword("systemFrameNumber", caseless=True)
spareToken = Keyword("spare", caseless=True)
phichDurationToken = Keyword("phich-Duration", caseless=True)
phichResourceToken = Keyword("phich-Resource", caseless=True)
 
dlBandwidthValue = oneOf("n6 n15 n25 n50 n75 n100", caseless=True).setResultsName( "dlBandwidth" )

systemFrameNumberValue = Word(nums,exact=8).setResultsName("systemFrameNumber")

spareValue =  Word(nums, exact=10).setResultsName("spare")

dlBandwidth = (dlBandwidthToken + dlBandwidthValue)

phichDuration = phichDurationToken + oneOf("normal extended").setResultsName("phichDuration")
phichResource = phichResourceToken + oneOf("oneSixth half one two").setResultsName("phichResource")

PHICHConfigClause = (phichDuration + "," + phichResource)

PHICHConfig = (PHICHConfigToken + sequenceToken + "{" + PHICHConfigClause + "}")

systemFrameNumber = (systemFrameNumberToken + systemFrameNumberValue)
spare = (spareToken + spareValue)

masterInfoBlockClause = (dlBandwidth + "," + PHICHConfig + "," + systemFrameNumber + "," + spare)

#masterInfoBlockClause = Word(nums)

masterInfoBlock = (masterInfoBlockToken + sequenceToken + "{" + masterInfoBlockClause + "}")

bcchMsgType = (bcchMsgTypeToken + "{" + masterInfoBlock + "}")
#sequenceClause = Forward()
message = (messageToken + "{" + bcchMsgType + "}")

bcchStmt = Forward()
bcchStmt	<< (bcchToken  + sequenceToken + "{" + message + "}")

simpleBCCH = bcchStmt 


msg1= '''
BCCH-BCH-Message SEQUENCE {
  message  { 
    BCCH-BCH-MessageType {
      MasterInformationBlock SEQUENCE {
		dl-Bandwidth n50,
		PHICH-Config SEQUENCE {
			phich-Duration normal,
            phich-Resource two
		},
		systemFrameNumber 10100110,
		spare 0000000000
      }    
    }
  }
}
'''

#test(msg1)

bcchTokens=simpleBCCH.parseString( msg1 )

bcchEncStr=""

#2018-11-12: start encoding
bcch_dlBandwidth={'n6':"000",'n15':"001",'n25':"010",'n50':"011",'n75':"100",'n100':"101"}
bcch_phichDuration={'normal':"0",'extended':"1"}
bcch_phichResource={'oneSixth':"00",'half':"01",'one':"10",'two':"11"}

bcchEncStr=bcch_dlBandwidth[bcchTokens.dlBandwidth] + bcch_phichDuration[bcchTokens.phichDuration] + bcch_phichResource[bcchTokens.phichResource] + bcchTokens.systemFrameNumber + bcchTokens.spare
#print bcchEncStr
bcchHexStr=hex(int(bcchEncStr,2))
print bcchHexStr.upper()[2:]


#bcchList=simpleBCCH.parseString( msg1 ).asList()
#print bcchList

#test(msg1)









