## Description:

Public-transit schedules and live data for Amtrak, BART, Deutsche Bahn, Swiss SBB, BC Ferries, BVG Berlin, and other transit services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and operators use this skill to query Pilot Protocol transit service agents for live departures, station lookups, multi-modal journey planning, and normalized inbox responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transit or location-related queries are sent to remote Pilot Protocol service agents.

Mitigation: Confirm that use of Pilot Protocol is acceptable for the deployment and avoid sending sensitive itinerary or location data unless that exposure is approved.

Risk: The inspected release has a minor scope mismatch around listed bike-share agents.

Mitigation: Verify the current agent catalogue with a fresh list-agents query and use the traffic bike-share skill for city bike-share requests when appropriate.

Risk: The skill depends on pilotctl, a running daemon, network 9 access, and the list-agents directory service.

Mitigation: Check those prerequisites before use and treat unavailable services as an operational dependency rather than a skill failure.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-transit)
- [Pilot Skills](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transit agent responses may arrive asynchronously in the pilotctl inbox and may include normalized JSON envelopes or prose summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
