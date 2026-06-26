## Description: <br>
ZIP and postal code lookup for place names, states, coordinates, and country information across 60+ countries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to validate postal codes, populate city and state fields, find postal codes for a city, and retrieve geographic coordinates for postal-code based workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Postal-code results may be incomplete, stale, or unsuitable as the sole source for high-impact address decisions. <br>
Mitigation: Verify important address and location decisions against authoritative postal or geocoding sources before acting on them. <br>
Risk: Lookup requests are sent to an external Pipeworx gateway endpoint. <br>
Mitigation: Review the MCP configuration before use and avoid sending sensitive or unnecessary address data. <br>


## Reference(s): <br>
- [Pipeworx zippopotam package page](https://pipeworx.io/packs/zippopotam) <br>
- [Pipeworx zippopotam ClawHub page](https://clawhub.ai/brucegutman/pipeworx-zippopotam) <br>
- [Zippopotam MCP endpoint](https://gateway.pipeworx.io/zippopotam/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration] <br>
**Output Format:** [JSON tool responses and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented direct API example; no hidden or destructive behavior was reported in the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
