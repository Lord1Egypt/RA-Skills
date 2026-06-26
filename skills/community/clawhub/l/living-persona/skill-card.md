## Description: <br>
Provides OpenClaw agents with dynamic, context-reactive personalities that adapt writing style and tone based on conversation signals and trait propagation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toxzak-svg](https://clawhub.ai/user/toxzak-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent builders use this skill to add a hook-driven personality system that responds to message tone and topic, persists trait state, and stages voice guidance for subsequent agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hook saves the latest raw user message and channel or sender identifiers into workspace memory. <br>
Mitigation: Review or modify persona-inbound.md handling before use in private, regulated, or multi-user workspaces, and reset or delete memory files when changing sessions or users. <br>
Risk: The hook can change the agent's writing style on every message by staging structural voice directives. <br>
Mitigation: Enable it only where dynamic persona behavior is desired, review persona-inject.md output, and use the reset script when starting a new session. <br>


## Reference(s): <br>
- [Living Persona ClawHub Page](https://clawhub.ai/toxzak-svg/living-persona) <br>
- [OpenClaw Hooks Documentation](https://docs.openclaw.ai/automation/hooks) <br>
- [Living Persona Setup Guide](references/setup.md) <br>
- [Personality Presets](references/presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown memory files, JSON trait state, and concise text directives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persona-inbound.md, persona-inject.md, persona-state.json, and a trigger sentinel in workspace memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
