## Description: <br>
Openclaw Backup provides setup guidance and backup scripts for OpenClaw local storage configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hi-Jiajun](https://clawhub.ai/user/Hi-Jiajun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and maintainers use this skill to configure local backup settings and run backups for configuration, credentials, scheduled tasks, device pairing data, identity data, and installed skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups can include credentials and API-key material from the OpenClaw credentials directory. <br>
Mitigation: Store backups in a dedicated private location, avoid shared or cloud-synced folders unless encrypted, and restrict access to backup archives. <br>
Risk: Old-backup cleanup can permanently delete backup folders when size limits are exceeded. <br>
Mitigation: Review config.sh before repeated or scheduled runs, keep old-backup paths narrow, and avoid broad paths such as a home directory or filesystem root. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hi-Jiajun/openclaw-backup-hiliang) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local backup folders and a shell configuration file when the setup script is run.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
