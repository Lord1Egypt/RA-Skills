## Description:

OpenClaw Timebox helps users plan a full day into focused timeboxes, stay undisturbed during execution, collect quick check-ins after each block, review the day, and optionally sync calendars, logs, and TickTick or Dida365 tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinile](https://clawhub.ai/user/vinile)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn a day's tasks into timeboxed plans, preserve focus during execution, capture lightweight completion notes, and produce an end-of-day review. It can also create calendar placeholders, write local Markdown logs, and synchronize selected task or summary data with configured third-party services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write detailed local work logs and optionally send summaries or task details to calendar, task, and note services.

Mitigation: Enable only the integrations needed for your workflow, keep sensitive tasks out of synced summaries when appropriate, and confirm destination workspaces before use.

Risk: TickTick OAuth uses a persistent token file and a generated local helper script.

Mitigation: Protect the token file and helper script with local file permissions or move credentials to a secure credential store before enabling TickTick sync.

Risk: OpenClaw cron reminders are identified by the security evidence as having unsafe persistence and shell-injection risk.

Mitigation: Avoid OpenClaw cron reminders until the scheduler command is one-shot and safely escaped; use manual return-to-check or a trusted external timer instead.

## Reference(s):

- [OpenClaw Timebox Skill Page](https://clawhub.ai/vinile/skills/openclaw-timebox)
- [Publisher Profile](https://clawhub.ai/user/vinile)
- [dida-cli](https://clawhub.ai/ilooch/dida-cli)
- [TickTick Developer Portal](https://developer.ticktick.com/)
- [TickTick Open API](https://api.ticktick.com/open/v1)
- [Feishu Calendar API](https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events)
- [Google Calendar API](https://www.googleapis.com/calendar/v3/calendars/{calendarId}/events)
- [Notion Pages API](https://api.notion.com/v1/pages)
- [Google Docs API](https://docs.googleapis.com/v1/documents/{documentId}:batchUpdate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational text and Markdown with inline shell commands, configuration snippets, task plans, logs, and review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown logs, create calendar or task entries, and call configured third-party services when the user enables those integrations.]

## Skill Version(s):

2.7.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
