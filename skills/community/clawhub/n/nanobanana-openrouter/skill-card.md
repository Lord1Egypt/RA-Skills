## Description:

Generates and edits images with Nano Banana Pro (Gemini 3 Pro Image) through OpenRouter, supporting text-to-image, image-to-image, and 1K/2K/4K output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate new images or edit existing images by calling OpenRouter with prompts, optional input images, and resolution choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional input images are sent to OpenRouter.

Mitigation: Use only prompts and images appropriate for OpenRouter processing, and avoid confidential content unless account data-handling expectations allow it.

Risk: OpenRouter API keys can be supplied in ways that may expose secrets.

Mitigation: Prefer OPENROUTER_KEY from a protected environment or secret manager, and avoid pasting API keys into chat or command history.

## Reference(s):

- [OpenRouter Chat Completions API endpoint](https://openrouter.ai/api/v1/chat/completions)
- [ClawHub skill page](https://clawhub.ai/liberalchang/skills/nanobanana-openrouter)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and generated PNG file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs PNG images to output_images or a custom directory; requires OPENROUTER_KEY or --api-key.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
