## Description:

Get the optimal LP strategy for a token pair by recommending Uniswap version, fee tier, range width, and rebalance approach based on pair characteristics, historical data, and risk tolerance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users, developers, and DeFi operators use this skill to evaluate Uniswap liquidity-provider strategy for a token pair, including pool version, fee tier, range width, rebalance timing, expected returns, and impermanent-loss risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill produces liquidity-provider strategy guidance involving APY and impermanent-loss estimates.

Mitigation: Treat recommendations as decision support, review assumptions before acting, and do not use the output as automatic execution instructions.

Risk: Mutable installation commands such as @latest or main can change what is installed over time.

Mitigation: Prefer a pinned ClawHub or package version and an immutable Git commit before installation.

Risk: Delegated agents such as lp-strategist, pool-researcher, or risk-assessor may affect recommendation quality.

Mitigation: Review those agents separately before relying on the combined workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/optimize-lp)
- [Skill specification](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [analysis, guidance, markdown]

**Output Format:** [Markdown or plain text strategy recommendation with pool, range, APY, impermanent-loss, rebalance, risk, and alternative-strategy sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces financial strategy guidance only; it does not execute liquidity-management actions.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
