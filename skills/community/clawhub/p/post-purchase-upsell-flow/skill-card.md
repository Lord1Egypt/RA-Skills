## Description:

Design and implement one-click post-purchase upsells and downsells that raise average order value without hurting the main conversion rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autonnel](https://clawhub.ai/user/autonnel)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketers, and developers use this skill to design post-purchase upsell and downsell flows, define one-click payment requirements, and measure AOV gains without degrading base checkout conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following external Docker setup instructions without review could expose unintended ports, volumes, privileges, or secrets.

Mitigation: Review the referenced repository, check out a trusted release or commit, inspect docker-compose.yml, and test payment flows with low-risk test credentials before connecting production accounts.

Risk: An untested upsell payment flow could create duplicate charges, refund problems, or chargeback pressure.

Mitigation: Run an end-to-end paid test, including acceptance, decline, and refund paths, before sending live traffic.

## Reference(s):

- [Autonnel repository](https://github.com/autonnel/autonnel)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables, flow diagrams, implementation notes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ecommerce offer design, payment-flow requirements, measurement guidance, and implementation checks.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
