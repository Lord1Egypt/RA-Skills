## Description: <br>
Access 398+ datasets from the City of Montreal open data portal. Search, fetch, and analyze city data on crime, transit, environment, permits, and more via the CKAN API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raychanpmp](https://clawhub.ai/user/raychanpmp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and public-sector data users use this skill to search, inspect, and fetch City of Montreal open datasets through the CKAN API for analysis or reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has Bash permission while its visible function is public open-data retrieval. <br>
Mitigation: Review the included Python script before installation and restrict use to the expected commands that call donnees.montreal.ca, print dataset results, and write the local cache. <br>
Risk: Dataset search and metadata are primarily in French, which can lead to missed or misunderstood results. <br>
Mitigation: Use French search terms where possible and verify dataset metadata before relying on fetched records. <br>


## Reference(s): <br>
- [City of Montreal open data portal](https://donnees.montreal.ca) <br>
- [Montreal Open Data - Popular Datasets](references/datasets.md) <br>
- [City of Montreal CKAN API endpoint](https://donnees.montreal.ca/api/3/action) <br>
- [ClawHub skill page](https://clawhub.ai/raychanpmp/montreal-opendata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CLI output in JSON, CSV, or plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included CLI can print dataset metadata, search results, datastore records, or CSV-formatted rows, and it writes a small local catalog cache.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
