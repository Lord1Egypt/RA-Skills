## Description: <br>
Dynamic OAuth for AI agents via Pipedream. Generate OAuth links for 2500+ APIs, let users authorize, then call MCP tools on their behalf. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to request user authorization for third-party apps through Pipedream, check connection status, list available tools, and call app tools on the user's behalf. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may gain broad, persistent access to connected third-party accounts. <br>
Mitigation: Authorize only the apps needed, inspect OAuth scopes before approval, and use dedicated or limited accounts where possible. <br>
Risk: Authorized tool calls may send, write, or update data in external services. <br>
Mitigation: Confirm every send, write, or update action before the agent runs it, and review how to revoke Pipedream or app access afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/G9Pedro/pdauth) <br>
- [Publisher profile](https://clawhub.ai/user/G9Pedro) <br>
- [Pipedream MCP app catalog](https://mcp.pipedream.com) <br>
- [Project homepage](https://github.com/Versatly/pdauth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and JSON-oriented CLI outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use the pdauth CLI for OAuth links, connection checks, tool discovery, and authorized tool calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
