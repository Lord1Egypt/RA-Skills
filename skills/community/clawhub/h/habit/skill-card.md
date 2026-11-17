## Description:

Build daily habits with streak tracking, reminders, and progress charts. Use when starting habits, maintaining streaks, or analyzing completion rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill as a command-line productivity and local logging assistant for habit-related entries, status checks, search, statistics, and exports. Review the local data behavior before entering sensitive personal information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary identifies the package as a habit tracker whose artifacts implement and document a generic local data-logging tool.

Mitigation: Review the stored files under ~/.local/share/habit before use and avoid entering sensitive health, routine, or personal information unless local search and export behavior is acceptable.

Risk: Entries may be searchable and exportable locally.

Mitigation: Limit inputs to low-sensitivity content and inspect generated JSON, CSV, or text exports before sharing or backing them up.

## Reference(s):

- [Habit skill page](https://clawhub.ai/ckchzh/skills/habit)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide use of a local command-line tool that stores, searches, and exports entries under ~/.local/share/habit.]

## Skill Version(s):

2.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
