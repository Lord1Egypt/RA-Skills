## Description: <br>
Generate high-resolution PNG images from detailed text prompts using the NVIDIA Stable Diffusion XL model with customizable style, lighting, and resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoxiasan](https://clawhub.ai/user/zhaoxiasan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create local image assets from detailed text prompts through NVIDIA's Stable Diffusion XL API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an embedded NVIDIA API credential and sends prompts to NVIDIA under that credential. <br>
Mitigation: Remove and rotate the embedded credential before use, and require users to supply their own credential through a secret or environment variable. <br>
Risk: Prompts are sent to an external image generation API and generated files persist locally. <br>
Mitigation: Do not submit confidential, personal, or proprietary information in prompts, and review local generated files before sharing or retaining them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoxiasan/nvidia-sdxl) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, API calls] <br>
**Output Format:** [Plain text status message with an absolute local PNG file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a PNG image file in the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
