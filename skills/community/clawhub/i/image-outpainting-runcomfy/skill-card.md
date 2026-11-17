## Description:

Helps agents extend still images beyond the original canvas by selecting RunComfy image-editing routes for outpainting, uncropping, aspect-ratio changes, reference-style matching, and brand-specific edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and creative operators use this skill to have an agent choose a RunComfy outpainting route and produce prompts or CLI invocations for extending image canvas, uncropping images, changing aspect ratio, and matching reference style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RunComfy CLI installation can introduce supply-chain risk if an unreviewed or unpinned package is installed.

Mitigation: Prefer a reviewed pinned version of @runcomfy/cli, install through a trusted package manager, and avoid running npm with administrator privileges.

Risk: Prompts and image URLs used for outpainting are sent to RunComfy services.

Mitigation: Provide RUNCOMFY_TOKEN only when RunComfy access is intended and avoid submitting sensitive prompts or image URLs unless that data sharing is acceptable.

Risk: Outpainted images can contain mismatched lighting, seams, or generated content that diverges from the user's prompt.

Mitigation: Review generated outputs before use and switch to reference-guided editing or a dedicated ComfyUI outpainting workflow when simple prompt-shaped outpainting is insufficient.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/permew/skills/image-outpainting-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI Documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-outpainting-runcomfy)
- [Best Image Editing Models](https://www.runcomfy.com/models/collections/best-image-editing-models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-outpainting-runcomfy)
- [Nano Banana 2 Edit Model](https://www.runcomfy.com/models/google/nano-banana-2/edit?utm_source=clawhub&utm_medium=skill&utm_campaign=image-outpainting-runcomfy)
- [RunComfy ComfyUI Workflows](https://www.runcomfy.com/comfyui-workflows?utm_source=clawhub&utm_medium=skill&utm_campaign=image-outpainting-runcomfy)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference RunComfy model endpoints, prompt patterns, image URLs supplied by the user, and output directory choices.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
