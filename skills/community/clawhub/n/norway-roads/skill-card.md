## Description: <br>
Query real-time road conditions, closures, and traffic issues in Norway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GeoffreyCasaubon](https://clawhub.ai/user/GeoffreyCasaubon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to check Norwegian road closures, barriers, and route conditions before planning travel. It supports route, city, road, and JSON-output queries against public Statens Vegvesen NVDB road data. <br>

### Deployment Geography for Use: <br>
Norway <br>

## Known Risks and Mitigations: <br>
Risk: Road-condition output may omit current traffic, weather, or safety-critical incidents that are not present in NVDB. <br>
Mitigation: Treat results as planning assistance and verify safety-critical travel with official live road sources such as Vegvesen before relying on them. <br>
Risk: Using the skill contacts the public NVDB road-data service at runtime. <br>
Mitigation: Install and run the skill only in environments where outbound requests to the disclosed public road-data API are acceptable. <br>


## Reference(s): <br>
- [Norway Roads API Reference](references/api-docs.md) <br>
- [Statens Vegvesen NVDB API](https://nvdbapiles-v3.atlas.vegvesen.no) <br>
- [ClawHub skill page](https://clawhub.ai/GeoffreyCasaubon/norway-roads) <br>
- [Publisher profile](https://clawhub.ai/user/GeoffreyCasaubon) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime results are plain text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries a public NVDB road-data service at runtime and does not require an API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
