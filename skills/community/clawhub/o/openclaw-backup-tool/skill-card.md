## Description:

OpenClaw 备份还原工具。每次安装调试功能前自动备份，支持终端一键还原和重启。让技术小白也能放心折腾。

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohanyang92](https://clawhub.ai/user/haohanyang92)

### License/Terms of Use:


## Use Case:

OpenClaw users and maintainers use this skill to back up local OpenClaw configuration and agent state before installation, debugging, or configuration work, then restore a selected backup or restart the OpenClaw Gateway when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may contain sensitive OpenClaw identity, user, memory, tool, soul, and configuration files.

Mitigation: Keep the backup directory private and treat backup snapshots as sensitive local data.

Risk: Restoring an untrusted or incorrect backup can replace current OpenClaw configuration and agent state.

Mitigation: Restore only trusted backup snapshots and confirm the selected backup before proceeding.

Risk: Restarting the OpenClaw Gateway can briefly interrupt local gateway availability.

Mitigation: Run the restart command during a maintenance window or when a short interruption is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haohanyang92/skills/openclaw-backup-tool)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local backup, restore, and restart command guidance for an OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
