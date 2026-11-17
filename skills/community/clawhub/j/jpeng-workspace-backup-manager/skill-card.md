## Description:

Manages workspace backups by creating snapshots and enabling restore points for recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create named recovery snapshots of an OpenClaw workspace, list available backups, restore from a selected backup, and remove older backup snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore and cleanup operations can overwrite or delete important workspace data.

Mitigation: Require explicit human confirmation and a preview of affected files before restore or cleanup operations.

Risk: Untrusted backup names or backup directories can direct file operations outside the intended backup location.

Mitigation: Validate backup names and paths, reject unsafe path components and symlinks, and require valid backup metadata before restore.

Risk: Backup snapshots may contain sensitive workspace state from root files, memory/, or logs/.

Mitigation: Store backups in a trusted access-controlled location and review backup contents before sharing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-workspace-backup-manager)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown, Text]

**Output Format:** [Backup snapshot files, JavaScript result objects, and formatted Markdown or text backup lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and restores selected root workspace files plus memory/ and logs/ directories under /root/.openclaw/workspace/backups/ by default.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
