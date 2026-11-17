## Description:

房产信息查询全维度助手，用于房源搜索、笋盘筛选、价格对比、成交记录、小区信息、学区和学校查询，并基于主流房产平台数据生成交互式 HTML 可视化报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and real-estate researchers use this skill to gather and compare Chinese housing, rental, transaction, community, school-district, and school information. The skill helps produce concise findings, actionable suggestions, and local interactive HTML reports for further review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may include third-party listing data or links that could become unsafe browser content.

Mitigation: Treat generated HTML reports as untrusted until reviewed; avoid opening them in sensitive browser profiles and validate or escape listing-derived content before reuse.

Risk: Real-estate listings, prices, school districts, and transaction data can be stale or incomplete.

Mitigation: Cross-check important findings with original listing pages, official education sources, and current market records before making decisions.

Risk: The report template loads Chart.js from a public CDN.

Mitigation: For controlled deployments, bundle the dependency or use an integrity-pinned and approved source.

## Reference(s):

- [主流房产平台数据源参考](references/platforms.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown summaries and local interactive HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated HTML, chart JavaScript, source links, ranked listings, comparison tables, and disclaimers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
