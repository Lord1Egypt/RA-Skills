## Description:

Helps agents send and track transactional email and manage Mailgun domains, routes, templates, mailing lists, suppressions, and webhooks through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage Mailgun email delivery and account resources, including sending messages, monitoring events, and configuring domains or webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A connected account grants access to Mailgun data through Maton.

Mitigation: Connect only an intended account, limit authorization to needed scopes, and review access before use.

Risk: Sending mail or changing and deleting account resources can affect recipients and operations.

Mitigation: Confirm every send, write, and delete with the user before executing it.

Risk: Triggers and destinations can forward data persistently to external URLs.

Mitigation: Require explicit approval for hosted functions, triggers, destinations, and each third-party URL.

Risk: API keys used outside the CLI can expose account access.

Mitigation: Prefer managed login and avoid exposing or storing API keys in commands, code, or logs.

## Reference(s):

- [Mailgun skill release](https://clawhub.ai/byungkyu/skills/mailgun-api)
- [Maton](https://maton.ai)
- [Mailgun API documentation](https://documentation.mailgun.com/docs/mailgun/api-reference/api-overview)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mailgun responses may contain personal or business data.]

## Skill Version(s):

1.2.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
