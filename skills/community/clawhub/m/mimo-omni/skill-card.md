## Description:

mimo-omni helps agents analyze images, videos, and audio through Xiaomi MiMo multimodal models for image description, OCR, object detection, scene understanding, video analysis, transcription, and audio understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xcchenx345](https://clawhub.ai/user/xcchenx345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route user-supplied image, video, and audio files or URLs to Xiaomi MiMo for multimodal understanding tasks such as description, OCR, object detection, video interpretation, transcription, and audio analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, videos, audio, prompts, and the Xiaomi API key are sent to a remote Xiaomi MiMo service.

Mitigation: Use the skill only with media and prompts approved for that service, and avoid sensitive or regulated content unless explicitly authorized.

Risk: The endpoint can be overridden with MIMO_API_ENDPOINT, which could redirect requests and credentials to an untrusted destination.

Mitigation: Leave the default endpoint in place unless the replacement endpoint has been reviewed and trusted.

Risk: Credential handling relies on environment variables or the local OpenClaw configuration.

Mitigation: Store the Xiaomi API key in controlled local configuration or environment management, and review access before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xcchenx345/skills/mimo-omni)
- [ClawHub publisher profile](https://clawhub.ai/user/xcchenx345)
- [Xiaomi MiMo API endpoint](https://api.xiaomimimo.com/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Plain text model responses with command-line examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The Python and Bash helpers accept image, multi-image, video, audio, and mixed video/audio inputs; stdout is intended to be returned to the user, while stderr carries timing and token diagnostics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
