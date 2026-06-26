## Description: <br>
Provides Tencent Maps location services for POI search, nearby search, route planning, travel planning, and trajectory or map visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qfish](https://clawhub.ai/user/qfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate Tencent Maps links or API-backed results for place discovery, nearby search, route planning, travel itineraries, and trajectory visualization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise location data, routes, itineraries, trajectory URLs, and possibly plate numbers may be sent to Tencent Maps. <br>
Mitigation: Use the skill only for intended Tencent Maps workflows and avoid entering sensitive home or work routes, real plate numbers, or other unnecessary personal location details. <br>
Risk: Generated links or command output can contain API keys or precise locations. <br>
Mitigation: Use a temporary, restricted, quota-limited Tencent Maps API key and do not share generated links that include keys or precise location data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qfish/have-a-nice-day) <br>
- [Tencent Maps Web Service overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview) <br>
- [Tencent Location Services](https://lbs.qq.com/) <br>
- [Tencent Maps Place Search API](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch) <br>
- [Keyword search reference](references/scene1-keyword-search.md) <br>
- [Nearby search reference](references/scene2-nearby-search.md) <br>
- [POI search reference](references/scene3-poi-search.md) <br>
- [Route planning reference](references/scene4-route-planning.md) <br>
- [Travel planner reference](references/scene5-travel-planner.md) <br>
- [Trail map reference](references/scene7-trail-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration guidance] <br>
**Output Format:** [Markdown with links, shell command examples, and JSON API result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Tencent Maps URLs and structured place, route, itinerary, or map visualization data.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
