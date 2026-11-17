## Description:

Downloads or accepts a local foreign-language video, transcribes and translates it to English with WhisperX, and recreates the video with English subtitles using ffmpeg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nelsonscott](https://clawhub.ai/user/nelsonscott)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and end users use this skill to create English-subtitled versions of local or downloaded videos. It is suited for requests to translate or subtitle foreign-language videos with a local WhisperX, yt-dlp, and ffmpeg pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation and media processing can expose the user to untrusted packages, large downloads, or unexpected local file creation.

Mitigation: Install ffmpeg, yt-dlp, and WhisperX from trusted sources, prefer a virtual environment for WhisperX, and review input URLs, disk space, and output directories before running.

Risk: Downloaded or processed media may create legal or operational issues if the user lacks rights or chooses an unsafe destination.

Mitigation: Only subtitle media the user has rights to process and direct outputs to an appropriate working directory.

## Reference(s):

- [Movie Subtitler repository](https://github.com/NelsonScott/movie-subtitler)
- [WhisperX](https://github.com/m-bain/whisperX)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with bash commands; generated media outputs are MP4 video and SRT subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally, downloads URL inputs when requested, and writes outputs to the current or chosen output directory.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
