## Description: <br>
Control mobile robots via instant messaging platforms, including Unitree quadruped and humanoid robots with optional Insight9 camera and navigation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Qinrui-dm](https://clawhub.ai/user/Qinrui-dm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, robotics operators, educators, and researchers use this skill to connect OpenClaw-style agents to mobile robots and issue movement, posture, status, SLAM, and navigation commands through supported messaging platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls physical robots through messaging commands without enough built-in safety, authorization, or movement-limit evidence. <br>
Mitigation: Use simulation or a cleared supervised area first, add authentication and confirmation before accepting commands, enforce movement limits, and verify an emergency stop before connecting real hardware. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Qinrui-dm/openclaw-robotics) <br>
- [Publisher Profile](https://clawhub.ai/user/Qinrui-dm) <br>
- [README](README.md) <br>
- [Contributing Guide](CONTRIBUTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets and robot command strings; runtime functions return JSON-like dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Robot actions may affect physical hardware and require operator safety controls outside the skill.] <br>

## Skill Version(s): <br>
2.1.0 (source: pyproject.toml and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
