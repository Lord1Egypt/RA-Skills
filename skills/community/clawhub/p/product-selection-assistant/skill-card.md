## Description: <br>
电商运营人员输入产品名称、描述或 ASIN 后，技能会基于公开网络信息进行市场调研、六维评分、上架建议和交互式 HTML 可视化报告生成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce operators and product teams use this skill to evaluate whether a single product is suitable for listing, especially for Amazon US cross-border commerce. It produces market-demand, competition, margin, seasonality, entry-barrier, and trend analysis with a clear launch recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product names, descriptions, ASINs, and market-research terms may be used in web searches. <br>
Mitigation: Avoid entering confidential supplier data, unreleased product plans, or other sensitive commercial details. <br>
Risk: Generated HTML reports load Chart.js from a CDN and include generated analysis text. <br>
Mitigation: Open generated reports with normal browser caution and review report content before sharing it externally. <br>
Risk: Market recommendations are based on public web information and may be incomplete or time-sensitive. <br>
Mitigation: Treat scores and launch advice as decision support, then verify key demand, pricing, compliance, and margin assumptions before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/product-selection-assistant) <br>
- [Chart.js 4.4.0 CDN script](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown summary plus generated interactive HTML report file; structured JSON is used as report input.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The HTML report includes a six-dimension radar chart, score cards, analysis cards, and prioritized action items; it loads Chart.js from a CDN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
