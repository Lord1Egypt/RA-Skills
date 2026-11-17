## Description:

Access 123+ datasets from the City of Lethbridge open data portal. Search, fetch, and analyze city data on transit, infrastructure, elections, environment, and more via ArcGIS Hub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raychanpmp](https://clawhub.ai/user/raychanpmp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and civic data users can use this skill to discover City of Lethbridge open datasets, inspect dataset metadata, fetch ArcGIS feature data, and export results for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper makes outbound requests to the Lethbridge open-data portal, ArcGIS, and dataset links advertised by portal metadata.

Mitigation: Run it only where those destinations are acceptable, and add URL allowlisting before use in sensitive internal network environments.

Risk: Large or unexpected dataset responses can consume bandwidth or processing time.

Mitigation: Use fetch limits for routine queries and add response-size limits for controlled deployments.

## Reference(s):

- [Popular & Useful Lethbridge Open Data Datasets](references/datasets.md)
- [City of Lethbridge Open Data Portal](https://opendata.lethbridge.ca)
- [City of Lethbridge DCAT Catalog Feed](https://opendata.lethbridge.ca/api/feed/dcat-us/1.1.json)
- [City of Lethbridge ArcGIS Open Data REST Services](https://gis.lethbridge.ca/gisopendata/rest/services/OpenData/)
- [ArcGIS Content Items API](https://www.arcgis.com/sharing/rest/content/items)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON, Code, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output depends on live public portal and ArcGIS responses; fetch commands support record limits and CSV output.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
