## Description: <br>
Access real-time and historical SpaceX data on launches, rockets, crew, and Starlink satellites with detailed status and media links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to query a disclosed Pipeworx MCP gateway for SpaceX launch, rocket, crew, and Starlink information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SpaceX data queries are sent to a disclosed third-party Pipeworx MCP gateway. <br>
Mitigation: Use the skill only when sending those queries to the gateway is acceptable for the deployment context. <br>
Risk: External SpaceX data can be incomplete, stale, or unavailable depending on the upstream service. <br>
Mitigation: Verify time-sensitive launch, crew, rocket, or satellite details against authoritative sources before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-spacex) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>
- [Pipeworx SpaceX MCP gateway](https://gateway.pipeworx.io/spacex/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return SpaceX launch, rocket, crew, and Starlink data from the configured MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
