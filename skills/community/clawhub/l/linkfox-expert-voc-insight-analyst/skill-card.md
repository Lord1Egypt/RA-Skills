## Description:

亚马逊评论 VOC 洞察分析专家。适用于用户提供 ASIN、标题、五点描述或评论数据后，需要结构化分析人群、使用场景、好评点、差评点、未满足需求和购买动机的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers, ecommerce operators, and listing analysts use this agent to turn product details, bullet points, ASINs, and review data into structured VOC insight reports for audience, use-case, positive-feedback, negative-feedback, unmet-need, and purchase-motivation analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs credential-bearing LinkFox network calls for Amazon research workflows.

Mitigation: Install only when the publisher is trusted, scope API keys to the intended workspace, and avoid custom gateway overrides unless they are approved.

Risk: Uploaded files and generated reports may become publicly accessible through the LinkFox upload flow.

Mitigation: Upload only files intended for external sharing and review generated report contents before distributing links.

Risk: Scheduled tasks can repeatedly run analysis or automation if enabled with broad prompts.

Mitigation: Review scheduled-task prompts, cadence, notification targets, and enabled status before activation.

Risk: Automatic feedback or telemetry behavior may submit task context outside the immediate chat.

Mitigation: Disable or block automatic feedback submission where possible when handling sensitive Amazon research context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-voc-insight-analyst)
- [VOC insight analyst skill definition](artifact/SKILL.md)
- [Amazon product detail API reference](artifact/skills/linkfox-amazon-product-detail/references/api.md)
- [Amazon reviews API reference](artifact/skills/linkfox-amazon-reviews-list/references/api.md)
- [SellerSprite competitor lookup API reference](artifact/skills/linkfox-sellersprite-competitor-lookup/references/api.md)
- [Keepa product history API reference](artifact/skills/linkfox-keepa-product-series/references/api.md)
- [Report layout reference](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)
- [Task scheduler API reference](artifact/skills/linkfox-task-scheduler/references/api.md)
- [File upload API reference](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown tables, with long reports saved as .md files and summarized by path in chat]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primarily Chinese output; analysis is constrained to provided product and review data, and missing data is labeled instead of invented.]

## Skill Version(s):

1.0.2 (source: server release evidence, released 2026-09-14; changelog: Update from 1.0.1 to 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
