## Description:

Practitioner guide to adding escrow payments, marketplace discovery, reputation-gated hiring, and dispute resolution to CrewAI, LangGraph, and AutoGen multi-agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this guide to add agent-to-agent commerce patterns, including escrow, discovery, reputation-gated hiring, and dispute handling, to CrewAI, LangGraph, and AutoGen workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment examples can create, release, dispute, or refund payments when adapted with live credentials.

Mitigation: Start with sandbox credentials, require explicit approval before fund movement, set strict per-agent budget caps, and allow only authenticated triggers.

Risk: The guide references powerful GreenHelix, signing, and Stripe credentials.

Mitigation: Store credentials in a secrets manager, scope keys to the minimum required permissions, and avoid exposing Stripe or signing keys unless a workflow specifically needs them.

Risk: Illustrative key-generation examples can return private-key material in process memory or logs if copied directly.

Mitigation: Replace returned private-key strings with secrets-manager references and prevent private keys from being committed, logged, or shared between agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-multi-agent-commerce-cookbook)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guide with Python examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing guide; workflows reference GREENHELIX_API_KEY, AGENT_SIGNING_KEY, and STRIPE_API_KEY when used with live services.]

## Skill Version(s):

1.3.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
