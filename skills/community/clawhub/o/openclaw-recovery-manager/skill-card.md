## Description: <br>
Creates and restores OpenClaw configuration, skills, and project snapshots, including a config-only dead-man's-switch watchdog for emergency rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to snapshot, restore, and test recovery for OpenClaw configuration, skills, and project state before or after risky changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite current OpenClaw configuration, skills, and project state. <br>
Mitigation: Keep backups under ~/.openclaw/rollback and manually confirm skills or project restores before running them. <br>
Risk: A wrong or tampered restart command can make automatic config recovery fail or restart the wrong gateway process. <br>
Mitigation: Verify the stored restart command in rollback-config.json before arming recovery and restrict who can edit it. <br>
Risk: Snapshot archives or rollback state can be altered before restore. <br>
Mitigation: Restrict write access to rollback-config.json and snapshot archives, and review the selected snapshot before restoring. <br>


## Reference(s): <br>
- [OpenClaw Recovery Manager - One-Time Setup](references/SETUP.md) <br>
- [Manual Recovery - No AI Required](references/RESTORE.md) <br>
- [Emergency Recovery Test - Destructive](references/TESTING.md) <br>
- [OpenClaw Recovery Manager release page](https://clawhub.ai/encryptshawn/openclaw-recovery-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct an agent to run local Node.js recovery scripts that create snapshots, restore archives, update watchdog state, or restart the OpenClaw gateway.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
