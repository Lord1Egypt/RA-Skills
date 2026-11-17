## Description:

Downloads Xiaoyuzhou podcast audio and show notes, with guidance for converting downloaded audio to MP3 and saving structured episode files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to download Xiaoyuzhou podcast episodes, save show notes, and prepare MP3 files for offline playback on compatible devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's metadata and shell workflow are loosely scoped for automatic use.

Mitigation: Review before installing and use it only for explicit Xiaoyuzhou podcast download requests.

Risk: The skill may attempt to run ./scripts/download.sh.

Mitigation: Confirm the intended script is present and trusted before allowing execution.

Risk: Podcast downloads may be written to an unintended location or original audio may be deleted.

Mitigation: Confirm PODCAST_DIR before downloading and set KEEP_M4A=true when original audio files should be preserved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/podcast-downloader-paid)
- [Xiaoyuzhou episode URL example](https://www.xiaoyuzhoufm.com/episode/abc123def456ghi789jklmno)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and file output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded MP3 audio files and Markdown show notes when the referenced downloader script is present and trusted.]

## Skill Version(s):

1.0.1 (source: target metadata, release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
