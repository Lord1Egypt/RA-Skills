## Description: <br>
Backs up and restores OpenClaw workspace state, memory, cron jobs, agent folders, and configuration across macOS and Linux machines using Git and a private GitHub repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnthonyFrancis](https://clawhub.ai/user/AnthonyFrancis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to checkpoint or restore personal workspace state, memory, cron jobs, and agent folders when migrating machines, recovering from data loss, or maintaining a private backup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill backs up and restores personal OpenClaw workspace, memory, agent, cron, and configuration data, so an incorrect repository or overly broad credential can expose sensitive state. <br>
Mitigation: Use a private repository, narrowly scoped GitHub authentication, and confirm the exact workspace, agent, scheduler, and restore paths before backup or restore operations. <br>
Risk: The quick install path pipes a remote GitHub installer into a shell. <br>
Mitigation: Prefer the documented git-clone installation path or review the installer script before executing it. <br>
Risk: Restore, reset, and scheduling commands can overwrite local state or add recurring user-level jobs. <br>
Mitigation: Review checkpoint status, keep a current backup before restore or reset, and enable automatic scheduling only after confirming the intended frequency and platform scheduler. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AnthonyFrancis/openclaw-checkpoint) <br>
- [OpenClaw Checkpoint GitHub Repository](https://github.com/AnthonyFrancis/openclaw-checkpoint) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>
- [Installation Guide](INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify OpenClaw workspace files, copied agent backups, Git commits, remote backup state, and user-level schedules when the documented commands are run.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
