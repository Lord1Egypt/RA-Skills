## Description: <br>
Connect OpenClaw to the Latitude MCP server so the agent can read and manage your Latitude workspace, including projects, traces, spans, issues, annotations, scores, saved searches, datasets, monitors, and members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[latitude](https://clawhub.ai/user/latitude) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use this skill to connect an agent to a Latitude workspace through Latitude's OAuth-authenticated remote MCP server. It helps the agent query and manage observability and evaluation resources such as traces, spans, issues, annotations, scores, datasets, monitors, and members. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected agent can access sensitive Latitude workspace resources, including projects, traces, spans, issues, annotations, scores, datasets, monitors, members, and API keys. <br>
Mitigation: Authorize only the intended Latitude organization, revoke OAuth access when it is no longer needed, and apply least-privilege access where Latitude supports it. <br>
Risk: The remote MCP server can expose high-impact management tools to the agent. <br>
Mitigation: Review the exposed tools before use, apply OpenClaw tool filters, and require explicit approval for member management, API key access, and other high-impact actions. <br>


## Reference(s): <br>
- [Latitude MCP documentation](https://docs.latitude.so/getting-started/mcp) <br>
- [Latitude](https://latitude.so) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides OpenClaw MCP setup, OAuth login, verification, logout, self-hosting, and tool-filter guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
