## Description:

亚马逊全品类铺货与 Listing 选品专家，用于跨类目发现近期上架且 BSR 快速上升的商品机会，并生成 Excel 结果、候选 ASIN 评分和可选定时任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon marketplace sellers and ecommerce operators use this skill to scan SellerSprite product data for recently listed, fast-rising products across categories, export deduplicated Excel workbooks, score candidate ASINs against seller preferences, and optionally schedule recurring scouting runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product-search queries, onboarding data, generated outputs, and scheduler operations may be exposed to LinkFox services.

Mitigation: Install only in environments where sharing those data categories with LinkFox is acceptable, and avoid submitting sensitive business or account information unless required.

Risk: Non-default LINKFOX_* endpoint variables can route requests to unexpected services.

Mitigation: Use default endpoints unless an operator has reviewed and approved the alternate endpoint configuration.

Risk: A bundled patcher can persistently modify agent instruction files.

Mitigation: Do not run the CLAUDE.md patcher unless persistent instruction changes are intended and have been reviewed.

Risk: Feedback reporting and printed API keys may leave data in remote systems or local logs.

Mitigation: Review logs and feedback behavior before use, and avoid exposing credentials in shared terminals, transcripts, or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-all-category-listing-scout)
- [Amazon product scout API parameters](artifact/skills/amazon-product-scout-agent/references/api-params-catalog.md)
- [SellerSprite product search API](artifact/skills/linkfox-sellersprite-product-search/references/api.md)
- [Task scheduler API](artifact/skills/linkfox-task-scheduler/references/api.md)
- [Report analysis layouts](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)
- [ASIN scoring example expectations](artifact/skills/amazon-asin-dynamic-scoring/references/example_expectations.json)
- [LinkFox platform](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, JSON parameters, Excel file outputs, and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Excel workbooks such as scouting, export, and scoring results; may also create scheduler configurations.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
