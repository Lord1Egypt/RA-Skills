## Description: <br>
上传商品列表表格（CSV/Excel）后，该技能从类目分布、标题词频、价格带、卖家品牌格局、卖点提炼和竞争度评估等维度生成选品分析和交互式 HTML 可视化报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
电商运营人员和数据分析人员用它将导出的商品表格快速转换为类目、关键词、价格带、卖家集中度和竞争度洞察，用于选品判断和行动建议。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests network-capable tools and can install Python packages even though the analysis is described as local. <br>
Mitigation: Review requested tool access before use, approve package installation explicitly, and remove WebFetch/WebSearch for confidential product tables. <br>
Risk: Uploaded product tables may contain sensitive commercial or competitive data. <br>
Mitigation: Use sanitized input files when possible and keep analysis in a trusted local environment. <br>
Risk: Generated recommendations are data-driven estimates and may be misleading if the input table is incomplete or biased. <br>
Mitigation: Review the source data quality and validate recommendations with business context before taking action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/product-table-analyzer) <br>
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON, HTML files] <br>
**Output Format:** [Markdown guidance with shell commands, structured JSON analysis, and a standalone interactive HTML report file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report is generated locally from user-provided CSV or Excel data and uses Chart.js for browser-based visualizations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
