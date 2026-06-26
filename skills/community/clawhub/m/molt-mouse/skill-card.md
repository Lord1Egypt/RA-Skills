## Description: <br>
Local mouse control via ydotool wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oguzhaslak](https://clawhub.ai/user/oguzhaslak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users on Linux use this skill when an agent needs to move or click the local desktop mouse through the reviewed molt-mouse wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move and click the local Linux mouse, which may interact with whatever sensitive prompt, payment flow, or administrative dialog is in focus. <br>
Mitigation: Keep sensitive workflows out of focus while using the skill, provide explicit coordinates and actions, and review the resulting desktop state before continuing. <br>
Risk: The skill depends on the local molt-mouse command and ydotool socket; an unexpected wrapper or missing daemon can change behavior or prevent operation. <br>
Mitigation: Verify that the local molt-mouse command is the reviewed wrapper and that ydotoold is running before enabling mouse-control actions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Text with shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are limited to the local molt-mouse interface and require explicit numeric coordinates when movement targets are ambiguous.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
