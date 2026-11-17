## Description:

Sync agent workspace with cloud storage (Dropbox, Google Drive, S3, etc.) using rclone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashbrener](https://clawhub.ai/user/ashbrener)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure rclone-backed workspace sync, run manual or scheduled syncs, and inspect sync status for cloud-backed backup and file transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can install system packages and configure cloud credentials for rclone.

Mitigation: Review the scripts before setup, avoid unattended package installation, and use a dedicated cloud account or scoped remote where possible.

Risk: Sync operations can modify files in the workspace or remote cloud storage, especially with bisync, --resync, or restore workflows.

Mitigation: Set an explicit mode and dedicated remote subfolder, run --dry-run first, and keep a recoverable backup before using --resync or restore.

Risk: The security scan notes defaults that do not match the safer documentation.

Mitigation: Configure the intended sync mode and paths explicitly before enabling automatic sync or running manual operations.

## Reference(s):

- [Workspace Sync & Backup ClawHub listing](https://clawhub.ai/ashbrener/skills/openclaw-workspace-sync)
- [rclone install documentation](https://rclone.org/install/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires rclone and a configured cloud storage remote; sync behavior depends on the selected mode and paths.]

## Skill Version(s):

2.4.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
