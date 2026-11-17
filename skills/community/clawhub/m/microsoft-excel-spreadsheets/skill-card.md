## Description:

Microsoft Excel API integration with managed OAuth. Read and write Excel workbooks, worksheets, ranges, tables, and charts stored in OneDrive. Use this skill when users want to read or modify Excel spreadsheets, manage worksheet data, work with tables, or access cell values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to let an agent read, search, create, and modify Microsoft Excel workbooks stored in OneDrive or SharePoint through managed Microsoft OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and globally enables an unpinned third-party ClawLink plugin that can access and modify Microsoft 365 spreadsheet data.

Mitigation: Review the ClawLink plugin and requested Microsoft OAuth scopes before installing, prefer a pinned or verified plugin version, and keep a clear removal path.

Risk: Workbook write, share, and delete operations can alter or expose OneDrive or SharePoint files.

Mitigation: Require explicit user confirmation and preview for every write, share, or delete action, and verify the target workbook, worksheet, range, table, or chart before execution.

Risk: The OAuth connection may expose workbook content from the connected Microsoft 365 account to the integration.

Mitigation: Use only Microsoft 365 accounts and workbooks the user is comfortable connecting, and inspect workbook permissions before granting or changing access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/microsoft-excel-spreadsheets)
- [Microsoft Graph Excel API Overview](https://learn.microsoft.com/en-us/graph/api/resources/excel)
- [Working with Excel in Microsoft Graph](https://learn.microsoft.com/en-us/graph/excel-concept-overview)
- [Excel Workbook Resource](https://learn.microsoft.com/en-us/graph/api/resources/workbook)
- [Excel Worksheet Resource](https://learn.microsoft.com/en-us/graph/api/resources/worksheet)
- [Excel Range Resource](https://learn.microsoft.com/en-us/graph/api/resources/range)
- [Excel Table Resource](https://learn.microsoft.com/en-us/graph/api/resources/table)
- [ClawLink Documentation](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions for connecting to ClawLink and using Microsoft Excel tools; write, share, and delete operations require explicit user confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
