## Description:

Reliable macOS AppleScript fallback for creating Apple Reminders, Apple Notes, Apple Calendar events, and sending iMessage when direct tool or plugin routes are unavailable or unreliable, especially on older macOS versions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qy-zhang](https://clawhub.ai/user/qy-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create reminders, notes, calendar events, and iMessages on macOS through bundled shell scripts when direct app integrations are unavailable or unreliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send iMessages and create or modify personal Reminders, Notes, and Calendar content on the user's Mac.

Mitigation: Require explicit user confirmation of the recipient, message text, calendar, account, note content, reminder title, and event times before running scripts.

Risk: Broad macOS permissions can expose personal app data if granted unnecessarily.

Mitigation: Grant Automation permissions only to the specific host app and target apps needed; avoid Full Disk Access unless independently required.

Risk: Locale-dependent date parsing can fail or produce incorrect reminder and calendar times.

Mitigation: Use YYYY-MM-DD HH:MM:SS inputs and verify the resulting time in the target app when date parsing is involved.

## Reference(s):

- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/qy-zhang/skills/macos-applescript-fallback)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return created object IDs or a sent status from the target macOS app.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
