## Description: <br>
Send emails via the gomail sender CLI with attachments, templates, and recipient management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[craftslab](https://clawhub.ai/user/craftslab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send SMTP email, notifications, or messages with optional attachments and templates, or to validate recipients with dry-run mode before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates email sending to a downloaded gomail sender CLI with SMTP authority. <br>
Mitigation: Install only from a trusted release source, use a dedicated SMTP account where possible, and review generated commands before execution. <br>
Risk: SMTP credentials and sender details are stored in sender.json-style configuration files. <br>
Mitigation: Replace template values with real credentials only in protected local files, keep secrets out of source control, and restrict file access. <br>
Risk: Incorrect recipients or attachments could send email to unintended parties or leak information. <br>
Mitigation: Verify recipients and attachment paths before sending, and use --dry-run to validate recipients without sending mail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/craftslab/gomail) <br>
- [gomail releases](https://github.com/craftslab/gomail/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include recipient validation output when --dry-run is used; sending behavior depends on the external gomail sender CLI and SMTP configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
