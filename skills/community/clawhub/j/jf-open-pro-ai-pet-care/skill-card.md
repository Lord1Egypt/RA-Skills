## Description: <br>
Provides developer-facing JF Tech pet-care integration support for abnormal event alerts, pet behavior reports, cloud video archiving, service controls, pet records, and behavior statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill to connect applications or automation workflows to JF Tech pet-monitoring APIs for service status, alert querying, pet record management, and behavior reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses powerful account credentials and tokens for JF Tech APIs. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid TOOLS.md for shared or committed workflows, and never commit tokens or app secrets. <br>
Risk: The included tools can change service state, alert settings, and pet records. <br>
Mitigation: Require explicit human confirmation before service switches, alert configuration changes, or pet record deletion. <br>
Risk: The integration can modify or delete remote pet-care data without strong built-in safeguards. <br>
Mitigation: Limit installation to developer-facing workflows that need write access and review requested actions before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jftech/jf-open-pro-ai-pet-care) <br>
- [JF Tech developer platform](https://developer.jftech.com) <br>
- [JF Tech pet-care API endpoints](https://api-cn.jftechws.com/aisvr/v3/gateway/api/scenepet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JF Tech credentials and device identifiers supplied by the user or deployment environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
