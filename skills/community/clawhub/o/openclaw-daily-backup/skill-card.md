## Description: <br>
This skill should be used when the user asks for daily backup, scheduled backup, restore, rollback, recovery, or routine protection of core OpenClaw workspace identity/config files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[X-RayLuan](https://clawhub.ai/user/X-RayLuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, list, validate, and restore local backups for OpenClaw workspace identity and configuration files. It is intended for routine protection before configuration changes, scheduled backups, and recovery from accidental deletion or bad restores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled backup contents could overwrite a user's OpenClaw identity and configuration with unrelated high-impact behavior. <br>
Mitigation: Review and remove bundled backups before installation, especially AGENTS.md, SOUL.md, BOOTSTRAP.md, TOOLS.md, USER.md, and openclaw.sanitized.json. <br>
Risk: Restore operations can change agent identity, messaging integrations, execution permissions, and persistent behavior. <br>
Mitigation: Create a fresh local backup first, use dry-run restore previews, and restore only backups confirmed to belong to the target workspace. <br>
Risk: Backup files may contain sensitive workspace configuration. <br>
Mitigation: Keep backup directories protected with workspace-equivalent permissions, avoid publishing backups, and encrypt backups when they may contain secrets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/X-RayLuan/openclaw-daily-backup) <br>
- [Project Homepage](https://github.com/X-RayLuan/soul-backup-skill) <br>
- [OpenClaw Daily Backup README](artifact/README.md) <br>
- [OpenClaw Daily Backup Runbook](artifact/RUNBOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and Node.js script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide creation, validation, listing, and restore of local backup files; restore actions can modify workspace identity and configuration.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
