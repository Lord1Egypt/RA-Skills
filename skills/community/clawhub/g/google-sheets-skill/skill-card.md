## Description: <br>
Google Sheets Secure Management. Use when the user wants to create, read, write, or append spreadsheet data; manage tabs (read/add/delete); copy spreadsheets; or manage sharing, permissions, renames, and deletes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porteden](https://clawhub.ai/user/porteden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Google Sheets through the PortEden CLI, including spreadsheet data operations, tab management, file copy/export, sharing, renaming, and trashing files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Google account, Sheets, and Drive data through PortEden credentials. <br>
Mitigation: Install only when that access is acceptable; review requested Google scopes and use a dedicated profile or token when possible. <br>
Risk: Share, delete, rename, and bulk write operations can expose, alter, or trash spreadsheet data. <br>
Mitigation: Confirm carefully before executing share, delete, rename, or bulk write commands, and prefer scoped credentials for the intended workspace. <br>
Risk: Read operations may return clipped tab data by default for larger sheets. <br>
Mitigation: Check for clipped responses and use the returned full range, explicit ranges, or a higher row cap when complete data is required. <br>


## Reference(s): <br>
- [PortEden homepage](https://porteden.com) <br>
- [ClawHub skill listing](https://clawhub.ai/porteden/google-sheets-skill) <br>
- [PortEden publisher profile](https://clawhub.ai/user/porteden) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly request compact JSON output with -jc; operations require PortEden authentication and Google Drive access where applicable.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
