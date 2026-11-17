## Description:

Generates DALL-E 3 images from user-provided text prompts and returns the generated image URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binkosun](https://clawhub.ai/user/binkosun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to create a 1024x1024 image from a short text description using DALL-E 3. It is intended for prompt-driven image generation while avoiding realistic human faces and following DALL-E usage policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The JavaScript path disables TLS certificate verification and allows BASE_URL or API_BASE_URL to redirect API traffic, which could expose API keys and prompts.

Mitigation: Prefer the Python path, or require the JavaScript code to enforce TLS verification and restrict endpoint overrides before using a real API key.

Risk: Image prompts may contain sensitive personal or confidential details that are sent to the image-generation API.

Mitigation: Avoid sensitive prompt content and use environment or secret-manager credentials instead of command-line API keys.

Risk: The skill can generate realistic imagery and its documentation calls out avoiding realistic human faces and following DALL-E policies.

Mitigation: Review prompts and outputs for policy compliance before sharing generated images.

## Reference(s):

- [ClawHub skill page for img2img](https://clawhub.ai/binkosun/skills/img2img)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text image URL with markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one 1024x1024 standard-quality DALL-E 3 image per prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
