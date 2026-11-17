## Description:

Use when a Polymarket outcome appears to overreact and then stall away from recent filled-price range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading-strategy agents use this skill to evaluate Polymarket outcomes for overreaction-fade setups and structure a backtest around filled trade history before considering live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading-analysis guidance may be mistaken for financial advice or used without independent validation.

Mitigation: Treat outputs as decision support only and independently verify liquidity, recent catalysts, time to resolution, spreads, and position sizing before live trading.

Risk: Backtests using filled TradeTick history cannot validate resting liquidity, spread paid, or missed maker-queue execution.

Mitigation: Review live order-book depth and execution costs, then paper trade or run small controlled tests before deploying the strategy.

Risk: Real information shocks and markets near resolution may trend to 0 or 1 instead of mean-reverting.

Mitigation: Exclude near-resolution markets and suspend use when fresh decisive catalysts change the probability thesis.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested strategyConfig parameters and trading-risk caveats.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
