## Description: <br>
HiDPI Mouse provides Linux desktop automation scripts that auto-detect or calibrate display scale and convert Claude display coordinates to xdotool screen coordinates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeyuyuyu](https://clawhub.ai/user/zeyuyuyu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to translate screenshot display coordinates into Linux/X11 mouse actions for clicking, dragging, moving, and calibrating HiDPI desktop automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move, click, and drag on a live Linux/X11 desktop. <br>
Mitigation: Supervise use on sensitive screens and verify target coordinates before important actions. <br>
Risk: Elevated privileges can increase the impact of unintended desktop automation actions. <br>
Mitigation: Run the scripts without elevated privileges unless a trusted operator has reviewed the action. <br>


## Reference(s): <br>
- [HiDPI Mouse on ClawHub](https://clawhub.ai/zeyuyuyu/hidpi-mouse) <br>
- [zeyuyuyu ClawHub profile](https://clawhub.ai/user/zeyuyuyu) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Linux/X11 mouse automation actions and calibration guidance using xdotool-based scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
