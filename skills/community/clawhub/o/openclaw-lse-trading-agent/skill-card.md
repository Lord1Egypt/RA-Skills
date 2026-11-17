## Description:

FTSE 350 trading analysis agent. Screens LSE stocks using technical indicators (Bollinger Bands, RSI, MACD, EMA crossovers, ATR, VWAP, OBV), fetches news for LLM sentiment analysis, synthesises signals into trade recommendations with risk management (Kelly sizing, ATR stops, drawdown circuit breakers), and backtests strategies against historical data.

This skill is for research and development only.

## Publisher:

[ankit-aglawe](https://clawhub.ai/user/ankit-aglawe)

### License/Terms of Use:


## Use Case:

External developers and trading-analysis users use this skill to screen London Stock Exchange equities, inspect technical indicators and news sentiment, backtest strategies, and manage a paper portfolio. It is suitable for educational research and paper-trading workflows, not as dependable financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may over-rely on the trading recommendations or risk checks as dependable financial advice.

Mitigation: Treat the skill as an educational paper-trading tool and independently verify recommendations, position sizing, sector exposure, drawdown, and daily-loss limits before taking action.

Risk: Portfolio commands can modify the local portfolio JSON file.

Mitigation: Back up portfolio JSON before using init, add, or remove operations.

Risk: The workflow depends on uv-run scripts and third-party market/news data retrieval.

Mitigation: Use a trusted or pinned uv installation and review fetched data before relying on the resulting analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ankit-aglawe/skills/openclaw-lse-trading-agent)
- [Publisher profile](https://clawhub.ai/user/ankit-aglawe)
- [Homepage declared in artifact metadata](https://github.com/ankit-aglawe/openclaw-lse-trading-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown analysis with tables, inline shell commands, and JSON script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses uv-run Python scripts for market data, indicators, backtesting, risk checks, sentiment headline retrieval, and local paper-portfolio JSON updates.]

## Skill Version(s):

0.1.1 (source: evidence.release.version and target metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
