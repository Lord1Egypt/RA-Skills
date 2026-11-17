## Description:

JL Video Downloader helps agents download videos and extract transcripts from Douyin, Kuaishou, Xiaohongshu, Bilibili, YouTube, and other yt-dlp-supported platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyzxs](https://clawhub.ai/user/pyzxs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to gather video metadata, download media, extract speech-to-text copy, and batch process video URLs from supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper script constructs and evaluates shell commands for user-supplied URLs and options.

Mitigation: Remove eval and pass command arguments as an array so URLs and options are not reinterpreted by the shell.

Risk: The setup flow installs external tooling and packages without pinned, verified artifacts.

Mitigation: Pin package versions, verify downloaded installers or packages, and replace curl-pipe-to-shell installation with a reviewable installation step.

Risk: The skill handles API keys, cookies, downloaded media, transcripts, and persistent shell startup configuration.

Mitigation: Make shell startup changes opt-in and document how API keys, cookies, media files, transcripts, logs, cache, and temporary files are stored and protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pyzxs/skills/jl-video-downloader)
- [Publisher profile](https://clawhub.ai/user/pyzxs)
- [Skill documentation](artifact/SKILL.md)
- [Script usage guide](artifact/scripts/README.md)
- [SILI_FLOW API](https://siliflow.com)
- [DeepSeek Platform](https://platform.deepseek.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples and generated media or transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require ffmpeg, uv or uvx, network access, optional proxy configuration, API keys for transcript extraction, and user-supplied video URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
