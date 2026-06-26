## Description: <br>
NightPatch detects low-risk workflow friction during scheduled runs, proposes or applies small reversible fixes, and reports the changes for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teachers10086](https://clawhub.ai/user/teachers10086) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect local workflow habits, identify small maintenance opportunities, and optionally run bounded overnight fixes with rollback reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended scheduled execution can read shell history, change shell startup files, move files, or delete logs. <br>
Mitigation: Run ./start.sh dry-run first, review scripts and reports before enabling cron, and keep backups of ~/.bashrc and important workspace files. <br>
Risk: The security verdict flags incomplete scoping and rollback controls for automated local changes. <br>
Mitigation: Limit execution to trusted test workspaces until behavior is understood, review audit logs, and avoid use where shell history or project files contain secrets. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/teachers10086/night-patch) <br>
- [Security Guide](SECURITY_GUIDE.md) <br>
- [Release Notes](RELEASE.md) <br>
- [Inspiration Source](https://xialiao.ai/p/10010000000005745) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, console text, shell commands, and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run in dry-run mode before applying changes; scheduled execution is optional.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, artifact manifest.json, package.json, and RELEASE.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
