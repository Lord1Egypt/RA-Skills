## Description:

Analyzes an uploaded photograph, provides detailed feedback on exposure, focus, composition, lighting, and suggests concrete camera settings and shooting technique.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickliu54](https://clawhub.ai/user/nickliu54)

### License/Terms of Use:

MIT-0

## Use Case:

External users and photography-focused agents use this skill to review uploaded photos, identify exposure, focus, composition, lighting, and noise issues, and provide concrete camera-setting, shooting-technique, and post-processing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release appears to be an incomplete photo-analysis scaffold rather than a fully implemented analysis and image-generation package.

Mitigation: Review the skill contents before deployment and require concrete implementation and model-use instructions before relying on its advertised behavior.

Risk: Photo recommendations or simulated correction previews may be inaccurate or misleading for a specific image or shooting environment.

Mitigation: Treat outputs as reviewable guidance and validate settings, composition advice, and generated previews against photographer judgment or test images before customer-facing use.

## Reference(s):

- [Reference Documentation for Photo Analyzer](artifact/references/api_reference.md)
- [Photo Analyzer ClawHub page](https://clawhub.ai/nickliu54/skills/photo-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, image]

**Output Format:** [Markdown analysis and recommendations, with an optional generated image artifact when supported by the agent environment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The simulated improved image is optional and depends on the availability of an image-generation model or tool.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
