## Description: <br>
Complete service registrations autonomously by receiving verification codes. Also: send and receive emails, monitor inbox, search by keyword, download attachments, view threads, filter by label, extract structured data, manage mailbox and webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[digidai](https://clawhub.ai/user/digidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with a controlled mailbox API for registration verification, inbox search, message sending, attachment retrieval, structured extraction, and mailbox or webhook management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can delete mailbox messages or pause mailbox operations. <br>
Mitigation: Confirm before deleting messages or pausing the mailbox, especially outside disposable or controlled email workflows. <br>
Risk: Agents can send email from the controlled mailbox. <br>
Mitigation: Confirm recipient, subject, body, and attachments before sending mail. <br>
Risk: Agents can change mailbox and label webhook URLs. <br>
Mitigation: Use only webhook destinations controlled by the operator and confirm webhook changes before applying them. <br>


## Reference(s): <br>
- [Mails for Agent on ClawHub](https://clawhub.ai/digidai/mails-for-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP request guidance and JSON request or response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAILS_API_URL, MAILS_AUTH_TOKEN, and MAILS_MAILBOX environment variables.] <br>

## Skill Version(s): <br>
1.8.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
