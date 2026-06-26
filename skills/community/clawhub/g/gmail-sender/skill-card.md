## Description: <br>
Send emails via Gmail SMTP using a Python CLI tool with a Google App Password for alerts, notifications, and automated reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junkaixue](https://clawhub.ai/user/junkaixue) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators can use this skill to configure Gmail App Password credentials and send automated email notifications, alerts, and reports from command-line or Python subprocess workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes a Gmail-sending executable, but the executable is not included in the artifact for review. <br>
Mitigation: Inspect and trust the actual gmail-send executable before running it, use a dedicated Gmail App Password, verify recipients and message contents, and add scheduled execution only deliberately. <br>


## Reference(s): <br>
- [Google Account Security](https://myaccount.google.com/security) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>
- [ClawHub Skill Page](https://clawhub.ai/junkaixue/gmail-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gmail credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: _meta.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
