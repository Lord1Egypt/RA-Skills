## Description: <br>
Google Workspace CLI for Gmail, Calendar, and Drive using official Google APIs for direct access without third-party proxies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JFab68](https://clawhub.ai/user/JFab68) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace users use this skill to configure and run a local CLI for Gmail search and label changes, email sending and drafts, Calendar event listing and creation, and Drive file lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI can access broad Google Workspace data and perform account-changing actions such as sending email, modifying Gmail labels, creating drafts, and creating calendar events. <br>
Mitigation: Use a Google Cloud project you control, review the OAuth scopes during consent, and require explicit confirmation before any action that sends email, changes labels, creates drafts, or creates calendar events. <br>
Risk: OAuth credentials and tokens are stored locally under ~/.config/praxis-gws/. <br>
Mitigation: Protect the local config directory, avoid shared or untrusted machines, and revoke or rotate Google OAuth credentials if the files are exposed. <br>
Risk: The skill depends on the local script and the googleapis package to interact directly with Google APIs. <br>
Mitigation: Install only when you trust the script and dependency source, and keep the runtime environment under user control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JFab68/praxis-gws) <br>
- [Google Cloud Console](https://console.cloud.google.com) <br>
- [Gmail modify OAuth scope](https://www.googleapis.com/auth/gmail.modify) <br>
- [Google Calendar OAuth scope](https://www.googleapis.com/auth/calendar) <br>
- [Google Drive readonly OAuth scope](https://www.googleapis.com/auth/drive.readonly) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Google OAuth credentials and tokens stored under ~/.config/praxis-gws/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
