## Description:

Set up mlx-whisper as the local audio transcription engine for OpenClaw on Apple Silicon Macs, automatically transcribing Telegram or WhatsApp voice notes locally before the agent processes them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinghaojia](https://clawhub.ai/user/yinghaojia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure local speech-to-text for OpenClaw voice messages on Apple Silicon Macs without requiring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically process private Telegram or WhatsApp voice notes and pass transcripts into the agent.

Mitigation: Confirm that users accept local media download and transcription before enabling the integration, and review where OpenClaw stores downloaded media and transcripts.

Risk: The setup depends on installing mlx-whisper and downloading a model before local inference can run.

Mitigation: Use an isolated, pinned installation where practical and verify the package and model download path before operational use.

Risk: The artifact references a wrapper script that is not present among the provided files.

Mitigation: Verify the wrapper script contents and executable path before configuring OpenClaw to invoke it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinghaojia/skills/jimmy-claw-mlx-whisper)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets macOS on Apple Silicon, requires python3 and pip3, downloads an initial local model, and runs transcription locally after setup.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
