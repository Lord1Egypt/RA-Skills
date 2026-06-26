## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ifocus1776](https://clawhub.ai/user/ifocus1776) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to work with Google Workspace through the gog CLI, including Gmail, Calendar, Drive, Contacts, Sheets, and Docs tasks after OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external gog CLI can read and modify Google account data after OAuth authorization. <br>
Mitigation: Install only if the gog CLI package is trusted and grant only the Google account access needed for the intended tasks. <br>
Risk: Commands can send mail, create events, change Drive content, update or clear Sheets ranges, and copy or export Docs. <br>
Mitigation: Require explicit user confirmation before running commands that send, create, update, clear, copy, export, or otherwise modify Google Workspace data. <br>


## Reference(s): <br>
- [GoG CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/ifocus1776/gogifocus) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external gog CLI and Google OAuth authorization.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
