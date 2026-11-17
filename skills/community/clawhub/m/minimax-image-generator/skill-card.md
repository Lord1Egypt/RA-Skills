## Description:

Text-to-image and image-to-image generation using MiniMax API. Generates images from text prompts (t2i) or transforms reference images (i2i) using MiniMax's image-01 or image-01-live models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanhaixuan](https://clawhub.ai/user/lanhaixuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate images from text prompts or transform reference images through the MiniMax image generation API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, or base64 image data are sent to MiniMax under the user's account.

Mitigation: Avoid sensitive images and confidential prompts, and review MiniMax account terms before use.

Risk: The skill depends on a local MiniMax API key for authenticated network calls.

Mitigation: Use a dedicated API key and rotate or revoke it if the execution environment is shared or compromised.

Risk: Optional image saving writes generated content to the local filesystem.

Mitigation: Save into a dedicated output directory and review saved files before sharing or reusing them.

Risk: The skill installs and imports the third-party requests package without a pinned version in the artifact documentation.

Mitigation: Pin and review the requests dependency before deployment in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanhaixuan/skills/minimax-image-generator)
- [MiniMax Platform](https://platform.minimaxi.com)
- [MiniMax Coding Plan](https://platform.minimaxi.com/subscribe/coding-plan)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [JSON with image URLs or base64 image data; optional saved PNG file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API key; prompt input is limited to 1500 characters and generation count is 1 to 9 images.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
