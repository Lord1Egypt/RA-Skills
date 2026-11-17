## Description:

Generate high-resolution PNG images from detailed text prompts using the NVIDIA Stable Diffusion XL model with customizable style, lighting, and resolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxiasan](https://clawhub.ai/user/zhaoxiasan)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill to generate local PNG image assets from detailed prompts, optional negative prompts, and resolution settings via NVIDIA Stable Diffusion XL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a hardcoded NVIDIA API credential.

Mitigation: Remove and revoke the bundled credential before use, then configure a user-provided secret through the runtime environment or another secret-management mechanism.

Risk: Prompt text is sent to the NVIDIA image-generation service.

Mitigation: Avoid submitting sensitive, confidential, or proprietary prompts unless that data sharing is acceptable for the intended deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxiasan/skills/nvidia-sdxl)
- [Publisher profile](https://clawhub.ai/user/zhaoxiasan)
- [NVIDIA Stable Diffusion XL API endpoint](https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl-base)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [Plain text status message with an absolute local path to a generated PNG file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a PNG image to the OpenClaw workspace. Width and height default to 1024 and may be set to 1024, 768, or 512.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
