## Description:

Aviation flight lookup skill that helps an agent query aircraft type, equipment changes, and confidence scoring for a flight number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iml1s](https://clawhub.ai/user/iml1s)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill through an OpenClaw agent to look up the likely aircraft assigned to a flight, compare aviation data sources, and identify possible equipment changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Flight lookup requests are sent to third-party aviation providers using RAPIDAPI_KEY and, optionally, AIRLABS_KEY.

Mitigation: Only provide API keys when those providers are approved for the intended use and avoid submitting sensitive operational queries unnecessarily.

Risk: The AirLabs key is placed in a URL query parameter by the artifact behavior identified in the security guidance.

Mitigation: Use a low-privilege or dedicated AirLabs key and rotate it if query logs or shared diagnostics may expose request URLs.

Risk: Aircraft type and equipment-change results depend on external provider availability and may have low or conflicting confidence.

Mitigation: Present confidence, source agreement, and type distribution to users, and avoid treating low-confidence results as operationally authoritative.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iml1s/skills/planefilter)
- [AeroDataBox on RapidAPI](https://rapidapi.com/aedbx-aedbx/api/aerodatabox)
- [AirLabs API Signup](https://airlabs.co/signup)
- [OpenSky Network API](https://opensky-network.org/api/states/all)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON flight lookup results with agent-facing interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence score, aircraft type distribution, source names, route fields, registration when available, and equipment-change details when detected.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
