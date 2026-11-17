## Description:

Configure Google Drive mounting on Linux with rclone and gog OAuth, including OAuth setup, rclone configuration, filesystem mounting, and optional systemd auto-mount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonglinmu](https://clawhub.ai/user/tonglinmu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to configure Google Drive as a local Linux filesystem mount. It guides OAuth token export, rclone configuration, mount commands, and optional boot-time auto-mount with systemd.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived Google OAuth credentials for Drive access.

Mitigation: Use restrictive permissions on credential files, prefer rclone's normal OAuth flow or a user-scoped service when appropriate, and review token handling before running commands.

Risk: The setup can create boot-time system persistence through a systemd service.

Mitigation: Inspect the generated service, mount point, and ExecStart command before enabling it, and use only trusted mount paths.

Risk: The --allow-other mount option can expose mounted Drive data to other local users.

Mitigation: Omit --allow-other unless local sharing is intended and local FUSE permissions are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tonglinmu/skills/google-drive-setup)
- [Google OAuth token endpoint](https://oauth2.googleapis.com/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, INI, and systemd unit blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that write credential-bearing rclone configuration and install a systemd service; review before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
