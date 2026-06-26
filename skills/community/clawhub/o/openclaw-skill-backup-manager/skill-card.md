## Description: <br>
Manage local and cloud backups with listing, creation, restore, scheduling, health checks, and rclone-based cloud sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ppopen](https://clawhub.ai/user/ppopen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to manage backups across local disks, Time Machine, rsync destinations, scheduled cron jobs, and optional cloud remotes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed artifact describes commands for a powerful local backup executable that is not included in the artifact. <br>
Mitigation: Confirm where the backup-manager executable comes from before running commands, and review it before use. <br>
Risk: Backup and restore commands can overwrite, expose, or delete important files if paths, remotes, or schedules are wrong. <br>
Mitigation: Test with non-critical folders first, use explicit paths, verify rclone remotes and cloud permissions, avoid syncing secrets unless encrypted, and remove cron schedules that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ppopen/openclaw-skill-backup-manager) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for backup listing, creation, restore, scheduling, cloud sync, and configuration review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
