## Description: <br>
Raspberry Pi system administration. Monitor resources, manage services, perform updates and maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and Raspberry Pi administrators use this skill to inspect host health, network state, storage, services, and hardware details, then run maintenance tasks such as updates, cleanup, reboot, gateway restart, and reversible optimizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maintenance commands can reboot the host, upgrade packages, clean Docker artifacts, disable services, change system settings, or restart the gateway. <br>
Mitigation: Install only on the intended Raspberry Pi, run information commands or --dry-run first, and require human approval before privileged maintenance commands. <br>
Risk: The skill can expose operational details such as hostnames, IP addresses, Tailscale status, services, ports, processes, logs, and hardware information. <br>
Mitigation: Treat command output as sensitive operational data and avoid sharing it outside trusted administration contexts. <br>
Risk: Hardcoded paths, ports, and local network addresses may not match the target system and can interrupt the wrong service if used without review. <br>
Mitigation: Review the configured paths, ports, and IP addresses before use, especially before running the gateway restart command. <br>


## Reference(s): <br>
- [Pi Admin on ClawHub](https://clawhub.ai/TheSethRose/pi-admin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes information-only commands, dry-run modes for maintenance commands, and interactive confirmation for several privileged changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
