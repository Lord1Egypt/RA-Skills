## Description:

Google Drive: Manage files, folders, and shared drives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent inspect Google Drive resources and compose gws CLI commands for managing files, folders, comments, revisions, permissions, and shared drives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward mutating Google Drive operations, including file changes, permission changes, deletions, and shared drive updates.

Mitigation: Before execution, review the target file or shared drive, requested permission changes, deletion operations, and active Google auth scopes.

Risk: Incorrect Drive resource IDs, query filters, or request parameters can affect the wrong files, folders, comments, revisions, permissions, or shared drives.

Mitigation: Inspect each method with gws schema, verify IDs and query parameters, and prefer read-only get or list commands before running create, update, delete, resolve, watch, or stop operations.

## Reference(s):

- [Gws Drive on ClawHub](https://clawhub.ai/googleworkspace-bot/skills/gws-drive)
- [Google Drive API: Return user info](https://developers.google.com/workspace/drive/api/guides/user-info)
- [Google Drive API: Return specific fields](https://developers.google.com/workspace/drive/api/guides/fields-parameter)
- [Google Drive API: Manage pending access proposals](https://developers.google.com/workspace/drive/api/guides/pending-access)
- [Google Drive API: Retrieve changes](https://developers.google.com/workspace/drive/api/guides/manage-changes)
- [Google Drive API: Push notifications](https://developers.google.com/workspace/drive/api/guides/push)
- [Google Drive API: Manage comments and replies](https://developers.google.com/workspace/drive/api/guides/manage-comments)
- [Google Drive API: Manage shared drives](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives)
- [Google Drive API: Search for shared drives](https://developers.google.com/workspace/drive/api/guides/search-shareddrives)
- [Google Drive API: Create and manage files](https://developers.google.com/workspace/drive/api/guides/create-file)
- [Google Drive API: Download and export files](https://developers.google.com/workspace/drive/api/guides/manage-downloads)
- [Google Drive API: Search for files and folders](https://developers.google.com/workspace/drive/api/guides/search-files)
- [Google Drive API: List labels on a file](https://developers.google.com/workspace/drive/api/guides/list-labels)
- [Google Drive API: Set a label field on a file](https://developers.google.com/workspace/drive/api/guides/set-label)
- [Google Drive API: Share files, folders, and drives](https://developers.google.com/workspace/drive/api/guides/manage-sharing)
- [Google Drive API: Manage file revisions](https://developers.google.com/workspace/drive/api/guides/manage-revisions)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws binary and Google Workspace authentication with appropriate Drive scopes.]

## Skill Version(s):

1.0.13 (source: server release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
