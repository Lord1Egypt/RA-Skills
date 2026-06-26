## Description: <br>
OpenClaw backup and restore tool that creates local backups before installation or debugging work, restores selected snapshots from the terminal, and restarts the OpenClaw Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohanyang92](https://clawhub.ai/user/haohanyang92) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and agents use this skill to protect local OpenClaw state before configuration, installation, or debugging changes. It helps create backups, restore a selected backup snapshot, and restart the Gateway after recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may contain sensitive OpenClaw memory, profile, tools, and configuration data. <br>
Mitigation: Keep the backup folder private and limit access to trusted local users. <br>
Risk: Restoring the wrong backup can replace current OpenClaw files. <br>
Mitigation: Review the selected backup snapshot before confirming restore. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haohanyang92/openclaw-backup-tool) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance, configuration] <br>
**Output Format:** [Markdown with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup, restore, and restart command guidance for OpenClaw state management.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
