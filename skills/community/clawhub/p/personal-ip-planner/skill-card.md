## Description: <br>
个人IP规划全流程助手根据用户输入的IP名称与定位方向，从竞品、用户、品牌、内容、平台、变现和风险维度生成交互式HTML决策报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, consultants, operators, and content strategists use this skill to evaluate whether a personal-brand idea is viable and to turn public research into a structured launch plan. It produces competitive analysis, positioning guidance, monetization paths, risk notes, and a 12-month action roadmap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public web research may be incomplete, stale, or biased, which can make market sizing, competitor comparisons, or launch recommendations misleading. <br>
Mitigation: Treat the report as a planning draft and validate important claims, metrics, and business decisions against current primary sources before acting. <br>
Risk: Broad personal-brand trigger phrases may cause the skill to run searches and create a report when the user only wanted a short discussion. <br>
Mitigation: Confirm the user wants a full IP planning report before running multiple searches or writing the HTML output file. <br>
Risk: The skill writes a local HTML file whose filename includes the IP name and whose content may include sourced business observations. <br>
Mitigation: Review the generated file path and report content before opening, sharing, or publishing it. <br>


## Reference(s): <br>
- [Chart.js CDN used by generated reports](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Files, Guidance] <br>
**Output Format:** [Standalone HTML report with Chinese planning content and Chart.js visualizations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves a complete local HTML report named with the IP name and date in the current workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
