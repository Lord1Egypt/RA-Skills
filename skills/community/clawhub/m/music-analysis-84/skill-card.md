## Description:

Analyze music/audio files locally without external APIs, producing tempo, groove, structure, harmonic, timbre, temporal mood, instrument, and lyric-aware emotional reads from audio files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dahuangfortoby](https://clawhub.ai/user/dahuangfortoby)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, producers, reviewers, and external users can use this skill to inspect local audio files, compare mixes, audit structure and feel, and generate producer-facing music analysis notes. It is intended for local files or user-supplied audio sources and can emit either human-readable reports or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer makes persistent shell-profile changes.

Mitigation: Review setup.sh before installation and remove or make opt-in the ~/.zshrc alias modification.

Risk: The installer downloads and installs dependencies without strong integrity controls.

Mitigation: Pin dependencies and verify the Whisper model checksum before use.

Risk: The installer uses a hard-coded local skill path.

Mitigation: Fix the install path for the target environment before running setup.sh.

Risk: Running setup with elevated privileges could make unintended persistent changes.

Mitigation: Run setup as a normal user after review, not as an elevated user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dahuangfortoby/skills/music-analysis-84)
- [ClawHub publisher profile](https://clawhub.ai/user/dahuangfortoby)
- [Whisper large-v3-turbo model download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable text or structured JSON reports, optionally written to an output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local audio file and local audio tooling such as ffmpeg, ffprobe, librosa, numpy, and optional whisper-cli for lyric transcription.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
