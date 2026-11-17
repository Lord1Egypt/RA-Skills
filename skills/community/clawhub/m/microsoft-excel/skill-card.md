## Description:

Helps agents read and update Microsoft Excel workbooks, worksheets, ranges, tables, and charts through a connected Microsoft account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers use this skill to inspect and edit Excel data in their connected Microsoft account. With separate approval, they can also set up functions and scheduled or cross-app triggers that act on Excel data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the wrong Microsoft account or granting overly broad access could expose workbook data.

Mitigation: Confirm the account and requested scopes before authorizing the connection; use only the access the task needs.

Risk: Workbook writes could unintentionally alter or delete data.

Mitigation: Start with read-only operations and obtain explicit approval for each write.

Risk: Scheduled or cross-app automation could repeatedly act on data or use an unintended source or destination.

Mitigation: Approve each automation separately, name its source and destination, and keep trigger scope narrow.

Risk: Using a long-lived API key outside the CLI could leak credentials.

Mitigation: Prefer OAuth through the CLI; when a key is necessary, keep it out of logs, command lines, and persistent files.

## Reference(s):

- [ClawHub Microsoft Excel skill](https://clawhub.ai/byungkyu/skills/microsoft-excel)
- [Maton](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Microsoft Graph Excel API overview](https://learn.microsoft.com/en-us/graph/api/resources/excel)
- [Working with Excel in Microsoft Graph](https://learn.microsoft.com/en-us/graph/excel-concept-overview)
- [Scheduled trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize or modify data from authorized Excel workbooks; automation is optional and requires separate approval.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
