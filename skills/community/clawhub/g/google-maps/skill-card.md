## Description: <br>
Google Maps integration for OpenClaw with Routes API for travel time calculations, directions, distance matrices, geocoding, place search, place details, and transit planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shaharsha](https://clawhub.ai/user/Shaharsha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call Google Maps services from OpenClaw for routing, traffic-aware travel estimates, geocoding, place discovery, and transit planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Place search and details results can include photo URLs containing the Google API key. <br>
Mitigation: Use a restricted Google Maps API key with quotas, and avoid sharing transcripts or logs containing place search or details results until the photo URL behavior is patched. <br>
Risk: Map, route, geocoding, and place queries are sent to Google Maps services. <br>
Mitigation: Avoid submitting sensitive locations or personal data unless that sharing is acceptable for the deployment context. <br>


## Reference(s): <br>
- [ClawHub Google Maps skill page](https://clawhub.ai/Shaharsha/google-maps) <br>
- [Google Maps Platform coverage](https://developers.google.com/maps/coverage) <br>
- [Google Maps API endpoint](https://maps.googleapis.com/maps/api) <br>
- [Google Routes API endpoint](https://routes.googleapis.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_API_KEY or GOOGLE_MAPS_API_KEY and the Python requests package; GOOGLE_MAPS_LANG is optional.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
