## Description: <br>
Provides Swiss public transport station search, route planning, live departure boards, schedules, platforms, and delay information through the Pipeworx Swiss Transport MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to look up Swiss transit stations, plan point-to-point journeys, and retrieve live departure information for trains, buses, and trams. <br>

### Deployment Geography for Use: <br>
Global use with Switzerland-focused public transport data. <br>

## Known Risks and Mitigations: <br>
Risk: Transit lookup queries are sent to the third-party Pipeworx gateway. <br>
Mitigation: Avoid unusually sensitive travel details unless the user trusts the Pipeworx service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-swisstransport) <br>
- [Pipeworx Swiss Transport MCP endpoint](https://gateway.pipeworx.io/swisstransport/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include station identifiers, coordinates, departure and arrival times, route sections, platforms, delays, destinations, and transfer counts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
