## Description:

Generates a single image from a text prompt through the Hugging Face Inference API using Stable Diffusion XL, then saves the image locally for delivery through the active chat provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slippersheepig](https://clawhub.ai/user/slippersheepig)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images from natural-language prompts with Hugging Face-hosted image models. It is suited to chat workflows where the agent creates a temporary image file, sends it using the active provider's image delivery format, and removes the file after successful delivery unless persistence is requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and the configured Hugging Face token are sent to Hugging Face during generation.

Mitigation: Use a low-privilege HUGGINGFACE_TOKEN and avoid prompts containing sensitive or confidential information.

Risk: Generated images are saved to local storage before delivery.

Mitigation: Use a private temporary output directory for normal chat delivery and delete generated files after successful send unless the user explicitly requested a saved copy.

Risk: Image delivery can fail if the agent assumes a universal local-file send format across chat providers.

Mitigation: Use the active provider's required outbound image or file-send format and only report success after the image has actually been delivered.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slippersheepig/skills/hf-sdxl-image)
- [Hugging Face Inference API model endpoint](https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands; the generation script prints a local image file path to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HUGGINGFACE_TOKEN, accepts optional HF_IMAGE_MODEL override, writes an image file to the requested output path, and expects temporary files to be deleted after successful delivery unless the user asks to keep them.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
