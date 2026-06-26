## Description: <br>
面向公募基金业绩归因分析，聚焦超额收益来源、选股能力、择时能力、配置支撑与业绩可持续性，并基于今日投资金融数据接口自动识别基金代码并输出结构化基金业绩归因报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenneth-bro](https://clawhub.ai/user/kenneth-bro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External finance analysts and agent users use this skill to generate structured public-fund performance attribution reports, including excess-return sources, stock-selection and timing signals, allocation support, and sustainability considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the required investoday-finance-data skill and external finance-data API calls. <br>
Mitigation: Confirm that the dependency and external finance-data calls are acceptable before installation and use. <br>
Risk: Prompts about funds could include unnecessary personal financial details. <br>
Mitigation: Use fund names or 6-digit fund codes and avoid account information or other personal financial details. <br>
Risk: Attribution reports could be mistaken for trading, subscription, redemption, or timing advice. <br>
Mitigation: Keep outputs framed as analysis only and follow the artifact constraint against investment recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenneth-bro/investoday-fund-performance-attribution-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured fund performance attribution report with numeric evidence requirements and no investment recommendations.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
