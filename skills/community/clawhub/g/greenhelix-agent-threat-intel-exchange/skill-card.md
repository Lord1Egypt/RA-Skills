## Description:

Agent Threat Intelligence Exchange is a guide for building agent-to-agent threat intelligence marketplaces with STIX/TAXII feed listings, paywall-gated IOC access, reputation-verified intel quality, autonomous SLA negotiation, and compliance-ready audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

SOC developers, security engineers, and agent builders use this guide to design provider and consumer agents for GreenHelix-based threat-intelligence exchange, including IOC feed listing, gated access, SLA negotiation, quality scoring, and compliance audit trails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide describes autonomous live marketplace actions involving payments, SLAs, disputes, and sensitive threat-intelligence data.

Mitigation: Treat the release as a review item before installation or use; require explicit endpoint selection, test-mode confirmation, budget limits, and legal/compliance review before any real GreenHelix account or real threat-intelligence data is used.

Risk: Security evidence reports inconsistent safety framing and flawed access-control examples.

Mitigation: Independently review and fix authorization checks, access gating, and SLA enforcement before adapting examples for production workflows.

Risk: Threat-intelligence exchange can involve handling restrictions and regulated data such as TLP/PAP-labeled intelligence or GDPR-relevant indicators.

Mitigation: Require policy review, TLP/PAP enforcement, audit logging, and human approval for sensitive feeds before enabling autonomous purchase, sharing, or dispute flows.

## Reference(s):

- [Agent Threat Intelligence Exchange on ClawHub](https://clawhub.ai/mirni/skills/greenhelix-agent-threat-intel-exchange)
- [Publisher profile: mirni](https://clawhub.ai/user/mirni)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API documentation](https://api.greenhelix.net/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python examples and API request patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; examples describe GreenHelix API calls and threat-intelligence marketplace workflows.]

## Skill Version(s):

1.3.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
