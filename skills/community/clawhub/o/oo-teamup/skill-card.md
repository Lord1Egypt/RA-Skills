## Description:

Teamup Calendar (teamup.com). Use this skill for ANY Teamup Calendar request — reading, creating, updating, and deleting data. Whenever a task involves Teamup Calendar, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read and manage Teamup Calendar events and subcalendars through their OOMOL-connected account. It provides agent guidance for listing, retrieving, creating, updating, and deleting calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI may execute changing remote software and may automatically install or synchronize agent skills, affecting the broader agent environment.

Mitigation: Review and install the CLI separately before using the skill, including its installation and synchronization behavior.

Risk: Creating, updating, or deleting calendar events changes calendar data.

Mitigation: Retain user confirmation for changes and deletions, and check the live action schema and intended payload before running a command.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Teamup Calendar](https://www.teamup.com/)
- [Teamup API documentation](https://calendar.teamup.com/kb/api-teamup-calendar/)

## Skill Output:

**Output Type(s):** [JSON data, Shell commands, Guidance]

**Output Format:** [JSON payloads and oo CLI commands with JSON responses, plus Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar write and delete actions require confirmation; commands use the live connector schema.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
