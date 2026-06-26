## Description: <br>
openclaw2backup helps agents guide OpenClaw backup, restore, and backup management workflows for workspaces, skills, configuration, wallet data, and memory files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuCriss](https://clawhub.ai/user/SuCriss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create quick or full backups, list existing backups, and restore selected OpenClaw workspace, skill, configuration, wallet, and memory data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may include wallet configuration, memory files, credentials, repository history, and personal workspace data. <br>
Mitigation: Store backup ZIP files only in protected or encrypted locations and treat them as sensitive data. <br>
Risk: Restore operations can overwrite active OpenClaw workspace, skill, and configuration data. <br>
Mitigation: Verify the backup source before restoring, use DryRun when possible, and keep a current backup of the existing state. <br>
Risk: The reviewed artifact references backup and restore scripts that were not included for inspection. <br>
Mitigation: Obtain and review the referenced scripts from a trusted source before granting the skill authority to run backup or restore workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SuCriss/openclaw2backup) <br>
- [Publisher profile](https://clawhub.ai/user/SuCriss) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer users to PowerShell backup, restore, and backup-listing commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
