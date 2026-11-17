## Description:

Use the Luckin Coffee connector to find stores and products, inspect and preview orders, and create or cancel orders through a connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to find Luckin Coffee stores and products, inspect order details, preview orders, and manage orders through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run downloaded software, and the required CLI may make broader changes to agent skills that the instructions do not explain.

Mitigation: Review and approve CLI installation separately, control automatic skill synchronization, connect only the intended Luckin Coffee account, and retain order confirmations.

## Reference(s):

- [Luckin Coffee connector documentation](https://open.lkcoffee.com/mcp)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands]

**Output Format:** [JSON connector responses and oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Order creation and cancellation require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
