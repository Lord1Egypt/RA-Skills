## Description:

Provides Tencent Maps location services for POI search, nearby search, route planning, travel planning, map data visualization, and GPS trail visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qfish](https://clawhub.ai/user/qfish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to generate Tencent Maps searches, inspect POI data, plan routes or travel itineraries, and produce map visualization links from user-supplied locations or trail data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Tencent Maps links may include a temporary API key and can expose that key if shared, logged, or stored in chat history.

Mitigation: Use a restricted temporary key with tight quotas and referrer or IP limits, avoid sharing generated links, and rotate the key if it appears outside the intended session.

Risk: POI search, route planning, travel planning, and visualization workflows send precise location or travel data to Tencent Maps services.

Mitigation: Do not submit sensitive home, work, or third-party location data unless the user accepts sending that data to Tencent Maps.

Risk: Map and route results can be incorrect, stale, incomplete, or unsuitable for safety-critical navigation decisions.

Mitigation: Review generated routes and POI results before acting on them, especially for time-sensitive, emergency, or high-risk travel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qfish/skills/have-a-nice-day)
- [Tencent Maps Web Service API overview](https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview)
- [Tencent Location Service](https://lbs.qq.com/)
- [Tencent Maps Place Search API documentation](https://lbs.qq.com/service/webService/webServiceGuide/webServiceSearch)
- [Keyword search workflow](references/scene1-keyword-search.md)
- [Nearby search workflow](references/scene2-nearby-search.md)
- [POI search workflow](references/scene3-poi-search.md)
- [Route planning workflow](references/scene4-route-planning.md)
- [Travel planning workflow](references/scene5-travel-planner.md)
- [Trail map workflow](references/scene7-trail-map.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown with links, shell command examples, and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tencent Maps URLs that contain precise locations or temporary API keys.]

## Skill Version(s):

1.0.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
