## Description: <br>
Google Sheets API integration with managed OAuth. Create spreadsheets, read and write cell values, manage sheets, append rows, create charts, and automate data operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect a Google account through ClawLink, inspect spreadsheets, and perform confirmed Google Sheets read and write operations from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires trusting ClawLink to broker and store the user's Google Sheets OAuth connection. <br>
Mitigation: Install only when ClawLink is trusted for the account, review requested Google permissions during connection, and use the connected account's normal access controls. <br>
Risk: Spreadsheet write, clear, delete, and batch operations can modify or remove user data. <br>
Mitigation: Require a clear preview and explicit user confirmation before executing any high-impact Google Sheets operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/google-sheets-spreadsheets) <br>
- [Google Sheets API overview](https://developers.google.com/sheets/api) <br>
- [Google Sheets Values resource](https://developers.google.com/sheets/api/reference/spreadsheets.values) <br>
- [Google Sheets Spreadsheets resource](https://developers.google.com/sheets/api/reference/spreadsheets) <br>
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink dashboard for Google Sheets](https://claw-link.dev/dashboard?add=google-sheets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes connection checks, previews, and user confirmation before spreadsheet write, clear, delete, or batch operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
