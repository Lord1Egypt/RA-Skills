## Description:

知识图谱工具(免费版) helps agents maintain a lightweight local JSON knowledge graph for personal entities, relationships, basic queries, and compact context summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent users, and agent operators use this skill to create and query a local personal knowledge graph, persist entities and relationships, and summarize graph context for later agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist memory and instructions into agent configuration files, which may carry unintended context into future sessions.

Mitigation: Review the proposed AGENTS.md, CLAUDE.md, or GEMINI.md changes before installation and use the skill only in workspaces where persistent local memory is intended.

Risk: Broad activation wording may cause the skill to be used outside focused knowledge-graph maintenance tasks.

Mitigation: Scope usage to explicit knowledge-graph create, read, update, delete, query, and summary workflows, and review outputs before relying on persisted context.

Risk: Personal notes, secrets, or sensitive graph data could enter future agent context through generated summaries.

Mitigation: Do not store secrets or sensitive private notes in the graph unless summary behavior has been reviewed and the workspace is approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-graph-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and KGML/text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs focus on local knowledge-graph operations, configuration guidance, and compact context summaries.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
