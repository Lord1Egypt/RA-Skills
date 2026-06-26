## Description: <br>
Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmundi3210](https://clawhub.ai/user/tmundi3210) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure and run gog commands for Google Workspace tasks such as Gmail search and send, Calendar event lookup, Drive search, Contacts listing, Sheets reads and updates, and Docs export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth authorization can grant access to Gmail, Calendar, Drive, Contacts, Sheets, and Docs data. <br>
Mitigation: Install only if the gog CLI is trusted and grant only the Google services needed for the intended workflow. <br>
Risk: Commands can send email, create events, or modify and clear Sheets, Drive, or Docs content. <br>
Mitigation: Review commands before execution, especially write or clear operations, and prefer non-interactive scripted use only after validating the command target and arguments. <br>


## Reference(s): <br>
- [gog CLI homepage](https://gogcli.sh) <br>
- [ClawHub skill page](https://clawhub.ai/tmundi3210/gog-disabled-20260401-113230) <br>
- [Publisher profile](https://clawhub.ai/user/tmundi3210) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and user-configured Google OAuth credentials; some commands can return JSON for scripting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
