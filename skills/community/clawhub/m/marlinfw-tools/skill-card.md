## Description:

Helps operators inspect, monitor, calibrate, home, and run a supervised first-layer test on a USB-connected Marlin 3D printer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Printer operators and technicians use this skill to inspect Marlin firmware and settings, record telemetry, and perform individually approved calibration or first-layer checks while physically supervising the machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Homing, setting changes, and SD print tests can move or heat a physical printer; serial telemetry cannot confirm physical safety.

Mitigation: Use a stable printer-specific serial path, obtain exact current-turn approval for each state-changing action, and keep an operator at the printer with access to its power switch.

Risk: The send operation may allow more printer commands than the documentation promises if the container image has not been reviewed.

Mitigation: Independently verify the image implementation or pin to reviewed code before using send on a real printer.

Risk: Serial cancellation may not interrupt blocking heat-up or homing commands on some firmware.

Mitigation: Keep the operator physically present and prepared to stop the printer directly.

## Reference(s):

- [Marlin printer tools project](https://github.com/psyb0t/marlinfw-tools)
- [Marlin reports](references/marlin-reports.md)
- [Device access](references/device-access.md)
- [Setting writes](references/setting-writes.md)
- [Creality Ender 3 family safety](references/creality-ender-3.md)
- [Marlin EEPROM documentation](https://marlinfw.org/docs/features/eeprom.html)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON reports, JSONL telemetry]

**Output Format:** [Markdown guidance and shell commands; JSON inspection reports and JSONL monitoring records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Printer settings require inspection before and after any approved change; persistent changes require separate approval.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
