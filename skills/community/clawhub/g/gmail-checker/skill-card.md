## Description:

Send, read, search, and manage Gmail emails via the Gmail REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cehd5170](https://clawhub.ai/user/cehd5170)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent send, read, search, reply to, draft, and label Gmail messages through the Gmail REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send, read, and modify Gmail messages using powerful Gmail credentials.

Mitigation: Use the narrowest OAuth scopes practical for the task and require manual confirmation before sending, replying, changing labels, marking messages, or performing bulk mailbox actions.

Risk: Long-lived refresh tokens and access tokens can expose mailbox access if included in prompts, logs, or shared artifacts.

Mitigation: Store credentials only in environment variables or a secrets manager, keep them out of prompts and logs, and avoid long-lived refresh tokens unless necessary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cehd5170/skills/gmail-checker)
- [Publisher Profile](https://clawhub.ai/user/cehd5170)
- [Google Cloud OAuth Credentials](https://console.cloud.google.com/apis/credentials)
- [Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com)
- [Gmail Send Scope](https://www.googleapis.com/auth/gmail.send)
- [Gmail Readonly Scope](https://www.googleapis.com/auth/gmail.readonly)
- [Gmail Modify Scope](https://www.googleapis.com/auth/gmail.modify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, YAML, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Gmail OAuth bearer tokens and requires curl, jq, and GMAIL_ACCESS_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
