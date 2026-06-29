## Description: <br>
Use when a Polymarket outcome price and filled volume are accelerating in the same direction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to identify and frame Polymarket probability-momentum strategies where price and filled volume accelerate together. It supports backtest-oriented analysis with filled TradeTick history and practical strategy-configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading-analysis output could be mistaken for authorization to trade or access user accounts. <br>
Mitigation: Require separate, explicit user approval before any account access or trade placement, and present strategy output as informational. <br>
Risk: Momentum signals can be misleading when liquidity is thin, one large fill dominates the move, or the market is close to resolution. <br>
Mitigation: Check filled-trade depth, notional size, expiry timing, and market-manipulation risk before relying on the signal. <br>
Risk: Filled-trade backtests do not prove maker queue position, maker rebates, or order-book depth. <br>
Mitigation: Treat backtest results as taker-style behavior evidence and avoid claims of execution certainty or spread capture. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and strategy-shape guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Informational trading-analysis output; it does not place trades or access accounts.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
