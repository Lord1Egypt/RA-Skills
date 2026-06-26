## Description: <br>
Analyzes stock and ETF portfolio screenshots using technical, capital-flow, and fundamental signals, then produces portfolio guidance and new holding recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tingdall](https://clawhub.ai/user/tingdall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors and portfolio analysts use this skill to turn uploaded holdings screenshots into structured A-share, Hong Kong stock, ETF, and fund analysis. It supports pre-market planning, post-market review, position sizing, risk notes, and candidate stock or ETF screening based on public market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce high-stakes buy, sell, target-price, and position-size guidance for financial assets. <br>
Mitigation: Treat outputs as informational analysis only, verify recommendations independently, and consult qualified financial advice before acting. <br>
Risk: Portfolio screenshots may contain account identifiers, balances, holdings, or other personal financial details. <br>
Mitigation: Redact account identifiers and unnecessary personal details before upload, and share only the holdings data needed for analysis. <br>
Risk: Market data may be stale, mixed across dates, or sourced from inconsistent public search results. <br>
Mitigation: Follow the artifact's multi-source verification process, prefer current source timestamps, and label data dates and sources in reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tingdall/portfolio-management) <br>
- [Publisher profile](https://clawhub.ai/user/tingdall) <br>
- [Analysis framework](artifact/analysis-framework.md) <br>
- [Data verification guide](artifact/data-verification-guide.md) <br>
- [Report template](artifact/report-template.md) <br>
- [Stock screening guide](artifact/stock-screening-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports with tables, ratings, portfolio actions, price ranges, target prices, stop-loss levels, and disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source and timestamp annotations for market data; does not execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
