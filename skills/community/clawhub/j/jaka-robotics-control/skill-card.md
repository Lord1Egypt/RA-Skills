## Description: <br>
Control Zu20, Zu12, Zu7, and MiniCobo collaborative robots through the JAKA SDK with joint motion, linear motion, state monitoring, tool I/O, and command-line helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qujingyang28](https://clawhub.ai/user/qujingyang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to connect an agent or local Python workflow to JAKA collaborative robots for motion control, status checks, homing, and tool I/O. It is intended for environments where operators can safely configure the robot IP address, install the JAKA SDK, and supervise physical robot movement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable and move real JAKA robot hardware without enough built-in safety gates. <br>
Mitigation: Install only when robot control is intended, test in simulation or reduced-speed/manual mode first, verify the work area is clear and the emergency stop works, and require human approval before enablement, motion, homing, or I/O commands. <br>
Risk: Using an untrusted or mismatched JAKA SDK could create unreliable control behavior. <br>
Mitigation: Use a trusted SDK source and verify the required JAKA SDK files and supported version before connecting to hardware. <br>


## Reference(s): <br>
- [JAKA SDK Python Documentation](https://www.jaka.com/docs/guide/SDK/Python.html) <br>
- [JAKA SDK Download and Introduction](https://www.jaka.com/docs/guide/SDK/introduction.html) <br>
- [RobotQu Community](https://robotqu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JAKA SDK files and robot IP configuration; generated or executed commands may control physical robot hardware.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
