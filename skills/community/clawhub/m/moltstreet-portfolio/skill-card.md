## Description: <br>
AI-powered ETF portfolio analysis for comparing signals across asset classes for allocation decisions, free with no API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fredxyt](https://clawhub.ai/user/fredxyt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to compare ETF signal data across holdings or asset classes for allocation, diversification, rebalancing, and risk-management decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ETF signals may be mistaken for personalized financial advice or a complete portfolio recommendation. <br>
Mitigation: Present results as informational signal data, disclose that it is not financial advice, and recommend independent review before investment decisions. <br>
Risk: Ticker symbols or portfolio holdings sent for analysis may reveal user investment interests to MoltStreet. <br>
Mitigation: Avoid sending brokerage credentials, account numbers, balances, or sensitive private portfolio details; use only tickers necessary for analysis. <br>
Risk: API data updates multiple times daily and is not a real-time quote feed. <br>
Mitigation: Do not present responses as live prices; note that signals are one input among others. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fredxyt/moltstreet-portfolio) <br>
- [MoltStreet](https://moltstreet.com) <br>
- [MoltStreet Skill Documentation](https://moltstreet.com/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and ETF signal summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for optional public MoltStreet API lookups; no API key required. Outputs should be treated as informational, not financial advice.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
