## Description:

A guide for building agent-to-agent payment workflows with GreenHelix, covering escrow, split payments, subscriptions, disputes, trust, and Python integration examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this guide to design autonomous B2B payment flows between agents, including wallet setup, service discovery, escrow, subscriptions, disputes, and trust scoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide asks for sensitive credentials, including a Stripe API key and agent signing key.

Mitigation: Use sandbox or tightly scoped test credentials, store secrets outside the skill content, and avoid real Stripe keys or long-lived signing keys unless a reviewed example truly requires them.

Risk: Copy-paste payment, escrow, or subscription flows may be adapted without adequate spending safeguards.

Mitigation: Add production gates, budget limits, human approval points, and recurring-subscription controls before using the flows with real funds.

Risk: Illustrative code may not match a specific deployment environment or current API behavior.

Mitigation: Review and test examples in the GreenHelix sandbox, verify endpoint behavior, and confirm authentication scopes before production use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/mirni/skills/greenhelix-agent-commerce-toolkit)
- [GreenHelix sandbox](https://sandbox.greenhelix.net)
- [GreenHelix API documentation](https://api.greenhelix.net/docs)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guide with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Non-executable guide; live integrations require user-supplied credentials.]

## Skill Version(s):

1.3.1 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
