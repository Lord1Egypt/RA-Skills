## Description:

专注对单个亚马逊 ASIN 进行全方位数据驱动的深度拆解，通过四步流水线整合 Keepa、Sorftime 与 SIF 数据，输出涵盖价格、BSR、评论、Deal、流量结构和生命周期等维度的 11 章节 HTML 深度报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon marketplace operators and e-commerce analysts use this skill to investigate one competitor ASIN at a time, combining Keepa, Sorftime, and SIF data into a structured competitive-analysis report. It supports pricing, BSR, review, deal, traffic, lifecycle, SWOT, and action-recommendation review across supported Amazon marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed network calls may expose or misuse LinkFox API access if credentials are broadly scoped.

Mitigation: Use a least-privilege API key, store it in a secret manager where possible, and run the skill only in a controlled environment.

Risk: Gateway URL environment variables can redirect requests away from LinkFox-controlled hosts.

Mitigation: Keep gateway URL settings pinned to expected LinkFox hosts and review any environment overrides before execution.

Risk: Public file upload behavior can expose files if untrusted prompts influence upload paths or file selection.

Mitigation: Do not allow untrusted prompts to choose upload paths, and review files before upload or publication.

Risk: Generated HTML reports are active content and may carry unsafe embedded content.

Mitigation: Treat generated HTML as active content; review it before opening in privileged contexts or sharing externally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-amazon-single-competitor-analysis)
- [LinkFox Skills](https://skill.linkfox.com/)
- [Top-level skill definition](artifact/SKILL.md)
- [Competitor reverse analysis workflow](artifact/skills/competitor-reverse-analysis/SKILL.md)
- [S1 data collection step](artifact/skills/competitor-reverse-analysis/references/steps/S1.md)
- [S2 product-detail step](artifact/skills/competitor-reverse-analysis/references/steps/S2.md)
- [S3 quantitative analysis step](artifact/skills/competitor-reverse-analysis/references/steps/S3.md)
- [S4 report generation step](artifact/skills/competitor-reverse-analysis/references/steps/S4.md)
- [Report layout components](artifact/skills/linkfox-report-generator/references/analysis-layouts.md)
- [Keepa product series API](artifact/skills/linkfox-keepa-product-series/references/api.md)
- [Keepa product detail API](artifact/skills/linkfox-keepa-product-request/references/api.md)
- [Sorftime Amazon product detail API](artifact/skills/linkfox-sorftime-amazon-product-detail/references/api.md)
- [SIF ASIN keywords API](artifact/skills/linkfox-sif-asin-keywords/references/api.md)
- [SIF ASIN summary API](artifact/skills/linkfox-sif-asin-summary/references/api.md)
- [AIGC text generation API](artifact/skills/linkfox-aigc-textgen/references/api.md)
- [File upload API](artifact/skills/linkfox-file-upload/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, HTML report, JSON analysis, shell commands, configuration, guidance]

**Output Format:** [Markdown status text plus generated JSON analysis and an HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ASIN and marketplace; intermediate calculations are produced by the bundled Python analysis script before report generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
