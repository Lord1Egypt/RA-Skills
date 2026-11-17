## Description:

Schedule Manager helps macOS agents manage Apple Calendar events and Apple Reminders tasks with osascript and reminders-cli using GTD-style workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niracler](https://clawhub.ai/user/niracler)

### License/Terms of Use:


## Use Case:

External users and productivity-focused agent operators use this skill to inspect schedules, create calendar events, manage reminders, and perform daily or weekly GTD planning on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, modify, complete, or delete Calendar and Reminders data.

Mitigation: Preview the exact matched items and require explicit user confirmation before destructive or bulk actions.

Risk: The skill requires Calendar and Reminders permissions for the invoking terminal.

Mitigation: Grant permissions only in trusted environments and review requested actions before execution.

Risk: The Reminders workflow depends on the third-party reminders-cli tool.

Mitigation: Install reminders-cli only from a trusted source and inspect Homebrew installer commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/niracler/skills/nini-schedule-manager)
- [GTD methodology guide](references/gtd-methodology.md)
- [Apple Calendar osascript reference](references/osascript-calendar.md)
- [Apple Reminders osascript reference](references/osascript-reminders.md)
- [reminders-cli command reference](references/reminders-cli-guide.md)
- [reminders-cli project](https://github.com/keith/reminders-cli)
- [GTD official forum](https://forum.gettingthingsdone.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and AppleScript command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS-only; requires osascript and reminders-cli for full Reminders functionality.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
