## Description: <br>
Gmail API integration with managed OAuth for reading, sending, and managing emails, threads, labels, and drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to access Gmail through Maton-managed OAuth, including mailbox lookup, message sending, label and thread management, and draft workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change content in a connected Gmail mailbox when provided a valid Maton API key and OAuth connection. <br>
Mitigation: Install only if Maton is trusted for the selected account, review Google OAuth permissions, and require the agent to show exact emails, drafts, labels, or threads before approving send, create, update, trash, or delete actions. <br>
Risk: Multiple active Gmail connections can cause actions to target the wrong mailbox. <br>
Mitigation: Specify the intended connection identifier whenever multiple Google Mail connections are active. <br>


## Reference(s): <br>
- [ClawHub Gmail Skill](https://clawhub.ai/byungkyu/gmail) <br>
- [Gmail API REST Reference](https://developers.google.com/gmail/api/reference/rest) <br>
- [Gmail Messages: Send](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Google Mail OAuth connection.] <br>

## Skill Version(s): <br>
1.0.8 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
