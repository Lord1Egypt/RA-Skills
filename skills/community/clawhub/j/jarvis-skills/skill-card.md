## Description: <br>
Controls robotic arms and grippers through voice or code with OpenClaw, including 6-DOF movement, force sensing, collision detection, and simulation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aly-Joseph](https://clawhub.ai/user/Aly-Joseph) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and robotics operators use this skill to prepare or run robotic arm and gripper actions through voice commands or programmatic control. Use with real hardware only after the control module, dependencies, and safety limits have been independently reviewed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real robotic arm or gripper movement can cause physical damage or injury if controls are used without verified safety limits. <br>
Mitigation: Treat the skill as simulation-only until the control module is obtained and audited, emergency stop behavior is configured, and workspace limits are confirmed. <br>
Risk: The release lacks reviewed control code and clear confirmation rules for physical movement. <br>
Mitigation: Require explicit operator approval for every movement or gripper action and verify dependency provenance before using real hardware. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe robotic movement commands, hardware setup, simulation use, and operator approval steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact metadata says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
