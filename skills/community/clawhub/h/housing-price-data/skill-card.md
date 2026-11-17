## Description:

Fetches official Chinese 70-city residential property price index data from the National Bureau of Statistics for recent and historical city-level housing trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangtianwd](https://clawhub.ai/user/fangtianwd)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and users use this skill to fetch official National Bureau of Statistics housing price index records for one of China's 70 major cities. It supports latest-period lookups, recent history, month-over-month, year-over-year, and fixed-base indicators for concise summaries, tables, or charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound web requests to fetch official housing price data.

Mitigation: Run it in an environment where network access is restricted to the official stats.gov.cn endpoints needed for the task.

Risk: Runtime dependencies are declared with minimum versions rather than pinned versions.

Mitigation: Pin and review dependency versions before deploying the skill in a shared or production agent environment.

Risk: Optional chart and validation features can write files to user-specified paths.

Mitigation: Choose output locations deliberately and review generated files before sharing or retaining them.

## Reference(s):

- [China Housing Price Data on ClawHub](https://clawhub.ai/fangtianwd/skills/housing-price-data)
- [National Bureau of Statistics RSS](https://www.stats.gov.cn/sj/zxfb/rss.xml)
- [REFERENCE.md](references/REFERENCE.md)
- [Validation Report](artifacts/validation-report.json)
- [Accuracy Boundary Report](artifacts/accuracy-boundary-report.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON data for agent reasoning, with optional Markdown summaries, tables, and chart files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live data from stats.gov.cn and may write optional chart or validation outputs to user-specified paths.]

## Skill Version(s):

2.2.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
