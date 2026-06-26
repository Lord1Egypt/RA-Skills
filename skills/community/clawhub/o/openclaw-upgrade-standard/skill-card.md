## Description: <br>
Safe OpenClaw upgrade procedure with backup, doctor fix, service migration, rollback, and post-upgrade testing to prevent silent failures from Dashboard upgrades, entrypoint renames, and config breaking changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gjoham](https://clawhub.ai/user/gjoham) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when upgrading OpenClaw installations, planning a safe version transition, or recovering from a failed upgrade. It guides backup, upgrade, service migration, rollback, and post-upgrade validation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup directories created during the procedure may contain credentials, agent data, or service configuration. <br>
Mitigation: Keep backup directories private, restrict access, and remove or secure them after the upgrade or rollback window closes. <br>
Risk: Upgrade and recovery commands can modify global packages, OpenClaw configuration, and the user systemd service. <br>
Mitigation: Confirm the package source and target version before running commands, keep the backup available, and review each command for the local installation path. <br>
Risk: Doctor output and gateway logs collected for troubleshooting may expose environment or account details. <br>
Mitigation: Redact doctor output and gateway logs before sharing them in public bug reports or support channels. <br>


## Reference(s): <br>
- [OpenClaw Releases](https://github.com/openclaw/openclaw/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and a validation checklist] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes backup, rollback, test checklist, and bug report evidence guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
