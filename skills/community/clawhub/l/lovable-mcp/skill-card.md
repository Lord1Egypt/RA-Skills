## Description: <br>
Use Lovable's MCP server to create, iterate on, and deploy full-stack web apps from natural-language prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merlindegrote](https://clawhub.ai/user/merlindegrote) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, iterate, inspect, and deploy Lovable full-stack web apps, and to manage Lovable projects, databases, connectors, analytics, and workspace governance through MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad Lovable project, deployment, database, workspace, and persistent OAuth authority. <br>
Mitigation: Install only when that authority is intended, and require explicit approval before delete, deploy, SQL, governance, connector, or workspace-wide actions. <br>
Risk: Local OAuth token files and refresh tokens can expose long-lived account access if mishandled. <br>
Mitigation: Inspect setup scripts before running them, protect local token storage, avoid committing credentials, and revoke exposed tokens through Lovable support. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/merlindegrote/lovable-mcp) <br>
- [Lovable](https://lovable.dev) <br>
- [Lovable MCP server](https://mcp.lovable.dev) <br>
- [Lovable OAuth authorization metadata](https://lovable.dev/oauth/.well-known/oauth-authorization-server) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with bash, JSON, and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to call Lovable MCP tools that create, modify, deploy, query, or manage projects and workspaces.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
