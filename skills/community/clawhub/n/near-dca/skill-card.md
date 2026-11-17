## Description:

Dollar-cost averaging for NEAR tokens with flexible scheduling, performance tracking, and cancellation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:

MIT

## Use Case:

Developers and NEAR users can use this skill to create, manage, pause, resume, and review dollar-cost averaging strategies for NEAR token purchases. It also tracks purchase history, calculates average cost basis, and exposes alert configuration for executions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents automated NEAR investing behavior while the reviewed release uses mock prices and fabricated transaction hashes.

Mitigation: Treat execution results as simulation until real price feeds, signed on-chain submission, receipt verification, confirmations, and clear simulation labels are implemented.

Risk: Wallet credentials can be supplied through configuration or action parameters.

Mitigation: Do not provide real NEAR private keys or funded accounts during review; use secure credential storage and testnet or unfunded accounts.

Risk: Scheduled execution could repeatedly act on strategies after real trading integration is added.

Mitigation: Keep scheduled execution disabled for funded accounts until spending limits, confirmation flows, receipt verification, and dependency updates are reviewed.

## Reference(s):

- [NEAR DeFi](https://near.org/defi/)
- [Ref Finance](https://ref.finance/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [JSON action responses and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON state for strategies, purchase history, and alert settings.]

## Skill Version(s):

1.0.0 (source: package.json, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
