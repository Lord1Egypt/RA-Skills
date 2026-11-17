## Description:

Generates bilingual Chinese and English picture-book story videos with scene images, narration, ASS subtitles, final MP4 files, and Douyin publishing copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to transform a supplied picture-book story script into bilingual narrated videos and accompanying Douyin release text after storyboarding confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Narration text may be sent to Edge TTS when the fallback path is used.

Mitigation: Do not process sensitive scripts through external TTS; prefer the local Qwen3-TTS path where available and disclose or approve external TTS use before generation.

Risk: Host-specific dependency paths and local media tools can fail or behave differently across environments.

Mitigation: Verify ComfyUI, ffmpeg, TTS dependencies, fonts, and character assets in a dedicated project environment before running the pipeline.

Risk: File-handling behavior can overwrite outputs or remove generated scene images in the selected output directory.

Mitigation: Use a fresh project output directory, keep backups of source assets, avoid pointing --output-dir at existing asset folders, and use --keep-temp when intermediate files need review.

Risk: Generated Douyin titles, descriptions, and hashtags may be unsuitable for publication without review.

Mitigation: Review all generated publishing copy and final videos before posting or handing off to a publishing skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vincentlau2046-sudo/skills/picture-book-video)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, video files, audio files]

**Output Format:** [Markdown guidance with shell commands; generated files include MP4, MP3, SRT, ASS, PNG, JSON, and Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese and English video variants, subtitles, narration audio, scene prompts, cover/scene media, and Douyin publishing copy; requires local ComfyUI, TTS, and ffmpeg dependencies.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
