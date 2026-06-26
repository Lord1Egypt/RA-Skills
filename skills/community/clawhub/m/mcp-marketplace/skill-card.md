## Description: <br>
Install, configure, and manage MCP servers with catalog search, config generation for OpenClaw, Claude Desktop, Claude Code, and Cursor, plus health-check and troubleshooting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiizzzyyy](https://clawhub.ai/user/iiizzzyyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to discover MCP servers, generate client configuration, install or record selected servers, check server health, and troubleshoot authentication or transport issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install, update, and health-check workflows can cause an agent to run package, Docker, or configured server commands. <br>
Mitigation: Review each generated command, package name, source, Docker image, and target config before execution or merge. <br>
Risk: Health checks can launch configured MCP servers and pass environment-derived secrets or Authorization headers. <br>
Mitigation: Health-check only trusted configs and endpoints, use least-privilege tokens, and prefer temporary environment variables or a secrets manager. <br>
Risk: Generated MCP configurations may connect clients to servers with local filesystem, network, database, or hosted service access. <br>
Mitigation: Confirm the server choice and auth readiness with the user, inspect the generated config entry, and avoid broad Docker mounts or unnecessary HTTP endpoints. <br>
Risk: Fallback results from npm or Smithery are not treated as team-verified servers by the skill text. <br>
Mitigation: Prefer curated or ClawHub bundle matches when available and warn users before installing unverified registry results. <br>


## Reference(s): <br>
- [MCP Marketplace skill page](https://clawhub.ai/iiizzzyyy/mcp-marketplace) <br>
- [OAuth Flow Patterns for MCP Servers](references/oauth-patterns.md) <br>
- [MCP Transport Patterns](references/transport-patterns.md) <br>
- [MCP Server Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated MCP config entries, install or health-check commands, registry search results, and troubleshooting steps.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
