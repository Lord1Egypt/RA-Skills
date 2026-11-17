## Description:

Helps agents generate image files through OpenRouter image models with prompt, size, aspect ratio, model, and output-path configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goforu](https://clawhub.ai/user/goforu)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to generate local image files from text prompts, optionally with an input image, in OpenClaw-compatible workflows backed by OpenRouter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image-to-image mode can upload any readable local file path selected through --input-image to OpenRouter.

Mitigation: Only provide non-sensitive image files, avoid private documents or secret-bearing paths, and require explicit upload confirmation in shared or sensitive workspaces.

Risk: The artifact does not show file type or size checks before reading an input image for upload.

Mitigation: Add file type and size validation before using --input-image, and reject unexpected or oversized files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/goforu/skills/phoenixclaw-image-gen)
- [Configuration Specification](references/configuration.md)
- [CLI Contract](references/cli-contract.md)
- [OpenRouter Image Generation Resolution Guide](references/resolution-guide.md)
- [Image Generation Extension Guide](references/extension-guide.md)
- [OpenRouter image generation documentation](https://openrouter.ai/docs/guides/overview/multimodal/image-generation)
- [OpenRouter Seedream 4.5 model page](https://openrouter.ai/bytedance-seed/seedream-4.5)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration]

**Output Format:** [PNG image file saved locally plus structured JSON success or error payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENROUTER_API_KEY; supports text-to-image and image-to-image, model selection, 1K/2K/4K size tiers, aspect ratio, and output path.]

## Skill Version(s):

0.2.1 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
