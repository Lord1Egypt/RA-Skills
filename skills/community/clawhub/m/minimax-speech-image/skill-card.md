## Description:

Connects an agent to MiniMax Token Plan APIs for text-to-speech, asynchronous speech tasks, voice cloning, voice design, voice management, text-to-image generation, and image-to-image editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[percivalee](https://clawhub.ai/user/percivalee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate speech and images through MiniMax using a configured API key. It supports TTS, voice cloning and design, voice listing/deletion, text-to-image generation, and image-based editing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, audio samples, local images, and generated media requests may be sent to MiniMax using the user's API key.

Mitigation: Use only approved inputs, avoid sensitive local media, and confirm that the workflow is allowed to transmit data to MiniMax before execution.

Risk: Voice cloning can create or store a cloned voice from an uploaded audio sample.

Mitigation: Use voice cloning only with rights and consent for the source voice sample.

Risk: Voice deletion is treated as irreversible and the command has no confirmation prompt.

Mitigation: Confirm the target voice ID outside the skill before running the delete command.

Risk: The image downloader accepts unrestricted URLs and should not be used as-is in untrusted workflows.

Mitigation: Restrict download sources or add URL validation before use with untrusted inputs.

## Reference(s):

- [MiniMax API endpoint (China)](https://api.minimaxi.com/v1)
- [MiniMax API endpoint (International)](https://api.minimax.io/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, Python examples, JSON task responses, and generated audio or image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and can use MINIMAX_REGION to select the China or international API endpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
