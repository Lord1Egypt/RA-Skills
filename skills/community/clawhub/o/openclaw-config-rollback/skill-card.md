## Description: <br>
Backs up OpenClaw configuration changes and automatically rolls back if the gateway is not restarted within five minutes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[echoflying](https://clawhub.ai/user/echoflying) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage OpenClaw configuration changes with pre-change backups, pending verification notes, and automatic rollback if the gateway does not restart successfully. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed cron task runs every minute and may persist after the user no longer needs rollback monitoring. <br>
Mitigation: Review the crontab entry during installation and remove the rollback-guardian entry when rollback monitoring is no longer required. <br>
Risk: Automatic rollback can overwrite ~/.openclaw/openclaw.json from a backup and restart the OpenClaw gateway after the timeout. <br>
Mitigation: Use the preparation script before intentional configuration changes, verify the backup path, and restart the gateway within the five-minute window when the change should be kept. <br>


## Reference(s): <br>
- [ClawHub skill page: Config Rollback](https://clawhub.ai/echoflying/openclaw-config-rollback) <br>
- [Publisher profile: echoflying](https://clawhub.ai/user/echoflying) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash commands and configuration file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup, rollback, cron setup, status, and verification guidance for OpenClaw configuration changes.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence release metadata, _meta.json, package.json, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
