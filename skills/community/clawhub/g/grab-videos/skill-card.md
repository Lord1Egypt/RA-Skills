## Description:

Download videos with yt-dlp and extract frames, thumbnails, clips, or converted outputs with ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qidu](https://clawhub.ai/user/qidu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-processing users use this skill to ask an agent for yt-dlp and ffmpeg commands that download supported online videos, extract frames, batch thumbnails, check duration, and organize media outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media downloads and frame extraction can create large local output files or overwrite existing files during batch operations.

Mitigation: Use a dedicated working folder, review matched files before batch commands, and remove forced overwrite flags unless replacement is intentional.

Risk: The skill can suggest downloading media from online services where site support, rate limits, or rights restrictions may apply.

Mitigation: Use yt-dlp only with supported sources and content the user is authorized to download.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qidu/skills/grab-videos)
- [yt-dlp releases](https://github.com/yt-dlp/yt-dlp/releases)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local video, image, thumbnail, and clip files when the suggested commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
