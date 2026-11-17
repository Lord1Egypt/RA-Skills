## Description:

Control LIFX smart lights via natural language. Toggle, set colors/brightness, activate scenes, create gradients on multi-zone devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stillstellung](https://clawhub.ai/user/stillstellung)

### License/Terms of Use:

GPL-3.0

## Use Case:

External users and developers use this skill to let an OpenClaw agent control LIFX smart lights, rooms, scenes, and multi-zone gradients through natural-language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control connected LIFX smart lights using a reusable LIFX API token.

Mitigation: Install only when that level of smart-home control is acceptable, and prefer providing the token through an environment secret.

Risk: setup.sh can store the LIFX token on disk in .lifx-token.

Mitigation: Keep .lifx-token private, do not commit or copy it, and rely on LIFX_TOKEN where possible.

Risk: LIFX device or scene names may be written into persistent agent context.

Mitigation: Review generated SKILL.md before use and avoid device or scene names containing Markdown, newlines, or instruction-like text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stillstellung/skills/lifx)
- [Publisher Profile](https://clawhub.ai/user/stillstellung)
- [LIFX HTTP API](https://api.lifx.com/docs/)
- [LIFX Token Settings](https://cloud.lifx.com/settings)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [LIFX](https://www.lifx.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline bash commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LIFX API token via LIFX_TOKEN or local .lifx-token; setup can generate a personalized SKILL.md with local device context.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
