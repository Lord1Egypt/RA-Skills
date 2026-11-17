## Description:

Calculates 20-day moving-average deviation and historical percentile references for four supported ETF tickers using public market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyonsli](https://clawhub.ai/user/lyonsli)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent for Chinese-language ETF moving-average deviation analysis across the supported tickers. The skill returns reference data for portfolio review and explicitly does not provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake ETF deviation and percentile output for investment advice.

Mitigation: Keep the non-advice disclaimer visible and treat results only as reference data for user-directed review.

Risk: Public market data may be delayed, incomplete, or unavailable.

Mitigation: Tell users the data source can lag or fail and avoid making time-sensitive decisions from the output alone.

Risk: Broad trigger wording may invoke the skill for finance questions outside its four supported tickers.

Mitigation: Limit use to the documented ticker list or ask the publisher to narrow the trigger wording.

Risk: The artifact includes an unused, unpinned Python dependency.

Mitigation: Remove the unused dependency or pin it before deployment when Python dependencies are installed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyonsli/skills/position-deviation-analysis)
- [Publisher profile](https://clawhub.ai/user/lyonsli)
- [Artifact documentation](docs/index.html)
- [Eastmoney realtime quote API](https://push2.eastmoney.com/api/qt/stock/get)
- [Eastmoney historical K-line API](https://push2his.eastmoney.com/api/qt/stock/kline/get)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown report with JSON-style status metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language ETF analysis for the supported tickers; data is for reference only and is not investment advice.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
