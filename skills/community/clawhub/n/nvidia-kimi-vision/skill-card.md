## Description: <br>
Analyze images using NVIDIA Kimi K2.5 vision model via NVIDIA NIM API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miladnoo](https://clawhub.ai/user/miladnoo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to add image analysis to workflows by sending a selected image and prompt to NVIDIA's hosted Kimi K2.5 vision model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and prompts are sent to NVIDIA's hosted API for processing. <br>
Mitigation: Use the skill only with images and prompts that are acceptable for external processing; avoid confidential documents, private screenshots, and personal data unless that processing is approved. <br>
Risk: The skill requires an NVIDIA API key, and the artifact allows passing a key directly as a command argument. <br>
Mitigation: Store the API key in a protected local configuration file when possible and avoid exposing it in shell history, process lists, or shared logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/miladnoo/nvidia-kimi-vision) <br>
- [NVIDIA Build](https://build.nvidia.com) <br>
- [NVIDIA NIM chat completions endpoint](https://integrate.api.nvidia.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Plain text with optional setup instructions and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API responses are printed to stdout; max response tokens are configured as 2048 in the artifact script.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
