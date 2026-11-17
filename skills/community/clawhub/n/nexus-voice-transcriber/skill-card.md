## Description:

Voice note transcription and archival for OpenClaw agents, powered by Deepgram Nova-3 or local Whisper, with saved audio and text transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthew00ita](https://clawhub.ai/user/matthew00ita)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to transcribe voice notes, audio files, or video audio into local transcript artifacts, with optional speaker diarization through Deepgram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio can be uploaded to Deepgram when the cloud provider is selected.

Mitigation: Use local Whisper for sensitive audio and require explicit user confirmation before selecting Deepgram.

Risk: The skill can fetch remote URLs supplied as transcription inputs.

Mitigation: Avoid untrusted URLs and prefer local files from known sources.

Risk: Transcript and optional audio archives are written under the user's home directory.

Mitigation: Review output paths and permissions before processing sensitive recordings.

Risk: Split-file cleanup may remove chunk_* files in the processing directory.

Mitigation: Run split transcription in a dedicated temporary or empty working directory.

Risk: Unpinned transcription dependencies can change behavior over time.

Mitigation: Install dependencies in a virtual environment with pinned versions where possible.

## Reference(s):

- [NEXUS Voice Transcriber Skill Page](https://clawhub.ai/matthew00ita/skills/nexus-voice-transcriber)
- [Whisper Models Guide](artifact/references/whisper-models.md)
- [Troubleshooting Guide](artifact/references/troubleshooting.md)
- [Deepgram Documentation](https://developers.deepgram.com/docs)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text guidance with shell commands; generated transcript files may be TXT, SRT, VTT, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save transcript and optional source-audio archives under ~/voice-transcriber/.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.lock.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
