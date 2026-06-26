## Description: <br>
Analyzes A-share stock technical conditions with trend, moving average, MACD, Bollinger Band, volume, and support-resistance evidence, using Investoday finance data to identify stock codes and produce a structured technical analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate structured technical analysis reports for A-share stocks from a stock name or 6-digit code. It focuses on current price state, trend direction, position, support and resistance, and volume confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the separate investoday-finance-data skill for market data. <br>
Mitigation: Install and use it only if that dependency is trusted and available. <br>
Risk: Stock names or codes may be sent to the finance-data provider during analysis. <br>
Mitigation: Use the skill for public stock technical analysis and avoid entering sensitive personal or proprietary trading context. <br>
Risk: Technical-analysis output may be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational, verify important conclusions independently, and do not use the report as the sole basis for investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-stock-technical-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown technical analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires investoday-finance-data for public market data; conclusions are informational and not investment advice.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
