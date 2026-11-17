## Description:

Converts QQ Music audio files such as OGG, FLAC, M4A, WAV, AAC, and Opus into MP3 using ffmpeg, with support for single-file and recursive directory conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT

## Use Case:

Developers and end users use this skill to convert supported local QQ Music downloads or other common audio files into broadly compatible MP3 files. It is intended for local audio conversion workflows that need ffmpeg checks, batch processing, VBR settings, and conversion summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local conversion commands can write MP3 files and direct ffmpeg examples using -y can overwrite an existing destination.

Mitigation: Review input and output paths before execution, keep source files by default, and avoid using -y unless overwriting is intended.

Risk: Documentation may overstate metadata preservation and encoding automation for all source files.

Mitigation: Test on a representative file and inspect the resulting MP3 metadata before running a large batch.

Risk: Encrypted QQ Music formats are not converted by this skill.

Mitigation: Use only supported unencrypted audio formats, or decrypt encrypted files with an appropriate separate tool before conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-qq-mp3)
- [Publisher profile](https://clawhub.ai/user/zhaobod1)
- [ffmpeg downloads](https://ffmpeg.org/download.html)
- [qmc-decoder](https://github.com/Presburger/qmc-decoder)
- [Unlock Music](https://git.unlock-music.dev/um/web)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and conversion summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local input and output paths, ffmpeg availability, quality settings, and success, failure, or skipped-file counts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
