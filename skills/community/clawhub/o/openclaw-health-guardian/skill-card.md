## Description: <br>
Deploy OpenClaw health monitoring on macOS with automatic Gateway recovery, a 180-second restart cooldown, and a five-restarts-per-hour limit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhilshi](https://clawhub.ai/user/zhilshi) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and OpenClaw users on macOS use this skill to install and operate a LaunchAgent that checks local Gateway health, attempts automatic recovery, and records operational logs and restart state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a macOS LaunchAgent that runs every five minutes and can automatically run OpenClaw repair, start, or restart commands. <br>
Mitigation: Install it only when recurring automatic Gateway recovery is desired, and review the launchctl and doctor --fix paths before enabling the service. <br>
Risk: Uninstall and reset workflows can delete OpenClaw health-check logs and restart state. <br>
Mitigation: Back up logs or state before using uninstall or reset commands when operational history matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhilshi/openclaw-health-guardian) <br>
- [Technical implementation details](artifact/references/technical-details.md) <br>
- [Troubleshooting guide](artifact/references/troubleshooting.md) <br>
- [Safety and security information](artifact/SAFETY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes macOS LaunchAgent setup, log inspection commands, uninstall/reset commands, and operational troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
