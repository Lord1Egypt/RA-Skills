## Description: <br>
Local AI image generation using OllamaDiffuser for generating, editing (img2img/inpaint), and controlling (ControlNet) images locally with models like FLUX, Stable Diffusion, or GGUF quantized models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1tsnakers](https://clawhub.ai/user/1tsnakers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to set up and operate local OllamaDiffuser image-generation workflows, including text-to-image, img2img, inpainting, ControlNet guidance, model management, and hardware-aware model selection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Third-party package installation can introduce unreviewed code into the local environment. <br>
Mitigation: Install in a virtual environment and review OllamaDiffuser and related package sources before approving pip installs. <br>
Risk: Gated model access can require a Hugging Face token that may be persisted in shell configuration. <br>
Mitigation: Use a least-privilege token and persist it only when gated models are required. <br>
Risk: Large model downloads and image-generation workloads can consume significant GPU memory and disk space. <br>
Mitigation: Confirm available hardware and storage before pulling models, and use the skill's VRAM-oriented model recommendations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and local API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may reference local files, base64 image inputs, model names, VRAM requirements, and optional Hugging Face token configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
