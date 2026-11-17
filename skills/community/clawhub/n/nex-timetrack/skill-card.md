## Description:

Billable time logger for freelancers and agencies. Start/stop timers or log manually. Client and project management, rate cascading, 15-minute rounding, billing summaries, full-text search, CSV/JSON export. Python stdlib only, SQLite storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexaiguy](https://clawhub.ai/user/nexaiguy)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, agencies, and the agents assisting them use this skill to record billable time, manage clients and projects, calculate billing summaries, and export timesheet data for invoicing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and export behavior can affect files outside the skill's expected data area.

Mitigation: Review setup before running, avoid elevated privileges, and keep export paths to simple filenames or trusted directories.

Risk: Time entries, client contacts, rates, and CSV/JSON exports may contain sensitive business data.

Mitigation: Store the local data directory securely, limit access to exports, and review files before sharing or opening them in spreadsheet software.

## Reference(s):

- [Nex Timetrack on ClawHub](https://clawhub.ai/nexaiguy/skills/nex-timetrack)
- [Nex AI](https://nex-ai.be)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline shell commands and file paths; CSV or JSON files when exports are requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local SQLite storage under ~/.nex-timetrack by default; exports may contain client, rate, and billing data.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
