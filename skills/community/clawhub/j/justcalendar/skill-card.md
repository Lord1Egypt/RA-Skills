## Description:

Use this skill when a user needs to install, authenticate, or operate the Just Calendar CLI against https://justcalendar.ai, including generating an agent token in the web UI and performing calendar/day-data management from terminal commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andredalmeida](https://clawhub.ai/user/andredalmeida)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to install and authenticate the JustCalendar CLI, then manage calendars and day-level data backed by Google Drive from terminal commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the CLI from an untrusted source or with elevated privileges could expose the environment to unwanted code execution.

Mitigation: Install only from a trusted source and version, and avoid running npm commands with elevated privileges.

Risk: Agent tokens grant access to JustCalendar operations and should be treated as credentials.

Mitigation: Keep tokens secret, paste them only into the intended CLI login command, and rotate them by generating a new token when needed.

Risk: Bulk delete and calendar removal commands can change or remove Drive-backed calendar data.

Mitigation: Review destructive commands before execution and verify affected days or calendars after changes.

## Reference(s):

- [JustCalendar web app](https://justcalendar.ai)
- [ClawHub skill page](https://clawhub.ai/andredalmeida/skills/justcalendar)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides command patterns for CLI setup, authentication, calendar management, day-data operations, bulk operations, and troubleshooting.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
