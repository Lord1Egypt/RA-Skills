## Description: <br>
Access JPX stock market data via the J-Quants API, including stock search, daily OHLCV prices, financial summaries, and earnings calendars for Tokyo Stock Exchange listed companies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and market-data users use this skill to query J-Quants market data for TSE-listed companies, including stock lookup, price history, financial metrics, and earnings dates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires J-Quants account credentials through environment variables. <br>
Mitigation: Provide only the required J-Quants credentials and confirm the installed jquants-mcp package source is trusted before use. <br>
Risk: Retrieved market data may be subject to J-Quants personal-use and redistribution restrictions. <br>
Mitigation: Review and follow J-Quants terms before using or sharing retrieved market data. <br>


## Reference(s): <br>
- [J-Quants](https://jpx-jquants.com/) <br>
- [J-Quants Terms of Service](https://jpx-jquants.com/termsofservice) <br>
- [ClawHub Skill Page](https://clawhub.ai/ajtgjmdjp/jquants-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the jquants-mcp command and JQUANTS_MAIL_ADDRESS and JQUANTS_PASSWORD environment variables.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
