## Description:

Local text-to-speech (TTS) and speech-to-text (STT) using FluidAudio on Apple Silicon, with on-device synthesis and transcription for local voice capabilities, voice assistant integration, and cloud TTS/STT replacement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trondw](https://clawhub.ai/user/trondw)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up local voice capabilities on Apple Silicon Macs, including on-device speech synthesis, transcription, and voice assistant integration without relying on cloud TTS or STT services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs a local voice daemon that starts at login and stays alive in the user's session.

Mitigation: Review the LaunchAgent behavior before installation, decide whether persistence is desired, and keep unload and removal steps for the plist and installed binary.

Risk: Swift dependencies are pulled during build and may change within allowed package ranges.

Mitigation: Pin or review Swift dependencies before deployment.

## Reference(s):

- [Kokoro Voice Reference](references/VOICES.md)
- [FluidAudio Swift package dependency](https://github.com/FluidInference/FluidAudio.git)
- [Hummingbird Swift package dependency](https://github.com/hummingbird-project/hummingbird.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API examples, Swift code references, and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local setup steps, LaunchAgent configuration, HTTP endpoint examples, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
