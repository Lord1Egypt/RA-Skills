## Description:

Track habits, routines, streaks, completions, reminders, and weekly progress with a local Node.js CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create local habit-tracking workflows, log completions, review streaks and progress, recover from missed routines, and set up reminder commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Habit names, schedules, completion history, and notes are stored in plaintext under ~/.config/habit-tracker.

Mitigation: Avoid recording sensitive medical or personal details in habit names or notes, and protect or review local files before sharing the machine or backups.

Risk: The delete command removes a habit and its associated log history.

Mitigation: Review the target habit carefully and back up ~/.config/habit-tracker before deleting records that may be needed later.

Risk: Optional cron-based reminder automation can run local commands on a schedule.

Mitigation: Review any cron entries before adding them and keep reminder commands scoped to the local habit-cli path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/habits-tracker)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes exact habit-cli commands, short explanations, habit-design suggestions, progress summaries, reminder setup guidance, and privacy notes when relevant.]

## Skill Version(s):

1.1.1 (source: server release evidence; artifact package.json and _meta.json report 1.1.0, SKILL.md frontmatter reports v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
