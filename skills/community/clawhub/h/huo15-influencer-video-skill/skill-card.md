## Description:

Generates short first-person product marketing videos from a product image and JSON script, with TTS voiceover, optional background music mixing, subtitles, template selection, dry-run checks, and cost estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agents use this skill to prepare short product sales videos from a local product image and script. It supports persona templates, voiceover, background music, subtitles, dry-run validation, and cost-aware rendering before producing the final media file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product images and scripts may be sent to external video and TTS services.

Mitigation: Use non-sensitive inputs, dedicated provider keys, and an isolated environment.

Risk: FFmpeg processing and output paths use loosely validated, overwrite-capable inputs.

Mitigation: Use a controlled output directory and review script JSON paths before execution.

Risk: Full rendering can incur provider costs.

Mitigation: Confirm estimated costs before rendering and use dry-run mode to validate scripts before paid video generation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaobod1/skills/huo15-influencer-video-skill)
- [Volcano Ark API endpoint](https://ark.cn-beijing.volces.com/api/v3)
- [ByteDance OpenSpeech TTS endpoint](https://openspeech.bytedance.com)
- [Pixabay Music](https://pixabay.com/music/)
- [Freesound](https://freesound.org/)
- [Incompetech Royalty-Free Music](https://incompetech.com/music/royalty-free/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON script examples, shell commands, and generated media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create MP4 video, MP3 voice or mixed audio, SRT subtitles, token estimates, and cost estimates; dry-run avoids the paid video generation step.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
