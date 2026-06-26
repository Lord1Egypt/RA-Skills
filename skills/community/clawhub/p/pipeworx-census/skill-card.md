## Description: <br>
Access U.S. Census Bureau housing data including ACS, building permits, housing starts, homeownership rates, and available census datasets by geography. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, developers, and agents use this skill to connect to Pipeworx Census MCP tools for housing-related Census lookups by geography, including ACS variables, building permits, housing starts, homeownership rates, and dataset discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests to the Census MCP endpoint leave the local agent environment and are handled by the Pipeworx gateway. <br>
Mitigation: Avoid sending private or confidential context in tool calls unless the Pipeworx gateway is trusted for the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-census) <br>
- [Pipeworx Census MCP endpoint](https://gateway.pipeworx.io/census/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, text] <br>
**Output Format:** [Markdown with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Configures a remote MCP endpoint for Census housing-data lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
