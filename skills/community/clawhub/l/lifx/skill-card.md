## Description: <br>
Control LIFX smart lights via natural language. Toggle, set colors/brightness, activate scenes, create gradients on multi-zone devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Stillstellung](https://clawhub.ai/user/Stillstellung) <br>

### License/Terms of Use: <br>
GPL-3.0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent discover and control LIFX smart lights, including rooms, scenes, brightness, colors, and multi-zone gradients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a local LIFX token and personalized home-light context. <br>
Mitigation: Keep .lifx-token and generated SKILL.md private, restrict file permissions, and avoid sharing generated device context. <br>
Risk: An agent with this skill can control the user's LIFX lights. <br>
Mitigation: Install only when agent-driven smart-light control is acceptable, and review commands before execution in sensitive environments. <br>
Risk: Instruction-like light, room, or scene names could influence agent behavior. <br>
Mitigation: Use plain, non-instructional names for lights, groups, and scenes. <br>
Risk: The published artifact references SKILL.md.template, but that file is not included in the package evidence. <br>
Mitigation: Verify the package includes the template before relying on setup.sh to regenerate SKILL.md. <br>


## Reference(s): <br>
- [LIFX HTTP API](https://api.lifx.com/docs/) <br>
- [LIFX token settings](https://cloud.lifx.com/settings) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [LIFX](https://www.lifx.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a LIFX API token and may read or generate local device context for rooms, lights, scenes, and multi-zone devices.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
