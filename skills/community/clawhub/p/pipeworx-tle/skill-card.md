## Description: <br>
Fetch and search Two-Line Element sets for satellites by NORAD ID or name, providing orbit data for tracking and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, satellite operators, and analysts use this skill to fetch current satellite TLE data, search satellites by name or keyword, and configure an agent to call the Pipeworx TLE MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Satellite names, lookup terms, or NORAD IDs are sent to an external Pipeworx MCP service. <br>
Mitigation: Use the skill only when sharing those lookup terms with the disclosed endpoint is acceptable. <br>
Risk: Results depend on the availability and accuracy of the external TLE service. <br>
Mitigation: Validate important orbit data against authoritative sources before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-tle) <br>
- [Pipeworx TLE MCP endpoint](https://gateway.pipeworx.io/tle/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with TLE lines, JSON-RPC examples, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on the disclosed Pipeworx TLE MCP endpoint and does not request credentials or local access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
