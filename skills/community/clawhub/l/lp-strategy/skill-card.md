## Description:

Comprehensive LP strategy comparison for a token pair, evaluating versions, fee tiers, range widths, rebalance approaches, APY, impermanent loss, gas costs, and risk ratings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers, DeFi operators, and liquidity providers use this skill to compare Uniswap LP options for a token pair across pool versions, fee tiers, range widths, rebalance approaches, and chains before choosing a strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LP strategy analysis can mislead users if pool data, APY, impermanent loss, gas costs, or risk assumptions are stale or incorrect.

Mitigation: Verify pool data and risk assumptions independently before relying on the analysis for financial decisions.

Risk: Installing a third-party skill from an untrusted or moving source can introduce supply-chain risk.

Mitigation: Install only from a trusted publisher and prefer pinned package versions or fixed commits instead of latest or main.

Risk: The analysis could be mistaken for authorization to move funds or add liquidity.

Mitigation: Confirm any separate liquidity-management action before moving funds; this skill itself produces analysis only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/lp-strategy)
- [Publisher profile](https://clawhub.ai/user/wpank)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with comparison tables and strategy recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces analysis only; it does not execute liquidity transactions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
