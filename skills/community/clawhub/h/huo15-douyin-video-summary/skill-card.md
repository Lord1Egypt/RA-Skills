## Description:

This skill helps an agent download a Douyin video without a watermark, extract MP3 audio, route the audio through a separate ASR skill, and produce a transcript-based summary and chapter structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn a Douyin video link into downloadable media, extracted audio, a transcript, and a concise content summary for personal analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader may allow yt-dlp to read local browser cookies from Chrome, Safari, or Firefox without clear per-run consent.

Mitigation: Review before installing; prefer an isolated browser profile, a narrowly scoped cookie file, or a version that requires explicit consent and validates Douyin domains before cookie access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-douyin-video-summary)
- [Project homepage](https://cnb.cool/huo15/ai/huo15-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with bash commands; generated artifacts include video.mp4, audio.mp3, transcript.txt, and summary markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp, ffmpeg, and a separate ASR skill for transcription.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
