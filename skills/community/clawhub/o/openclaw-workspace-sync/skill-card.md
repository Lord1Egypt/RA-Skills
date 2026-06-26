## Description: <br>
Sync agent workspace with cloud storage (Dropbox, Google Drive, S3, etc.) using rclone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashbrener](https://clawhub.ai/user/ashbrener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to sync workspace files with cloud storage, check sync health, configure rclone-backed providers, and create encrypted workspace backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud sync and backups can include sensitive workspace or agent state, including configuration, cron, and memory. <br>
Mitigation: Use trusted cloud remotes, review exclude patterns before syncing, keep backups disabled or workspace-only unless needed, and protect any backup passphrase. <br>
Risk: Bidirectional sync, restore, resync, or setup operations can overwrite files, reintroduce deleted files, or make host-level package changes. <br>
Mitigation: Prefer mailbox or mirror mode, dry-run or verify both sides before destructive operations, and run restore or sudo-based setup only when those changes are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ashbrener/openclaw-workspace-sync) <br>
- [Publisher profile](https://clawhub.ai/user/ashbrener) <br>
- [rclone installation documentation](https://rclone.org/install/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, sync, status, backup, restore, and troubleshooting guidance for rclone-backed workspace operations.] <br>

## Skill Version(s): <br>
2.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
