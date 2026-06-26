## Description: <br>
Analyzes A-share stock financial quality across profitability, earnings quality, growth durability, cash flow, and financial safety, using Investoday finance data to identify stock codes and produce structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agents use this skill to produce structured financial quality reports for A-share companies from public market data. It supports profitability, earnings quality, cash-flow, balance-sheet, solvency, and growth analysis without giving buy, sell, position-sizing, price-target, or timing advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill analyzes public company financial statements and could be mistaken for investment advice. <br>
Mitigation: Keep outputs framed as informational analysis, include the skill's no-investment-advice constraint, and avoid buy or sell recommendations, position sizing, target prices, or trading timing. <br>
Risk: The skill depends on investoday-finance-data for actual data access, so incorrect or unavailable data can affect the report. <br>
Mitigation: Review the dependency before installation and require each conclusion to cite numeric evidence from the retrieved data, writing that a dimension cannot be judged when data is missing. <br>
Risk: Users could provide personal or confidential financial information even though the skill is intended for public market data. <br>
Mitigation: Avoid entering personal or confidential financial information and use the skill only for public company analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-stock-financial-analysis) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown financial analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the investoday-finance-data skill for public market data access; conclusions must include numeric evidence and avoid investment advice.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
