## Description:

将本地视频或音频文件转写为 SRT 字幕文件和 TXT 纯文本文件.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chentx1243](https://clawhub.ai/user/chentx1243)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe selected local video or audio files into timestamped SRT subtitles and plain TXT text for captioning, media review, and video understanding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses unpinned Python dependency ranges, so installation may fetch newer package versions than originally tested.

Mitigation: Install in a controlled environment and review dependency resolution before deployment.

Risk: The first run may download Whisper model files and create a local model cache.

Mitigation: Run only where model downloads and local cache storage are acceptable.

Risk: The script writes SRT and TXT files to user-selected output paths.

Mitigation: Review input and output paths before execution and run it only on media files intentionally selected for transcription.

## Reference(s):

- [ClawHub skill release: maple-video2txt](https://clawhub.ai/chentx1243/skills/maple-video2txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime output is SRT and TXT files plus progress logs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes SRT/TXT files to the selected output path, uses local media input, and may create a model cache directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
