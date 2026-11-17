## Description:

Generate images with Nano Banana Pro via OpenRouter. Use when the user asks for image generation, mentions Nano Banana Pro, Gemini 3 Pro Image, or OpenRouter image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duffycoder](https://clawhub.ai/user/duffycoder)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate new PNG images from text prompts through OpenRouter's Nano Banana Pro image model, with selectable 1K, 2K, and 4K resolutions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed through agent-readable .env files or command-line arguments.

Mitigation: Use environment-level secret handling instead of reading .env contents into agent context or passing keys with --api-key.

Risk: OPENROUTER_BASE_URL can redirect credentials and prompts to an unintended endpoint.

Mitigation: Restrict the base URL to the intended OpenRouter chat completions endpoint unless a reviewer explicitly approves another endpoint.

Risk: Downloaded image URLs are not validated before retrieval.

Mitigation: Validate returned image URLs and data URLs before downloading or decoding generated image content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duffycoder/skills/nano-banana-pro-openrouter)
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Shell command output with generated PNG file paths and MEDIA_URL entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under ~/.openclaw/workspace/outputs/nano-banana-pro-openrouter; this shell version supports generation only, not input image editing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
