## Description:

Local AI image generation using OllamaDiffuser for generating, editing, inpainting, and controlling images with FLUX, Stable Diffusion, or GGUF quantized models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1tsnakers](https://clawhub.ai/user/1tsnakers)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run local image generation workflows through OllamaDiffuser, including text-to-image, image-to-image, inpainting, ControlNet guidance, model management, and hardware-aware setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation for local image generation can introduce unreviewed packages or unreproducible environments.

Mitigation: Install in a dedicated virtual environment, avoid running pip as root or administrator, and pin package versions for reproducible reviewed installs.

Risk: Hugging Face tokens used for gated models can be exposed if stored persistently without care.

Mitigation: Avoid storing HF_TOKEN permanently unless the exposure risk is understood and acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1tsnakers/skills/ollamadiffuser)
- [Publisher profile](https://clawhub.ai/user/1tsnakers)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands, API endpoint guidance, and parameter notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local REST API endpoints, CLI commands, model names, image inputs, masks, control images, and HF_TOKEN for gated model access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
