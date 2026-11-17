## Description:

OpenClaw Configuration Management & Emergency Recovery helps agents snapshot and restore OpenClaw configuration, skills, and project state, including an automatic config-only watchdog recovery path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when changing OpenClaw configuration, skills, or project setup and need snapshots, restores, or a dead-man's-switch fallback. It is intended for OpenClaw environments where recovery commands may overwrite local configuration and restart the gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The startup hook and watchdog can overwrite OpenClaw configuration and restart the gateway.

Mitigation: Install only for environments that need emergency rollback, review the hook before enabling it, and keep manual recovery access available.

Risk: Snapshot archives and manifests under ~/.openclaw/rollback may contain sensitive configuration or operational state.

Mitigation: Restrict filesystem permissions, protect or inspect archives before sharing, and confirm credential exclusions remain appropriate for the deployment.

Risk: A free-form restart command can execute with the user's shell privileges during restore.

Mitigation: Use the bundled restart-command detection flow, confirm the detected command before storing it, and avoid arbitrary custom restart commands.

Risk: Manual skills and project restores can overwrite local skill directories or project manifests and state.

Mitigation: Require explicit confirmation, verify the target and snapshot slot, and review restore results before continuing work.

## Reference(s):

- [OpenClaw Recovery Manager Setup](references/SETUP.md)
- [Manual Recovery - No AI Required](references/RESTORE.md)
- [Emergency Recovery Test - Destructive](references/TESTING.md)
- [ClawHub Skill Page](https://clawhub.ai/encryptshawn/skills/openclaw-recovery-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions and command selections for local OpenClaw snapshot, restore, watchdog, setup, and test workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
