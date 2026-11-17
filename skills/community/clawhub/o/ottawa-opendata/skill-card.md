## Description:

Access 670+ datasets from the City of Ottawa open data portal. Search, fetch, and analyze city data on transit, environment, health, elections, and more via ArcGIS Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and civic data users use this skill to search, inspect, fetch, and export public City of Ottawa datasets from ArcGIS Hub for analysis and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetch command can follow dataset-controlled service URLs outside the stated Ottawa/ArcGIS scope.

Mitigation: Run the skill in an environment where outbound requests to unintended internal services are not sensitive, and review dataset metadata before fetching.

Risk: CSV exports may contain public data values that spreadsheet software interprets unexpectedly.

Mitigation: Treat exported CSV files as untrusted public data and inspect or sanitize them before opening in spreadsheet software.

## Reference(s):

- [Ottawa Open Data Portal](https://open.ottawa.ca)
- [Ottawa DCAT Feed](https://open.ottawa.ca/api/feed/dcat-us/1.1.json)
- [ArcGIS Content Items REST Endpoint](https://www.arcgis.com/sharing/rest/content/items)
- [Popular Datasets Reference](references/datasets.md)
- [ClawHub Skill Page](https://clawhub.ai/raychanpmp/skills/ottawa-opendata)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; command output may be plain text, JSON, or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI may create a local catalog cache when run.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
