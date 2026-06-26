## Description: <br>
Google Sheets: Read and write spreadsheets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to inspect Google Sheets API resources and construct gws commands for reading, writing, creating, retrieving, and updating spreadsheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary flags default full-access nested review execution and staff moderation commands as suspicious capabilities in the broader skill set. <br>
Mitigation: Install only when those capabilities are expected, review the full skill set before use, and disable or constrain fallback reviewers when diffs may contain sensitive code or secrets. <br>
Risk: The skill invokes Google Workspace spreadsheet operations through the gws CLI, which can read or modify spreadsheet data when authenticated. <br>
Mitigation: Use least-privilege Google Workspace credentials, inspect commands with gws sheets --help and gws schema before execution, and confirm spreadsheet IDs and write parameters before running mutating methods. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/googleworkspace-bot/gws-sheets) <br>
- [Google Sheets API field masks guide](https://developers.google.com/workspace/sheets/api/guides/field-masks) <br>
- [Google Sheets API metadata guide](https://developers.google.com/workspace/sheets/api/guides/metadata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command-line tool and shared Google Workspace authentication setup.] <br>

## Skill Version(s): <br>
1.0.12 (source: server-resolved release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
