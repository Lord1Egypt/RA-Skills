## Description: <br>
Google Calendar via gogcli: reliable cross-calendar agenda (today/week/range) and best-effort keyword search across calendars (iterate + aggregate). Token-efficient output (`--plain` default, `--json` only when needed). Post-filters unwanted calendars (e.g., holidays) and confirms before writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lstpsche](https://clawhub.ai/user/lstpsche) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve Google Calendar agendas across all calendars, search events by keyword, filter unwanted calendars such as holidays, and prepare calendar write actions only after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on gogcli access to the user's Google Calendar account. <br>
Mitigation: Install only after reviewing the gogcli Homebrew package source and confirming it is authenticated to the intended Google Calendar account. <br>
Risk: Calendar create, update, delete, or RSVP actions can modify user data. <br>
Mitigation: Require an explicit yes after summarizing the calendar, title, time, timezone, attendees, and location before any write command is run. <br>


## Reference(s): <br>
- [gogcli Agent Guidance](https://github.com/steipete/gogcli/blob/main/AGENTS.md?utm_source=chatgpt.com) <br>
- [gogcli README](https://github.com/steipete/gogcli/blob/main/README.md?utm_source=chatgpt.com) <br>
- [Google Calendar API Events: list](https://developers.google.com/workspace/calendar/api/v3/reference/events/list?utm_source=chatgpt.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON] <br>
**Output Format:** [Plain text or Markdown summaries with inline shell commands; JSON when structured calendar data is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to token-efficient --plain output for listings and uses --json for aggregation, deduplication, exact field extraction, and write workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
