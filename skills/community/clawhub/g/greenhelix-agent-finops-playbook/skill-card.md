## Description:

Guides developers and platform teams through multi-agent FinOps patterns for per-agent wallets, budget caps, spend alerts, cost attribution, volume discounts, fleet dashboards, and API key isolation using GreenHelix examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and FinOps teams use this guide to design cost controls for multi-agent systems, including wallet isolation, budget enforcement, alerting, attribution, and spend analytics. The artifact is educational and non-executing, but its examples describe live billing, webhook, and API-key operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can affect live billing, webhook, and API-key state if used against production services.

Mitigation: Use a sandbox endpoint and test GreenHelix account first, and do not paste production API keys into examples.

Risk: Webhook-driven pause, kill, or key-revocation actions can disrupt agents if webhook authenticity or replay protection is missing.

Mitigation: Add webhook signature verification and replay protection before connecting alerts to pause, kill, or credential-rotation actions.

Risk: API-key rotation or revocation can invalidate active credentials without a verified fallback.

Mitigation: Test key rotation with rollback before invalidating old credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-finops-playbook)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix developer documentation](https://api.greenhelix.net/docs)
- [FinOps Foundation](https://www.finops.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide; examples reference GREENHELIX_API_KEY and AGENT_SIGNING_KEY environment variables.]

## Skill Version(s):

1.3.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
