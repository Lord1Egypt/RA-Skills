## Description:

Knowledge Graph Buil guides an agent through building and managing a knowledge graph with typed entities, SQLite migration, graph visualization, SPARQL-like queries, version tracking, cross-skill events, and platform integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, architects, and technical leads use this skill to maintain larger agent knowledge graphs, generate visualizations and reports, query relationships, and manage snapshots or integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad command and file access.

Mitigation: Review generated commands before execution and keep graph operations local unless the user explicitly approves broader access.

Risk: Callback URLs, bidirectional sync, and automatic event subscriptions can expose private project, team, Jira, CI/CD, or knowledge-base data.

Mitigation: Require explicit approval for callbacks and sync targets, prefer local-only graph operations by default, and verify kg commands before snapshot restore, bidirectional sync, or automatic event subscriptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-graph-builder-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, JSON/configuration snippets, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local graph files, SQLite storage, visualizations, reports, snapshots, callback configuration, and sync commands for user review.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
