## Description:

Smart public transport routing for Hong Kong that queries Google Maps for transit alternatives, enriches bus legs with real-time ETAs, and ranks routes by effective total time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[7ito](https://clawhub.ai/user/7ito)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to answer Hong Kong public transport routing questions, including one-shot and multi-turn origin-destination flows. It runs a Node CLI that returns transit route JSON for agent formatting into concise user-facing directions.

### Deployment Geography for Use:

Hong Kong

## Known Risks and Mitigations:

Risk: Origin and destination information is sent to Google Maps and public Hong Kong transit data services.

Mitigation: Use the skill only for routing queries where sharing location details with those services is acceptable.

Risk: A Google Maps API key is required for Directions API calls.

Mitigation: Use a restricted API key with only the needed Directions API enabled and set usage quotas.

Risk: The skill maintains a local public ETA database cache under ~/.cache/hk-route.

Mitigation: Account for the local cache in endpoint cleanup and avoid treating cached transit data as sensitive user input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/7ito/skills/hkroute)
- [ClawHub package homepage](https://clawhub.ai/7ito/hkroute)
- [hk-bus-eta project](https://github.com/hkbus/hk-bus-eta)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output for route results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node >= 18 and GOOGLE_MAPS_API_KEY; route answers may include live ETA availability, scheduled fallback data, and actionable first-bus timing.]

## Skill Version(s):

1.0.3 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
