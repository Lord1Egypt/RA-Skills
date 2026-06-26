## Description: <br>
Google Sheets skill for reading, creating, updating, and deleting spreadsheet data through the OOMOL oo CLI connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Google Sheets through an OOMOL-connected account, including reading ranges, creating spreadsheets, updating values, and managing sheet structure. It is suited for agent workflows that need Google Sheets actions through the oo CLI connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change spreadsheet state through write actions. <br>
Mitigation: Confirm the exact spreadsheet target, action, and payload with the user before running any action tagged [write]. <br>
Risk: The skill can remove or overwrite spreadsheet data through destructive actions. <br>
Mitigation: Get explicit user approval for the target and effect before running any action tagged [destructive], especially clear, delete row or column, and delete sheet operations. <br>
Risk: The skill depends on an OOMOL-connected Google Sheets account. <br>
Mitigation: Install only when the operator is comfortable granting OOMOL access to Google Sheets and use the first-time setup flow only after an auth or connection error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-googlesheets) <br>
- [Google Sheets homepage](https://workspace.google.com/products/sheets/) <br>
- [oo CLI repository](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [OOMOL Google Sheets connection page](https://console.oomol.com/app-connections?provider=googlesheets) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects with data and meta.executionId fields when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
