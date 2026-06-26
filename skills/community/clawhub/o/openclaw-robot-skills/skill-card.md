## Description: <br>
通过统一 API 支持 OMRON TM、JAKA 和 DOBOT 协作机器人，用于连接、状态监控、关节和路径运动、安全控制以及 IO 操作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qujingyang28](https://clawhub.ai/user/qujingyang28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to guide agents in connecting to supported collaborative robot controllers, reading robot state, issuing motion commands, and handling IO through a common Python-oriented interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples and tests that can enable, move, or change outputs on real robot controllers. <br>
Mitigation: Require explicit trained-operator approval for enable, motion, and IO actions, and run first in simulation or an isolated lab. <br>
Risk: Hard-coded or example controller IP addresses may target unintended equipment if reused as-is. <br>
Mitigation: Replace example IP addresses with environment-specific configuration and separate read-only diagnostics from live motion scripts. <br>
Risk: Physical robot motion can create safety hazards if workspace controls are not in place. <br>
Mitigation: Use guarded workspace procedures, maintain emergency-stop access, and keep a trained operator present during live tests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qujingyang28/openclaw-robot-skills) <br>
- [Publisher profile](https://clawhub.ai/user/qujingyang28) <br>
- [OpenClaw Robot Skills overview](artifact/SKILL.md) <br>
- [TM Robot documentation](artifact/tm-robot/README.md) <br>
- [JAKA Robot documentation](artifact/jaka-robot/README.md) <br>
- [DOBOT Robot documentation](artifact/dobot-robot/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce robot connection, diagnostic, motion, and IO-control instructions that require human approval before use on physical equipment.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
