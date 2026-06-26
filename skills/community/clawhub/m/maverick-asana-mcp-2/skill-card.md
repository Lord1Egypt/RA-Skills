## Description: <br>
Manage Asana tasks, projects, portfolios, goals, and team workspaces via Asana's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and agents use this skill to search, read, create, and update Asana work items through Asana's hosted MCP server when the user asks for help with tasks, projects, portfolios, goals, assignees, or team workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can act through the connected Asana OAuth grant, including reading and updating work visible to that account. <br>
Mitigation: Use an appropriately scoped Asana account and confirm create, update, or delete intent for the specific Asana object before invoking write-capable tools. <br>
Risk: Tool arguments and results transit Asana's hosted MCP server, so unrelated sensitive data could be exposed if included in requests. <br>
Mitigation: Send only Asana-relevant data through tool calls and avoid passing unrelated sensitive content. <br>
Risk: The OAuth grant persists until revoked and stale credential rotation can break the integration. <br>
Mitigation: Revoke the Asana grant when no longer needed and rerun setup only with freshly issued OAuth credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-asana-mcp-2) <br>
- [Asana MCP server overview](https://developers.asana.com/docs/mcp-server) <br>
- [Integrating with Asana's MCP Server](https://developers.asana.com/docs/integrating-with-asanas-mcp-server) <br>
- [mcporter config docs](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON tool output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool results and write effects depend on the live Asana MCP server and the connected OAuth grant.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
