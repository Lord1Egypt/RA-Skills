## Description: <br>
Access 670+ datasets from the City of Ottawa open data portal. Search, fetch, and analyze city data on transit, environment, health, elections, and more via ArcGIS Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to search, inspect, fetch, and export City of Ottawa open datasets from ArcGIS Hub for civic-data analysis and automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests Bash permission and runs a Python script that performs network requests. <br>
Mitigation: Review the script and commands before installation, and approve shell execution only for expected Ottawa open-data tasks. <br>
Risk: Activation phrases are broad enough to trigger during general Ottawa data discussions. <br>
Mitigation: Narrow activation to explicit requests involving open.ottawa.ca or City of Ottawa open datasets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/raychanpmp/ottawa-opendata) <br>
- [Ottawa Open Data Portal](https://open.ottawa.ca) <br>
- [Ottawa DCAT Feed](https://open.ottawa.ca/api/feed/dcat-us/1.1.json) <br>
- [ArcGIS Content Items API](https://www.arcgis.com/sharing/rest/content/items) <br>
- [Ottawa Open Data - Popular Datasets](references/datasets.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, CSV, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CLI output as text, JSON, CSV, or URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public Ottawa and ArcGIS endpoints and caches the dataset catalog locally for up to one hour.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
