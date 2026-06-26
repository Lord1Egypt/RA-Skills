## Description: <br>
This skill retrieves and displays 24/7 real-time financial news from sources such as Jin10 Data through a Prana remote client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyffeifeifei](https://clawhub.ai/user/cyffeifeifei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request current financial-market news and pass the returned Prana result through to users without rewriting it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and requests are sent to the Prana/ebonex remote backend for execution. <br>
Mitigation: Use the skill only when remote processing is acceptable for the data being submitted. <br>
Risk: The client can fetch or store API credentials in config/api_key.txt. <br>
Mitigation: Prefer environment variables, set PRANA_SKILL_SKIP_WRITE_API_KEY=1 and PRANA_SKILL_NO_AUTO_API_KEY=1 when local credential storage or automatic key creation is not desired, and do not commit config/api_key.txt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyffeifeifei/prana-market-beats) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON response containing server-produced financial-news content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pass-through remote response; agent-run and agent-result output should not be summarized or rewritten.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
