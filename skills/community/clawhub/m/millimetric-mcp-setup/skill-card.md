## Description: <br>
Connect AI agents (Claude Code, Claude Desktop, Cursor, MCP Inspector, OpenClaw) to the Millimetric MCP server so they can natively call track_event, query_events, get_stats, top_sources, and compare_projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soybelli](https://clawhub.ai/user/soybelli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analytics operators use this skill to configure MCP-capable agents so they can read Millimetric analytics, verify connectivity, and optionally write events when an appropriately scoped key is supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An AI agent can access Millimetric analytics through the supplied bearer token. <br>
Mitigation: Prefer a read-only rk_* key, grant sk_* or ak_* only when the agent truly needs write or account-wide access, and rotate the key if it is exposed. <br>
Risk: MCP client configuration files can contain sensitive bearer tokens. <br>
Mitigation: Protect local MCP configuration files, avoid committing them, and limit file access to users and processes that need the key. <br>
Risk: Account keys can expose analytics across multiple projects. <br>
Mitigation: Use ak_* keys only for deliberate multi-project workflows and confirm project visibility before allowing an agent to query account-wide data. <br>


## Reference(s): <br>
- [Millimetric MCP endpoint](https://api.millimetric.ai/mcp) <br>
- [Millimetric account MCP endpoint](https://api.millimetric.ai/mcp/account) <br>
- [ClawHub skill page](https://clawhub.ai/soybelli/millimetric-mcp-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes MCP endpoint setup, key-scope guidance, CLI verification commands, tool names, result-shape notes, and error explanations] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
