## Description: <br>
MemPalace provides local AI memory with semantic search, a temporal knowledge graph, and a palace-style wing, room, and drawer organization model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to a local MemPalace MCP memory store, search prior conversation-derived memories, maintain temporal facts, and write session diary entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory may preserve conversation-derived information across sessions without clear consent or retention boundaries. <br>
Mitigation: Define explicit save rules before use, avoid saving secrets or sensitive personal data, and require confirmation before diary writes or knowledge-graph changes. <br>
Risk: Memory write, invalidation, and deletion tools can alter or remove local records. <br>
Mitigation: Require user confirmation before adding drawers, invalidating graph facts, or deleting drawers, and review proposed writes for sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blueworldmarketing/mempalace-bwm) <br>
- [Publisher profile](https://clawhub.ai/user/blueworldmarketing) <br>
- [MemPalace GitHub repository](https://github.com/MemPalace/mempalace) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent to call MemPalace MCP tools for local search, browsing, writing, deletion, and temporal knowledge-graph updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists MemPalace 3.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
