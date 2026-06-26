## Description: <br>
Google Maps and Places API integration for searching places, geocoding addresses, calculating routes, getting directions, and retrieving location data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to access Google Maps and Places workflows through ClawLink, including place search, geocoding, routing, directions, distance calculations, elevation, timezone, roads, geolocation, and static map requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise location, WiFi, and cell-tower geolocation requests can expose sensitive location signals through the integration path. <br>
Mitigation: Use those requests only when the user intentionally wants that location signal sent through ClawLink and Google Maps. <br>
Risk: The skill relies on ClawLink as the broker for Google Maps requests and credentials. <br>
Mitigation: Review the ClawLink plugin before approving the local install and allowlist changes. <br>


## Reference(s): <br>
- [Google Maps skill page](https://clawhub.ai/hith3sh/google-maps-places) <br>
- [Publisher profile](https://clawhub.ai/user/hith3sh) <br>
- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation) <br>
- [Places API](https://developers.google.com/places/web-service/overview) <br>
- [Directions API](https://developers.google.com/maps/documentation/directions/overview) <br>
- [Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview) <br>
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to discover the live Google Maps tool catalog before calling tools; no API key is requested in chat.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
