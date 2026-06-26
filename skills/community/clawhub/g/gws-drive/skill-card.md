## Description: <br>
Google Drive: Manage files, folders, and shared drives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Google Drive v3 resources and compose `gws drive` commands for files, folders, permissions, shared drives, comments, revisions, and change notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents powerful Google Drive actions, including create, update, delete, sharing, and watch operations. <br>
Mitigation: Confirm the active Google account and scopes, inspect method requirements with `gws schema`, and review any command that changes Drive data, sharing, or watch channels before execution. <br>
Risk: The skill depends on the local `gws` CLI and companion authentication guidance. <br>
Mitigation: Install and use it only in environments where the `gws` CLI and `gws-shared` authentication setup are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-drive) <br>
- [Google Drive API: Return user info](https://developers.google.com/workspace/drive/api/guides/user-info) <br>
- [Google Drive API: Return specific fields](https://developers.google.com/workspace/drive/api/guides/fields-parameter) <br>
- [Google Drive API: Manage pending access proposals](https://developers.google.com/workspace/drive/api/guides/pending-access) <br>
- [Google Drive API: Retrieve changes](https://developers.google.com/workspace/drive/api/guides/manage-changes) <br>
- [Google Drive API: Push notifications](https://developers.google.com/workspace/drive/api/guides/push) <br>
- [Google Drive API: Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments) <br>
- [Google Drive API: Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives) <br>
- [Google Drive API: Create and manage files](https://developers.google.com/workspace/drive/api/guides/create-file) <br>
- [Google Drive API: Download and export files](https://developers.google.com/workspace/drive/api/guides/manage-downloads) <br>
- [Google Drive API: Search for files and folders](https://developers.google.com/workspace/drive/api/guides/search-files) <br>
- [Google Drive API: Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing) <br>
- [Google Drive API: Manage file revisions](https://developers.google.com/workspace/drive/api/guides/manage-revisions) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and command-reference text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the `gws` CLI and companion `gws-shared` authentication guidance.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
