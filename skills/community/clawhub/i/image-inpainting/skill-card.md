## Description: <br>
Mask-driven image inpainting on RunComfy via the runcomfy CLI for object removal, watermark removal, region replacement, blemish cleanup, and controlled local edits where a binary mask defines the target area. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route still-image inpainting requests through RunComfy, choosing a mask-driven Z-Image endpoint when a mask is available and description-based edit models when the region must be specified in prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends images and masks to RunComfy for processing, which can expose private visual content to an external service. <br>
Mitigation: Use only images and masks the user intends to process with RunComfy, avoid sensitive inputs where possible, and use a dedicated or revocable RunComfy token. <br>
Risk: Broad object or watermark removal requests can modify content in unintended or inappropriate ways. <br>
Mitigation: Confirm the user's intent and the masked region before execution, especially for object or watermark removal. <br>
Risk: Using an untrusted CLI installation path or long-lived token increases account and environment exposure. <br>
Mitigation: Install the RunComfy CLI only through the documented package manager flow and prefer scoped, revocable credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/image-inpainting) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=image-inpainting) <br>
- [Z-Image Turbo Inpainting](https://www.runcomfy.com/models/tongyi-mai/z-image/turbo/inpainting?utm_source=clawhub&utm_medium=skill&utm_campaign=image-inpainting) <br>
- [Z-Image Turbo Inpainting LoRA](https://www.runcomfy.com/models/tongyi-mai/z-image/turbo/inpainting/lora?utm_source=clawhub&utm_medium=skill&utm_campaign=image-inpainting) <br>
- [RunComfy image editing models collection](https://www.runcomfy.com/models/collections/best-image-editing-models?utm_source=clawhub&utm_medium=skill&utm_campaign=image-inpainting) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the runcomfy CLI, a RunComfy account token, and user-provided image and mask URLs for mask-driven workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
