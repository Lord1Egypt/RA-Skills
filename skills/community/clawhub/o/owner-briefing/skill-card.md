## Description:

Generate and send a daily briefing to your owner covering today's meetings, urgent emails, open tasks, and anything that needs attention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or personal operations users use this skill to assemble and send a concise daily owner briefing from calendar events, unread email, and open task data. It can be run on request or scheduled for weekday delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The briefing may include sensitive calendar, email, and task content and send it through a configured messaging or email channel.

Mitigation: Confirm the Google, monday.com, and messaging or email accounts are approved, and verify the destination is private before enabling scheduled delivery.

Risk: The monday.com API token could expose task data if stored insecurely or granted broad access.

Mitigation: Store the token securely and use the least privilege access needed for the selected board.

Risk: Unreplaced owner, account, phone, email, or board placeholders could send incomplete or misdirected briefings.

Mitigation: Replace all placeholders and run a manual test before enabling the cron schedule.

## Reference(s):

- [Owner Briefing ClawHub listing](https://clawhub.ai/netanel-abergel/skills/owner-briefing)
- [monday.com API endpoint](https://api.monday.com/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing text with inline bash examples and JSON cron configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sections can be marked unavailable when calendar, email, or task data cannot be fetched.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
