## Description: <br>
Builds and runs Python-based options strategy backtests for iron condors, strangles, calendar spreads, and vertical credit spreads, reporting simulated metrics such as win rate, Sharpe ratio, drawdown, expectancy, and estimated profit and loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and trading researchers use this skill to ask an agent to prepare or run Python options strategy backtests and summarize simulated performance metrics for strategy exploration. Review outputs before any trading use because the server security summary says the skill overstates realistic financial backtesting capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat synthetic or simplified backtest outputs as realistic trading evidence. <br>
Mitigation: Treat outputs as synthetic demonstration data unless the missing strategy logic, historical data loading, and documented risk checks are implemented and independently verified. <br>
Risk: The skill may overstate its financial backtesting completeness. <br>
Mitigation: Independently verify strategy logic, data sources, slippage, commissions, implied-volatility behavior, and risk filters before relying on results. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/ssidharhubble/options-trading-backtester) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell command blocks, plus optional JSON backtest output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce simulated financial metrics and generated configuration examples; results require independent review before use.] <br>

## Skill Version(s): <br>
1.0.18 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
