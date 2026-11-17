## Description:

Habit tracker with streak counting and visual calendars. Use when you need habithero.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to manage personal habits, mark daily completions, inspect streaks, and export local habit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal habit entries and history in local files.

Mitigation: Avoid entering sensitive health, schedule, or private notes, and review file permissions for ~/.local/share/habithero before regular use.

Risk: The skill can export habit data into portable JSON, CSV, or text files.

Mitigation: Inspect exported files before sharing or syncing them, and delete exports that are no longer needed.

Risk: The implemented command set is broader than the listing advertises.

Mitigation: Review the help output and script behavior before relying on commands in regular workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/habithero)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files, Configuration]

**Output Format:** [Command-line text output and local JSON, CSV, or text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local habit data under ~/.local/share/habithero]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
