## Description:

Personal habit coach that tracks daily habits, streaks, and provides AI-powered coaching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinesh18s](https://clawhub.ai/user/dinesh18s)

### License/Terms of Use:


## Use Case:

External users use HabitChat to create daily habits, log completion or skips, inspect streaks and stats, and receive concise coaching based on their habit data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reminder feature can create executable shell scripts and cron lines from habit names.

Mitigation: Avoid enabling system reminders until shell-script generation is fixed, and do not add generated reminder scripts to cron when habit names contain shell metacharacters.

Risk: The skill stores personal routine data locally under ~/.habitchat.

Mitigation: Use it only where local JSON storage of habit and routine data is acceptable, and avoid entering sensitive details that should not remain on the device.

## Reference(s):

- [Habit Science Reference](references/habit_science.md)
- [HabitChat Skill Page](https://clawhub.ai/dinesh18s/skills/habitchat)
- [Project Homepage](https://github.com/Dinesh18S/dailyping)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON returned by local Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local JSON habit data under ~/.habitchat when helper scripts run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
