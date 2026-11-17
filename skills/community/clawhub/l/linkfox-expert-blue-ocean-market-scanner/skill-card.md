## Description:

An Amazon blue-ocean category market scanning skill for multi-source market insight, keyword validation, trend analysis, competitive landscape scanning, top-ASIN breakdown, profit calculation, and HTML category reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers and ecommerce operators use this skill to evaluate one product category or ASIN at a time, combining marketplace, keyword, trend, social, and supplier signals into an entry-readiness assessment and HTML report.

### Deployment Geography for Use:

Global; marketplace analysis is limited to the supported Amazon sites documented by the skill, with some data sources available only for specific sites.

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API credentials and Amazon market queries.

Mitigation: Install only in environments where LinkFox is trusted, keep API keys scoped and private, and rotate any key that appears in logs.

Risk: The bundled upload workflow can make local files publicly accessible.

Mitigation: Upload only files that are approved for public sharing and avoid uploading sensitive local data.

Risk: Scheduled tasks can trigger recurring market scans or notifications.

Mitigation: Review task content, schedule, notification targets, and enabled state before activating or changing scheduled tasks.

Risk: The security scan marked the release suspicious due to combined credential, upload, execution, and scheduling behavior.

Mitigation: Review the skill and its configured actions before deployment, and limit use to trusted workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-blue-ocean-market-scanner)
- [Publisher profile](https://clawhub.ai/user/linkfox-ai)
- [Top-level skill definition](artifact/SKILL.md)
- [Amazon niche radar workflow](artifact/skills/amazon-niche-radar/SKILL.md)
- [Report output schema](artifact/skills/amazon-niche-radar/references/output-schema.md)
- [Profit calculation and FBA fee reference](artifact/skills/amazon-niche-radar/references/fba-fee-table.md)
- [Keepa interpretation reference](artifact/skills/amazon-niche-radar/references/keepa-interpretation.md)
- [SIF ASIN interpretation reference](artifact/skills/amazon-niche-radar/references/sif-asin-interpretation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [HTML report files with concise text summaries; supporting outputs may include JSON, markdown dashboards, and chart-ready HTML or JavaScript snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One category or ASIN per run; long deliverables are written as files and returned by path with a brief summary.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
