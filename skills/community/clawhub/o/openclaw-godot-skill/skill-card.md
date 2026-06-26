## Description: <br>
Control Godot Editor via OpenClaw Godot Plugin. Use for Godot game development tasks including scene management, node manipulation, input simulation, debugging, and editor control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TomLeeLive](https://clawhub.ai/user/TomLeeLive) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to control a Godot 4.x editor from OpenClaw for scene management, node manipulation, debugging, input simulation, script inspection, screenshots, and gameplay testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad Godot editor automation through a local HTTP bridge, including scene saves, node deletion, property changes, script reads, screenshots, and simulated input. <br>
Mitigation: Install only when intentional, keep the OpenClaw gateway reachable only by trusted local components, and require explicit user approval before project-changing or sensitive actions. <br>
Risk: Automated editor actions can damage or corrupt a Godot project. <br>
Mitigation: Back up projects first and test the skill in a separate project before using it on important work. <br>
Risk: Leaving the extension enabled when not actively using it increases exposure to unwanted editor control. <br>
Mitigation: Disable or remove the extension when it is not needed. <br>


## Reference(s): <br>
- [Godot Skill on ClawHub](https://clawhub.ai/TomLeeLive/openclaw-godot-skill) <br>
- [OpenClaw Godot Plugin](https://github.com/TomLeeLive/openclaw-godot-plugin) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include proposed Godot editor actions, command results, session status, script content, screenshots, and project state summaries.] <br>

## Skill Version(s): <br>
1.2.7 (source: server release metadata and extension/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
