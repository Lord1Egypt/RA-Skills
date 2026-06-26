## Description: <br>
Search, read, and manage Canva design work through Canva's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and creative teams use this skill to let an agent search, inspect, export, and manage Canva designs, assets, folders, comments, brand materials, and templates through Canva's hosted MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected Canva OAuth grant lets the agent act through the user's Canva account, including write-capable actions when the grant allows them. <br>
Mitigation: Use the least-privileged Canva grant available, confirm clear user intent before write actions, inspect relevant design or asset state before editing, and revoke the integration when it is no longer needed. <br>
Risk: Tool arguments and results transit Canva's hosted MCP service, so unrelated sensitive content could be exposed if included in requests. <br>
Mitigation: Only send content needed for the Canva task and avoid placing unrelated secrets or sensitive material in tool arguments. <br>
Risk: Re-running setup with stale OAuth values can overwrite fresher local credentials and break the integration. <br>
Mitigation: Run credential setup only with freshly minted OAuth values, and re-authorize in Canva if calls keep failing with authentication errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-canva-mcp) <br>
- [Canva MCP overview and endpoint](https://www.canva.dev/docs/mcp/) <br>
- [Canva MCP troubleshooting and authentication](https://www.canva.dev/docs/mcp/troubleshooting/) <br>
- [mcporter configuration reference](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-capable MCP tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and user-provided Canva OAuth credentials; live tool schemas come from Canva's hosted MCP server.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
