## Description:

Access 398+ datasets from the City of Montreal open data portal. Search, fetch, and analyze city data on crime, transit, environment, permits, and more via the CKAN API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and data analysts use this skill to search Montreal's open data catalog, inspect dataset metadata, and fetch queryable CKAN resources for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Python CLI queries donnees.montreal.ca over the network.

Mitigation: Install and run the skill only in environments where public CKAN API access to donnees.montreal.ca is acceptable.

Risk: CSV exports contain untrusted remote data and may be unsafe to open directly in spreadsheet software.

Mitigation: Review or sanitize exported CSV data before opening it in spreadsheet tools or sharing it downstream.

Risk: Broad Montreal-related activation prompts could lead the agent to run data-query commands unexpectedly.

Mitigation: Review proposed commands before execution, especially fetch and CSV export commands.

## Reference(s):

- [Montreal Open Data Portal](https://donnees.montreal.ca)
- [CKAN API Endpoint](https://donnees.montreal.ca/api/3/action)
- [Popular Datasets Reference](references/datasets.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI commands can return text, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public CKAN API responses and can cache catalog metadata in the skill script directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
