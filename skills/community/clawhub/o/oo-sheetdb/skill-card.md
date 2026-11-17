## Description:

SheetDB (sheetdb.io). Use this skill for ANY SheetDB request — reading, creating, updating, and deleting data. Whenever a task involves SheetDB, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and spreadsheet users use the connected SheetDB account to inspect spreadsheet structure and rows, search and count data, and create, update, or delete rows through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute unverified remote code and make broader changes to other agent skills.

Mitigation: Review setup behavior before installing, install a verified CLI release, and decide whether to disable startup synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Create, update, and delete actions can change or remove spreadsheet data.

Mitigation: Inspect the live action schema and retain approval for the exact payload and effect before changing data; confirm the target before deleting rows.

## Reference(s):

- [SheetDB](https://sheetdb.io)
- [SheetDB API documentation](https://docs.sheetdb.io)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with oo CLI commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas and payloads vary by SheetDB operation.]

## Skill Version(s):

1.0.5 (source: release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
