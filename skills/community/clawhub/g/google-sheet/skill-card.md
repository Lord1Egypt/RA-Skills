## Description: <br>
Read, write, append, and manage Google Sheets via the Google Sheets API using a Node.js CLI and a Google Cloud service account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longmaba](https://clawhub.ai/user/longmaba) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to read spreadsheet data, update cells, append rows, clear ranges, format sheets, and manage Google Sheets tabs through command-line operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete Google Sheets data when given write, clear, delete, merge, or formatting commands. <br>
Mitigation: Use a dedicated service account, share only the specific spreadsheets it should access, and review spreadsheet IDs, ranges, and sheet names before running modifying commands. <br>
Risk: Google service account JSON keys can expose spreadsheet access if stored in version control or shared folders. <br>
Mitigation: Keep credential files outside source control and shared folders, and provide them through a controlled environment variable or protected local configuration path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/longmaba/google-sheet) <br>
- [Google Sheets API authorization scope](https://www.googleapis.com/auth/spreadsheets) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Google service account key and spreadsheet sharing permissions before commands can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
