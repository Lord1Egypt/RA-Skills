## Description: <br>
Interact with Google Workspace APIs (Gmail, Calendar, Drive, Sheets) using gsuite-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PabloAlaniz](https://clawhub.ai/user/PabloAlaniz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with Google Workspace and read or modify Gmail, Calendar, Drive, and Sheets resources through gsuite-sdk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and modify Google Workspace data after OAuth authorization. <br>
Mitigation: Use the narrowest OAuth scopes possible and confirm recipients, attendees, file IDs, spreadsheet ranges, uploads, and edits before write actions. <br>
Risk: OAuth tokens are stored locally after authentication. <br>
Mitigation: Protect or delete tokens.db when finished and revoke Google account access if the authorization is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PabloAlaniz/gsuite-sdk) <br>
- [Project homepage](https://github.com/PabloAlaniz/google-suite) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google OAuth credentials via GOOGLE_CREDENTIALS_FILE before use.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
