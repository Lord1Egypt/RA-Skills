## Description:

OpenClaw Emergency Rollback gives OpenClaw users a local dead man's switch for snapshotting known-good configuration, arming a rollback timer, and restoring that snapshot if risky configuration changes break access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when changing OpenClaw configuration and needing a recovery path that can save local snapshots, arm or extend an automatic rollback timer, manually restore a snapshot, and explain or test the recovery workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The rollback system can overwrite OpenClaw configuration and restart the gateway after a timer expires.

Mitigation: Install and arm it only when intentional; create and validate a known-good snapshot before making changes, and confirm the configured restart command before relying on automatic recovery.

Risk: Persistent rollback files and hooks can affect future OpenClaw startups.

Mitigation: Restrict permissions on the rollback directory, review the installed startup hook, and disarm the watchdog after accepting changes or completing manual recovery.

Risk: A recovery test intentionally interrupts OpenClaw access and active sessions.

Mitigation: Run destructive tests only after the user confirms terminal or SSH access and has a manual recovery copy and restart command available.

Risk: Arbitrary or incorrect restart commands can fail recovery or execute unintended shell behavior.

Mitigation: Use the narrowest restart command appropriate for the deployment and avoid broad shell patterns when OpenClaw is running in containers or managed process trees.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/encryptshawn/skills/openclaw-emergency-rollback)
- [EncryptShawn publisher profile](https://clawhub.ai/user/encryptshawn)
- [OpenClaw Emergency Rollback setup guide](references/SETUP.md)
- [Emergency recovery test procedure](references/TESTING.md)
- [Manual recovery guide](references/RESTORE.md)
- [Watchdog recovery hook](hooks/watchdog-recovery/HOOK.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and procedural guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run bundled local Node.js scripts and install an OpenClaw startup hook for rollback recovery.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
