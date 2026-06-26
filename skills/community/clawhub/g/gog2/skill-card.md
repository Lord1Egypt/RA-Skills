## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fionn1989](https://clawhub.ai/user/fionn1989) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up and run the gog CLI for Google Workspace tasks across Gmail, Calendar, Drive, Contacts, Sheets, and Docs. It provides command examples for OAuth setup, searches, sends, exports, sheet operations, and scripting with JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gog CLI requires Google Workspace OAuth access and may expose email, calendar, drive, contact, sheet, or document data to commands the user runs. <br>
Mitigation: Install only when the CLI is trusted, review the OAuth consent screen, and grant only the Google services needed for the task. <br>
Risk: Commands can send mail, create calendar events, modify or clear spreadsheets, copy documents, and run scripted no-input workflows. <br>
Mitigation: Require explicit confirmation before state-changing actions and review scripted commands before enabling no-input mode. <br>


## Reference(s): <br>
- [Gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/fionn1989/gog2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional JSON-output command patterns for scripting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
