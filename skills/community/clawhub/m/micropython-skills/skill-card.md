## Description:

MicroPython Skills helps agents program and interact with embedded development boards through REPL workflows for sensor reads, actuator control, firmware flashing, device diagnostics, and on-device algorithms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x1abin](https://clawhub.ai/user/0x1abin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to let an agent discover, diagnose, program, and recover MicroPython-capable microcontroller boards. It supports local USB workflows and optional WebREPL workflows for sensor reading, actuator control, networking, firmware flashing, and algorithm deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable wireless device access through WebREPL and may handle WiFi or WebREPL credentials.

Mitigation: Prefer USB workflows, avoid default WebREPL passwords, and review boot.py or main.py changes before enabling persistent wireless access.

Risk: Serial-port guidance could broaden host device access if users apply overly permissive permissions.

Mitigation: Do not use chmod 666 for serial access; use the least-permissive OS-specific group or device permission change that allows the intended connection.

Risk: Firmware flashing can erase or permanently change connected microcontroller devices.

Mitigation: Flash only after explicit user confirmation, verify firmware sources before use, and make backups before destructive operations.

Risk: Agent-generated GPIO, PWM, relay, motor, or persistence actions can affect attached hardware or make a board hard to recover.

Mitigation: Confirm wiring and device intent before control actions, bound loops with timeouts or iteration limits, and back up boot.py and main.py before modifying autostart files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0x1abin/skills/micropython-skills)
- [Project homepage](https://github.com/0x1abin/agents-workspace)
- [Connection Reference](references/connections.md)
- [ESP32 Platform Reference](references/esp32.md)
- [Safety Constraints & Recovery](references/safety.md)
- [MicroPython firmware downloads](https://micropython.org/download/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with MicroPython and shell command snippets, plus tagged device output such as RESULT, ERROR, STATUS, and LOG lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for local device interaction through mpremote or optional WebREPL, with JSON used inside tagged result lines when device data is returned.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
