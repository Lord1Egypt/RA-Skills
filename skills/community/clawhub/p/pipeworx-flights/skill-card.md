## Description:

Live aircraft tracking - flights in a geographic area, individual aircraft by transponder, and airport arrivals/departures via OpenSky Network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and aviation analysts use this skill to query live aircraft in a geographic area, track aircraft by ICAO24 transponder address, and retrieve airport arrivals or departures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup uses an unpinned npm helper, mcp-remote@latest.

Mitigation: Pin mcp-remote to a reviewed version and run the MCP process with only the network and environment access it needs.

Risk: Anonymous flight data access is rate-limited and may be slightly delayed.

Mitigation: Account for delayed or missing flight records in downstream workflows and avoid relying on anonymous access for strict real-time guarantees.

## Reference(s):

- [Pipeworx Flights](https://pipeworx.io/packs/flights)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-flights)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight queries return aircraft details such as ICAO24 address, callsign, origin country, altitude, velocity, heading, and position when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
