## Description:

Set up and manage an Obsidian task board with Kanban + Dataview. Creates a Tasks/Board.md pipeline (Backlog/Todo/In Progress/Review/Done), per-task notes with YAML frontmatter (status/priority/category/due), and dashboards via Dataview queries. Use for task tracking, moving cards between columns, keeping board + frontmatter in sync, and linking tasks to supporting notes/research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larsderidder](https://clawhub.ai/user/larsderidder)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to initialize and maintain task tracking inside an Obsidian vault with Kanban boards, Dataview dashboards, structured task notes, and wikilinks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can escape the chosen vault when unsafe folder values are used.

Mitigation: Use a simple relative --folder value such as Tasks and avoid absolute paths or ../ components.

Risk: The documented install and publish commands run mutable remote ClawHub CLI code.

Mitigation: Pin or preinstall the ClawHub CLI before use, and run publishing with limited credentials in an isolated environment.

Risk: The skill can write markdown task-board and dashboard files in an Obsidian vault.

Mitigation: Install only where vault file creation is acceptable, and review generated Board.md, Dashboard.md, and task note changes before relying on them.

## Reference(s):

- [Obsidian](https://obsidian.md)
- [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban)
- [Obsidian Dataview plugin](https://github.com/blacksmithgu/obsidian-dataview)
- [ClawHub skill page](https://clawhub.ai/larsderidder/skills/openclaw-obsidian-tasks)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates Obsidian vault files such as Board.md, Dashboard.md, and per-task markdown notes.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
