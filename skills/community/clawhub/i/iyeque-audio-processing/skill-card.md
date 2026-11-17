## Description:

Privacy-first local audio toolkit for OpenClaw: transcribe voice notes, create timestamped segments, extract features, detect speech, and run deterministic FFmpeg transforms. Use remote TTS only when explicitly requested and network consent is provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyeque](https://clawhub.ai/user/iyeque)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users process workspace audio locally for transcription, speech segmentation, feature extraction, and FFmpeg transformations; they may generate speech through an explicitly authorized remote TTS option.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote text-to-speech sends supplied text to Google when network access is explicitly enabled.

Mitigation: Confirm consent before using --allow-network; never submit secrets or confidential transcripts.

Risk: Local transcription may download model files or dependencies during setup or first use.

Mitigation: Plan for initial downloads and review dependencies before processing sensitive audio.

## Reference(s):

- [Audio Processing on ClawHub](https://clawhub.ai/iyeque/skills/iyeque-audio-processing)
- [Source link listed in skill documentation](https://github.com/iyeque/openclaw-skills/tree/main/skills/audio-processing)

## Skill Output:

**Output Type(s):** [Text, Audio files]

**Output Format:** [JSON responses, with MP3 or WAV files for audio-producing actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcripts include timestamped segments; audio outputs remain in the workspace.]

## Skill Version(s):

1.3.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
