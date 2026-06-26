## Description: <br>
Query Naver Cloud Maps APIs for route navigation, using Directions5 by default and automatically switching to Directions15 for 5 or more waypoints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beomsu317](https://clawhub.ai/user/beomsu317) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and route-planning agents use this skill to calculate vehicle driving routes from longitude,latitude coordinates, including distance, duration, toll fare, taxi fare, and fuel cost. It supports optional waypoints, route preferences, vehicle settings, and fuel settings through Naver Cloud Maps Directions APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Route start, destination, and waypoint coordinates are sent to Naver Cloud Maps and may reveal sensitive travel patterns. <br>
Mitigation: Use the skill only for routes appropriate to share with Naver Cloud Maps, avoid sensitive home, work, customer, or regulated-location routes unless approved, and disclose this data flow to users. <br>
Risk: Runtime logs can include exact coordinates for route inputs and waypoints. <br>
Mitigation: Disable or remove coordinate logging before production use, restrict log access, and avoid retaining logs that contain precise route locations. <br>
Risk: Naver Cloud API credentials are required and may be exposed if .env files or environment variables are mishandled. <br>
Mitigation: Use a dedicated, least-privilege Naver Maps API key, protect local .env files, rotate credentials if exposed, and monitor quota usage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/beomsu317/ncloud-maps) <br>
- [Ncloud Maps API specification](references/api-spec.md) <br>
- [Naver Cloud Console](https://console.ncloud.com) <br>
- [Naver Cloud Maps Directions API documentation](https://api.ncloud-docs.com/docs/ko/application-maps-directions) <br>
- [npm package](https://www.npmjs.com/package/ncloud-maps-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON route summaries and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Route results include success status, start and goal coordinates, distance, duration, toll fare, taxi fare, fuel cost, departure time, and optional error text.] <br>

## Skill Version(s): <br>
1.0.8 (source: package.json, README changelog, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
