## Description:

Operate LINE Messaging API through UXC with a curated OpenAPI schema, bearer-token auth, and messaging-core guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure bearer-token access and run supported LINE Messaging API read, messaging, quota, and webhook endpoint operations through UXC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a privileged LINE channel bearer token with a generated UXC client.

Mitigation: Install only from trusted schema sources, bind credentials to api.line.me, and keep the token in the LINE_CHANNEL_ACCESS_TOKEN environment variable.

Risk: Message send operations and webhook endpoint changes can affect real LINE users or delivery configuration.

Mitigation: Require explicit approval before push, reply, webhook update, or webhook test operations, and prefer read-only validation before writes.

Risk: Release security evidence reports a mutable remote schema link.

Mitigation: Prefer the bundled schema or a pinned commit or digest before granting credentials to generated API commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jolestar/skills/line-openapi-skill)
- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/line-messaging.openapi.json)
- [LINE Messaging API reference](https://developers.line.biz/en/reference/messaging-api/)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses UXC's JSON output envelope for API responses and errors.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
