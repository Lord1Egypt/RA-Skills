## Description: <br>
This skill helps agents use JFTech child-care monitoring APIs to manage service status, abnormal alarm settings, alarm queries, stranger records, and child activity statistics for configured home devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate JFTech child monitoring workflows for bound, online devices with an active child-care package. It provides configuration guidance and script-based actions for checking service state, querying alerts, managing stranger records, and reviewing activity counts or time charts. <br>

### Deployment Geography for Use: <br>
China Mainland, Asia, Europe, and North America, based on the documented JFTech service regions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to child-monitoring accounts and remote JFTech APIs, so outputs and API responses may involve sensitive household and child data. <br>
Mitigation: Use the skill only where household privacy, consent, retention, and legal requirements are handled outside the skill, and limit access to authorized users and devices. <br>
Risk: The skill requires app secrets, authorization tokens, user identifiers, and device serial numbers, creating credential exposure risk if values are reused or passed on shared command lines. <br>
Mitigation: Use least-privilege and short-lived credentials where possible, avoid exposing secrets in shared shell history or logs, and rotate any app secret or token that may have been disclosed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-ai-child-care) <br>
- [JFTech Open Platform](https://developer.jftech.com) <br>
- [JFTech signature algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=609261d9bb5049c3a2fc7222adf465fb&lang=zh) <br>
- [JFTech timestamp algorithm documentation](https://docs.jftech.com/docs?menusId=2531aba7e2d84e13ad8ce977007922f3&siderId=8da7ad6119fd41159e2026c71ddb3555&lang=zh) <br>
- [JFTech package card usage documentation](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=d2c0d9105d9c4b78bc0d2ee3851d2557&lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and script-produced text or JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured JFTech credentials, device serial number, user identifier, and network access to JFTech APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
