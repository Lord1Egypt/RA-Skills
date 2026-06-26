## Description: <br>
Personal knowledge graph. Record notes, track moods, manage tasks, spot patterns in someone's life. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Vladikasik](https://clawhub.ai/user/Vladikasik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their connected agents use Neron to query and update a personal knowledge graph built from notes, moods, activities, body states, tasks, people, projects, and AI-generated insights. The skill helps agents search the graph, synthesize patterns, manage tasks, and write back notes or insights through the Neron MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Connected agents can access private notes, inferred moods, body and substance data, relationships, tasks, and long-term memories. <br>
Mitigation: Install only for trusted, user-directed agents and avoid sharing tokens, passwords, screenshots, logs, or chats that contain credentials or sensitive graph data. <br>
Risk: The skill exposes write, delete, bulk-create, and raw Cypher capabilities that can change or remove graph data. <br>
Mitigation: Review agent actions before enabling autonomous writes, deletes, or raw queries, and prefer explicit user approval for destructive operations. <br>
Risk: Bearer tokens and connector passwords grant access to a user's Neron graph if exposed. <br>
Mitigation: Store credentials outside shared repositories and logs, rotate them if exposed, and use the documented per-user revocation flow. <br>


## Reference(s): <br>
- [Neron ClawHub page](https://clawhub.ai/Vladikasik/neron) <br>
- [Neron README](README.md) <br>
- [Neron User Guide](docs/USER-GUIDE.md) <br>
- [Connect Neron to Your Agent](docs/CONNECT-AGENT.md) <br>
- [Neron MCP Tool Reference](docs/mcp-tools.md) <br>
- [Neron MCP endpoint](https://mcp.neron.guru/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON and Cypher examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to call Neron MCP tools for search, graph traversal, entity creation, updates, deletion, bulk creation, and raw Cypher analytics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
