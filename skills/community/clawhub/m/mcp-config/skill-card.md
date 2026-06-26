## Description: <br>
Mcp Config helps agents add, move, format, and troubleshoot MCP server configuration across Claude Code, Cursor, and Antigravity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure MCP servers, choose the correct scope, validate JSON or CLI registration, and diagnose connection failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP configuration examples can expose sensitive credentials or grant broad database access, especially when copied without review. <br>
Mitigation: Use least-privilege credentials, avoid storing secrets in shared project config, prefer read-only database roles, and confirm global or project MCP changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drumrobot/mcp-config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP configuration examples that reference credentials or database access; users should apply least-privilege settings before use.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
