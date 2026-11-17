## Description:

Convert, compress, merge, split, clip, inspect, and extract audio locally with FFmpeg, plus decode supported music-cache formats including pure-Python Ximalaya .xm and optional Kugou/local helper formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luis1213899](https://clawhub.ai/user/luis1213899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to process local audio and video files, including conversion, compression, merging, splitting, clipping, metadata inspection, and supported cache-format decoding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The split cleanup option can recursively delete a writable output directory selected by an agent.

Mitigation: Avoid `split --clean` unless the output directory is a safe generated directory or the user has clearly confirmed cleanup.

Risk: FFmpeg, Kugou, and optional decode helper paths can be configured through environment variables.

Mitigation: Use only trusted local binaries for FFmpeg, FFprobe, Kugou, and decode helpers, and review configured paths before autonomous use.

## Reference(s):

- [Core Behavior Reference](references/core-behavior.md)
- [ClawHub skill page](https://clawhub.ai/luis1213899/skills/luis-audio-translator)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; scripts emit JSON status and local media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local-first and may include input or output paths needed for follow-on agent workflows.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
