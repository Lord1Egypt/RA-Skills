## Description:

Inspect SQLite schemas, run bounded read-only queries, export CSV/JSON and import CSV into a fresh database. Use for SQLite Query and Export Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts can use this skill to inspect SQLite structure, run bounded read-only queries, export results, check database integrity, and import CSV data into a fresh database while preserving the source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exported reports can contain sensitive database records and remain on disk.

Mitigation: Use a separate workspace containing only the files to process, and remove exported reports when they are no longer needed.

## Reference(s):

- [Action contract](references/input.md)
- [ClawHub skill release](https://clawhub.ai/hznetnewpower/skills/mochi-sqlite-desk)
- [MochiLab](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [Analysis, CSV files, JSON files, HTML reports, SQLite database files]

**Output Format:** [Text summaries and CSV, JSON, HTML, or SQLite files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query reports are bounded and indicate when returned rows are truncated. CSV imports create a fresh database with text columns.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
