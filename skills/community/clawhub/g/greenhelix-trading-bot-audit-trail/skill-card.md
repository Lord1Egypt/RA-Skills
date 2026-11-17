## Description:

Tamper-Proof Audit Trails for Trading Bots. EU AI Act, MiFID II, and SEC 17a-4 compliance audit trail implementation for autonomous trading bots. Includes detailed Python code examples with full API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this guide to design tamper-evident audit trails for autonomous trading bots, including event schemas, signed trade events, Merkle claim chains, webhook forwarding, local buffering, and compliance report examples for financial audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples handle private signing keys used for agent identity.

Mitigation: Do not print or log private signing keys; store keys in a secrets manager and rotate keys through a controlled process.

Risk: Audit events may contain sensitive trading, account, or strategy data.

Mitigation: Redact sensitive fields before sending audit events and confirm platform data handling, retention, and regulatory suitability with compliance counsel.

Risk: Local outage buffers can expose audit data or allow tampering if stored insecurely.

Mitigation: Use restrictive filesystem permissions, encryption at rest, replay controls, and integrity checks for buffered audit events.

Risk: Compliance examples may be incomplete for a specific jurisdiction or trading venue.

Mitigation: Treat the guide as implementation guidance and have compliance counsel validate obligations, retention, data residency, and reporting formats before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/greenhelix-trading-bot-audit-trail)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API Reference](https://api.greenhelix.net/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python examples, shell commands, JSON payloads, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide; references AGENT_SIGNING_KEY as the primary required environment variable.]

## Skill Version(s):

1.3.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
