## Description:

输入商品名称或类目，搜索淘宝/天猫、京东、拼多多、抖音电商等平台的爆款商品，拆解标题关键词、价格区间、销量评分、核心卖点和视觉风格，并生成交互式 HTML 可视化分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, product researchers, and market analysts use this skill to compare hot products across major Chinese commerce platforms, identify category patterns, and prepare product-selection guidance. It is intended for point-in-time marketplace research and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Bash and broad file/write authority beyond what the report workflow usually requires.

Mitigation: Run with the smallest practical tool set; restrict or remove Bash and limit write access unless explicitly needed to create the requested report.

Risk: Generated HTML is active browser content that can load third-party JavaScript and may include marketplace text gathered from web results.

Mitigation: Review generated reports before opening or sharing them, use a trusted browser context, and avoid carrying untrusted snippets into HTML without appropriate escaping or sanitization.

Risk: Prices, sales counts, ratings, and rankings are time-sensitive marketplace snapshots and may be estimated from search snippets.

Mitigation: Label report data as point-in-time and verify important business decisions against primary platform data before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/hot-product-analyzer)
- [Chart.js CDN dependency](https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [Text, Code, Files, Guidance]

**Output Format:** [Interactive single-file HTML report with narrative analysis and Chart.js charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses web-sourced marketplace snapshots; generated HTML can load third-party JavaScript from the Chart.js CDN.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
