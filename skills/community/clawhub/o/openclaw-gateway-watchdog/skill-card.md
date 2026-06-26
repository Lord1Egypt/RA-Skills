## Description: <br>
Automatically installs and configures Gateway Watchdog to monitor OpenClaw Gateway status, restart it when unavailable, enable optional DingTalk alerts, and set up autostart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install and configure a local background watchdog that checks OpenClaw Gateway health, restarts the gateway after failures, sends optional DingTalk notifications, and helps enable autostart on supported operating systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can run persistently and restart OpenClaw Gateway by stopping broad local process groups, which may affect unrelated Node.js or OpenClaw-related processes. <br>
Mitigation: Install only on machines where persistent monitoring and automated Gateway restarts are acceptable, and review or modify the restart logic to target only the intended Gateway process. <br>
Risk: DingTalk notification setup can introduce webhook and signing-secret handling concerns. <br>
Mitigation: Enable DingTalk only when needed, keep webhook and signing-secret values in local configuration, and avoid committing populated config files. <br>
Risk: Autostart behavior differs across Windows, Linux, and macOS and may leave a background service running longer than intended. <br>
Mitigation: Confirm OS-specific install and uninstall steps before enabling autostart, and verify service status and logs after installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adminlove520/openclaw-gateway-watchdog) <br>
- [README.md](artifact/README.md) <br>
- [ARCHITECTURE.md](artifact/ARCHITECTURE.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, configuration, autostart, status, uninstall, and log-checking guidance for a local watchdog service.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
