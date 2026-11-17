## Description:

Use when a Linux service is down or unreachable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterliu-512](https://clawhub.ai/user/peterliu-512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to diagnose unreachable Linux services by checking hardware, kernel drivers, firewall or rfkill state, service state, and effective configuration before applying fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may advise administrative Linux commands that persistently change firewall or Bluetooth startup settings.

Mitigation: Confirm the exact port, subnet, service name, whether changes should persist after reboot, and rollback commands before applying fixes.

Risk: SSH and firewall changes can interrupt access when applied without confirming the current effective configuration and active sessions.

Mitigation: Verify effective SSH configuration, listening ports, firewall state, and live sessions before tightening authentication or changing firewall rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peterliu-512/skills/linux-service-troubleshooting)
- [Bluetooth 设备配对流程（交互式）](artifact/references/bluetooth-pairing.md)
- [蓝牙键盘配对（Logitech K780/K380 类）](artifact/references/bluetooth-keyboard-pairing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and ordered troubleshooting steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include administrative Linux commands that should be confirmed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-09-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
