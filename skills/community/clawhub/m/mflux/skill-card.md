## Description: <br>
Local image generation using Apple MLX via mflux with FLUX.2 Klein and Z-Image Turbo models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjain](https://clawhub.ai/user/pjain) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content-creation agents use this skill to generate, edit, and transform images locally on Apple Silicon Macs using mflux CLI commands and Python examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup process installs an external Python package and may download large model files during installation or first use. <br>
Mitigation: Verify the intended mflux package and model sources before installation, and plan for network access and persistent local model cache storage. <br>
Risk: Image-generation commands write local output files and may use substantial RAM and disk space. <br>
Mitigation: Use the documented output paths, quantization options, and model-size guidance to control storage and memory use on Apple Silicon Macs. <br>


## Reference(s): <br>
- [MFlux Skill for OpenClaw release page](https://clawhub.ai/pjain/mflux) <br>
- [Publisher profile](https://clawhub.ai/user/pjain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, Python snippets, model-selection guidance, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated image files are produced locally by mflux when the agent or user runs the provided commands.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
