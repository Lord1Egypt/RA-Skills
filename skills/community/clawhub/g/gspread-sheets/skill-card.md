## Description: <br>
Batch read/write Google Sheets using the gspread Python library with service account authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nuokunkeji](https://clawhub.ai/user/nuokunkeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to read, write, update, clear, append, and manage Google Sheets data through the gspread Python library instead of browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Service-account credentials can access spreadsheets shared with that account and may expose or modify sensitive sheet data if mishandled. <br>
Mitigation: Use a dedicated service account, keep the JSON key secret and out of source control, share only intended spreadsheets with the account, and use the narrowest Google scopes that support the workflow. <br>
Risk: Bulk update, clear, replace, worksheet delete, and sync patterns can make large spreadsheet changes quickly. <br>
Mitigation: Require exact spreadsheet IDs, worksheet names, ranges, and confirmation before destructive or high-volume write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nuokunkeji/gspread-sheets) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples require gspread, google-auth, and a Google service account shared with the target spreadsheet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
