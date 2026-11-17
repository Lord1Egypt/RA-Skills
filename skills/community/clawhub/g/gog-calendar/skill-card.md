## Description:

Google Calendar via gogcli: reliable cross-calendar agenda (today/week/range) and best-effort keyword search across calendars (iterate + aggregate). Token-efficient output (`--plain` default, `--json` only when needed). Post-filters unwanted calendars (e.g., holidays) and confirms before writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lstpsche](https://clawhub.ai/user/lstpsche)

### License/Terms of Use:


## Use Case:

Agents use this skill to answer user questions about Google Calendar availability, agendas, and event search across calendars through gogcli. It also guides write workflows by requiring an explicit user confirmation before creating, updating, deleting, or responding to events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on gogcli access to Google Calendar data.

Mitigation: Install only if that data access is acceptable, and review the Google authorization scope before use.

Risk: The skill relies on a third-party Homebrew formula for gogcli installation.

Mitigation: Review the Homebrew formula and gogcli project before installing in a managed environment.

Risk: Calendar write actions can create, update, delete, or respond to events.

Mitigation: Require the skill's explicit user-confirmation step before any calendar write or RSVP command is run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lstpsche/skills/gog-calendar)
- [gogcli AGENTS.md](https://github.com/steipete/gogcli/blob/main/AGENTS.md?utm_source=chatgpt.com)
- [gogcli README](https://github.com/steipete/gogcli/blob/main/README.md?utm_source=chatgpt.com)
- [Google Calendar API events.list](https://developers.google.com/workspace/calendar/api/v3/reference/events/list?utm_source=chatgpt.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text or JSON command-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to token-efficient plain output for summaries, uses JSON when structure is needed, filters excluded calendars after broad queries, and requires explicit confirmation before calendar writes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
