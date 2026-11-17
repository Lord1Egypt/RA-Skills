## Description:

亚马逊竞品动态监控专家。适用于周期性跟踪竞品 ASIN、价格变化、BSR 波动、评论变化、Listing 改动、定时提醒和竞品动态报告的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and commerce analysts use this skill to monitor competitor ASINs, prices, BSR, sales estimates, reviews, listing changes, keyword traffic, and scheduled alerts. It cleans collected data, detects anomalies, and produces Chinese monitoring reports with optional HTML dashboards, CSV/Excel-ready exports, or PPT-style weekly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentialed LinkFox network calls can expose API keys and Amazon research data to the service provider.

Mitigation: Install only when LinkFox is trusted, use scoped credentials where available, and avoid custom gateway endpoints unless controlled by the user.

Risk: Uploaded files, generated reports, and scheduled tasks may include private business data.

Mitigation: Do not upload private files, review report contents before sharing, and confirm scheduled task frequency, recipients, and report format before activation.

Risk: Generated HTML dashboards or reports may carry unreviewed content.

Mitigation: Review generated HTML before distribution and treat report files as outputs that require user approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-amazon-competitor-monitor)
- [Amazon competitor monitor workflow](artifact/skills/amazon-competitor-monitor/SKILL.md)
- [Data cleaning rules](artifact/skills/amazon-competitor-monitor/references/data-cleaning.md)
- [Anomaly detection rules](artifact/skills/amazon-competitor-monitor/references/anomaly-rules.md)
- [Credit alert rules](artifact/skills/amazon-competitor-monitor/references/credit-alert-rules.md)
- [Report template](artifact/skills/amazon-competitor-monitor/references/report-template.md)
- [Visualization guide](artifact/skills/amazon-competitor-monitor/references/visualization-guide.md)
- [Keepa product history API reference](artifact/skills/linkfox-keepa-product-series/references/api.md)
- [Amazon product detail API reference](artifact/skills/linkfox-amazon-product-detail/references/api.md)
- [Amazon reviews API reference](artifact/skills/linkfox-amazon-reviews-list/references/api.md)
- [SIF ASIN keywords API reference](artifact/skills/linkfox-sif-asin-keywords/references/api.md)
- [SellerSprite competitor lookup API reference](artifact/skills/linkfox-sellersprite-competitor-lookup/references/api.md)
- [Task scheduler API reference](artifact/skills/linkfox-task-scheduler/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Chinese Markdown summaries, generated report files, CSV-compatible tables, HTML dashboards, and HTML presentation decks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on LinkFox API credentials, Amazon marketplace inputs, scheduled task settings, and user-selected report formats.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
