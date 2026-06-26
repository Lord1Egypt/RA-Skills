## Description: <br>
Microsoft Excel API integration with managed OAuth. Read and write Excel workbooks, worksheets, ranges, tables, and charts stored in OneDrive. Use this skill when users want to read or modify Excel spreadsheets, manage worksheet data, work with tables, or access cell values. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to connect a Microsoft account through ClawLink and work with Excel workbooks stored in OneDrive or SharePoint. It supports reading worksheets, ranges, tables, charts, and workbook metadata, and it can perform confirmed write actions such as updating ranges, creating worksheets, editing tables, and managing workbook permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses ClawLink OAuth to access Microsoft Excel, OneDrive, or SharePoint content from the connected Microsoft account. <br>
Mitigation: Install only if the user trusts ClawLink to manage Microsoft OAuth access, and connect only accounts whose workbooks are intended for OpenClaw access. <br>
Risk: Write, delete, sharing, upload, or permission-changing actions can modify workbook content or access settings. <br>
Mitigation: Review previews carefully and approve these actions only after the target resource and intended effect match the user's request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/microsoft-excel-spreadsheets) <br>
- [Microsoft Graph Excel API Overview](https://learn.microsoft.com/en-us/graph/api/resources/excel) <br>
- [Working with Excel in Microsoft Graph](https://learn.microsoft.com/en-us/graph/excel-concept-overview) <br>
- [Excel Workbook Resource](https://learn.microsoft.com/en-us/graph/api/resources/workbook) <br>
- [Excel Worksheet Resource](https://learn.microsoft.com/en-us/graph/api/resources/worksheet) <br>
- [Excel Range Resource](https://learn.microsoft.com/en-us/graph/api/resources/range) <br>
- [Excel Table Resource](https://learn.microsoft.com/en-us/graph/api/resources/table) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are agent-facing instructions for discovering Microsoft Excel tools, previewing write operations, and executing ClawLink tool calls after user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
