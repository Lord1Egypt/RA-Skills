## Description:

全域情报简报生成系统。手动触发，从多信源采集、评分、去重、输出HTML情报简报。覆盖国际形势、AI应用、社会民生、潮流热点四大分类。触发词：情报简报、早报、午报、晚报、推送简报、生成简报、daily briefing。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lodligos](https://clawhub.ai/user/lodligos)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and analysts use this skill to collect current news from multiple sources, score and deduplicate events, and produce concise intelligence briefings. It is intended for manually triggered morning, midday, evening, or ad hoc briefing generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes recurring briefing setup that can run unattended in the main agent session if enabled.

Mitigation: Do not enable the bundled cron setup unless recurring runs are intentional; prefer a dedicated restricted session for scheduled execution.

Risk: The skill can read and update agent notes and save local HTML or media files as part of briefing generation.

Mitigation: Run it in a workspace where these memory and file side effects are expected, and review generated files before distribution.

Risk: Briefings rely on web searches, fetched news pages, and optional skill dependencies that may vary in quality or provenance.

Mitigation: Verify cited sources and optional dependencies by publisher, version, and digest, and review generated briefings for source quality before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lodligos/skills/intel-briefing)
- [Scoring reference](references/scoring.md)
- [Architecture review reference](references/architecture-review.md)
- [Version history](references/version-history.md)
- [Version management](references/version-management.md)
- [HTML briefing template](references/template.html)
- [Cron setup guide](CRON_SETUP.md)
- [财联社快讯](https://www.cls.cn/telegraph)
- [华尔街见闻](https://wallstreetcn.com)
- [36氪快讯](https://36kr.com/newsflashes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML briefing files with concise text or Markdown status summaries when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces timestamped and latest-copy HTML briefing files, updates agent notes, and may emit channel-specific media references when configured.]

## Skill Version(s):

1.5.3 (source: release evidence and version history, released 2026-04-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
