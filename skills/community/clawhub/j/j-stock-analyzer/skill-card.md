## Description: <br>
输入股票代码，深入分析财务数据、估值、护城河，生成投资分析报告 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jearrylee](https://clawhub.ai/user/jearrylee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request a structured fundamental analysis of a stock, including financial health, valuation, moat, management, risks, and an investment-decision summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial figures, valuation assumptions, or source data may be stale, incomplete, or incorrect. <br>
Mitigation: Treat outputs as informational, require cited data sources, and independently verify financial figures before relying on the analysis. <br>
Risk: Stock research requests may disclose sensitive portfolio details when the agent uses external finance sites or APIs. <br>
Mitigation: Limit prompts to public ticker or company information unless the user is comfortable sharing portfolio details with the agent's external data sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jearrylee/j-stock-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes source notes, risk prompts, scoring tables, and an informational-use disclaimer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
