## Description:

Integrates open construction datasets by combining government, industry, weather, geospatial, material price, labor rate, permit, energy, and economic sources for enhanced analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction data analysts, estimators, and project teams use this skill to enrich project inputs with open construction-related data and produce structured findings about costs, labor, permits, and weather risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sample connector values for prices, labor rates, permits, and weather may be mistaken for verified live data.

Mitigation: Replace or verify connectors against authoritative data sources and independently validate outputs before using them for business decisions.

Risk: Filesystem access to user-supplied project files and network access for open-data lookups can expose sensitive project data or unapproved endpoints.

Mitigation: Limit file access to intended project inputs, use approved data endpoints, validate inputs, and review generated results before deployment.

## Reference(s):

- [DataDrivenConstruction website](https://datadrivenconstruction.io)
- [OpenWeatherMap API](https://api.openweathermap.org/data/2.5)
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/open-data-integrator)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with structured tables, code snippets, and optional export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include summary statistics, key findings, validation errors, and suggested follow-up analysis.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
