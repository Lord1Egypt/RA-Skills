## Description:

Generate or edit images through OpenRouter's multimodal image generation endpoint (`/api/v1/chat/completions`) using OpenRouter-compatible image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bawerlacher](https://clawhub.ai/user/bawerlacher)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate new images or edit existing images through OpenRouter-compatible image models, with support for model selection, aspect ratio, image size, and provider-specific image configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to OpenRouter for generation or editing.

Mitigation: Use the skill only when those prompts and images are appropriate to share with OpenRouter.

Risk: Passing the API key as a command-line argument can expose it through shell history or process listings.

Mitigation: Set OPENROUTER_API_KEY in the environment instead of using --api-key.

Risk: Generated files can overwrite existing outputs if reused filenames are supplied.

Mitigation: Save outputs under ~/.openclaw/media/outbound with fresh timestamped filenames.

Risk: Model or image_config choices may be unsupported by a selected OpenRouter model.

Mitigation: If a request fails, remove unsupported image_config options or switch to a compatible image-capable model.

## Reference(s):

- [OpenRouter image generation documentation](https://openrouter.ai/docs/guides/overview/multimodal/image-generation)
- [OpenRouter Chat Completions endpoint](https://openrouter.ai/api/v1/chat/completions)
- [ClawHub skill page](https://clawhub.ai/bawerlacher/skills/openrouter-image-generation)
- [Publisher profile](https://clawhub.ai/user/bawerlacher)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with shell command examples and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves the first returned image to a requested file path and prints the saved path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
