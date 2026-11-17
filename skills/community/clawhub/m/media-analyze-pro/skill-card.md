## Description:

Analyzes local audio and video files to extract media metadata, audio details, video frame information, cover images, and waveform visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media operations teams use this skill to inspect local audio and video assets, extract structured metadata, generate frame or cover images, create waveform previews, and batch analyze media folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Frame, cover, and waveform commands may silently overwrite existing output files.

Mitigation: Use explicit output paths in a scratch directory and check whether the target file already exists before running write-producing commands.

Risk: The tool reads local files or directories selected by the user.

Mitigation: Run it only on intended media paths and avoid pointing batch analysis at directories that contain unrelated or sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxliuyu/skills/media-analyze-pro)
- [Publisher profile](https://clawhub.ai/user/sxliuyu)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [JSON metadata, command-line status text, and generated image files for frames, covers, or waveforms]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg and ffprobe. Frame, cover, and waveform commands write to default or user-specified output paths.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
