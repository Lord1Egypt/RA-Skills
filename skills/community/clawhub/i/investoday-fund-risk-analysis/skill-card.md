## Description: <br>
Analyzes public fund risk using Investoday financial data, focusing on drawdown, volatility, downside risk, VaR, Beta, Sharpe ratio, and risk-return fit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance-focused agents use this skill to turn a fund name or six-digit fund code into a structured fund risk report. The report covers fund risk profile, drawdown, volatility, downside risk, risk-adjusted return, market sensitivity, fund manager context, and follow-up risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on investoday-finance-data for actual data access, so incorrect, stale, or unavailable upstream fund data can affect the report. <br>
Mitigation: Review and approve the investoday-finance-data dependency separately, and surface data gaps as insufficient evidence rather than definitive conclusions. <br>
Risk: Fund risk analysis can be mistaken for investment advice or trading guidance. <br>
Mitigation: Keep outputs informational, avoid subscription, redemption, timing, and position-sizing recommendations, and preserve the skill's requirement to explain each risk conclusion with numeric evidence. <br>
Risk: Ambiguous fund names can resolve to the wrong product. <br>
Mitigation: Use entity recognition for names and request a fuller name or six-digit fund code when identification is not stable and unique. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-fund-risk-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown fund risk analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the investoday-finance-data skill for market data access; reports are informational and do not provide trading, subscription, redemption, timing, or position-sizing advice.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
