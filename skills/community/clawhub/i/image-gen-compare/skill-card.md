## Description:

Side-by-side comparison of paid vs local image generation models, including DALL-E 3, FLUX.1-schnell, Gemini Imagen, and others, that generates images from the same prompt, logs metadata, and stores run history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to compare cloud and local image generation models on the same prompt, including cost, latency, image files, and run history. It supports model-selection decisions for projects that need production-quality imagery, local experimentation, or offline generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated images may be sent to OpenAI for paid cloud generation.

Mitigation: Use the skill only with prompts and outputs that are appropriate to send to OpenAI, or select local model paths for work that should remain on-device.

Risk: Generated images may be saved to a Proton Drive-synced folder when that local path is present.

Mitigation: Inspect or change the output directory before using confidential creative work.

Risk: The skill can use a 1Password service-token fallback to retrieve the OpenAI API key.

Mitigation: Prefer setting OPENAI_API_KEY directly and run the skill in an environment without unrelated secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/image-gen-compare)
- [Publisher profile](https://clawhub.ai/user/nissan)
- [OpenAI image generation API endpoint](https://api.openai.com/v1/images/generations)

## Skill Output:

**Output Type(s):** [text, shell commands, files, code, configuration]

**Output Format:** [CLI text output, generated image files, and JSON run metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and OPENAI_API_KEY for OpenAI image generation; may use OP_SERVICE_ACCOUNT_TOKEN for 1Password credential retrieval.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
