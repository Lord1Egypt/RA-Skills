## Description: <br>
OpenClaw skill that installs a Google Sheets CLI with setup steps and commands for read/write, batch, formatting, and sheet management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation teams use this skill to install and run a service-account Google Sheets CLI for repeatable spreadsheet reads, writes, batch updates, formatting, and sheet management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Google Sheets that are shared with its service account. <br>
Mitigation: Use a dedicated service account, share only the specific spreadsheets required, and prefer read-only scopes for read workflows. <br>
Risk: Commands such as clear, deleteSheet, write, batchWrite, and raw batch can make destructive or broad spreadsheet changes. <br>
Mitigation: Manually review those commands and payloads before execution, and test high-impact changes on copies or limited ranges first. <br>
Risk: Service-account keys provide access to shared spreadsheets if exposed. <br>
Mitigation: Keep keys private, avoid committing or logging credentials, and load credentials through controlled environment variables or secure files. <br>


## Reference(s): <br>
- [Google Sheets API Field Guide](artifact/assets/sheets-api-guide.md) <br>
- [Google Sheets API Usage Limits](https://developers.google.com/workspace/sheets/api/limits) <br>
- [spreadsheets.values.append Reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets.values/append) <br>
- [ValueInputOption Reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/ValueInputOption) <br>
- [spreadsheets.batchUpdate Reference](https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/batchUpdate) <br>
- [Google Sheets Batch Requests Guide](https://developers.google.com/workspace/sheets/api/guides/batch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed CLI emits JSON to stdout and returns non-zero exit codes on errors.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact package.json reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
