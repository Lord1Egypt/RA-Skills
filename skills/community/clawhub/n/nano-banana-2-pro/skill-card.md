## Description:

Generate and edit images with Google's Nano Banana 2 API (Gemini 3.1 Flash Image Preview), including text-to-image and image-to-image workflows with resolution, aspect ratio, thinking level, and multi-image controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gybin02](https://clawhub.ai/user/gybin02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to ask an agent to generate new PNG images, edit existing images, compose multiple reference images, and choose model, resolution, aspect ratio, and thinking-level options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images may be sent to Google image-generation services, which can expose private or regulated content.

Mitigation: Avoid private or regulated images and prompts unless Google processing is acceptable for the user's use case.

Risk: API keys can be supplied through chat or command-line arguments, increasing the chance of accidental disclosure.

Mitigation: Set GEMINI_API_KEY through a protected environment variable and avoid sharing API keys in chat or shell history.

Risk: The documentation points to a different skill path than the inspected artifact path.

Mitigation: Use only the inspected script path for installation and execution, and verify the local path before running commands.

Risk: Unpinned dependency ranges may change behavior over time.

Mitigation: Pin google-genai and pillow versions before routine or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gybin02/skills/nano-banana-2-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/gybin02)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated PNG files are saved by the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script prints status text and the resolved output image path; generated images include a SynthID watermark.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
