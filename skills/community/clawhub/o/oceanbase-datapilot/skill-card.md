## Description:

DataPilot uses the DataPilot OpenAPI to connect data sources, create and manage data analysis agents, answer natural-language data questions, validate SQL, generate charts, export reports, and maintain agent knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hsunboy](https://clawhub.ai/user/hsunboy)

### License/Terms of Use:


## Use Case:

Developers and data teams use this skill to create DataPilot analysis agents for business data sources, ask analytics questions in natural language, inspect SQL and results, export reports, and maintain reference SQL, business knowledge, and analysis templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that the CLI exposes the user's API key in a local log.

Mitigation: Remove or fix raw API-key logging before use, and rotate any DATAPILOT_API_KEY that may have been run through this CLI.

Risk: The server security summary reports that credentials or datasource data can be sent to any configured API URL.

Mitigation: Use only a trusted HTTPS DataPilot endpoint and require explicit approval before datasource uploads or other data-transfer operations.

Risk: The skill can overwrite or delete agent knowledge and create downloadable reports.

Mitigation: Require explicit user approval for report downloads, knowledge overwrites, and deletions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hsunboy/skills/oceanbase-datapilot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, SQL text, tables, chart or report download URLs, and shell command invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js plus DATAPILOT_API_URL and DATAPILOT_API_KEY; uses a configured DataPilot endpoint for API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
