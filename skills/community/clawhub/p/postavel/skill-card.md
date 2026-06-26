## Description: <br>
Connects an agent to Postavel through MCP so users can create, schedule, approve, and manage Facebook, Instagram, and LinkedIn posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nezaboravi](https://clawhub.ai/user/nezaboravi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and social media managers use this skill to connect an agent to their Postavel account, inspect workspaces and brands, draft or schedule social posts, and manage approval workflows through natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation workflows can execute shell commands, install mcporter, and may fall back to direct binary download with sudo. <br>
Mitigation: Prefer Homebrew or npm installation, review scripts before running them, and avoid the sudo direct-download fallback unless the binary source can be verified. <br>
Risk: Publishing, scheduling, approving, bulk-approving, or deleting social posts can have high-impact external effects. <br>
Mitigation: Require explicit user confirmation before actions that publish, schedule, auto-approve, bulk-approve, or delete posts. <br>
Risk: OAuth tokens or Postavel account access can expose workspace and brand data if handled carelessly. <br>
Mitigation: Use least-privileged Postavel accounts, rely on OAuth, avoid placing tokens in shell environment variables, and revoke access from Postavel settings when no longer needed. <br>


## Reference(s): <br>
- [Postavel MCP Tools Reference](references/mcp-tools.md) <br>
- [Postavel MCP Setup Guide](references/setup-guide.md) <br>
- [Postavel MCP Server](https://postavel.com/mcp/postavel) <br>
- [Postavel ClawHub Release](https://clawhub.ai/nezaboravi/postavel) <br>
- [mcporter Repository](https://github.com/steipete/mcporter.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or schedule social media content through the user's authenticated Postavel account, subject to Postavel permissions and approval workflows.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
