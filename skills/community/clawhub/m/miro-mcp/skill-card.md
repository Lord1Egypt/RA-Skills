## Description: <br>
Connects OpenClaw agents to Miro through the Model Context Protocol for diagram generation, board analysis, code-oriented workflows, and collaborative planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigbubbaagent-bot](https://clawhub.ai/user/bigbubbaagent-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and project teams use this skill to connect an AI assistant to Miro boards, generate diagrams from code or product requirements, summarize board content, and turn visual designs into implementation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated agents may read from or write to shared Miro boards within the selected team. <br>
Mitigation: Prefer read-only scopes when possible, keep auto-approval disabled for write-capable tools, and verify the target team and board before edits or bulk synchronization. <br>
Risk: Board images, documents, prototype details, and URLs may contain sensitive information that is exposed to the connected AI client. <br>
Mitigation: Review the client's data-handling policy before use and avoid sharing sensitive board content with clients that have not been approved for that data. <br>
Risk: Broad or parallel board reads can trigger rate limits or consume Miro AI credits through expensive context operations. <br>
Mitigation: Use discovery tools before detailed reads, run context retrieval selectively and sequentially, and cache frequently accessed board content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bigbubbaagent-bot/miro-mcp) <br>
- [Miro MCP server](https://mcp.miro.com/) <br>
- [GitHub MCP Registry entry for Miro](https://github.com/mcp/miroapp/mcp-server) <br>
- [Connecting Miro MCP to AI Coding Tools](references/ai-coding-tools.md) <br>
- [Best Practices for Miro MCP](references/best-practices.md) <br>
- [Connecting to Miro MCP](references/mcp-connection.md) <br>
- [Miro MCP Overview](references/mcp-overview.md) <br>
- [Miro MCP Tools & Prompts](references/mcp-prompts.md) <br>
- [REST API Essentials for Miro MCP](references/rest-api-essentials.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets, prompts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Miro board URLs, OAuth setup steps, MCP client configuration, REST API examples, and generated implementation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
