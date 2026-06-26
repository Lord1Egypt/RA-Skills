## Description: <br>
Set up and manage an Obsidian task board with Kanban + Dataview. Creates a Tasks/Board.md pipeline (Backlog/Todo/In Progress/Review/Done), per-task notes with YAML frontmatter (status/priority/category/due), and dashboards via Dataview queries. Use for task tracking, moving cards between columns, keeping board + frontmatter in sync, and linking tasks to supporting notes/research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larsderidder](https://clawhub.ai/user/larsderidder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, knowledge workers, and agent users use this skill to initialize and maintain task-management files inside an Obsidian vault. It helps create Kanban and Dataview Markdown artifacts, manage task notes with frontmatter, move cards between workflow columns, and link tasks to supporting notes or research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and edit task Markdown files in the Obsidian vault and folder selected by the user. <br>
Mitigation: Confirm the vault path before running setup, and use backups or version control when task history matters. <br>
Risk: The generated board and dashboard depend on the Obsidian Kanban and Dataview community plugins. <br>
Mitigation: Install and enable the required Obsidian plugins before relying on Board.md and Dashboard.md behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/larsderidder/openclaw-obsidian-tasks) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Obsidian](https://obsidian.md) <br>
- [Obsidian Kanban Plugin](https://github.com/mgmeyers/obsidian-kanban) <br>
- [Obsidian Dataview Plugin](https://github.com/blacksmithgu/obsidian-dataview) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files and concise setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates Obsidian task-board and dashboard Markdown files in a user-selected vault folder.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
