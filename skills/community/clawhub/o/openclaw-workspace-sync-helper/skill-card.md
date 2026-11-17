## Description:

Guides Chinese-speaking users through selecting and preparing manual commands to sync a cloud OpenClaw workspace to a local computer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zionfusu](https://clawhub.ai/user/zionfusu)

### License/Terms of Use:


## Use Case:

Developers using cloud OpenClaw workspaces use this skill to choose a safe sync approach for local editing, debugging, real-time synchronization, or backup. It asks for environment details, recommends rsync with inotify, sshfs, or Syncthing, and then provides manual setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated rsync, sshfs, or Syncthing commands could copy secrets, overwrite files, or sync in the wrong direction if paths, exclusions, credentials, or direction are wrong.

Mitigation: Review all generated commands, paths, sync direction, exclusions, and credential handling before manually running any command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zionfusu/skills/openclaw-workspace-sync-helper)
- [Artifact README](artifact/README.md)
- [Skill behavior description](artifact/skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese-language conversational Markdown with manual command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are examples for manual review and execution; the skill does not run them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
