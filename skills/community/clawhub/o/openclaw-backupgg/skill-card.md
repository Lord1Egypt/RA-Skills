## Description: <br>
Backs up an OpenClaw workspace into a ZIP archive with a manifest and SHA256 checksum, with restore support for trusted backup archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hhse](https://clawhub.ai/user/hhse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to create local backups of workspace memory, skills, identity files, configuration, logs, tasks, documents, and knowledge files, then restore those backups when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain sensitive workspace data and are stored as unencrypted ZIP archives. <br>
Mitigation: Keep backup files private or encrypt them separately before storing or sharing them. <br>
Risk: Restoring a backup can replace memory, configuration, tools, and installed skills in the OpenClaw workspace. <br>
Mitigation: Restore only archives from trusted sources and review the backup contents with dry-run or listing options before confirming restore. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hhse/openclaw-backupgg) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, files, guidance] <br>
**Output Format:** [Markdown instructions with shell commands; runtime output includes ZIP backup files, a manifest, and checksum text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Backups are local ZIP archives and are not encrypted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
