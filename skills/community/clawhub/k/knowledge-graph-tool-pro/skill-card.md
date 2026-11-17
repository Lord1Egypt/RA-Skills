## Description:

知识图谱工具(专业版) helps teams and enterprises manage long-term structured knowledge with KGML-compatible graph querying, entity merging, encrypted vault storage, offline visualization, multi-agent sharing, and reviewed memory import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, team knowledge curators, and enterprise agent operators use this skill to build and maintain shared knowledge graphs, preserve decision records, manage sensitive configuration references, generate offline graph views, and coordinate long-term memory across agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to handle credentials and vault files, including raw secret retrieval flows.

Mitigation: Require explicit user confirmation before vault access, never display retrieved secrets in chat or logs, and keep vault files and workspace paths tightly scoped.

Risk: The skill can affect shared team folders, memory imports, writes, exports, and exec-backed actions with unclear operational boundaries.

Mitigation: Default to read-only access where possible, require confirmation before writes, exports, memory import, or command execution, and review generated changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-graph-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files, guidance]

**Output Format:** [Markdown guidance with JSON responses, KGML text, bash and JavaScript snippets, and generated HTML or JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose exec-backed actions, workspace paths, vault operations, memory imports, exports, and generated visualization files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
