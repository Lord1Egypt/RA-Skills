## Description: <br>
Amap location-service skill for POI search, route planning, travel planning, nearby search, and heatmap data visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyanFE](https://clawhub.ai/user/zhangyanFE) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Amap places, find nearby locations, plan walking, driving, cycling, or transit routes, build travel itineraries, and generate map or heatmap visualization links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Amap API keys may be exposed or overused if saved in local configuration or shared in prompts. <br>
Mitigation: Set AMAP_WEBSERVICE_KEY in the environment, use a limited-quota key, and avoid sharing keys in conversation history or generated files. <br>
Risk: Location requests, home/work addresses, routes, and heatmap data URLs can reveal sensitive personal or business information. <br>
Mitigation: Avoid submitting private locations or private heatmap data unless intended, and review any generated Amap URLs before sharing them. <br>
Risk: The skill depends on axios for outbound web requests. <br>
Mitigation: Install with a reviewed lockfile or patched axios version before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyanFE/ll) <br>
- [Amap Web Service API overview](https://lbs.amap.com/api/webservice/summary) <br>
- [Create an Amap application and key](https://lbs.amap.com/api/webservice/create-project-and-key) <br>
- [Amap POI Search API documentation](https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with Amap URLs, shell command examples, and JSON API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, axios, and AMAP_WEBSERVICE_KEY for Amap Web Service calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
