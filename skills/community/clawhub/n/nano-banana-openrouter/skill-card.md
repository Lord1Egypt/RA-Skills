## Description:

Generate images from text prompts with Google's Nano Banana/Gemini image models through the OpenRouter API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyi0329-pixel](https://clawhub.ai/user/fyi0329-pixel)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to add text-to-image generation to an OpenClaw workflow via OpenRouter-hosted Gemini image models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes unsafe API key handling, including a bundled test script with a hardcoded key.

Mitigation: Remove or ignore the bundled test script, rotate any exposed key, and configure only a dedicated OpenRouter API key before use.

Risk: The skill can fall back to GEMINI_API_KEY and send the wrong provider credential to OpenRouter.

Mitigation: Remove the GEMINI_API_KEY fallback and require OPENROUTER_API_KEY for normal use.

Risk: Image prompts are sent to OpenRouter and may contain sensitive or regulated information.

Mitigation: Do not include secrets, private data, or regulated content in prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fyi0329-pixel/skills/nano-banana-openrouter)
- [OpenRouter image generation guide](https://openrouter.ai/docs/guides/overview/multimodal/image-generation)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [String containing an image URL, base64 image data, or raw model response text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts and aspect ratio settings are sent to OpenRouter, and output depends on the selected model and provider response format.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
