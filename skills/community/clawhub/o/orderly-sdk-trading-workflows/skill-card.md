## Description:

Complete trading workflows for Orderly Network DEX applications, from wallet connection through order execution, position management, and withdrawal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers building Orderly Network DEX interfaces or trading bots use this skill to implement wallet authentication, deposits, order execution, position monitoring, leverage management, risk checks, and withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deposit, withdrawal, leverage, order, and close-position paths may affect real funds if used directly in production code.

Mitigation: Require human confirmation, parameter review, validation, pending-state protection, and tests before executing or deploying generated trading flows.

Risk: The security evidence reports underdeveloped safety controls and one verified order-direction bug in the trading workflow examples.

Mitigation: Test the exact submitted side, symbol, quantity, price, and reduce-only settings for each generated order path before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tarnadas/skills/orderly-sdk-trading-workflows)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown with TypeScript and TSX code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow examples for wallet connection, deposits, orders, positions, leverage, risk monitoring, and withdrawals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
