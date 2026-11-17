## Description:

Analyze images using NVIDIA Kimi K2.5 vision model via NVIDIA NIM API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miladnoo](https://clawhub.ai/user/miladnoo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to send local PNG, JPG, JPEG, or WebP images with a prompt to NVIDIA NIM for visual description, text extraction, or general image analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and prompts are sent to NVIDIA NIM for analysis, so selected local files may leave the user's environment.

Mitigation: Use only files intentionally approved for upload and avoid confidential screenshots, documents, or regulated data.

Risk: API keys may be exposed if passed directly on the command line or stored with broad file permissions.

Mitigation: Store the key with restrictive permissions or a secret manager, and avoid passing secrets as command-line arguments.

Risk: The script accepts any readable local path supplied by the caller.

Mitigation: Review the path before execution and limit use to known image files intended for analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miladnoo/skills/nvidia-kimi-vision)
- [NVIDIA Build](https://build.nvidia.com)
- [NVIDIA NIM chat completions endpoint](https://integrate.api.nvidia.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses with setup guidance and command-line status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns model-generated image analysis text; the script allows up to 2048 response tokens and exits with error messages for missing keys, missing files, timeouts, or API failures.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
