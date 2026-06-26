## Description: <br>
Send an email by specifying the receiver's address, subject, and content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhaoYaofeng168](https://clawhub.ai/user/ZhaoYaofeng168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send a single SMTP email notification when a recipient, subject, and message body are supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a reusable corporate SMTP password. <br>
Mitigation: Rotate the exposed password before use and replace hardcoded credentials with a user-managed secret. <br>
Risk: The skill can send arbitrary outbound email without clear confirmation controls. <br>
Mitigation: Require explicit confirmation of the recipient, subject, and body before sending any email. <br>
Risk: The security verdict is suspicious. <br>
Mitigation: Review carefully before installing or deploying the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhaoYaofeng168/mysendemail) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ZhaoYaofeng168) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends outbound email through SMTP using receiver, subject, and content parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
