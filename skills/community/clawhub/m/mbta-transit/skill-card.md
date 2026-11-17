## Description:

Provides real-time MBTA transit information including next departures, service alerts, live vehicle locations, stop searches, and route listings for Boston-area subway, bus, commuter rail, and ferry service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squidpunch](https://clawhub.ai/user/squidpunch)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to answer Boston-area transit questions by querying MBTA public API data for departures, alerts, vehicle locations, stops, and routes. It is useful for trip-status checks, station lookup, and service disruption awareness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured MBTA_API_KEY values are sent to the MBTA API for rate limiting.

Mitigation: Use an MBTA-specific API key, keep it in the environment, and avoid placing unrelated secrets in MBTA_API_KEY.

Risk: Real-time predictions or vehicle data may be unavailable during off-hours, outages, or on routes without tracking.

Mitigation: Use the scheduled-departure fallback when predictions are empty and present results as MBTA-provided status rather than guaranteed service.

## Reference(s):

- [MBTA V3 API Reference](references/API.md)
- [MBTA V3 API](https://api-v3.mbta.com/)
- [ClawHub Skill Page](https://clawhub.ai/squidpunch/skills/mbta-transit)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text transit lookup results with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MBTA public API responses; MBTA_API_KEY is optional for higher rate limits.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
