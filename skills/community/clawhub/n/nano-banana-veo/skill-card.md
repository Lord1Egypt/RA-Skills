## Description:

Generate images with Nano Banana (Gemini 3 Pro Image) and animate them into videos with Veo 3.1 for websites, landing pages, and marketing assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bermyboystechsolutions](https://clawhub.ai/user/bermyboystechsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to generate static image assets and optionally animate them into short MP4 videos through the Gemini API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The video download path can expose a Gemini API key to an unvalidated URL returned by a remote service.

Mitigation: Use a restricted Gemini API key with tight quotas and billing controls, avoid sensitive prompts or assets, and prefer a fixed version or patched release that validates video download hosts and redirects before attaching credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bermyboystechsolutions/skills/nano-banana-veo)
- [Veo 3.1 predictLongRunning API endpoint](https://generativelanguage.googleapis.com/v1beta/models/veo-3.1-generate-preview:predictLongRunning)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated image or video file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved as PNG or JPG files, and optional videos are saved as MP4 files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
