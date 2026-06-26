## Description: <br>
Provides real-time and historical USGS streamflow and gage height data for rivers, creeks, and streams across the United States. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up current USGS monitoring-site readings, search active stream gages by state, and retrieve daily mean streamflow history for US waterways. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: USGS site IDs, state searches, and date-range queries are handled by the Pipeworx gateway. <br>
Mitigation: Users with strict query-privacy or official-source-only requirements should use a direct USGS integration instead. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/b-gutman/pipeworx-usgswater) <br>
- [Pipeworx USGS Water MCP gateway](https://gateway.pipeworx.io/usgswater/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns USGS site readings, stream-gage search results, daily streamflow values, and MCP server configuration guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
