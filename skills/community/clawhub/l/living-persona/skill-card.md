## Description:

Provides OpenClaw agents with dynamic, context-reactive personalities that adapt writing style and tone based on conversation signals and trait propagation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toxzak-svg](https://clawhub.ai/user/toxzak-svg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this OpenClaw hook to add dynamic personality behavior to agents, including signal-based trait activation, trait persistence, and prompt-facing voice directives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hook can persistently change how every agent response is written.

Mitigation: Review the generated voice directives before deployment and use ambient mode or remove structural prompt injection where stable agent behavior is required.

Risk: The hook stores raw conversation text in workspace memory.

Mitigation: Do not use it in sensitive, shared, or regulated workspaces unless raw message logging is disabled or clearly scoped and memory files are regularly cleared.

Risk: The bundled persona includes hard-coded relationship framing and anchors.

Mitigation: Remove or customize those anchors before installing the hook for users or teams other than the original publisher's intended context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/toxzak-svg/skills/living-persona)
- [OpenClaw Hooks Documentation](https://docs.openclaw.ai/automation/hooks)
- [Setup Guide](artifact/references/setup.md)
- [Personality Presets](artifact/references/presets.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prompt files, JSON state, and setup command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persona-inject.md, persona-inbound.md, persona-state.json, and persona-trigger.txt under workspace memory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
