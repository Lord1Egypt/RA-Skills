## Description:

kenoodl is an orthogonal injection engine that sends an agent's working context to an external synthesis service and returns cross-domain structure for problems where the agent is looping or losing novelty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenoodl-synthesis](https://clawhub.ai/user/kenoodl-synthesis)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to let an agent submit sanitized working context to kenoodl.com when it detects stagnation, then integrate the returned synthesis into ongoing reasoning or coding work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends working context to kenoodl.com for external synthesis.

Mitigation: Sanitize every payload and exclude secrets, credentials, private customer data, proprietary code, and regulated information unless the exact payload is explicitly approved.

Risk: The skill describes funded token and autonomous crypto payment flows.

Mitigation: Require human approval for paid calls and disable or avoid autonomous wallet and payment flows.

Risk: On-chain calldata can expose submitted context.

Mitigation: Do not submit sensitive context on-chain; use an approved encrypted path only when the payload and encryption behavior have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenoodl-synthesis/skills/kenoodl-synthesis)
- [Publisher profile](https://clawhub.ai/user/kenoodl-synthesis)
- [kenoodl API documentation](https://kenoodl.com/api)
- [kenoodl OpenAPI specification](https://kenoodl.com/api/openapi.json)
- [kenoodl agent card](https://kenoodl.com/.well-known/agent-card.json)
- [kenoodl AI discovery document](https://kenoodl.com/.well-known/ai.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTTP examples, curl commands, JSON snippets, and MCP text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include queued job IDs, polling status, account balance text, or synthesis content returned by the external service.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
