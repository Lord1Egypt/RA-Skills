## Description:

Helps choose the right fal.ai model before API calls, with decision matrices for video generation, image editing, image generation, background removal, upscaling, TTS, and 3D tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to select fal.ai models for media generation and editing workflows before making API calls. It supports tasks such as text-to-video, image-to-video, image editing, background removal, upscaling, TTS, and image-to-3D selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad trigger description may invoke the skill for general image or video generation requests where fal.ai recommendations are not desired.

Mitigation: Review routing behavior before installation and narrow triggers if recommendations should be limited to explicit fal.ai requests.

Risk: The model tables include pricing and availability details that may become stale.

Mitigation: Verify current fal.ai model documentation and pricing before relying on recommendations for production or budget decisions.

## Reference(s):

- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-fal-model-selector)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown with decision matrices and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces model recommendations, pricing notes, and fal_client usage examples; it does not execute code.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
