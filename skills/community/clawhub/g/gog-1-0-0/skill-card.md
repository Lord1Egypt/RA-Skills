## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical users use this skill to prepare and run gog CLI commands for Google Workspace tasks such as email search and sending, calendar event lookup, Drive search, contact listing, Sheets updates, and Docs export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gog CLI can access or modify Google account data after OAuth access is granted. <br>
Mitigation: Review requested OAuth scopes and connect only the accounts and services needed for the task. <br>
Risk: Commands can send email, create calendar events, modify Drive or Docs content, or update, append, and clear Sheets data. <br>
Mitigation: Require explicit user approval before running commands that create, send, update, append, clear, or otherwise modify Google Workspace data. <br>
Risk: The skill depends on an external gog binary and Homebrew tap. <br>
Mitigation: Install only when the user trusts the gog CLI and the Homebrew tap steipete/tap/gogcli. <br>


## Reference(s): <br>
- [Gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub release page](https://clawhub.ai/Sieyer/gog-1-0-0) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Sieyer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command options such as --json and --no-input for scripting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
