## Description: <br>
Generates structured valuation analysis reports for Chinese A-share equities using PE, PB, PS, PEG, historical percentile, industry comparison, profitability, growth, and analyst-rating data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to identify a stock by name or six-digit code, gather public market and fundamental data through the investoday-finance-data dependency, and produce an evidence-based valuation report. The skill is intended for informational valuation assessment, not trading, position sizing, or personalized investment advice. <br>

### Deployment Geography for Use: <br>
Global; analysis scope is Chinese A-share equities. <br>

## Known Risks and Mitigations: <br>
Risk: Generated valuation analysis could be mistaken for personalized investment advice. <br>
Mitigation: Present conclusions as informational valuation status only, avoid buy/sell prices, position sizing, and trade timing, and preserve the skill's investment-advice caveat. <br>
Risk: The skill depends on the separate investoday-finance-data skill and public market data quality for its conclusions. <br>
Mitigation: Review the dependency before deployment, cite the data dimensions used, and state that a dimension cannot be judged when required data is unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-stock-valuation-analysis) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/kenneth-bro) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown valuation analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market data from the investoday-finance-data skill and reports insufficient data when valuation evidence is missing.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
