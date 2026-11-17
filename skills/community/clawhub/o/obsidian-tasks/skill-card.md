## Description:

Set up and manage Obsidian task boards with Kanban, Dataview dashboards, structured task notes, and synchronized board/frontmatter workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[larsderidder](https://clawhub.ai/user/larsderidder)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and Obsidian users use this skill to initialize and maintain a task board in an Obsidian vault, including task notes, board cards, status updates, and Dataview dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script can write outside the intended Obsidian vault folder if given an absolute path or traversal value in --folder.

Mitigation: Use the skill first on a test or backed-up vault, pass a simple relative folder name such as Tasks, and avoid absolute paths or ../ in --folder.

## Reference(s):

- [Obsidian](https://obsidian.md)
- [Obsidian Kanban plugin](https://github.com/mgmeyers/obsidian-kanban)
- [Obsidian Dataview plugin](https://github.com/blacksmithgu/obsidian-dataview)
- [ClawHub skill page](https://clawhub.ai/larsderidder/skills/obsidian-tasks)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and concise setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates Obsidian board and dashboard files in a selected vault folder; requires the Kanban and Dataview community plugins.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
