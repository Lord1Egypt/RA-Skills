## Description: <br>
Access 123+ datasets from the City of Lethbridge open data portal, including transit, infrastructure, elections, environment, and other city data via ArcGIS Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to discover, inspect, and fetch public City of Lethbridge open datasets through a Python CLI and ArcGIS Hub endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes user-invoked public open-data requests and creates a small local cache. <br>
Mitigation: Run commands only for intended public datasets and review fetched output before relying on it. <br>
Risk: Large datasets may produce high-volume output or long-running requests. <br>
Mitigation: Use fetch limits for exploratory queries and choose CSV output intentionally when tabular export is needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raychanpmp/lethbridge-opendata) <br>
- [Popular Lethbridge datasets](references/datasets.md) <br>
- [City of Lethbridge Open Data Portal](https://opendata.lethbridge.ca) <br>
- [City of Lethbridge ArcGIS REST OpenData services](https://gis.lethbridge.ca/gisopendata/rest/services/OpenData/) <br>
- [City of Lethbridge DCAT feed](https://opendata.lethbridge.ca/api/feed/dcat-us/1.1.json) <br>
- [ArcGIS item details API](https://www.arcgis.com/sharing/rest/content/items) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, CSV, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples; CLI output may be plain text, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetch limits can constrain result size; CSV output is printed rather than silently saved.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
