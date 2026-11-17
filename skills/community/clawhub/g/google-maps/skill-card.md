## Description:

Google Maps integration for OpenClaw with Routes API for travel-time estimates, turn-by-turn directions, distance matrices, geocoding, place search, place details, and transit planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaharsha](https://clawhub.ai/user/shaharsha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to call Google Maps services for route planning, traffic-aware travel estimates, geocoding, reverse geocoding, distance matrices, place search, and place details from an OpenClaw workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and details results can include photo_url values containing the Google API key.

Mitigation: Use a restricted Google API key with quota and billing limits, avoid sharing raw outputs that contain photo_url fields, and rotate the key if such outputs have already been printed or stored.

Risk: Location, route, place, and address queries are sent to Google Maps services.

Mitigation: Avoid sensitive home, work, medical, legal, client, or otherwise confidential locations unless sending that data to Google is acceptable for the user's workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaharsha/skills/google-maps)
- [Google Maps coverage](https://developers.google.com/maps/coverage)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON responses from a Python command-line helper, with Markdown usage examples and configuration guidance in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Google Maps API key and the Python requests package; optional language configuration is available through GOOGLE_MAPS_LANG.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
