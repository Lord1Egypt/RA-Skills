## Description: <br>
Raspberry Pi health monitor. Check CPU temperature, throttling status, voltage levels, memory/disk usage, fan RPM, overclock detection, and power issues. Use when monitoring Pi health, diagnosing thermal throttling, checking for under-voltage, or verifying system stability on any Raspberry Pi (Pi 3/4/5, arm64/armhf). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JosunLP](https://clawhub.ai/user/JosunLP) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and Raspberry Pi users use this skill to run a local diagnostic report for thermal, power, memory, disk, fan, overclock, and stability checks on Raspberry Pi systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local diagnostic output may reveal system health details such as disk usage, boot configuration, and power-event logs. <br>
Mitigation: Run the script only on systems where sharing local health details with the agent is acceptable, and review the report before copying it into external tickets or channels. <br>
Risk: The script reads local Raspberry Pi diagnostics and depends on host commands and system files, so results may be incomplete when optional tools or permissions are unavailable. <br>
Mitigation: Install recommended Raspberry Pi OS utilities such as vcgencmd and bc where appropriate, and treat unavailable checks as gaps rather than confirmed healthy status. <br>


## Reference(s): <br>
- [Pi Health ClawHub Release](https://clawhub.ai/JosunLP/pi-health) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text report with process exit code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The health script returns exit code 0 for healthy, 1 for warnings, and 2 for critical findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
