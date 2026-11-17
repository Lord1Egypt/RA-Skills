## Description:

Place live bets on Polymarket CLOB with EIP-712 signing on Polygon. Handles USDC.e approval, order submission, and position tracking. Use for Polymarket automation, live crypto betting, or prediction market trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamierossouw](https://clawhub.ai/user/jamierossouw)

### License/Terms of Use:


## Use Case:

Developers and external trading operators use this skill to automate Polymarket CLOB betting workflows on Polygon, including USDC.e approval, EIP-712 signing, order submission, and position tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that approve tokens, request wallet signatures, and submit real Polymarket orders.

Mitigation: Require explicit confirmation before any token approval, signature, or order submission, and use only wallets, funds, markets, and limits chosen by the operator.

Risk: The server security summary says the skill is under-scoped for actions involving real on-chain orders.

Mitigation: Prefer testnet, simulation, or a low-balance wallet until the workflow is reviewed and proven safe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamierossouw/skills/polymarket-live-bet)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide live trading actions that involve token approvals, EIP-712 signatures, and order submissions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
