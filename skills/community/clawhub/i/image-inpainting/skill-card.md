## Description:

Mask-driven image inpainting on RunComfy via the runcomfy CLI, routing to Z-Image Turbo Inpainting for masked region edits and to instruction-driven image edit models when no mask is available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-production teams use this skill to guide an agent through local image edits such as object removal, region replacement, blemish cleanup, and masked fill workflows using RunComfy model endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports watermark or attribution removal.

Mitigation: Use the skill only for images the user has rights to edit, and avoid removing watermarks, attribution, or other ownership marks.

Risk: The workflow depends on a third-party CLI with account access.

Mitigation: Prefer a pinned, locally installed RunComfy CLI version and use a narrowly scoped token where possible.

Risk: Uploaded images, masks, prompts, and generated outputs are handled by RunComfy.

Mitigation: Do not send sensitive or unauthorized media, and treat all inputs and generated outputs as data shared with RunComfy.

Risk: Mask-driven edits can modify the wrong area if the mask does not match the user's intent.

Mitigation: Confirm that the mask corresponds to the current source image and the exact region the user asked to replace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/permew/skills/image-inpainting)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI Documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-inpainting)
- [Z-Image Turbo Inpainting](https://www.runcomfy.com/models/tongyi-mai/z-image/turbo/inpainting?utm_source=clawhub&utm_medium=skill&utm_campaign=image-inpainting)
- [Z-Image Turbo Inpainting LoRA](https://www.runcomfy.com/models/tongyi-mai/z-image/turbo/inpainting/lora?utm_source=clawhub&utm_medium=skill&utm_campaign=image-inpainting)
- [Best Image Editing Models Collection](https://www.runcomfy.com/models/collections/best-image-editing-models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-inpainting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON input snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the runcomfy CLI, RUNCOMFY_TOKEN, and RunComfy configuration; generated image files are written by the CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
