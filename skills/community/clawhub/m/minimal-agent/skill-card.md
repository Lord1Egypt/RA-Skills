## Description: <br>
Minimal Agent controls Windows applications, processes, hardware settings, GUI automation, serial communication, and IoT interactions through an external system-controller skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and control a local Windows environment, including windows, processes, input devices, screen capture, serial devices, and IoT endpoints. It is suited to intentional local automation where the user accepts high-privilege system control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate as a high-privilege local automation agent. <br>
Mitigation: Install it only where local system control is intended, and run it under a restricted account or sandbox where possible. <br>
Risk: Text mode and automatic fallback can allow arbitrary command execution. <br>
Mitigation: Prefer function or force_function mode on sensitive systems, and avoid auto or mixed mode unless unrestricted command execution is acceptable. <br>
Risk: The skill depends on an external system-controller skill for many control actions. <br>
Mitigation: Verify the external system-controller dependency before use. <br>


## Reference(s): <br>
- [Minimal Agent release page](https://clawhub.ai/wangjiaocheng/minimal-agent) <br>
- [Publisher profile](https://clawhub.ai/user/wangjiaocheng) <br>
- [System-controller dependency on ClawHub](https://clawhub.ai/wangjiaocheng/system-controller) <br>
- [System-controller dependency on SkillHub](https://skillhub.tencent.com/skills/system-controller) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Plain text or Markdown with command output and inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local system-controller scripts or unrestricted text-mode system commands depending on configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
