## Description: <br>
Backup, restore, and manage encrypted OpenClaw agent snapshots using the Keep My Claw API for configuration, workspace files, and credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ryce](https://clawhub.ai/user/Ryce) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to configure encrypted off-site backups, run backup and restore workflows, list snapshots, prune old backups, and migrate agent state between machines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can back up credentials, workspace files, cron jobs, and other sensitive OpenClaw state to an off-site service. <br>
Mitigation: Install only when full-agent encrypted backup is intended; review the file list before first upload, use an agent-scoped API key where possible, and keep API keys and passphrases out of chat logs. <br>
Risk: Restores can overwrite existing local OpenClaw files. <br>
Mitigation: Preview the backup contents, confirm the target agent and backup ID, and test restore on a non-production machine or fresh profile before replacing active data. <br>
Risk: Pruning can delete remote backup snapshots. <br>
Mitigation: List available backups first, choose a retention count deliberately, and keep at least one known-good recovery snapshot before pruning. <br>
Risk: Losing the encryption passphrase makes encrypted backups unrecoverable. <br>
Mitigation: Store the recovery email, account password, API key, and encryption passphrase in a password manager outside the backed-up machine before relying on the backups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ryce/keepmyclaw) <br>
- [Keep My Claw documentation](https://keepmyclaw.com/docs.html) <br>
- [Keep My Claw service](https://keepmyclaw.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing operational guidance for backup, restore, listing, pruning, account setup, credential handling, and scheduled backup workflows.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
