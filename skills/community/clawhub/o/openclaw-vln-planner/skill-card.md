## Description:

Plans the next high-level robot navigation step from a natural-language instruction, one current image, and historical images, returning one structured JSON action for an OpenAI-compatible multimodal gateway and execution bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiktokdad](https://clawhub.ai/user/tiktokdad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robotics engineers use this skill to plan closed-loop vision-language navigation steps for a robot from camera observations and a natural-language goal. It returns one bounded mid-level action at a time and falls back to STOP when parsing, confidence, or safety conditions are not acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge can send local frame files and robot context to a configurable remote endpoint.

Mitigation: Restrict image inputs to trusted camera directories, validate image content and size, and require an HTTPS allowlisted gateway before deployment.

Risk: The documented low_visibility safety fallback is not deterministically enforced before model calls or executor actions.

Mitigation: Add low_visibility to the pre-call force-stop checks so the planner returns STOP before contacting the gateway or bridge.

Risk: The sample configuration stores an API key in ordinary YAML and dependencies are not pinned to exact versions.

Mitigation: Move secrets to a managed secret source or environment variable and pin dependency versions during release packaging.

## Reference(s):

- [Navigation Schema Reference](artifact/references/navigation-schema.md)
- [OpenClaw VLN Planner on ClawHub](https://clawhub.ai/tiktokdad/skills/openclaw-vln-planner)

## Skill Output:

**Output Type(s):** [json, code, shell commands, configuration, guidance]

**Output Format:** [Pure JSON navigation actions, with supporting Markdown guidance and Python/YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One next action per planning round; allowed actions are MOVE_FORWARD, TURN_LEFT, TURN_RIGHT, and STOP.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
