## Description: <br>
Gold price query tool supporting CNY (RMB/gram) and USD (USD/oz) currency options for real-time spot gold price lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanghaolie](https://clawhub.ai/user/yanghaolie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query current spot gold prices in CNY or USD and receive formatted price, movement, volume, and update-time data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound network requests to jijinhao.com for gold pricing. <br>
Mitigation: Install and run it only in environments where outbound access to that service is acceptable. <br>
Risk: The runtime may not include the aiohttp Python dependency required by the script. <br>
Mitigation: Provide aiohttp in the agent runtime before using the skill. <br>
Risk: The upstream quote service may rate-limit frequent requests. <br>
Mitigation: Use appropriate request intervals when invoking the script repeatedly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanghaolie/gold-price-query) <br>
- [jijinhao.com real-time quote API](https://api.jijinhao.com/quoteCenter/realTime.htm) <br>
- [cngold quote reference](https://quote.cngold.org/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [JSON returned by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports USD output by default and CNY output when the currency parameter is set to CNY.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
