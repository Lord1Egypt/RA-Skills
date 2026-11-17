## Description:

Track daily habits, streaks, and completions locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage a local habit tracker: add or archive habits, log completions, check streaks, and generate weekly reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and updates local habit files under the default habit data directory or a user-specified data directory.

Mitigation: Review HABIT_DATA_DIR and --data-dir before running commands, and point them only at directories intended for habit data.

Risk: Weekly review output can overwrite a file when --output targets an existing path.

Mitigation: Choose a dedicated report path or check whether the target file exists before saving a weekly review.

## Reference(s):

- [Habit Tracker Data Format](references/data-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Plain text, JSON, Markdown reports, and Python CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local JSON habit data; weekly reviews can be printed or written as Markdown files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
