## Description: <br>
System-level watchdog for OpenClaw gateway restarts and sub-agent task PIDs. Monitors registered PIDs and optional log or directory freshness, auto-reverts config on failed gateway restarts, and requires explicit registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[camopel](https://clawhub.ai/user/camopel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use ClawGuard to monitor explicitly registered OpenClaw background tasks and gateway restarts. It helps surface stopped or stale work, backs up gateway configuration before restarts, and attempts rollback when a restart fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs an always-running user-level watchdog service. <br>
Mitigation: Install only when continuous OpenClaw background monitoring is desired, and disable the user service when monitoring is no longer needed. <br>
Risk: Failed gateway restarts can trigger automatic rollback of OpenClaw configuration from stored backups. <br>
Mitigation: Review the installer and keep an independent known-good OpenClaw configuration backup before relying on automated rollback. <br>
Risk: Notifications may include diagnostic details about tasks, logs, gateway status, or restart failures. <br>
Mitigation: Choose notification targets carefully and avoid routing alerts to channels that should not receive operational diagnostics. <br>


## Reference(s): <br>
- [ClawGuard release page](https://clawhub.ai/camopel/openclaw-claw-guard) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, service setup, task registration, status, and operational guidance for OpenClaw watchdog use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
