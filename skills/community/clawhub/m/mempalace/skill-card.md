## Description:

MemPalace provides local AI memory with semantic search over past conversations, a temporal knowledge graph, and a palace-style organization model for stored memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanikua](https://clawhub.ai/user/wanikua)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to a local MemPalace memory store, search prior conversation archives, query temporal facts, and write updated memories across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation archives may contain secrets, regulated data, or sensitive personal information that the skill can store and search locally.

Mitigation: Mine only approved folders, exclude sensitive archives, and avoid using the skill with data the user is not comfortable storing and searching locally.

Risk: The local MemPalace package receives access to private conversation history during initialization, mining, and MCP operation.

Mitigation: Pin and separately review the mempalace package before installation or deployment, especially in managed or commercial environments.

Risk: Stored memories and temporal facts can be reused in later sessions and may influence responses if stale or incorrect.

Mitigation: Use the documented delete and knowledge-graph invalidation workflows to remove outdated entries and replace changed facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanikua/skills/mempalace)
- [MemPalace project homepage](https://github.com/milla-jovovich/mempalace)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP tool usage guidance and local installation/setup steps.]

## Skill Version(s):

1.4.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
