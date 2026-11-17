## Description:

GoalGetter helps OpenClaw agents create, track, complete, and display tasks and goals using local markdown files with streak tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steffano198](https://clawhub.ai/user/steffano198)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use GoalGetter to manage personal or team tasks, goals, and habit streaks through an agent workflow backed by local markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task names, goal names, streak counts, and completion history are stored in local markdown files under ~/.openclaw/goalgetter/.

Mitigation: Avoid entering sensitive personal or work information unless local plaintext storage is acceptable for the environment.

Risk: Casual phrasing could be interpreted as a request to update a task or goal streak.

Mitigation: Use explicit commands for task completion and goal updates, and review the current markdown state before modifying files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/steffano198/skills/goalgetter)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and local file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes task, goal, streak, and completion history to local markdown files under ~/.openclaw/goalgetter/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
