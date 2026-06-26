## Description: <br>
Backup and restore OpenClaw data, including backup scheduling, restore guidance, and backup rotation for the ~/.openclaw directory with documented exclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alessandropcostabr](https://clawhub.ai/user/alessandropcostabr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and operators use this skill to create local backups, configure daily backup reminders, restore OpenClaw data, and keep a short backup rotation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives can contain sensitive OpenClaw credentials, session data, memory, user files, and scheduled tasks. <br>
Mitigation: Keep archives private, restrict filesystem access, and consider encryption for stored backups. <br>
Risk: Restoring from an untrusted or stale archive can overwrite current OpenClaw state. <br>
Mitigation: Restore only trusted archives and create or locate a current safety copy before restoring. <br>
Risk: The detailed rollback example may not match the timestamped safety-copy path created during restore. <br>
Mitigation: Verify the actual rollback directory name before moving directories during rollback. <br>


## Reference(s): <br>
- [Restore OpenClaw from Backup](references/restore.md) <br>
- [OpenClaw Backup Safe release page](https://clawhub.ai/alessandropcostabr/openclaw-backup-safe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces backup and restore instructions for local OpenClaw files; backup archives may contain credentials, sessions, memory, and scheduled tasks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
