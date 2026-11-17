## Description:

Nano Banana Image T8 helps an agent generate or edit images with the Nano Banana API using a user-provided prompt, optional source images, and saved model preferences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flywhale-666](https://clawhub.ai/user/flywhale-666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run text-to-image or image-to-image generation workflows from conversation parameters, including prompts, optional image inputs, aspect ratio settings, and model preference changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses API keys for an external image service and can save the key locally.

Mitigation: Use a key that can be rotated, pass it only through the documented parameter or NANO_BANANA_API_KEY, and remove or rotate the saved key when the skill is no longer used.

Risk: Prompts, source images, and generated image downloads may leave the local machine through the configured service path.

Mitigation: Avoid sensitive prompts or private images unless the external service is approved for that data.

Risk: A custom base URL could route prompts, images, or credentials to an unintended service.

Mitigation: Use the documented default service endpoint and avoid passing a custom --base-url.

## Reference(s):

- [Nano Banana Image T8 ClawHub Page](https://clawhub.ai/flywhale-666/skills/nano-banana-image-t8-win)
- [flywhale-666 Publisher Profile](https://clawhub.ai/user/flywhale-666)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Concise text or Markdown with shell commands, status messages, and generated image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save API keys and default model preferences locally, and writes generated PNG files to the configured output directory.]

## Skill Version(s):

0.1.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
