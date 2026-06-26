## Description: <br>
Search, read, and update Monday.com boards, workspaces, items, updates, and columns via Monday.com's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to search, read, and update Monday.com boards, workspaces, items, updates, and column values through Monday.com's hosted MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bearer token can allow access to Monday.com workspace data visible to the connected account. <br>
Mitigation: Use the least-privileged token available, keep it out of user-visible output, and rotate it if exposed. <br>
Risk: Write tools can create, update, delete, archive, publish, comment on, or otherwise modify Monday.com workspace data. <br>
Mitigation: Require explicit user confirmation before write operations and inspect target board, workspace, item, and column state before changing it. <br>
Risk: The live Monday.com MCP server is the source of truth for available tools and schemas, so the active tool surface can differ from remembered examples. <br>
Mitigation: List the live tool catalog and schemas before sensitive work, then use only the tools and parameters returned by the server. <br>
Risk: The artifact installs mcporter from npm without pinning a package version. <br>
Mitigation: Operators with strict supply-chain requirements should override the install with a pinned mcporter version. <br>


## Reference(s): <br>
- [Monday.com hosted MCP server](https://mcp.monday.com/mcp) <br>
- [mcporter MCP CLI](https://github.com/openclaw/mcporter) <br>
- [ClawHub skill release](https://clawhub.ai/maverick/maverick-monday-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and MCP tool results, optionally JSON when requested through mcporter] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAVERICK_MONDAY_MCP_ACCESS_TOKEN and the mcporter CLI.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
