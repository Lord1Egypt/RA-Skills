## Description:

Generates SEO and GEO performance reports or configures monitoring alerts for rankings, traffic, authority, backlinks, technical health, competitor movement, and AI visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO, and growth teams use this skill to create source-tagged performance dashboards, executive SEO/GEO summaries, and threshold-based monitoring plans. It is intended for reporting on measured or user-provided metrics and for configuring alerts around future traffic, ranking, technical, backlink, competitor, and AI-visibility changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A documented ledger command could become command injection if an agent builds a shell string from a user-supplied domain.

Mitigation: Validate domains and pass command arguments as structured values instead of constructing shell strings.

Risk: The skill may connect analytics, search, SEO, crawler, notification, or memory storage integrations.

Mitigation: Enable integrations only when needed and after explicit user approval.

## Reference(s):

- [Performance Monitor ClawHub Page](https://clawhub.ai/aaron-he-zhu/skills/performance-monitor)
- [Publisher Profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Alert Configuration Templates](references/alert-configuration-templates.md)
- [Alert Threshold Guide](references/alert-threshold-guide.md)
- [SEO/GEO KPI Definitions](references/kpi-definitions.md)
- [Performance Report Output Templates](references/report-output-templates.md)
- [SEO/GEO Report Templates](references/report-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report or alert configuration summary with source-tagged metrics and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report mode emits a delta-based dashboard and handoff summary; alert mode emits named triggers, thresholds, priorities, routing, and response plans.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
