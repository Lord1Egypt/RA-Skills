## Description:

Transfers the visual style of a reference image to a target photo using image-to-image processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyang-youloft](https://clawhub.ai/user/wangyang-youloft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to apply a reference image's lighting, mood, color grading, and composition to a target photo while preserving the subject.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided reference and target image URLs are sent to ngmob.com for processing.

Mitigation: Use public, non-sensitive image URLs unless the provider's handling and retention practices are acceptable.

Risk: Swapping the reference image and target photo changes the generated result.

Mitigation: Confirm that the first image is the style reference and the second image is the target photo before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangyang-youloft/skills/masterpiece-clone)
- [Publisher Profile](https://clawhub.ai/user/wangyang-youloft)
- [Pixify Console](https://ai.ngmob.com)
- [ngmob API Base](https://api.ngmob.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples; API responses return a generated image URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires two publicly accessible image URLs and an API key; asynchronous polling returns outputs[0].url.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
