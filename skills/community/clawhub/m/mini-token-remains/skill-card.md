## Description: <br>
Checks MiniMax API token usage, including hourly request counts and weekly quota remaining. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regexl](https://clawhub.ai/user/regexl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MiniMax API users use this skill to check local MiniMax API quota status without manually querying the usage endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local MiniMax authentication profile to obtain credentials. <br>
Mitigation: Install and invoke it only when local MiniMax credential access is intended, and review the configured credential source before use. <br>
Risk: The skill makes an authenticated request to MiniMax and may be triggered by broad quota-related phrases. <br>
Mitigation: Use explicit MiniMax-only phrasing when invoking the skill and confirm the endpoint before deployment. <br>


## Reference(s): <br>
- [MiniMax token_plan remains endpoint](https://www.minimaxi.com/v1/token_plan/remains) <br>
- [ClawHub skill page](https://clawhub.ai/regexl/mini-token-remains) <br>
- [Publisher profile](https://clawhub.ai/user/regexl) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Structured text status report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports hourly and weekly MiniMax token usage and remaining quota, or a failure message if the query fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
