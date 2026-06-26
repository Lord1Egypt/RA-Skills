## Description: <br>
Gmail API integration with smart AI features - read, send, search, and manage emails with Claude-powered summarization and drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to let an agent read, search, send, reply to, label, archive, and trash Gmail messages from a terminal workflow. Optional AI features summarize unread mail, draft replies, and prioritize messages through EvoLink when an API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI commands may handle email text unsafely, and server evidence says a crafted email could run local code when AI features are used. <br>
Mitigation: Do not use AI commands on real mail until email content is safely JSON-encoded without code interpolation. <br>
Risk: The skill can send, reply, archive, trash, label, and otherwise modify Gmail messages. <br>
Mitigation: Use a dedicated Gmail account for testing and confirm every send, reply, archive, trash, and label operation before execution. <br>
Risk: Google OAuth credentials and tokens grant access to the connected Gmail account. <br>
Mitigation: Store local credentials and tokens carefully, revoke tokens when finished, and use the documented revoke command or Google Account permissions page. <br>
Risk: Optional AI features transmit email subject, sender, and body content to api.evolink.ai. <br>
Mitigation: Avoid EvoLink AI features for sensitive email unless the user has reviewed the data-sharing behavior and explicitly accepts it. <br>


## Reference(s): <br>
- [Gmail API Parameter Reference](references/api-params.md) <br>
- [EvoLink Claude Messages API](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=gmail) <br>
- [Gmail API Reference](https://developers.google.com/gmail/api/reference/rest) <br>
- [Gmail Search Operators](https://support.google.com/mail/answer/7190) <br>
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown instructions, and shell command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core Gmail actions use Google OAuth credentials; optional AI actions require EVOLINK_API_KEY and may send email content to api.evolink.ai.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
