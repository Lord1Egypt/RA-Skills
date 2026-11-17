## Description:

Build autonomous P2P energy trading agents for prosumer microgrids, including prosumer registration, smart meter integration, dynamic pricing, escrow-protected settlement, microgrid orchestration, EV charging coordination, and compliance reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and energy platform teams use this skill as a guide for building agent workflows that trade energy between prosumers, coordinate microgrid assets, handle escrow settlement, and prepare compliance reports. The guidance is especially relevant to sandbox-first prototyping before connecting real payment credentials, smart-meter data, or physical energy assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial escrow and payment workflows could affect real funds if examples are adapted without production controls.

Mitigation: Use sandbox credentials first; require explicit owner consent, operator approval workflows, transaction limits, idempotency, rollback, and reconciliation before using production payment keys.

Risk: Smart-meter and battery-control workflows could affect physical energy assets if connected directly to real devices.

Mitigation: Do not connect real smart-meter data or physical battery controllers until device-scoped authorization and local safety interlocks are in place.

Risk: The guide is not a drop-in production recipe for regulated energy trading.

Mitigation: Treat the examples as high-impact integration guidance and require qualified operational, security, and regulatory review before deployment.

## Reference(s):

- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)
- [ClawHub skill page](https://clawhub.ai/mirni/skills/greenhelix-agent-energy-p2p-trading)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown guide with Python code examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples reference GREENHELIX_API_KEY and STRIPE_API_KEY.]

## Skill Version(s):

1.3.1 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
