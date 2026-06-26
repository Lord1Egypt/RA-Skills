## Description: <br>
Set up and manage an Obsidian task board with Kanban + Dataview, including a Tasks/Board.md pipeline, per-task notes with YAML frontmatter, and Dataview dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larsderidder](https://clawhub.ai/user/larsderidder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Obsidian users use this skill to initialize and maintain task-tracking files in an Obsidian vault, including Kanban board entries, task-note frontmatter, and dashboard queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local task-board setup and task management can modify files inside an Obsidian vault. <br>
Mitigation: Use a precise vault path, keep normal Obsidian backups or sync history, and review broad task edits before relying on them. <br>
Risk: The maintainer publish helper can publish this skill to ClawHub if run with publisher credentials. <br>
Mitigation: Ignore the publish script during normal task-board use and run it only when intentionally publishing a release. <br>
Risk: Board and dashboard behavior depends on the Obsidian Kanban and Dataview community plugins. <br>
Mitigation: Install and enable those plugins in the target Obsidian vault before relying on rendered boards or dashboard queries. <br>


## Reference(s): <br>
- [Obsidian](https://obsidian.md) <br>
- [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban) <br>
- [Obsidian Dataview plugin](https://github.com/blacksmithgu/obsidian-dataview) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and concise setup or task-management instructions with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local Obsidian task-board files under a user-specified vault folder.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
