## Description:

High-quality Chinese TTS using GPT-SoVITS v2 Pro+ to convert text to natural-sounding speech with voice cloning support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huizong-cpu](https://clawhub.ai/user/huizong-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to synthesize Chinese voice responses, narration, and IVR-style audio from text through a local GPT-SoVITS API server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured GPT-SoVITS endpoint receives the input text, and reference voice recordings can be sensitive biometric data.

Mitigation: Use a trusted local endpoint, protect reference recordings, and synthesize only voices the operator has permission to clone.

Risk: The security evidence reports that an untrusted output path can be abused to run local shell commands.

Mitigation: Restrict callers and output paths to a dedicated directory, and replace shell command execution with execFileSync or spawnSync argument arrays before broad use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huizong-cpu/skills/gptsovits-tts)

## Skill Output:

**Output Type(s):** [text, files]

**Output Format:** [MP3 audio file with the generated output path returned as a string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converts generated WAV audio to 128 kbps, 44100 Hz, mono MP3 output when ffmpeg succeeds.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
