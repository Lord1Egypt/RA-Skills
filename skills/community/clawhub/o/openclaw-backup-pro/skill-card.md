## Description: <br>
Backs up and restores OpenClaw configuration, credentials, sessions, workspace data, and scheduled tasks with backup rotation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardx0319](https://clawhub.ai/user/richardx0319) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create, schedule, rotate, and restore backups of a local ~/.openclaw directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can contain OpenClaw credentials, API tokens, session data, workspace files, and scheduled tasks. <br>
Mitigation: Store backup archives privately, prefer encryption, and do not share them. <br>
Risk: Restoring an archive can replace the current ~/.openclaw state. <br>
Mitigation: Inspect the archive, verify it came from a trusted backup, and keep a separate copy of the current ~/.openclaw state before restoring. <br>
Risk: Restore commands operate on files in the user's home directory. <br>
Mitigation: Review the selected backup path and restore commands before running them. <br>


## Reference(s): <br>
- [Restore OpenClaw from Backup](references/restore.md) <br>
- [Openclaw Backup on ClawHub](https://clawhub.ai/richardx0319/openclaw-backup-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, and script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or restore compressed archives containing local OpenClaw state.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
