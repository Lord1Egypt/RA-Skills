## Description:

项目中枢 — 跨平台项目管理聚合器，统一管理 Trello、GitHub Issues、Linear、Notion、Obsidian 任务，支持自学习引擎和任务关系图谱

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanjing5024064](https://clawhub.ai/user/hanjing5024064)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers, developers, and teams use this skill to connect project-management sources, synchronize and search tasks, create or update work items, analyze sprints and blockers, and generate standup reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connected-service credentials may allow the skill to create, update, and comment on tasks.

Mitigation: Use least-privilege tokens and configure only the project-management services needed for the intended workflow.

Risk: Obsidian vault scanning can expose unrelated personal notes or local task data.

Mitigation: Point Obsidian only at a task-specific vault or folder and avoid mixed personal notes.

Risk: Local project-nerve data can contain cached task details and sensitive project information.

Mitigation: Treat the local project-nerve data directory as sensitive and restrict access to it.

## Reference(s):

- [Project Nerve Skill Page](https://clawhub.ai/hanjing5024064/skills/project-nerve)
- [Platform API Guide](references/api-guide.md)
- [Unified Task Model](references/unified-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON command results, Mermaid diagrams, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, update, cache, and analyze project-management tasks when configured with user-provided service credentials.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
