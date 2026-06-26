## Description: <br>
OpenClaw Backup & Restore helps agents create, validate, list, restore, and optionally Git-sync backups of OpenClaw workspace state files and configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[X-RayLuan](https://clawhub.ai/user/X-RayLuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to protect agent workspace files from accidental deletion, bad configuration changes, and workspace loss. It provides backup, dry-run restore, rollback, validation, and optional off-machine Git backup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can include sensitive workspace data and, in raw config mode, real OpenClaw configuration values. <br>
Mitigation: Prefer sanitized config backups, use raw config mode only with a private intended backup destination, and avoid committing backup data to public repositories. <br>
Risk: Remote backup sync can push copied backup data to the wrong Git remote or branch if configured incorrectly. <br>
Mitigation: Review the selected remote and branch before running backup-and-push, and use a private backup repository for off-machine backups. <br>
Risk: Restore operations can overwrite live workspace files. <br>
Mitigation: Run restore with --dry-run first, validate the selected backup, and rely on the automatic pre-restore backup for rollback. <br>
Risk: Hard-coded or stale example paths can operate on the wrong workspace when copied without adjustment. <br>
Mitigation: Replace example paths with the intended workspace path and set OPENCLAW_BACKUP_DIR when a custom backup location is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/X-RayLuan/openclaw-workspace-backup-restore) <br>
- [Publisher profile](https://clawhub.ai/user/X-RayLuan) <br>
- [Artifact README](README.md) <br>
- [Operations runbook](RUNBOOK.md) <br>
- [Package repository](https://github.com/X-RayLuan/openclaw-backup-restore.git) <br>
- [Node.js](https://nodejs.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON backup manifests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup directories, manifest.json files, validation output, restore previews, and optional Git commits or pushes when invoked by the user.] <br>

## Skill Version(s): <br>
1.5.4 (source: server release evidence and package.json; CHANGELOG latest entry is 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
