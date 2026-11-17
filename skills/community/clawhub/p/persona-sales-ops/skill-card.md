## Description:

Manage sales workflows - track deals, schedule calls, and client communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and revenue teams use this persona to prepare client calls, triage follow-up email, update deal-tracking spreadsheets, share proposals, and summarize pipeline activity through Google Workspace workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persona can guide Gmail, Calendar, Sheets, and Drive actions involving client and deal data.

Mitigation: Use accounts, folders, and shared drives appropriate for sales data, and review generated emails, calendar actions, spreadsheet updates, and uploaded files before committing changes.

Risk: Pipeline summaries, deal updates, and follow-up tasks may be wrong if the underlying workspace data is incomplete or stale.

Mitigation: Check proposed summaries and updates against source emails, calendar events, sheets, and documents before relying on them for customer-facing or revenue decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/persona-sales-ops)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Google Workspace actions for Gmail, Calendar, Sheets, and Drive that should be reviewed before execution.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
