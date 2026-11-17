## Description:

ASIN Keepa 曲线与竞品生命周期分析专家。适用于深度诊断亚马逊 ASIN 的价格历史、BSR、销量趋势、评论增长、流量结构、生命周期阶段，并生成完整 HTML 竞品报告的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and marketplace analysts use this skill to evaluate a single ASIN's price history, BSR movement, sales trend, review growth, traffic mix, lifecycle stage, and competitor positioning. It coordinates Keepa, Sorftime, SIF, and report-generation capabilities to produce a data-grounded competitive diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ASIN queries, usage metadata, and feedback summaries may be sent to LinkFox services.

Mitigation: Use the skill only for data that is acceptable to share with LinkFox-operated services, and avoid entering sensitive or confidential product research data.

Risk: Custom LinkFox gateway environment variables can redirect requests to destinations the user may not trust.

Mitigation: Set custom LinkFox gateway variables only when the destination is explicitly trusted and reviewed.

Risk: Uploaded files and generated reports may include sensitive business information.

Mitigation: Avoid uploading sensitive files and review report contents before sharing or publishing them.

Risk: Generated HTML reports should be treated as active content.

Mitigation: Open generated HTML only in trusted environments and review it before distribution.

Risk: Credential and report handling are described by the security evidence as under-scoped.

Mitigation: Review required credentials, report output paths, and retention expectations before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-asin-keepa-curve-analyst)
- [LinkFox Skills](https://skill.linkfox.com/)
- [LinkFox Skills guide](https://skill.linkfox.com/linkfoxskills/guide.htm)
- [Root skill definition](artifact/SKILL.md)
- [Competitor reverse analysis skill](artifact/skills/competitor-reverse-analysis/SKILL.md)
- [Keepa product series API reference](artifact/skills/linkfox-keepa-product-series/references/api.md)
- [Keepa product request API reference](artifact/skills/linkfox-keepa-product-request/references/api.md)
- [Sorftime Amazon product detail API reference](artifact/skills/linkfox-sorftime-amazon-product-detail/references/api.md)
- [SIF ASIN keywords API reference](artifact/skills/linkfox-sif-asin-keywords/references/api.md)
- [SIF ASIN summary API reference](artifact/skills/linkfox-sif-asin-summary/references/api.md)
- [Report layout reference](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with generated HTML report files and supporting JSON or data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Long analyses over 400 Chinese characters are routed to generated HTML reports; short answers may be returned directly.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
