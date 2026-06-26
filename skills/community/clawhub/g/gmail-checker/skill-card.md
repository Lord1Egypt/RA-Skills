## Description: <br>
Send, read, search, draft, reply to, and manage Gmail messages through the Gmail REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cehd5170](https://clawhub.ai/user/cehd5170) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and developers use this skill to let an agent work with Gmail messages, drafts, replies, searches, labels, and read state through OAuth-authenticated Gmail API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Gmail read, send, and mailbox-change capability. <br>
Mitigation: Install only when that access is acceptable, use the narrowest OAuth scopes possible, and revoke tokens when finished. <br>
Risk: The skill lacks clear confirmation safeguards for email sending, message body changes, attachments, external research sources, labels, and read-state changes. <br>
Mitigation: Require the agent to confirm exact recipients, message body, attachments, external research sources, and label or read-state changes before acting. <br>
Risk: Long-lived refresh tokens can preserve Gmail access beyond a single session. <br>
Mitigation: Avoid refresh tokens unless needed and store any client secrets or refresh tokens outside shared prompts or logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cehd5170/gmail-checker) <br>
- [Google Cloud OAuth credentials](https://console.cloud.google.com/apis/credentials) <br>
- [Gmail API enablement](https://console.cloud.google.com/apis/library/gmail.googleapis.com) <br>
- [Gmail API send endpoint](https://gmail.googleapis.com/gmail/v1/users/me/messages/send) <br>
- [OAuth token endpoint](https://oauth2.googleapis.com/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash, JSON, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, GMAIL_ACCESS_TOKEN, Gmail API network access, and OAuth scopes for send, readonly, or modify operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
