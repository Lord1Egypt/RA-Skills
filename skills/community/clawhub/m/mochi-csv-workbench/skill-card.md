## Description:

Clean and analyze local UTF-8 CSV or TSV files with quoted fields, exact decimal statistics, explicitly grouped amounts, duplicate and empty counts, and formula-safe CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to clean local UTF-8 CSV or TSV files, review missing and duplicate rows, and calculate exact decimal statistics or totals grouped by explicitly selected columns. It works with delimited text files and does not read or create XLSX workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default duplicate removal can remove legitimate repeated transactions.

Mitigation: Use --keep-duplicates for transaction data unless the user explicitly requests duplicate removal, and report any rows removed.

Risk: Sensitive records passed to a cloud-backed model may leave the local host.

Mitigation: Share only necessary aggregate statistics and use an approved or local model for sensitive data.

Risk: Formula protection can cause exported values to display as text in spreadsheet software.

Mitigation: Explain the protection and retain it; use a text-import workflow when lossless literal display is needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/hznetnewpower/skills/mochi-csv-workbench)
- [MochiLab homepage](https://mochilab.bz)

## Skill Output:

**Output Type(s):** [CSV files, JSON, Markdown, Analysis]

**Output Format:** [Creates cleaned.csv, report.json, and report.md, with concise analysis text for the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grouped totals use exact decimal arithmetic and require explicit group and amount columns. Formula-shaped values in CSV exports are prefixed with an apostrophe, which can make them display as text in spreadsheet software.]

## Skill Version(s):

1.0.1 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
