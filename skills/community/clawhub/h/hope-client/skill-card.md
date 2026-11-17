## Description:

Hope Client helps agents make authenticated Hope Server Max API requests for channel, upload, download, account, and engine management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query and manage Hope Server Max resources through documented API endpoints and reusable shell helper functions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes live-looking API key and SSH password defaults.

Mitigation: Rotate any real exposed secrets, remove default credentials, and require explicit user-provided secrets before use.

Risk: Password-based SSH and API helper commands can access sensitive data and modify server state.

Mitigation: Tightly scope SSH/API access, validate command inputs, redact sensitive fields, and require confirmation before write operations.

## Reference(s):

- [Hope Client ClawHub Release](https://clawhub.ai/linux2010/skills/hope-client)
- [Common Queries](artifact/references/common-queries.md)
- [Response Format](artifact/references/response-format.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Hope Server Max host and API key environment configuration.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
