## Description:

Agent Commerce Discovery. Build machine-readable service catalogs, knowledge graphs, and UCP/MCP/A2A protocol endpoints so AI shopping agents can discover, evaluate, and transact with your services autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and commerce teams use this guide to make services discoverable to AI shopping agents through machine-readable catalogs, knowledge graphs, structured data, and UCP/MCP/A2A protocol endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide references sensitive credentials that may not be needed for every example.

Mitigation: Provide only narrowly scoped credentials required for the specific operation, and avoid supplying Stripe or agent signing keys unless that operation explicitly needs them.

Risk: Copyable production patterns may introduce credential handling or file-write risk if reused without review.

Mitigation: Review examples before production use, validate webhook service identifiers, and restrict any copied file-write or marketplace-update behavior to trusted inputs and hosts.

Risk: API examples can be redirected or adapted to untrusted origins.

Mitigation: Pin the GreenHelix API origin to trusted hosts before using the examples with real credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-commerce-discovery)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API endpoint](https://api.greenhelix.net/v1)
- [Schema.org](https://schema.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide; examples may require user-supplied credentials and review before production use.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
