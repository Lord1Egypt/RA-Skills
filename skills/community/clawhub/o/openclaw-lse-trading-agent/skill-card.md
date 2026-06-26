## Description: <br>
FTSE 350 trading analysis agent. Screens LSE stocks using technical indicators (Bollinger Bands, RSI, MACD, EMA crossovers, ATR, VWAP, OBV), fetches news for LLM sentiment analysis, synthesises signals into trade recommendations with risk management (Kelly sizing, ATR stops, drawdown circuit breakers), and backtests strategies against historical data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ankit-aglawe](https://clawhub.ai/user/ankit-aglawe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to screen and analyze London Stock Exchange equities, retrieve market and news data, backtest signal strategies, validate risk constraints, and manage a local paper portfolio. Outputs should be treated as trading research rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio commands can initialize, add to, remove from, or otherwise change the local paper portfolio file. <br>
Mitigation: Back up data/portfolio.json before using --init, --add, or --remove, and review command arguments before execution. <br>
Risk: The skill fetches market prices and news from Yahoo Finance, so outputs depend on external data availability and freshness. <br>
Mitigation: Confirm important price, news, and corporate-action data against trusted market sources before using the analysis. <br>
Risk: Generated trade recommendations and backtests can be mistaken for financial advice or reliable forecasts. <br>
Mitigation: Treat all outputs as research support, not investment advice, and require independent review before acting. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ankit-aglawe/openclaw-lse-trading-agent) <br>
- [Publisher profile](https://clawhub.ai/user/ankit-aglawe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with inline shell commands and JSON-producing helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local paper portfolio file at data/portfolio.json when portfolio commands are used.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
