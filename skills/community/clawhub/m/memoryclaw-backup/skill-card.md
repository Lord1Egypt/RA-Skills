## Description:

Helps users install and use MemoryClaw to securely back up and restore their OpenClaw setup across machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iarayan](https://clawhub.ai/user/iarayan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install MemoryClaw and follow backup, restore, migration, and recovery workflows for OpenClaw settings, memory, and claw metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended external plugin can access the user's OpenClaw folder, settings, metadata, network connection, and backup scheduling.

Mitigation: Confirm that clawhub:memoryclaw is the intended trusted plugin before installation and use it only for documented backup and restore workflows.

Risk: Restore, login, and first-time setup are interactive workflows that may require user confirmation or passphrase handling.

Mitigation: Direct users to run interactive commands in their own terminal and reserve automated backup commands for users who have already completed setup.

Risk: Force-install or mutable @latest publisher workflows can increase trust and supply-chain risk.

Mitigation: Suggest force-install only after the user explicitly accepts the trust tradeoff.

## Reference(s):

- [MemoryClaw package](https://clawhub.ai/packages/memoryclaw)
- [MemoryClaw documentation](https://memoryclaw.ai/docs)
- [MemoryClaw dashboard](https://memoryclaw.ai/dashboard)
- [MemoryClaw Backup skill page](https://clawhub.ai/iarayan/skills/memoryclaw-backup)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct users to run interactive login or restore commands in their own terminal.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
