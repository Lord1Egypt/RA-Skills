## Description:

Manage macOS Calendar with OpenClaw in IM-first workflows (Telegram/Discord/Feishu/iMessage/Slack), including screenshot-to-schedule extraction, idempotent create/update, move/extend/reschedule, reminders, conflict checks, daily review sync, and duplicate cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryant24hao](https://clawhub.ai/user/bryant24hao)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn chat messages, screenshots, and planning notes into macOS Calendar events, reminders, conflict checks, and cleanup actions. It supports IM-first schedule maintenance and plan-execute-summarize-adjust workflows through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests real macOS Calendar access and can create, update, move, or delete calendar events.

Mitigation: Grant Calendar access only on a Mac account where those changes are acceptable, review proposed writes and cleanup plans first, and use dry-run flows before applying changes.

Risk: The security evidence flags unsafe scripting patterns around cron installation and configuration values that could cause unintended calendar changes or user-level command execution from crafted configuration.

Mitigation: Inspect config.json yourself, use only trusted configuration files, and avoid running the cron installer until cron validation and AppleScript escaping issues are fixed.

Risk: Regression tests and duplicate cleanup can affect live calendar data if run against a personal calendar.

Mitigation: Run tests only against isolated test calendars or accounts, and require snapshot review plus explicit confirmation before using cleanup with --apply.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bryant24hao/skills/macos-calendar-assistant)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or status outputs from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar operations require macOS, Swift command line tools, Python 3.9+, and Calendar permission for the terminal or host process.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
