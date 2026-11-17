## Description:

Track habits, log completions, and analyze progress with CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create habits, log completions, review statistics, generate progress reports, and check local reminders from a Node.js CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit names, reminders, completion history, and optional notes are stored as local plaintext JSON files.

Mitigation: Use the skill only for information you are comfortable storing locally in plaintext under ~/.config/habit-tracker.

Risk: The delete command removes a habit and its logs immediately.

Mitigation: Review the target habit name or ID before running delete, and keep separate backups if the history must be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/pearl-habit-tracker)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local JSON files under ~/.config/habit-tracker when the CLI is executed.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
