## Description: <br>
Backup and restore OpenClaw data, including configuration, credentials, workspace files, scheduled tasks, and backup rotation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenswj](https://clawhub.ai/user/kenswj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create and rotate backups of ~/.openclaw data, set up daily backup schedules, and follow restore or rollback steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain OpenClaw credentials, local agent state, and other sensitive files. <br>
Mitigation: Store generated backups in encrypted or access-restricted locations and treat them as sensitive secrets. <br>
Risk: Restore commands can replace or remove the current ~/.openclaw directory. <br>
Mitigation: Verify the backup archive and keep a recoverable copy of the current ~/.openclaw directory before running restore or rollback commands. <br>


## Reference(s): <br>
- [Restore OpenClaw from Backup](references/restore.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create compressed backup archives when the provided shell script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
