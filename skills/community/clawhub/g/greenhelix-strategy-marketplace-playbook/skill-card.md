## Description:

The Agent Strategy Marketplace Playbook is a guide to selling verified trading strategies with escrow-protected subscriptions, covering marketplace listings, performance verification, subscription management, and dispute resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and strategy sellers use this guide to structure GreenHelix marketplace listings, escrow-protected subscriptions, performance proofs, and dispute workflows for trading strategy services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-paste examples can contact GreenHelix with user credentials and create listings, escrows, dispute actions, messages, or metric submissions.

Mitigation: Run examples with sandbox credentials first and add explicit approval checks before using production endpoints.

Risk: The guide references API credentials and an agent signing key that could affect account actions if exposed.

Mitigation: Store keys in a secrets manager or local environment, never paste private signing keys into chats or logs, and rotate credentials if exposure is suspected.

Risk: Automated escrow release, dispute resolution, and subscriber messaging examples can change commercial outcomes.

Mitigation: Review these flows before deployment and require human approval for release, resolution, and outbound subscriber communication steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirni/skills/greenhelix-strategy-marketplace-playbook)
- [GreenHelix Sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API Documentation](https://api.greenhelix.net/docs)
- [Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; authenticated examples require GREENHELIX_API_KEY and AGENT_SIGNING_KEY.]

## Skill Version(s):

1.3.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
