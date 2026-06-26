## Description: <br>
Access and search Bureau of Labor Statistics economic data series, including historical and latest data for employment, inflation, wages, productivity, and housing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search BLS economic series, retrieve historical data, fetch latest series points, and browse popular series categories through the Pipeworx BLS MCP gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BLS search terms and series requests are sent to the third-party Pipeworx MCP gateway. <br>
Mitigation: Install only when that routing is acceptable; use a direct BLS API connector when official-source-only data paths are required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/brucegutman/pipeworx-bls) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>
- [Pipeworx BLS MCP gateway](https://gateway.pipeworx.io/bls/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown with a JSON MCP server configuration block and text responses from BLS lookup tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests are routed through the third-party Pipeworx MCP gateway; the evidence does not indicate credentials or local access are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
