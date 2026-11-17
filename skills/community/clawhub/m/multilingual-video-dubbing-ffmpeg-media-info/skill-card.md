## Description:

Analyze media file properties - duration, resolution, bitrate, codecs, and stream information

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media engineers use this skill to inspect video and audio file metadata with FFmpeg and ffprobe, including duration, stream layout, resolution, bitrate, codecs, frame rate, sample rate, and channel counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media metadata can reveal technical details about private files when commands are run on user-selected media.

Mitigation: Run the commands only on files intended for inspection and avoid sharing terminal output from private media unless the metadata has been reviewed.

Risk: The skill proposes local FFmpeg and ffprobe shell commands that depend on the user's installed binaries and file paths.

Mitigation: Review the command and substitute the intended local file path before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lnj22/skills/multilingual-video-dubbing-ffmpeg-media-info)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and ffprobe JSON command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated commands inspect user-selected local media files and may print media metadata to the terminal.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
