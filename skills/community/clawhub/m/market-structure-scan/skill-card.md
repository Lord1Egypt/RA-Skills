## Description:

Rule-based market analysis skill that fetches public market data and summarizes multi-timeframe technical indicators, confluence score, and directional signal without trade execution or financial advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigedsherer-ctrl](https://clawhub.ai/user/bigedsherer-ctrl)

### License/Terms of Use:


## Use Case:

External users and market analysts use this skill to request structured technical analysis for crypto, stocks, metals, and forex across 5m, 1h, and 4h timeframes. It is intended for informational analysis only and does not provide trade recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse external market-data websites and those sources can be delayed, unavailable, incomplete, or inconsistent.

Mitigation: Verify current prices, indicator values, and timezones independently before using the analysis.

Risk: The skill produces market signals that could be mistaken for financial advice.

Mitigation: Treat outputs as informational analysis only and make independent decisions; the skill does not execute trades or provide risk advice.

Risk: The short trigger phrase "mss" may activate the skill unintentionally.

Mitigation: Confirm the requested ticker, market, and timeframe context when a trigger is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigedsherer-ctrl/skills/market-structure-scan)
- [Publisher profile](https://clawhub.ai/user/bigedsherer-ctrl)
- [TradingView symbols](https://www.tradingview.com/symbols/)
- [Investing.com technical analysis](https://www.investing.com/technical/)
- [Yahoo Finance quote pages](https://finance.yahoo.com/quote/)
- [CoinGecko coin pages](https://www.coingecko.com/en/coins/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted market analysis with indicator breakdowns by timeframe]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes EST or Maryland timestamp, confluence score, 5m/1h/4h indicator summaries, signal label, key observation, and analysis-only disclaimer.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
