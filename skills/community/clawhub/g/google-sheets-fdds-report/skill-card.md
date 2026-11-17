## Description:

Reads FDDS metrics from a specified Google Sheets document and generates or updates a report comparing the latest available day with the same day from the previous week.

This skill is ready for commercial/non-commercial use.

## Publisher:

[craken-ia86](https://clawhub.ai/user/craken-ia86)

### License/Terms of Use:

MIT-0

## Use Case:

Operations analysts and logistics teams use this skill to read FDDS performance data from Google Sheets, compare D-1 against W-1, and produce a concise delivery performance report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read business or logistics data from a Google Sheet.

Mitigation: Use least-privilege Google access and share only the spreadsheet, tabs, and ranges needed for the report.

Risk: If asked to write results back, the skill may update the report template in the spreadsheet.

Mitigation: Confirm the destination tab and range before writing and review generated report values before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/craken-ia86/skills/google-sheets-fdds-report)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read specified spreadsheet tabs and optionally write the generated report back when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
