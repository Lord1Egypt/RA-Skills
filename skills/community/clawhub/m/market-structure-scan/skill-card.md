## Description: <br>
Multi-timeframe market scanner that uses Ichimoku Cloud, Bollinger Bands, MACD, RSI, Fibonacci ratios, EMA Ribbon, and Linear Regression to produce confluence scores and informational signals across asset classes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigedsherer-ctrl](https://clawhub.ai/user/bigedsherer-ctrl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to scan a requested ticker or market symbol across 5m, 1h, and 4h timeframes, then summarize technical-indicator alignment as an analysis-only confluence score and signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces technical-analysis signals that could be mistaken for financial or trading advice. <br>
Mitigation: Treat results as informational analysis only, verify with independent sources, and make trading or investment decisions outside this skill. <br>
Risk: Public market-data pages can be delayed, unavailable, incomplete, or inconsistent across providers. <br>
Mitigation: Check source timestamps and compare the generated summary with authoritative market data before relying on any indicator value. <br>
Risk: Ticker or symbol queries are sent to public market-data sites during browsing. <br>
Mitigation: Use explicit public tickers or coin slugs and avoid entering private portfolio details or sensitive trading plans. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bigedsherer-ctrl/market-structure-scan) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/bigedsherer-ctrl) <br>
- [TradingView Symbols](https://www.tradingview.com/symbols/) <br>
- [Investing.com Technical Analysis](https://www.investing.com/technical/) <br>
- [Yahoo Finance Quotes](https://finance.yahoo.com/quote/) <br>
- [CoinGecko Coins](https://www.coingecko.com/en/coins/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted market-structure summary with timestamp, confluence score, indicator breakdown by timeframe, signal, and key observation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis-only output; normal operation browses public market-data pages for the requested ticker or symbol.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
