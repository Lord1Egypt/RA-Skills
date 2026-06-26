## Description: <br>
OpenClaw Watchdog Pro backs up OpenClaw configuration, monitors the local gateway, restores from backups, and detects gateway error patterns across Linux, macOS, and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doradx](https://clawhub.ai/user/doradx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to keep a local OpenClaw gateway healthy, preserve recent configuration backups, and recover after gateway failures without reconstructing configuration by hand. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Always-on recovery can restore configuration, restart the gateway, and run repair commands automatically. <br>
Mitigation: Install only when this behavior is intended, review the installer first, and monitor watchdog logs and state after enabling it. <br>
Risk: The installer can configure persistent services or scheduled tasks with elevated privileges. <br>
Mitigation: Avoid root or SYSTEM deployment where possible and confirm how to remove the service, scheduled task, and shell alias before use. <br>
Risk: Configuration backups under `~/.openclaw/backups` may contain sensitive OpenClaw settings. <br>
Mitigation: Protect the backup directory with appropriate filesystem permissions and retention controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/doradx/openclaw-watchdog-pro) <br>
- [Publisher profile](https://clawhub.ai/user/doradx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance and command suggestions; when executed, bundled scripts may create backups, logs, state files, shell aliases, and service or scheduled-task configuration.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
