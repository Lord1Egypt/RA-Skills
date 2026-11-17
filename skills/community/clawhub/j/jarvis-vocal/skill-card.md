## Description:

Authentic J.A.R.V.I.S. voice synthesis using Piper TTS with a HuggingFace-trained model, with optional delivery to connected Android devices through OpenClaw nodes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kishen35](https://clawhub.ai/user/kishen35)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to synthesize J.A.R.V.I.S.-style speech locally with Piper TTS and optionally send generated audio to a paired Android device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external TTS tooling and downloaded model files without pinned checksums in the release evidence.

Mitigation: Install external tooling only from trusted sources and pin or verify downloaded model artifacts before operational use.

Risk: Synthesized audio may be pushed or streamed to a connected Android device.

Mitigation: Avoid synthesizing sensitive text and confirm the intended ADB target before sending audio.

Risk: The artifact describes jarvis-tts and jarvis-speak wrapper behavior, but the release artifact does not include those wrapper scripts.

Mitigation: Review or create the wrapper scripts before relying on device playback workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kishen35/skills/jarvis-vocal)
- [jgkawell/jarvis Hugging Face model](https://huggingface.co/jgkawell/jarvis)
- [jgkawell/jarvis discussions](https://huggingface.co/jgkawell/jarvis/discussions)
- [Piper TTS](https://github.com/rhasspy/piper)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of local WAV audio files or playback on a connected Android device when commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
