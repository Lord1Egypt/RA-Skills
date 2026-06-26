## Description: <br>
Sends email through SMTP with configurable recipients, subject, and body, using an email account and app password for authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jaskies](https://clawhub.ai/user/Jaskies) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to send plain-text email through an SMTP server after configuring account credentials such as a Gmail App Password. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SMTP script requires email credentials or an app password to send mail. <br>
Mitigation: Use provider-specific app passwords where available, pass secrets through environment variables or a secret manager, and avoid placing credentials in prompts, command history, or committed files. <br>
Risk: Running the script can send account-changing outbound email to an external recipient. <br>
Mitigation: Review recipient, subject, body, sender account, and SMTP server before execution, and test with a controlled recipient before production use. <br>
Risk: The security evidence reports a clean verdict but notes limited artifact review context. <br>
Mitigation: Review the bundled files and installation instructions before use, especially any request to read private data, run shell commands, or store credentials. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/Jaskies/mail-sender-jaskies) <br>
- [Google Account](https://myaccount.google.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and environment variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces email-sending guidance and invokes SMTP when the bundled script is run with credentials and message fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
