## Description:

Helps agents manage Instantly cold-email campaigns, leads, sending accounts, email, and analytics through a Maton-managed connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and marketing teams and developers use this skill to review outreach results, manage campaigns, leads, and sending accounts, and perform approved email or automation actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected outreach and automation actions can change campaigns, leads, sender accounts, emails, or destinations.

Mitigation: Start with read-only operations and approve each connection, write, send, delete, function, trigger, or destination change explicitly.

Risk: Sharing mailbox passwords or long-lived API keys can expose account access.

Mitigation: Prefer managed OAuth and avoid giving the agent mailbox passwords or long-lived API keys unless absolutely necessary.

## Reference(s):

- [Instantly skill on ClawHub](https://clawhub.ai/byungkyu/skills/instantly)
- [Maton](https://maton.ai)
- [Instantly API reference](https://developer.instantly.ai/api-reference)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.2.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
