## Description:

Personal scheduler for creating, updating, deleting, viewing, importing, and exporting calendar events with natural-language input, reminders, and a local web interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tech-fcc-sys](https://clawhub.ai/user/tech-fcc-sys)

### License/Terms of Use:

MIT

## Use Case:

Individual users use this skill to manage personal calendar events locally through natural-language commands, CLI commands, and a browser UI. It supports reminders, recurring events, SQLite-backed storage, backups, and .ics import/export for calendar interoperability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The web server can expose private calendar data and event creation without authentication.

Mitigation: Bind the web server to 127.0.0.1 and add authentication before storing real calendar details.

Risk: The Flask web server is configured for debug mode.

Mitigation: Disable debug mode before any non-local or shared deployment.

Risk: Reminder delivery may use a configured Feishu user identifier.

Mitigation: Remove any hard-coded Feishu ID and require user-specific configuration.

Risk: Delete or update actions can modify calendar records from natural-language input.

Mitigation: Add explicit confirmation before destructive or modifying actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tech-fcc-sys/skills/personal-scheduler)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Console text, JSON-like status data, local SQLite/JSON/ICS files, and web UI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores schedule data locally and can emit reminder messages for external delivery channels.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
