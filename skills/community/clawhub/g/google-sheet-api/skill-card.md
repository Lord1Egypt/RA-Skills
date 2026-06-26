## Description: <br>
OpenClaw skill that installs a Google Sheets CLI with setup steps and commands for read/write, batch, formatting, and sheet management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to configure and run a Google Sheets CLI for service-account based read, write, formatting, batch, and sheet-management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured service account can read and modify spreadsheets shared with it. <br>
Mitigation: Share only the specific spreadsheets needed for the workflow and prefer read-only scope when write access is not required. <br>
Risk: Write, clear, delete, batch, and formatting commands can make destructive spreadsheet changes. <br>
Mitigation: Test destructive commands on a copy or non-critical spreadsheet before using them on important data. <br>
Risk: Service account credentials may be exposed if key files or inline credential JSON are logged or committed. <br>
Mitigation: Keep credential files private, avoid logging credential values, and do not commit service account keys. <br>


## Reference(s): <br>
- [Google Sheet API ClawHub release](https://clawhub.ai/codedao12/google-sheet-api) <br>
- [Google Sheets API Field Guide](assets/sheets-api-guide.md) <br>
- [Google Sheets API usage limits](https://developers.google.com/workspace/sheets/api/limits) <br>
- [spreadsheets.values.append reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/append) <br>
- [ValueInputOption reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/ValueInputOption) <br>
- [spreadsheets.batchUpdate reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate) <br>
- [Google Sheets API batch requests guide](https://developers.google.com/workspace/sheets/api/guides/batch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands return JSON to stdout and use non-zero exit codes on errors.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
