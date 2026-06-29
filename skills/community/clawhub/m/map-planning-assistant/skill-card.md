## Description: <br>
An AMap-based map planning assistant that helps agents generate multi-scenario local travel plans, route recommendations, weather-aware itineraries, cultural notes, and shareable personal map links or QR codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tix007](https://clawhub.ai/user/tix007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to answer Chinese-language requests for city maps, POI recommendations, route plans, local activities, travel itineraries, and cultural explanations. It can also create AMap personal map outputs for selected POIs when an AMap Web Service API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location and travel requests are sent to AMap for live POI, route, weather, traffic, and personal-map generation. <br>
Mitigation: Use only with location data that is appropriate to share with AMap, and avoid sensitive home, work, family, customer, or operational locations unless consent and policy approval are clear. <br>
Risk: The skill saves location-related history, created maps, visited cities, and inferred user preferences in local long-term memory and profile files. <br>
Mitigation: Review local data retention before deployment, restrict filesystem access where possible, and provide a process to inspect, reset, or delete stored profile and memory data. <br>
Risk: Generated AMap links and QR-code URLs can reveal included POIs to anyone who receives them. <br>
Mitigation: Review POI lists before sharing generated links or QR codes, and do not include sensitive destinations in shareable maps. <br>
Risk: The release evidence reports a suspicious security verdict because the privacy impact is understated. <br>
Mitigation: Review the skill before installing and document the location-sharing, local-memory, and profiling behavior for users before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tix007/map-planning-assistant) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/tix007) <br>
- [AMap Open Platform](https://lbs.amap.com/) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact API Guide](artifact/API_GUIDE.md) <br>
- [Artifact Personal Map Feature Guide](artifact/MAP_FEATURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown-style travel plans with POI lists, route summaries, activity suggestions, cultural notes, AMap links, and QR-code URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMAP_API_KEY for live AMap API calls; generated map links or QR codes may expose included POIs if shared.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
