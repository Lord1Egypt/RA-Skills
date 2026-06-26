## Description: <br>
OpenClaw Guard helps protect OpenClaw configuration changes by backing up selected files before risky operations and restoring them if rollback is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zebra679096](https://clawhub.ai/user/Zebra679096) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining OpenClaw deployments use this skill to start, stop, inspect, restore, and clean a guard process around high-risk configuration edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime notification settings may send messages to a hardcoded Feishu recipient. <br>
Mitigation: Disable Feishu notifications unless explicitly needed, remove the hardcoded Open ID, and configure any recipient in a local settings file before running the script. <br>
Risk: Rollback, restore, check, and clean commands can change files, restart the Gateway service, or permanently delete backups. <br>
Mitigation: Run these commands only when automatic file rollback, Gateway restart, and backup deletion are acceptable; review the configured file list and backup directory first. <br>
Risk: The runtime configuration includes a hardcoded backup path that may not match the installing user's environment. <br>
Mitigation: Change the backup path to a controlled local directory before deployment and verify permissions on the OpenClaw workspace and backup location. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zebra679096/openclaw-guard-v2) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Zebra679096) <br>
- [Usage example](assets/example.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash commands and YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill also includes a Bash guard script and YAML settings for local OpenClaw backup, rollback, notification, health-check, and cleanup workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
