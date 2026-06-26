## Description: <br>
Control Midea ACs. Use this skill when the user wants to control ACs. Supports turning ACs on/off, setting temperature, setting fan speed, switching modes, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Iamanorange](https://clawhub.ai/user/Iamanorange) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and home-automation operators use this skill to control configured Midea air conditioners on a local network, including power state, target temperature, fan speed, operating mode, auxiliary heat, and status checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vague comfort requests such as warmer, cooler, or full speed could unintentionally change a real air conditioner setting. <br>
Mitigation: Check current device status and require clarification or confirmation before acting on vague requests. <br>
Risk: Incorrect room names or IP addresses could direct commands to the wrong local device or fail discovery. <br>
Mitigation: Verify the configured room-to-IP mapping before use and report the command result after execution. <br>
Risk: The skill depends on the external msmart-ng package to communicate with Midea devices. <br>
Mitigation: Install msmart-ng from a trusted package source and keep the local environment under user control. <br>


## Reference(s): <br>
- [Midea Air Conditioners on ClawHub](https://clawhub.ai/Iamanorange/midea-ac) <br>
- [msmart-ng Python package](https://pypi.org/project/msmart-ng) <br>
- [Mijia ClawHub skill](https://clawhub.ai/hqman/mijia) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands operate against locally configured room names and IP addresses.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
