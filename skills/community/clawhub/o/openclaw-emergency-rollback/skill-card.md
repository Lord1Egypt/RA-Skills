## Description: <br>
OpenClaw Emergency Rollback provides a local dead man's switch for OpenClaw configuration changes, using snapshots, watchdog timers, and startup recovery to restore a known-good config if changes are not accepted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill before risky OpenClaw config or agent workspace changes to create snapshots, arm or extend rollback timers, restore snapshots, and test emergency recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The rollback system can persist across restarts, overwrite OpenClaw configuration, and restart the gateway automatically. <br>
Mitigation: Install only when this behavior is intended, verify rollback-config.json contains the correct restart command, and restrict permissions on ~/.openclaw/rollback. <br>
Risk: Restoring a snapshot can replace the current OpenClaw config and agent workspace config files. <br>
Mitigation: Inspect snapshot contents and confirm the target snapshot before restoring; keep manual shell access available for recovery. <br>
Risk: The recovery test deliberately breaks OpenClaw configuration and can interrupt active sessions. <br>
Mitigation: Run the destructive test only with terminal access and a manual recovery copy ready. <br>


## Reference(s): <br>
- [One-Time Setup](references/SETUP.md) <br>
- [Manual Recovery](references/RESTORE.md) <br>
- [Emergency Recovery Test](references/TESTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local rollback instructions and command outputs for snapshots, watchdog timers, restores, status checks, and recovery testing.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
