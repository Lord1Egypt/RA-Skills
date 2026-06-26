## Description: <br>
OpenClaw infrastructure heartbeat monitoring and automatic recovery for deploying or removing a heartbeat daemon, configuring host and Gateway checks, setting Feishu alerts, and restarting a failed Gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[u0003-yxuan](https://clawhub.ai/user/u0003-yxuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and manage an OpenClaw heartbeat daemon that monitors Gateway availability, host resources, and process health, sends Feishu alerts, and attempts automatic Gateway recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installed heartbeat service runs continuously and can restart OpenClaw Gateway automatically. <br>
Mitigation: Install it only on systems where automatic Gateway recovery is intended, and review the systemd service and recovery behavior before enabling it. <br>
Risk: The configuration file contains Feishu credentials, Gateway tokens, and notification targets. <br>
Mitigation: Use only a configuration file you created and trust, keep config.env permission-restricted, and rotate credentials if the file is exposed. <br>
Risk: The daemon sources shell configuration and can edit or roll back OpenClaw configuration files. <br>
Mitigation: Avoid --config paths from other users or downloads, inspect configuration values before use, and keep separate backups of important OpenClaw settings. <br>


## Reference(s): <br>
- [Configuration Reference](artifact/references/configure.md) <br>
- [Release Notes](artifact/RELEASE.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/u0003-yxuan/openclaw-auto-recovery) <br>
- [Publisher Profile](https://clawhub.ai/user/u0003-yxuan) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and configuration file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for installing, configuring, monitoring, restarting, and uninstalling the heartbeat daemon.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
