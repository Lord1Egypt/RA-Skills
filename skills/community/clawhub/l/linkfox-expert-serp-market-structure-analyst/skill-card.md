## Description:

亚马逊前三页 SERP 市场格局分析专家。适用于分析页面级竞争、自然排名结构、价格分布、评论分布、品牌与卖家集中度、新品机会，并生成 SERP 市场报告的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, ecommerce operators, and market analysts use this skill to analyze organic Amazon search results, enrich products with Keepa-derived fields, and generate market-structure reports for competitive positioning and new-product opportunity review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox credentials and supports endpoint override variables.

Mitigation: Use a controlled runtime, prefer session-scoped credentials or a credential manager, and only use endpoint overrides for trusted hosts.

Risk: Generated reports and uploads can expose local analysis outputs or public artifacts.

Mitigation: Review report, feedback, and upload contents before sharing, and open generated HTML as active content in a controlled browser context.

Risk: The artifact includes behavior for modifying or extending skills.

Mitigation: Review and scan any generated skill changes before installation or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-serp-market-structure-analyst)
- [Amazon search API reference](artifact/skills/linkfox-amazon-search/references/api.md)
- [SERP competition API reference](artifact/skills/linkfox-amazon-search-competition/references/api.md)
- [Keepa field reference](artifact/skills/linkfox-amazon-search-competition/references/keepa-fields.md)
- [38-section chart templates](artifact/skills/linkfox-amazon-search-competition/references/chart-templates.md)
- [Analysis report component library](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)
- [File upload API reference](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown response with file paths plus generated HTML, JSON, and comparison-table artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided keyword and marketplace; discloses sample scope, imputation rules, Keepa coverage, and rank limitations in reports.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
