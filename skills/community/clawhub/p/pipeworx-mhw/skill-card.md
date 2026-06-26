## Description: <br>
MHW MCP — Monster Hunter World data (mhw-db.com, free, no auth) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can connect an agent to a remote MCP server for Monster Hunter World data lookups, including monsters, weapons, armor, and skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The remote MCP service may receive lookup requests and related context. <br>
Mitigation: Use it for public Monster Hunter World lookups and avoid sending unrelated sensitive information. <br>
Risk: The connection example installs mcp-remote@latest at setup time. <br>
Mitigation: Pin a trusted mcp-remote package version in stricter environments. <br>


## Reference(s): <br>
- [Pipeworx MHW Pack](https://pipeworx.io/packs/mhw) <br>
- [Pipeworx](https://pipeworx.io) <br>
- [Pipeworx MHW MCP Gateway](https://gateway.pipeworx.io/mhw/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [MCP tool responses and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; requests are handled by a remote MCP service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
