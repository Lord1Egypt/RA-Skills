## Description:

Generates images from English or Chinese text prompts locally on Windows using Z-Image-Turbo with Intel OpenVINO, preferring Intel iGPU and falling back to CPU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juan-oy](https://clawhub.ai/user/juan-oy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Windows users use this skill to set up local OpenVINO image generation and create PNG images from text prompts without a cloud API after setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad automatic setup authority, including silent prerequisite installation and host modifications.

Mitigation: Review setup actions before first use, prefer manually installing Python and Git, and run setup in a contained user environment.

Risk: Setup depends on external package and model downloads, including pinned Git dependencies and an approximately 10 GB ModelScope model.

Mitigation: Verify installer and model sources, review or lock dependencies, and allow the download only on networks where these sources are trusted.

Risk: The skill creates persistent local files for its virtual environment, model files, state, generated script, and image outputs.

Mitigation: Confirm available disk space and review the generated output directory before using it on a primary or managed machine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juan-oy/skills/local-image-gen-aipc)
- [ModelScope Z-Image-Turbo INT4 model files](https://modelscope.cn/models/snake7gun/Z-Image-Turbo-int4-ov/files)
- [Pinned Optimum Intel dependency](https://github.com/openvino-dev-samples/optimum-intel.git@2f62e5aee74b4acba3836e1f26678c0db0a09c00)
- [Pinned Diffusers dependency](https://github.com/huggingface/diffusers.git@a1f36ee3ef4ae1bf98bd260e539197259aa981c1)
- [Artifact requirements](artifact/requirements_imagegen.txt)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with PowerShell commands and PNG image file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a required text prompt plus optional steps, size, seed, and output path; setup downloads dependencies and an approximately 10 GB model, then inference runs offline.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md SKILL_VERSION v1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
