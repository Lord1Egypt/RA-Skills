## Description:

Google Maps and Places API integration. Search places, geocode addresses, calculate routes, get directions, and retrieve location data. Use this skill when users want to look up locations, convert addresses to coordinates, or get routing information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to search places, geocode addresses, retrieve place details, calculate routes, and obtain Google Maps location data through ClawLink-managed Google Maps access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and persistently allowlist an unpinned third-party ClawLink plugin.

Mitigation: Install only after verifying the ClawLink plugin publisher, source, or version, and keep allowlisting limited to the intended plugin.

Risk: Google Maps requests may include precise addresses, routes, nearby searches, or cell/WiFi geolocation data.

Mitigation: Require explicit user approval before precise location, route, nearby-search, or geolocation requests, and connect only the intended Google Maps credential.

## Reference(s):

- [Google Maps Platform Documentation](https://developers.google.com/maps/documentation)
- [Places API](https://developers.google.com/places/web-service/overview)
- [Directions API](https://developers.google.com/maps/documentation/directions/overview)
- [Geocoding API](https://developers.google.com/maps/documentation/geocoding/overview)
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/google-maps-places)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown]

**Output Format:** [Markdown with inline shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces tool-selection guidance and ClawLink Google Maps calls; results depend on the live connected Google Maps tool catalog.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
