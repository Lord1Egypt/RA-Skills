## Description: <br>
Performs a complete OpenClaw backup, fresh installation, and restore cycle with verification and troubleshooting for reliable disaster recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefanferreira](https://clawhub.ai/user/stefanferreira) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to back up configuration and skill files, reinstall OpenClaw, restore saved state, and verify the result before upgrades, migrations, or disaster recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reinstall commands can remove an existing OpenClaw installation before recovery is proven. <br>
Mitigation: Verify backup archives can be listed or extracted before removing OpenClaw, and run the workflow only in the intended environment. <br>
Risk: The installer command pipes a remote script directly into a shell. <br>
Mitigation: Download and inspect or verify the installer before running it when possible. <br>
Risk: Restoring untrusted backups can reintroduce unsafe configuration or skills. <br>
Mitigation: Restore only OpenClaw configuration and skills from backups you trust, then verify the restored files and OpenClaw behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stefanferreira/openclaw-backup-mother-skill) <br>
- [OpenClaw Backup Quick Reference](references/quick-reference.md) <br>
- [Backup verification script](scripts/verify-backup.sh) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command blocks and a verification shell script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes backup, reinstall, restore, and verification steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
