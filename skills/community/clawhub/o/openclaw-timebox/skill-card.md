## Description: <br>
OpenClaw Timebox helps OpenClaw users plan a day into timeboxes, run focused work sessions without agent interruptions, collect quick check-ins, and produce an end-of-day review with optional calendar, task, and note synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinile](https://clawhub.ai/user/vinile) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and productivity-focused OpenClaw users use this skill to structure daily work into planned timeboxes, preserve local work logs, and optionally sync summaries or tasks to their chosen calendar, task, and note services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store detailed daily work records locally and optionally send summaries, tasks, or calendar entries to third-party services. <br>
Mitigation: Keep local logging and task_sync set to none unless integrations are needed, and avoid entering confidential client or business details into synced notes or tasks. <br>
Risk: TickTick, Dida, calendar, note, and document integrations can require OAuth tokens, API tokens, or locally stored token files. <br>
Mitigation: Protect token files and API tokens, use only the integrations required for the workflow, and rotate credentials if a local device or workspace is shared. <br>
Risk: Automatic calendar and task updates can create or modify user-facing work records. <br>
Mitigation: Review the planned timeboxes and selected target calendar, project, or workspace before enabling synchronization. <br>


## Reference(s): <br>
- [OpenClaw Timebox on ClawHub](https://clawhub.ai/vinile/openclaw-timebox) <br>
- [dida-cli on ClawHub](https://clawhub.ai/ilooch/dida-cli) <br>
- [TickTick Developer Portal](https://developer.ticktick.com/) <br>
- [TickTick Open API](https://api.ticktick.com/open/v1) <br>
- [Feishu Calendar API endpoint](https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events) <br>
- [Google Calendar API endpoint](https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events) <br>
- [Notion Pages API endpoint](https://api.notion.com/v1/pages) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, YAML configuration, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown logs and optional task, calendar, or note updates when the user configures integrations.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
