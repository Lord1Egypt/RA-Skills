## Description: <br>
Program and interact with embedded development boards through MicroPython REPL workflows for sensor reads, actuator control, firmware flashing, diagnostics, and algorithm deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x1abin](https://clawhub.ai/user/0x1abin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill to generate, deploy, and troubleshoot MicroPython code on connected microcontroller boards for local prototyping, diagnostics, networking, and device control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently modify connected microcontroller devices, including boot.py/main.py changes and firmware flashing. <br>
Mitigation: Require explicit user confirmation for dangerous operations, explain data-loss consequences, and back up boot.py/main.py before changing persistent device files. <br>
Risk: WebREPL and WiFi setup can expose remote device access or credentials if used on untrusted networks. <br>
Mitigation: Prefer USB, avoid WebREPL on untrusted networks, use a strong non-default WebREPL password, and keep WiFi credentials out of logs and shell history. <br>
Risk: Broad serial-port permission changes can weaken local host access controls. <br>
Mitigation: Do not use chmod 666 for serial ports; use group membership, udev rules, or a user-scoped ACL instead. <br>
Risk: GPIO, motor, relay, and other actuator control can damage hardware or create unsafe physical states. <br>
Mitigation: Confirm wiring before high-current control, use appropriate driver circuits and current limiting, bound loops with timeouts, and provide reset or power-off recovery steps. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0x1abin/micropython-skills) <br>
- [Publisher profile](https://clawhub.ai/user/0x1abin) <br>
- [Project homepage](https://github.com/0x1abin/agents-workspace) <br>
- [Connection reference](references/connections.md) <br>
- [ESP32 reference](references/esp32.md) <br>
- [Safety constraints and recovery](references/safety.md) <br>
- [MicroPython firmware downloads](https://micropython.org/download/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline MicroPython, Python, and shell command examples; generated device output uses tagged text and JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bounded hardware-control instructions and code snippets for local USB serial or WebREPL workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
