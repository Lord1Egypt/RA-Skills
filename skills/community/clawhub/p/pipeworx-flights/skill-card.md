## Description: <br>
Live aircraft tracking for flights in a geographic area, individual aircraft by transponder, and airport arrivals or departures via OpenSky Network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and aviation teams use this skill to query live aircraft positions by area or ICAO24 address and retrieve airport arrivals or departures for dashboards, research, and operational awareness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight data may be rate-limited, delayed, or incomplete for real-time decisions. <br>
Mitigation: Confirm critical aviation information against authoritative operational sources before relying on it. <br>
Risk: The skill sends tool calls to an external Pipeworx MCP endpoint. <br>
Mitigation: Review intended tool calls and network access requirements before enabling the skill in restricted environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-flights) <br>
- [Pipeworx Flights homepage](https://pipeworx.io/packs/flights) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OpenSky Network data through the Pipeworx MCP endpoint; anonymous access is rate-limited, aircraft positions may be delayed, and airport arrival/departure time ranges are limited to 7-day windows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
