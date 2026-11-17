## Description:

Sync Obsidian OpenClaw config across multiple iCloud devices and manage symlinks for multi-device sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyd4y](https://clawhub.ai/user/boyd4y)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users on macOS use this skill to inspect iCloud Obsidian vaults, select a vault, and sync local OpenClaw configuration through symlinks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can persistently redirect active OpenClaw skills and configuration to content from a selected iCloud Obsidian vault.

Mitigation: Install and run it only with iCloud vaults you trust, and review the printed symlink plan before confirming setup.

Risk: Using --overwrite can replace the local openclaw.json path with a symlink to the iCloud version.

Mitigation: Back up local ~/.openclaw configuration and avoid --overwrite unless replacing the local configuration is intended.

Risk: Using --no-confirm skips the interactive review step before filesystem changes.

Mitigation: Prefer the confirmation flow and reserve --no-confirm for reviewed, repeatable setup commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boyd4y/skills/obsidian-openclaw-sync)
- [OpenClaw Vault Structure Reference](references/vault-structure.md)
- [Sync Helper Script](scripts/sync_helper.py)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Terminal text with command output and prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or remove local symlinks as part of setup and unset flows.]

## Skill Version(s):

1.0.1 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
