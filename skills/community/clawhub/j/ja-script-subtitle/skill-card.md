## Description:

Aligns Japanese audio with a supplied script to create Japanese, Chinese, and bilingual subtitles, with optional Chinese-subtitled video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiwei12333-bit](https://clawhub.ai/user/shiwei12333-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and subtitle editors use this skill to align Japanese scripts with audio, translate lines, and prepare Japanese, Chinese, or bilingual SRT subtitles; they can optionally burn Chinese subtitles into a vertical video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup installs Python packages and downloads a Whisper model, and rendering runs ffmpeg.

Mitigation: Review the installation and media-processing steps before running them in your environment.

Risk: The optional WorkBuddy helper downloads files by node ID.

Mitigation: Provide only node IDs and files you are authorized to access.

Risk: Audio-to-script mismatches or misnumbered translations can produce inaccurate subtitle timing or text.

Mitigation: Check alignment coverage, subtitle timings, and translation numbering before delivery.

## Reference(s):

- [ja-script-subtitle ClawHub release](https://clawhub.ai/shiwei12333-bit/skills/ja-script-subtitle)

## Skill Output:

**Output Type(s):** [Text, Subtitle files, Video files]

**Output Format:** [Japanese, Chinese, and bilingual SRT subtitles; optional MP4 video and text quality summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese translations require line-numbered input; video rendering is optional.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
