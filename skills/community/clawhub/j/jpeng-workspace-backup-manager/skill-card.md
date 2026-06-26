## Description: <br>
Manages workspace backups by creating snapshots and enabling restore points for recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, list, restore, and clean up snapshots of important workspace files and directories for recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore operations can overwrite current workspace files. <br>
Mitigation: Create a fresh backup or commit current changes before restoring from an older backup. <br>
Risk: Cleanup operations can permanently delete older backup snapshots. <br>
Mitigation: Review the backup list and retention count before running cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-workspace-backup-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Markdown, Shell commands] <br>
**Output Format:** [JavaScript return objects, backup snapshot files, Markdown-formatted backup lists, and CLI invocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates backups under /root/.openclaw/workspace/backups/ and can restore workspace files or delete older backups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
