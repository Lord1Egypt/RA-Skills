## Description: <br>
Send plain-text emails through the user's local msmtp configuration, using an existing ~/.msmtprc setup and without reading inbox data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[izombix](https://clawhub.ai/user/izombix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send short notifications, test messages, alerts, or other trusted plain-text email from a locally configured msmtp account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email from the account configured in ~/.msmtprc. <br>
Mitigation: Review the recipient, subject, and body before invocation and install only when outbound email from that account is intended. <br>
Risk: Plain-text email bodies may expose secrets or regulated data if included by the user or agent. <br>
Mitigation: Avoid sending secrets or regulated data and keep ~/.msmtprc private with restrictive file permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/izombix/msmtp-send) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>
- [Google app passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain-text email fields and shell command invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Send-only; no attachments, HTML email, inbox access, or message retrieval.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
