## Description: <br>
MCP CLI Manager - Manage MCP servers and call tools <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maplezzk](https://clawhub.ai/user/maplezzk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to manage MCP server configurations, run the mcps daemon, list available tools, and call tools from configured MCP servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured MCP server commands can run on the user's machine through the mcps daemon. <br>
Mitigation: Install only trusted packages and add only trusted MCP server commands before starting the daemon. <br>
Risk: Secrets in configuration files or environment variables may be exposed to configured MCP servers. <br>
Mitigation: Keep ~/.mcps/mcp.json and environment variables sensitive, scope credentials narrowly, and pass secrets only to servers that require them. <br>
Risk: Tool calls can send user-provided arguments and data to configured MCP servers or external services. <br>
Mitigation: Review server configuration and tool parameters before invoking tools, especially for database, web, and remote HTTP servers. <br>


## Reference(s): <br>
- [Mcps ClawHub page](https://clawhub.ai/maplezzk/mcps-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that start or stop a daemon, edit MCP server configuration, and call tools on configured MCP servers.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
