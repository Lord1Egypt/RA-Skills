## Description:

Guides developers through building protocol-agnostic copy trading infrastructure with verified leader performance, follower allocation models, slippage handling, performance escrow, revenue sharing, and Python integration examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as a guide for designing copy trading agents and services that use GreenHelix marketplace, event, reputation, and escrow patterns. The artifact is educational and non-executing, with examples that should be hardened before any live trading or fund movement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production-adaptable financial automation examples could be copied into live trading before they are ready.

Mitigation: Treat the code as architecture notes, require paper trading first, and add manual approval thresholds and loss limits before connecting exchange credentials or moving funds.

Risk: Weak signal verification or replay handling could allow incorrect or forged trade actions.

Mitigation: Use authenticated webhooks, real Ed25519 verification, and replay protection before processing leader signals.

Risk: Automatic escrow or revenue-release examples could move funds incorrectly if enforcement is incomplete.

Mitigation: Require server-side escrow enforcement and review automatic release behavior carefully before production use.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/mirni/skills/greenhelix-copy-trading-infrastructure)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API reference](https://api.greenhelix.net/v1)
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guide with Python examples and curl command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executing educational guide; examples reference GREENHELIX_API_KEY and AGENT_SIGNING_KEY.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
