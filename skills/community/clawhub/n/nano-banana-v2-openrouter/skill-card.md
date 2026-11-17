## Description:

Generate/edit images with Gemini 3.1 Flash Image Preview via OpenRouter. Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 0.5K/1K/2K/4K; use --input-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tclxhai-lv](https://clawhub.ai/user/tclxhai-lv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to ask an agent to generate new PNG images or edit existing images through OpenRouter using text prompts, optional input images, and selectable output resolutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and any edited input images are sent to OpenRouter.

Mitigation: Avoid submitting confidential, regulated, or proprietary prompts and images unless the user's OpenRouter account and policy requirements permit that transfer.

Risk: Passing an OpenRouter API key in chat or with the --api-key command-line option can expose the key in logs or process metadata.

Mitigation: Prefer OPENROUTER_API_KEY from the environment or a secret manager, and do not paste the key into chat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tclxhai-lv/skills/nano-banana-v2-openrouter)
- [OpenRouter Chat Completions API endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image file with terminal status text and a saved file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and OPENROUTER_API_KEY; supports optional input-image editing and 0.5K, 1K, 2K, and 4K resolutions.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
