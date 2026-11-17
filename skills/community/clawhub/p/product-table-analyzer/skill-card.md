## Description:

商品表市场洞察分析读取 CSV/Excel 商品列表，从类目分布、标题词频、价格带、卖家格局、卖点提炼和竞争度评估生成交互式 HTML 选品报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Operations, ecommerce, and product-selection teams use this skill to turn exported product tables into market-insight reports for category, pricing, seller, keyword, competition, and recommendation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product spreadsheets may contain sensitive business data.

Mitigation: Review the skill before installation and run it only in an approved local workspace for sensitive datasets.

Risk: The workflow can install unpinned Python packages.

Mitigation: Pin and approve dependencies such as jieba and openpyxl before execution.

Risk: Generated HTML reports load Chart.js from a third-party CDN.

Mitigation: Use an approved local Chart.js asset or allow the CDN only after review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/product-table-analyzer)
- [Chart.js CDN used by generated HTML reports](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown summary plus shell commands and a standalone HTML report file; the analyzer script returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may load Chart.js from a third-party CDN unless changed before use.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
