## Description: <br>
Microsoft Excel API integration with managed OAuth for reading and writing Excel workbooks, worksheets, ranges, tables, and charts stored in OneDrive or SharePoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to Microsoft Excel through Maton-managed OAuth, inspect workbooks in OneDrive or SharePoint, and perform approved edits to worksheets, ranges, tables, and charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or modify Excel files in the connected Microsoft account. <br>
Mitigation: Install only if you trust Maton and approve writes after checking the exact workbook, worksheet, range, table, chart, or upload target. <br>
Risk: MATON_API_KEY grants access to the Maton API and connected Excel resources. <br>
Mitigation: Store it as a secret, avoid logging it, and rotate or revoke it if exposed. <br>
Risk: Multiple Microsoft Excel connections can send requests to the wrong account if a connection is not selected. <br>
Mitigation: Use the Maton-Connection header when more than one Microsoft Excel connection exists. <br>


## Reference(s): <br>
- [ClawHub Microsoft Excel Skill](https://clawhub.ai/byungkyu/microsoft-excel) <br>
- [Microsoft Graph Excel API Overview](https://learn.microsoft.com/en-us/graph/api/resources/excel) <br>
- [Working with Excel in Microsoft Graph](https://learn.microsoft.com/en-us/graph/excel-concept-overview) <br>
- [Microsoft Graph Workbook Resource](https://learn.microsoft.com/en-us/graph/api/resources/workbook) <br>
- [Microsoft Graph Worksheet Resource](https://learn.microsoft.com/en-us/graph/api/resources/worksheet) <br>
- [Microsoft Graph Range Resource](https://learn.microsoft.com/en-us/graph/api/resources/range) <br>
- [Microsoft Graph Table Resource](https://learn.microsoft.com/en-us/graph/api/resources/table) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and may require the Maton-Connection header when multiple Microsoft Excel connections are available.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
