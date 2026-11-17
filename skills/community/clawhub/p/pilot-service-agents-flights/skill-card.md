## Description:

Aircraft tracking and aviation weather for ADS-B feeds, aircraft and callsign lookups, airport metadata, and METAR, TAF, AIRMET, and SIGMET data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

External developers and aviation data users use this skill to query Pilot Protocol service agents for live aircraft positions, aircraft or callsign records, airport metadata, and aviation weather products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: pilotctl traffic reaches external Pilot Protocol service agents, and /summary or free-text responses may include service-side Gemini-generated prose.

Mitigation: Install only when intending to use Pilot Protocol aviation data agents, and review generated prose before relying on it.

Risk: ADS-B and aviation data coverage can be incomplete or change with receiver density, source availability, and each agent's current filter contract.

Mitigation: Use /help and fresh list-agents queries to confirm available filters, and verify critical aviation decisions against authoritative sources.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-flights)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Skills Catalog](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, a running Pilot Protocol daemon joined to network 9, and reachable Pilot Protocol service agents; service responses are read from pilotctl inbox.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
