## Description:

Extract, normalize, mix, and process audio tracks - audio manipulation and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media engineers use this skill as an FFmpeg command reference for extracting, normalizing, mixing, converting, delaying, filtering, and analyzing audio tracks in local media files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FFmpeg examples write local media outputs and may overwrite files when users choose existing output paths.

Mitigation: Use copies for important media and choose output filenames carefully before running commands.

Risk: Command examples may need adjustment for the user's input streams, codecs, channels, and loudness targets.

Mitigation: Review the selected streams and parameters before execution, and inspect results with ffprobe or FFmpeg analysis commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/multilingual-video-dubbing-ffmpeg-audio-processing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FFmpeg and ffprobe command examples that users adapt to local media files.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
