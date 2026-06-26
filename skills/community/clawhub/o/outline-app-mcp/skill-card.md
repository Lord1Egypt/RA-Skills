## Description: <br>
Model Context Protocol (MCP) bridge for Outline (getoutline.com). Enables AI agents to search, read, create, and manage documents, collections, and comments in an Outline workspace via SSE transport. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuellie](https://clawhub.ai/user/samuellie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to let an agent work with Outline knowledge bases: search and read documents, create or update content, manage collections, and collaborate through comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can read local files for upload and send them to the configured Outline workspace. <br>
Mitigation: Install only where the agent is trusted, run from a host account with limited file access, and monitor or restrict upload and bulk-sync usage. <br>
Risk: Authenticated tool calls can modify Outline documents, collections, and comments. <br>
Mitigation: Use the least-privileged Outline API key available and review agent activity for unexpected workspace changes. <br>


## Reference(s): <br>
- [Outline MCP on ClawHub](https://clawhub.ai/samuellie/outline-app-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/samuellie) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown and JSON responses with command-line configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OUTLINE_API_KEY, OUTLINE_URL, node, and npm; can use local files for Outline uploads when enabled.] <br>

## Skill Version(s): <br>
1.3.4 (source: server release evidence, frontmatter metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
