## Description:

Reasoning-driven image generation using structured creative briefs that generate high-fidelity images via muapi.ai with logic-based prompting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anil-matcha](https://clawhub.ai/user/anil-matcha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative agents use this skill to convert brief image requests into structured, reasoning-driven creative prompts and invoke Nano Banana Pro image generation through muapi.ai.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unaudited local image-generation provider outside the reviewed package.

Mitigation: Install only when the local core/media/generate-image.sh provider path is platform-managed or otherwise trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anil-matcha/skills/muapi-nano-banana-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/anil-matcha)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Reasoning brief text and bash invocation that returns JSON from the image-generation provider.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a subject; action, context, style, lighting, resolution, text, and view flag are optional script parameters.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
