## Description: <br>
Deploy a remote MCP server on Vercel with Next.js and mcp-handler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucaperret](https://clawhub.ai/user/lucaperret) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add a Streamable HTTP MCP endpoint to a Next.js application and deploy it on Vercel for clients such as Claude Desktop, claude.ai, Smithery, and other MCP clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public MCP endpoints may expose write or delete operations to remote clients without adequate access control. <br>
Mitigation: Add real authentication and authorization before exposing write or destructive tools, and review each tool annotation before deployment. <br>
Risk: Deployment commands may target the wrong Vercel account or project. <br>
Mitigation: Confirm the active Vercel account, project, and production target before running deployment commands. <br>
Risk: Generated route code or dependency versions may not match the application's production requirements. <br>
Mitigation: Review the generated route code, lock dependency versions, and test the MCP initialize request before publishing the endpoint. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lucaperret/mcp-vercel) <br>
- [Skill Homepage](https://github.com/lucaperret/agent-skills) <br>
- [mcp-handler](https://github.com/vercel/mcp-handler) <br>
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) <br>
- [Vercel MCP Documentation](https://vercel.com/docs/mcp) <br>
- [Smithery Publishing](https://smithery.ai/new) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, JavaScript, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for creating and deploying a Vercel-hosted MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
