## Description: <br>
Automates live portfolio tracking and analysis using browser automation on Yahoo Finance, updating portfolio-tracker.md with performance summaries, winners/losers, rebalancing suggestions, and market news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vachanalaviswanath](https://clawhub.ai/user/vachanalaviswanath) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to update a local portfolio tracker from Yahoo Finance prices and generate portfolio performance analysis, including winners/losers, concentration flags, and rebalancing suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording could cause the skill to read holdings, contact Yahoo Finance, or edit a local tracker file without a clear portfolio update request. <br>
Mitigation: Invoke it with explicit portfolio-update requests and review generated tracker changes or logs before sharing them. <br>
Risk: Portfolio holdings and generated summaries may reveal portfolio composition. <br>
Mitigation: Treat holdings and generated output as private financial information and remove sensitive details before sharing. <br>
Risk: Live browser-fetched market data can be stale, incomplete, or misread from page snapshots. <br>
Mitigation: Verify important prices and investment decisions against a trusted brokerage or market data source before acting. <br>


## Reference(s): <br>
- [Portfolio holdings reference](references/portfolio-holdings.md) <br>
- [Portfolio Tracker ClawHub release](https://clawhub.ai/vachanalaviswanath/portfolio-tracker) <br>
- [Yahoo Finance crypto quote example](https://finance.yahoo.com/quote/BTC-USD) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with plain-text analysis and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update portfolio-tracker.md and summarize live market data.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
