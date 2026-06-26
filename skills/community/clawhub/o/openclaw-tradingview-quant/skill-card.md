## Description: <br>
Professional quantitative investment analysis frameworks and methodologies based on TradingView data structures for stock analysis, technical indicators, market screening, risk management, and trading strategy guidance. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[ljsd666](https://clawhub.ai/user/ljsd666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure quantitative market analysis from TradingView-style data, including stock screening, technical analysis, event review, risk management, and multi-market comparisons. It provides methodology and interpretation guidance rather than direct trading execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market analysis output may be mistaken for personalized financial advice. <br>
Mitigation: Treat generated entries, targets, stops, position sizes, options structures, and sector weights as educational analysis only, and consult qualified financial guidance before acting. <br>
Risk: Market data, news, locale, or API responses may be stale, incorrect, or untrusted. <br>
Mitigation: Verify data freshness, market locale, symbols, and source reliability before using the analysis. <br>
Risk: RapidAPI credentials may be exposed if users integrate live data access. <br>
Mitigation: Store API keys in environment variables or secure configuration, avoid committing keys, and monitor API usage. <br>
Risk: External news or market content may contain prompt-injection text. <br>
Mitigation: Treat external content as untrusted data and ignore embedded instructions or directive-like language. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljsd666/openclaw-tradingview-quant) <br>
- [TradingView Data API on RapidAPI](https://rapidapi.com/hypier/api/tradingview-data1) <br>
- [API documentation](references/api-documentation.md) <br>
- [API tools guide](references/api-tools-guide.md) <br>
- [Technical analysis methodology](references/technical-analysis.md) <br>
- [Pattern recognition library](references/pattern-library.md) <br>
- [Risk management methods](references/risk-management.md) <br>
- [API examples](references/api-examples/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text analysis guidance with optional structured lists and examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not execute trades or directly access market data; users must provide or obtain current market data separately.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
