## Description:

Manage Google Tasks from the command line - view, create, update, delete tasks and task lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bro3886](https://clawhub.ai/user/bro3886)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, developers, and agents use this skill to inspect, create, update, complete, delete, and export Google Tasks and task lists through the gtasks CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide commands that grant a third-party CLI access to Google Tasks data.

Mitigation: Install only when the gtasks CLI is trusted, authenticate with the minimum needed account, protect ~/.gtasks/token.json, and run gtasks logout when access is no longer needed.

Risk: Commands or examples may expose GTASKS_CLIENT_SECRET or OAuth token details if copied into logs, shell history, or shared output.

Mitigation: Avoid printing secrets, store credentials in a secrets manager or restricted private env file, and keep token and env files at restrictive permissions such as 0600.

Risk: Task-list and task delete or update commands can make destructive changes to Google Tasks data.

Mitigation: Review selected lists and task numbers immediately before destructive commands because task numbers are ephemeral and can change after list updates.

Risk: The advanced parallel-export shell example can run unintended shell commands when task-list names are interpolated into bash -c.

Mitigation: Do not copy the bash -c parallel-export example; use safer scripts that pass task-list names as data and quote all user-controlled values.

## Reference(s):

- [gtasks GitHub repository](https://github.com/BRO3886/gtasks)
- [gtasks releases](https://github.com/BRO3886/gtasks/releases)
- [dateparse examples](https://github.com/araddon/dateparse#extended-example)
- [Advanced Usage and Integration](references/ADVANCED.md)
- [Quick Reference Card](references/QUICK-REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and occasional JSON or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run gtasks CLI commands that access Google Tasks after local installation and OAuth authentication.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
