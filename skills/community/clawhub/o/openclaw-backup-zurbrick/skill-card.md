## Description: <br>
Encrypted backup and restore for OpenClaw agents that creates cloud-safe operational archives and optional age-encrypted secrets archives for disaster recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to back up, verify, restore, schedule, and optionally push OpenClaw workspace recovery archives while keeping secrets encrypted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restore operations can replace the current OpenClaw state. <br>
Mitigation: Verify the manifest and archive first, run restore with --dry-run, and perform live restore only from trusted backup sets. <br>
Risk: A restored pre-restart-check.sh can execute during the restore health check. <br>
Mitigation: Inspect any restored pre-restart-check.sh before allowing a live restore workflow to run it. <br>
Risk: Weekly verification includes retention pruning and orphan cleanup that can delete older backup files. <br>
Mitigation: Review retention settings and confirm backup inventory before running weekly cleanup on important archives. <br>
Risk: Secrets archives may contain credentials and local authentication state. <br>
Mitigation: Keep secrets archives encrypted, restore them only with trusted decryption material, and avoid pushing them unless explicitly intended. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/zurbrick/openclaw-backup-zurbrick) <br>
- [Restore Guide](references/restore-guide.md) <br>
- [What to Back Up](references/what-to-backup.md) <br>
- [Retention Policy](references/retention-policy.md) <br>
- [Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct high-impact backup, cleanup, restore, and GitHub push operations that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and CHANGELOG, released 2026-03-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
