## Description: <br>
Read, write, and append to Google Sheets via service account authentication with a zero-dependency Node.js script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheAgentWire](https://clawhub.ai/user/TheAgentWire) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to list, read, append to, and overwrite Google Sheets data through a service account in headless workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses service-account access to Google Sheets, and append/write commands can make live spreadsheet edits. <br>
Mitigation: Use a dedicated service account, share only the sheets required for the task, grant Viewer access for read-only workflows, and review append/write commands before execution. <br>
Risk: Server security evidence says the skill requests broader write-capable Sheets access for read operations than the documentation claims. <br>
Mitigation: Treat installation as granting write-capable Sheets access unless scopes are verified in code, and restrict spreadsheet sharing permissions accordingly. <br>
Risk: The skill loads service-account key material from environment variables, a local file, or 1Password. <br>
Mitigation: Store keys in a managed secret store where possible, avoid exposing key JSON in logs or shell history, and rotate the key if it may have been disclosed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheAgentWire/google-sheets-agent) <br>
- [Publisher profile](https://clawhub.ai/user/TheAgentWire) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command logs go to stderr; spreadsheet command results are emitted as JSON to stdout.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
