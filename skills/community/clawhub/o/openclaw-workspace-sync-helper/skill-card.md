## Description: <br>
Guides users through selecting safe, manual synchronization options for moving a cloud OpenClaw workspace to a local computer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zionfusu](https://clawhub.ai/user/zionfusu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and DevOps users use this skill to choose between rsync with inotify, sshfs, and Syncthing for local development, debugging, real-time sync, or backup workflows. The skill produces recommended options, manual command examples, validation steps, and safety notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated synchronization commands may use the wrong source, destination, direction, or exclusions. <br>
Mitigation: Review paths, sync direction, and exclusions for secrets or private files before manually running any command. <br>
Risk: A chosen sync approach may introduce unwanted read/write behavior, background processes, or remote mounts. <br>
Mitigation: Confirm read-only versus two-way behavior and whether background processes or remote mounts are acceptable for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zionfusu/openclaw-workspace-sync-helper) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill description](artifact/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with copy-ready shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are examples for manual review and execution; the skill does not execute them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
