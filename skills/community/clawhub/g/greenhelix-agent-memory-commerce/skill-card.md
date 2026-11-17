## Description:

Agent Memory for Commerce helps developers build commerce agents that remember customers, maintain transaction state across sessions, and reconcile billing context at scale using a tiered memory architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to design memory-backed commerce agents that persist customer context, transaction state, reconciliation data, and audit records across sessions and agent handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide includes production-style commerce memory examples that handle customer and payment-flow state.

Mitigation: Review examples before real deployment, minimize stored audit and handoff fields, and validate payment-flow state against an authoritative source before persisting it.

Risk: Examples use external GreenHelix endpoints and API credentials.

Mitigation: Pin and validate GreenHelix endpoints before sending API keys, and keep GREENHELIX_API_KEY, WALLET_ADDRESS, and REDIS_URL in a protected environment.

Risk: Agent handoff examples can expose transaction context if recipients are not authorized.

Mitigation: Require recipient authorization for agent handoffs and avoid using session tokens as identity lookup values or Redis key material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/greenhelix-agent-memory-commerce)
- [ClawHub Publisher Profile](https://clawhub.ai/user/mirni)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API Endpoint](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guide with Python code examples and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples reference GREENHELIX_API_KEY, WALLET_ADDRESS, and REDIS_URL.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
