## Description: <br>
OpenClaw Recovery provides scripts and configuration that back up OpenClaw settings, monitor service health, restart or roll back the gateway, and notify the user during recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoyoyosan](https://clawhub.ai/user/yoyoyosan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to keep a local OpenClaw service available by creating configuration backups, scheduling health checks, and restoring a working configuration when the gateway fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install background recovery tasks that restart OpenClaw and overwrite its active configuration. <br>
Mitigation: Review scheduled cron or Task Scheduler entries during installation, enable autonomous recovery only where it is acceptable, and remove the scheduled tasks if continuous recovery is not desired. <br>
Risk: Backups may include local authentication files in ~/.openclaw/backups. <br>
Mitigation: Restrict permissions on the backup directory, decide whether auth-profiles.json and auth-state.json should be backed up, and remove sensitive backups that are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yoyoyosan/openclaw-recovery) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown instructions with shell scripts and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install, backup, recovery, rollback, uninstall, and safe-mode configuration files.] <br>

## Skill Version(s): <br>
4.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
