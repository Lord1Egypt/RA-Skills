## Description: <br>
Protect openclaw.json with automatic rollback, lock mode, multi-version baseline snapshots, audit log, and SIGUSR1 gateway hot-reload. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbcvv](https://clawhub.ai/user/xbcvv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
System administrators and OpenClaw operators use this skill to install and operate a persistent guard for /root/.openclaw/openclaw.json. It monitors config writes, validates changes, rolls back invalid updates, keeps baseline history, records audit events, and provides a manual unlock path after lock mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent root systemd service that watches and rewrites the OpenClaw configuration file. <br>
Mitigation: Install it only on intended Linux OpenClaw hosts, review the install script before execution, and ensure operators know how to stop or disable the service and run the unlock command. <br>
Risk: Operational alerts are sent to hard-coded Discord and Telegram targets through the OpenClaw messaging command. <br>
Mitigation: Remove or reconfigure those alert targets before deployment and confirm that alert contents are acceptable for the environment. <br>
Risk: Configuration backups and snapshots may contain sensitive OpenClaw settings. <br>
Mitigation: Verify permissions on /root/.openclaw/backups/config and handle backup retention according to the sensitivity of openclaw.json. <br>
Risk: Automatic rollback depends on a valid baseline configuration. <br>
Mitigation: Validate the current OpenClaw configuration before enabling the guardian and verify baseline integrity during operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xbcvv/openclaw-config-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/xbcvv) <br>
- [Design](references/DESIGN.md) <br>
- [Usage](references/USAGE.md) <br>
- [Operation](references/OPERATION.md) <br>
- [Archive](references/ARCHIVE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and operational instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install, status, unlock, audit-log, baseline-history, and troubleshooting commands for a Linux systemd OpenClaw deployment.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
