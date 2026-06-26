## Description: <br>
Guides agents in helping users install and use gogcli to manage Google Workspace services including Gmail, Calendar, Drive, Sheets, Docs, Slides, Contacts, Tasks, People, Groups, and Keep. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luccast](https://clawhub.ai/user/luccast) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, administrators, and agents supporting Google Workspace users use this skill to install gogcli, configure OAuth credentials, and prepare commands for common Workspace tasks. It is intended for Gmail, Calendar, Drive, Sheets, Docs, Slides, Contacts, Tasks, People, Groups, and Keep workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install an external CLI and grant Google OAuth access. <br>
Mitigation: Verify the gogcli repository or Homebrew tap before installation, avoid sudo unless a global install is required, and enable only the Google APIs needed for the task. <br>
Risk: Generated commands may send email, upload files, create calendar events, or modify Google Workspace data. <br>
Mitigation: Confirm recipients, file paths, event details, target account, and intended service before running commands that create, send, upload, or modify data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require local OAuth credentials and access to selected Google Workspace APIs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
