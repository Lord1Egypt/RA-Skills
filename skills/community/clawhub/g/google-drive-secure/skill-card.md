## Description:

Google Drive Secure Management for listing, searching, reading text content, creating files and folders, uploading binaries, moving, copying, sharing, and managing permissions on Google Drive files through porteden.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porteden](https://clawhub.ai/user/porteden)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Google Drive files and folders through the porteden CLI, including search, content reads, file creation, uploads, copying, moving, sharing, permissions, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent access to Google Drive files and folders through porteden credentials.

Mitigation: Use a least-privileged Google account or token, verify Drive access and scopes, and review accessInfo and authWarnings before acting.

Risk: Sharing or delete commands can expose files or move them to trash.

Mitigation: Confirm the target file, recipient, role, and delete intent before running share or delete commands.

Risk: Unpinned porteden installation commands may install a newer CLI than the reviewed release.

Mitigation: Prefer a pinned or verified porteden release when installing for controlled environments.

## Reference(s):

- [PortEden homepage](https://porteden.com)
- [ClawHub Google Drive skill page](https://clawhub.ai/porteden/skills/google-drive-secure)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses compact JSON CLI output guidance (-jc) and requires porteden authentication for Drive access.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
