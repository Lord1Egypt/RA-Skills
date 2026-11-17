## Description:

Retrieve World Bank development indicators, including GDP, population, CO2 emissions, literacy, and mortality data, by country code and date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query country metadata and World Bank time-series indicators through a Pipeworx-hosted MCP gateway. It supports quick retrieval of standard development metrics for research, reporting, and agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to Pipeworx's hosted gateway, which may expose country codes, indicator codes, and date ranges.

Mitigation: Avoid confidential research queries and use only data you are comfortable sending to the hosted endpoint.

Risk: Returned development indicators could be stale, unavailable, or inconsistent with official World Bank records.

Mitigation: Verify important numbers against the official World Bank source before using them in decisions or publications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucegutman/skills/pipeworx-worldbank)
- [Pipeworx World Bank MCP endpoint](https://gateway.pipeworx.io/worldbank/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include country metadata, indicator values, date ranges, and MCP server configuration snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
