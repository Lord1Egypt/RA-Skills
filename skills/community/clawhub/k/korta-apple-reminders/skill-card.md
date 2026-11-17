## Description:

Manage Apple Reminders via the `remindctl` CLI on macOS, including listing, adding, editing, completing, and deleting reminders with list filters, date filters, and JSON or plain-text output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landercortazarromero](https://clawhub.ai/user/landercortazarromero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to have an agent propose `remindctl` commands for viewing and managing Apple Reminders from the terminal. It is useful for reminder workflows that need list filtering, date-based views, scripting output, or batch completion and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide users to grant remindctl access to Apple Reminders.

Mitigation: Install and authorize remindctl only on Macs where the user is comfortable allowing terminal-based access to reminder data.

Risk: Delete commands, especially commands using --delete or --force, may remove reminder data.

Mitigation: Check list names and reminder IDs before running destructive commands, and prefer viewing the target reminders first.

## Reference(s):

- [Korta Apple Reminders on ClawHub](https://clawhub.ai/landercortazarromero/skills/korta-apple-reminders)
- [remindctl project homepage](https://github.com/steipete/remindctl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; referenced command output may be JSON, plain text, TSV, or counts-only.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; requires the remindctl binary and Apple Reminders permission on the Mac where commands run.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
