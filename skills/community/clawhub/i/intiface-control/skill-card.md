## Description: <br>
Control 750+ BLE intimate devices from natural language via Intiface Central and buttplug-mcp across macOS, Windows, and Linux. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AmandaClarke61](https://clawhub.ai/user/AmandaClarke61) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to connect OpenClaw to Intiface Central and send device listing, vibration, and stop commands to compatible intimate devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue physical-control commands to connected intimate devices. <br>
Mitigation: Install only when that control is intended, list connected devices first, verify the target device, require explicit approval for every start or strength change, and prefer low strength with short timed sessions. <br>
Risk: An Intiface server that is not kept local could increase the chance of unintended device control. <br>
Mitigation: Keep Intiface Central bound to localhost and stop Intiface Central when finished. <br>


## Reference(s): <br>
- [Intiface Central](https://intiface.com/central/) <br>
- [Buttplug.io Compatible Device Index](https://iostindex.com) <br>
- [buttplug-mcp releases](https://github.com/ConAcademy/buttplug-mcp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local mcporter, buttplug-mcp, Intiface Central, and an explicitly selected connected device.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
