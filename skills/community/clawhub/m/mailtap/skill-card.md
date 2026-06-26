## Description: <br>
Generate and manage temporary disposable email addresses valid for 30 minutes to receive and retrieve verification emails and messages without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zororaka00](https://clawhub.ai/user/zororaka00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create short-lived disposable email addresses, poll inboxes for verification messages, and retrieve available attachment metadata for authorized testing, signup, privacy, or automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disposable inboxes and attachments are public, low-sensitivity data and are unsuitable for sensitive accounts, financial services, production account recovery, personal documents, or confidential messages. <br>
Mitigation: Use the skill only for authorized low-risk testing, signup, privacy, or automation workflows, and avoid sending or receiving sensitive information through generated addresses. <br>
Risk: Email bodies and downloaded attachments can contain untrusted content. <br>
Mitigation: Treat all messages and attachments as untrusted, download attachments only to a dedicated folder, validate file type and size, and do not execute downloaded files. <br>


## Reference(s): <br>
- [Mailtap ClawHub page](https://clawhub.ai/zororaka00/mailtap) <br>
- [Publisher profile](https://clawhub.ai/user/zororaka00) <br>
- [Official MailTap service](https://www.mailtap.org) <br>
- [MailTap API root](https://api.mailtap.org) <br>
- [OpenAPI specification](openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with JSON examples, shell commands, and Python helper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interacts with public MailTap API endpoints and returns disposable email, inbox, message, and attachment metadata.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
