## Description:

Geographic and geolocation APIs through Pilot Protocol service agents, including Google Maps Platform, open geocoders, and IP-to-location lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover and query geography service agents for address geocoding, reverse geocoding, directions, distance, elevation, timezone, air quality, places, postal validation, and IP-based location lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Precise location, device observation, address, coordinate, IP address, WiFi, or cell data may be routed through Pilot Protocol service agents and upstream providers.

Mitigation: Confirm before sending sensitive location inputs, verify the selected hostname and provider, and run the skill with the least local privilege available.

Risk: The security review notes that the package documents a flight-tracking agent while also saying flight tracking is out of scope.

Mitigation: Avoid the documented aircraft-state agent until the package scope is clarified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-geo)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Skills](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries return service-agent responses through pilotctl inbox entries; upstream services may return JSON envelopes or natural-language summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
