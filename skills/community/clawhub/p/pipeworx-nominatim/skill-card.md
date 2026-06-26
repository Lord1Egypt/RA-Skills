## Description: <br>
OpenStreetMap geocoding for forward and reverse address lookup and OpenStreetMap object lookups through the Nominatim API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert place names or addresses into coordinates, reverse geocode coordinates into addresses, and look up specific OpenStreetMap objects by ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address and coordinate queries can contain sensitive location information and are sent to Pipeworx's gateway. <br>
Mitigation: Use the skill only when sending the relevant location data to the remote endpoint is appropriate for the user and environment. <br>
Risk: Setup uses npx mcp-remote to connect an agent to a remote MCP endpoint. <br>
Mitigation: Use that setup only when the npm package and the Pipeworx endpoint are trusted for the deployment context. <br>


## Reference(s): <br>
- [Pipeworx Nominatim pack](https://pipeworx.io/packs/nominatim) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-nominatim) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration and curl examples; tool calls return JSON geocoding results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and uses a Pipeworx-hosted Nominatim MCP endpoint; the gateway respects Nominatim's 1 request per second usage policy.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
