## Description:

Track leads locally, manage outreach campaigns, and export as CSV for download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3rdbrain](https://clawhub.ai/user/3rdbrain)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and outreach users use this skill to store leads locally, log interactions, generate outreach sequences, score prospects, and export lead data for CSV-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The clear command can permanently remove stored lead records without an explicit confirmation step.

Mitigation: Require confirmation, a force flag, or a backup/export workflow before clearing retained lead data.

Risk: CSV exports may contain untrusted lead fields that spreadsheet software can interpret as formulas.

Mitigation: Neutralize formula-prefixed values before opening or sharing exports, and treat generated CSV files as untrusted data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3rdbrain/skills/outreach-crm)
- [ClawHub publisher profile](https://clawhub.ai/user/3rdbrain)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Plain text command output with local JSON and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores retained lead records in the agent workspace and can export those records as CSV.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
