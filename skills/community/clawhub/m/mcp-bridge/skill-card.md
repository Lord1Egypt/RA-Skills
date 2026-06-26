## Description: <br>
Use mcp-bridge-openclaw CLI to connect to and manage Model Context Protocol (MCP) servers with auto-reconnection and retry logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaggu1999](https://clawhub.ai/user/jaggu1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate an npm-based bridge for connecting agents to user-configured MCP servers with retry and reconnection behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an npm CLI and running configured MCP server commands can execute third-party code. <br>
Mitigation: Review the npm package and each command in config.json before use. <br>
Risk: MCP servers may receive access to sensitive files, accounts, or tokens based on the configured command and environment. <br>
Mitigation: Connect only trusted MCP servers, use least-privilege tokens, and pass secrets through environment variables instead of plaintext config. <br>


## Reference(s): <br>
- [mcp-bridge-openclaw npm package](https://www.npmjs.com/package/mcp-bridge-openclaw) <br>
- [ClawHub skill page](https://clawhub.ai/jaggu1999/mcp-bridge) <br>
- [OpenClaw MCP Bridge repository](https://github.com/Jatira-Ltd/OpenClaw-MCP-Bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI commands, MCP server configuration examples, and programmatic usage guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
