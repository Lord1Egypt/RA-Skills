## Description:

OpenClaw API reference documentation with examples for authentication, chat, sessions, messages, skills, configuration, users, webhooks, errors, and SDK usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration teams use this skill as a concise OpenClaw API reference for constructing authenticated requests, managing chat resources, using webhooks, handling errors, and installing SDK clients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reference includes DELETE operations and configuration updates that could remove OpenClaw data or alter runtime behavior if used with broad credentials.

Mitigation: Use least-privilege API keys and require explicit confirmation before DELETE, PATCH, or other state-changing API calls.

Risk: The reference includes skill execution and skill creation examples that could run or create agent behavior.

Mitigation: Require review and confirmation before running or creating skills, and restrict these actions to trusted workspaces and credentials.

Risk: The SDK installation examples do not pin package versions.

Mitigation: Pin or verify SDK package versions before installation in production or shared environments.

## Reference(s):

- [OpenClaw API base URL](http://localhost:3000/api/v1)
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-api-reference)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with API endpoint examples, JSON payloads, shell commands, and SDK code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language API reference content with examples for JavaScript/TypeScript and Python SDK use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
