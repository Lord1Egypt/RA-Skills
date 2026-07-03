## Description: <br>
Install and configure the AgentPMT MCP server for AI agents and MCP-compatible clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect Claude Desktop, Claude Code, Cursor, Windsurf, VS Code, Zed, Codex CLI, Gemini CLI, or other MCP-compatible clients to AgentPMT tools using either a local STDIO router or a remote HTTPS MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects agents to paid AgentPMT tools and APIs, which can spend from configured budgets. <br>
Mitigation: Use tightly scoped budget keys, approve only needed products, and review spending caps before enabling tools. <br>
Risk: The STDIO setup path installs local npm code and stores a bearer token in MCP client configuration. <br>
Mitigation: Review the package and setup behavior before installation, consider pinning package versions, and verify where the client stores the token. <br>
Risk: AgentPMT API keys, budget keys, and derived bearer tokens are sensitive credentials. <br>
Mitigation: Do not log or commit credentials; rotate keys after exposure and prefer least-privilege budget keys. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/agentpmt/install-agentpmt-mcp) <br>
- [AgentPMT website](https://www.agentpmt.com) <br>
- [AgentPMT MCP endpoint](https://api.agentpmt.com/mcp) <br>
- [AgentPMT dashboard](https://www.agentpmt.com/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes client-specific MCP configuration examples and troubleshooting checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
