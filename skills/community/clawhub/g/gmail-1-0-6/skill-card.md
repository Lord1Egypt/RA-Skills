## Description: <br>
Gmail API integration with managed OAuth for reading, sending, and managing emails, threads, labels, and drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobbyzzhao](https://clawhub.ai/user/bobbyzzhao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to Gmail through Maton-managed OAuth, then inspect messages and threads or perform mailbox actions such as sending mail, changing labels, trashing messages, and managing drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent sensitive Gmail access, including reading email content and metadata. <br>
Mitigation: Install only when you trust Maton with the connected Gmail account and configure the agent to ask for explicit confirmation before reading sensitive threads. <br>
Risk: The skill supports mailbox-changing actions such as sending mail, sending drafts, changing labels, trashing messages, and deleting OAuth connections. <br>
Mitigation: Require explicit user approval before any send, draft-send, label change, trash/delete, or connection-deletion action. <br>
Risk: The skill depends on a Maton API key and managed OAuth connection. <br>
Mitigation: Store MATON_API_KEY securely, avoid exposing it in logs or prompts, and periodically review active Gmail connections. <br>


## Reference(s): <br>
- [ClawHub: Gmail 1.0.6](https://clawhub.ai/bobbyzzhao/gmail-1-0-6) <br>
- [Gmail API REST Reference](https://developers.google.com/gmail/api/reference/rest) <br>
- [Gmail API: List Messages](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list) <br>
- [Gmail API: Send Message](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send) <br>
- [Gmail API: Create Draft](https://developers.google.com/gmail/api/reference/rest/v1/users.drafts/create) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, API calls, configuration] <br>
**Output Format:** [Markdown with Python and JavaScript examples, HTTP endpoint examples, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY.] <br>

## Skill Version(s): <br>
1.0.6 (source: _meta.json; release version 1.0.0 in server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
