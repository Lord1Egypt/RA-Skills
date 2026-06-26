## Description: <br>
Geographic utilities for geocoding, reverse geocoding, country information, timezone lookup, and sunrise/sunset times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert place names and coordinates, retrieve country metadata, resolve local timezones, and calculate daylight information through a remote MCP geography service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location queries and coordinates may be sent to Pipeworx's remote gateway and upstream public APIs. <br>
Mitigation: Avoid sending sensitive location data unless the remote service is acceptable for the user's privacy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-geo) <br>
- [Pipeworx geo homepage](https://pipeworx.io/packs/geo) <br>
- [Pipeworx geo MCP gateway](https://gateway.pipeworx.io/geo/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return location data, coordinates, timezone details, country metadata, and sunrise/sunset information from remote services.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
