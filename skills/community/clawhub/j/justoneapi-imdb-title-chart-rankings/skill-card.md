## Description:

Call GET /api/imdb/title-chart-rankings/v1 for IMDb Chart Rankings through JustOneAPI with rankingsChartType.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justoneapi](https://clawhub.ai/user/justoneapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve IMDb title chart rankings from JustOneAPI, including Top 250 movie and TV chart positions for ranking monitoring and title benchmarking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JustOneAPI token can be exposed through command-line process arguments or full request URLs.

Mitigation: Use a narrowly scoped token, avoid shared machines and telemetry that records command arguments or full URLs, and rotate the token if it may have been logged.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justoneapi/skills/justoneapi-imdb-title-chart-rankings)
- [JustOneAPI Homepage](https://api.justoneapi.com)
- [JustOneAPI Usage Guide](https://docs.justoneapi.com/en/?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_chart_rankings&utm_content=project_link)
- [JustOneAPI Dashboard](https://dashboard.justoneapi.com/en/login?utm_source=clawhub.ai&utm_medium=referral&utm_campaign=justoneapi_imdb_title_chart_rankings&utm_content=project_link)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a JustOneAPI token in JUST_ONE_API_TOKEN and the rankingsChartType query parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
