## Description: <br>
Calculates 20-day moving-average deviation and historical percentile references for supported Chinese ETF tickers using public Eastmoney market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyonsli](https://clawhub.ai/user/lyonsli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate reference-only moving-average deviation, current price, 20-day average, and historical percentile information for a fixed set of ETF tickers. It supports single-ticker and batch analysis but is not a financial adviser and should not be used as the sole basis for trading or position-sizing decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides market-data calculations that could be mistaken for investment advice. <br>
Mitigation: Keep the output framed as reference-only data and require users to make their own investment decisions. <br>
Risk: Eastmoney public market data may be delayed, unavailable, incomplete, or inaccurate. <br>
Mitigation: Display the data source and timestamp, and advise users to verify important values with authoritative market-data sources. <br>
Risk: Runtime logs may include the OpenClaw user ID and requested ticker symbols. <br>
Mitigation: Avoid entering sensitive personal or portfolio information and review runtime log retention before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lyonsli/position-deviation-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/lyonsli) <br>
- [Artifact overview page](docs/index.html) <br>
- [Eastmoney quote API endpoint used by artifact](https://push2.eastmoney.com/api/qt/stock/get) <br>
- [Eastmoney historical K-line API endpoint used by artifact](https://push2his.eastmoney.com/api/qt/stock/kline/get) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [JSON response containing a Markdown market-data report and metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include analyzed ticker count, ticker list, data source, and timestamp metadata.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact frontmatter and package.json use 2.0.0-free) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
