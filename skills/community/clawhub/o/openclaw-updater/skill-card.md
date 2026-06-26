## Description: <br>
Safely update OpenClaw with pre-flight checks, workspace snapshots, config backups, notification support, rollback, and post-update verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigsan](https://clawhub.ai/user/bigsan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to prepare for OpenClaw updates, run update commands with notification support, verify the result, and roll back when an update fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's scripts change local OpenClaw and workspace state, including git commits, config backups, package updates, gateway restarts, and optional rollback installs. <br>
Mitigation: Run the update script with --dry-run first, review workspace contents before allowing automatic git add or commit, and verify rollback versions and backup contents before restoring or running npm install -g. <br>
Risk: Telegram notification setup uses a bot token and chat ID stored in or sourced from the local OpenClaw directory. <br>
Mitigation: Store the Telegram token file with restrictive permissions or skip the notification wrapper when notification credentials are not needed. <br>
Risk: The optional BACKUP_SCRIPT environment variable can execute an additional local script during pre-flight checks. <br>
Mitigation: Set BACKUP_SCRIPT only to a trusted executable script that has been reviewed for the current environment. <br>


## Reference(s): <br>
- [OpenClaw Updater on ClawHub](https://clawhub.ai/bigsan/openclaw-updater) <br>
- [Telegram Bot API sendMessage endpoint](https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces update, dry-run, notification, verification, and rollback instructions for local OpenClaw maintenance.] <br>

## Skill Version(s): <br>
1.6.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
