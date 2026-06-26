## Description: <br>
Set up a monday.com account for an OpenClaw agent and work with monday.com boards, items, and updates via the GraphQL API or MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure monday.com access for an OpenClaw agent and to query, create, or update monday.com boards, items, columns, and updates through GraphQL or the monday.com MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A monday.com token may grant access to boards, items, updates, and account data beyond the agent's intended scope. <br>
Mitigation: Install the skill only for an agent-specific monday.com account with the least permissions needed, and store MONDAY_API_TOKEN in OpenClaw environment settings or a secret manager. <br>
Risk: Plaintext token examples or saved board identifiers can expose credentials or private workspace context if checked into files. <br>
Mitigation: Do not paste real tokens into checked-in JSON files, avoid logging tokens, and keep TOOLS.md or saved board IDs private. <br>
Risk: Incorrect board, item, or column IDs can cause unwanted monday.com mutations or data corruption. <br>
Mitigation: Verify workspace, board, item, and column IDs before mutations and require explicit owner instruction before creating or updating board items. <br>


## Reference(s): <br>
- [monday.com GraphQL API reference](https://developer.monday.com/api-reference) <br>
- [monday.com MCP server docs](https://mcp.monday.com) <br>
- [Hosted monday.com MCP endpoint](https://mcp.monday.com/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/monday-for-agents) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with bash, JSON, and GraphQL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a monday.com API token supplied through MONDAY_API_TOKEN or OAuth for hosted MCP.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
