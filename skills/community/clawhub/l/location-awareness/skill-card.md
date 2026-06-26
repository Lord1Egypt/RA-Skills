## Description: <br>
Location awareness via privacy-friendly GPS tracking (Home Assistant, OwnTracks, GPS Logger). Set location-based reminders and ask about movement history, travel time, and nearby POIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hegghammer](https://clawhub.ai/user/Hegghammer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to query personal location state, calculate travel time, manage saved places, geofences, and reminders, and inspect recent movement history from configured location providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive location and credential data. <br>
Mitigation: Review before installing, use a dedicated minimal configuration or environment, and avoid placing unrelated secrets in ~/.openclaw/.env. <br>
Risk: Location coordinates or place searches may be sent to public mapping services. <br>
Mitigation: Confirm the deployment is comfortable with external location lookups before enabling commands that geocode, reverse geocode, search nearby places, or calculate routes. <br>
Risk: Cron-based checks can create continuous location monitoring and trigger reminder or geofence actions. <br>
Mitigation: Enable scheduled checks only when continuous monitoring is intended, and require confirmation before deleting or changing saved places, reminders, or geofence rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hegghammer/location-awareness) <br>
- [OpenStreetMap Nominatim service](https://nominatim.openstreetmap.org/) <br>
- [Overpass API](https://overpass-api.de/api/interpreter) <br>
- [OSRM public route service](http://router.project-osrm.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Human-readable text, Markdown command guidance, and optional JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and configured location-provider credentials; environment variables take precedence over config.json.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
