## Description: <br>
Automatically backs up OpenClaw configuration and supports manual backup, backup listing, diff preview, and selected rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyuyang2](https://clawhub.ai/user/wuyuyang2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to keep rolling local backups of their OpenClaw configuration and restore a selected backup when a configuration change needs to be reversed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rollback can overwrite current OpenClaw configuration and state. <br>
Mitigation: Review the diff preview, verify the selected backup, keep the pre-rollback backup, and test on non-critical data before restoring important environments. <br>
Risk: Rollback commands can stop or restart OpenClaw services and interrupt active work. <br>
Mitigation: Run restores during an acceptable maintenance window and confirm the affected OpenClaw services recover afterward. <br>
Risk: Frequent local backups may contain sensitive OpenClaw configuration data. <br>
Mitigation: Protect the backup directory, restrict local access to backup archives, and prune archives that no longer need to be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuyuyang2/openclaw-backup-rollback) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain-text command responses, JSON script results, and compressed backup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and restores local OpenClaw backup archives under ~/.openclaw/backups.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
