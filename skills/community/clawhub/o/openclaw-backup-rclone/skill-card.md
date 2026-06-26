## Description: <br>
Backs up OpenClaw configuration, skills, agents, workspaces, memory, and credentials to an rclone remote with scheduling and rotation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doradx](https://clawhub.ai/user/doradx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to configure and run recurring remote backups through rclone, rotate retained backup files, and restore backed-up OpenClaw data when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default backup can include credentials, memory, agents, and workspaces, which may expose sensitive OpenClaw data at the remote destination. <br>
Mitigation: Use a private encrypted rclone destination where possible, verify access controls, and disable unnecessary backup sections such as credentials, memory, or workspaces. <br>
Risk: An incorrect rclone path or remote configuration can send backups to the wrong destination or fail silently in scheduled operation. <br>
Mitigation: Verify the rclone remote path before scheduling, run check-only or manual backup tests first, and keep cron logs for troubleshooting. <br>
Risk: The cron example continues sending backups until the scheduled task is removed or changed. <br>
Mitigation: Document the installed cron entry, review retention settings, and remove or disable the cron job when recurring backups are no longer intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/doradx/openclaw-backup-rclone) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples and configuration options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes rclone remote path, retention count, include/exclude flags, check-only mode, cron scheduling, and restore examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
