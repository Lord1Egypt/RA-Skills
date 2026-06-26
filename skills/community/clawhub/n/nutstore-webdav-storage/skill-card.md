## Description: <br>
Provides backup, archival, and restore guidance and scripts for OpenClaw multi-agent workspaces using Nutstore WebDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenmuting](https://clawhub.ai/user/chenmuting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure rclone, run Nutstore WebDAV backups, check backup state, and restore identity or memory data for OpenClaw agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenClaw identity and memory data can be uploaded to Nutstore, and the scanner warns that uploads may be broader than the safety notes imply. <br>
Mitigation: Use dry-run before real backups or cron, inspect memory and custom backup paths for secrets, and add explicit rclone filters instead of relying only on documented exclusions. <br>
Risk: Nutstore credentials or account passwords could be exposed if handled directly in scripts, shell history, or workspace files. <br>
Mitigation: Use a dedicated Nutstore app password through rclone configuration and avoid storing raw account credentials in the repository, memory, or documentation. <br>
Risk: Restoring directly into a live OpenClaw workspace can overwrite local files. <br>
Mitigation: Run restore dry-runs first, prefer RESTORE_TARGET_ROOT for test restores, and require explicit RESTORE_FORCE=1 before path-mode restores to the live workspace. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/chenmuting/nutstore-webdav-storage) <br>
- [Automation guidance](references/automation.md) <br>
- [Nutstore and WebDAV notes](references/nutstore-notes.md) <br>
- [Rclone setup](references/rclone-setup.md) <br>
- [Storage scope and exclusions](references/storage-scope.md) <br>
- [Nutstore WebDAV endpoint](https://dav.jianguoyun.com/dav/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash and cron command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes shell scripts for backup, restore, rclone configuration, cron examples, and backup checks.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
