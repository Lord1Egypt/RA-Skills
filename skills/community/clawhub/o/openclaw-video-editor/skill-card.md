## Description:

Openclaw Video Editor is a local ffmpeg-based video editing skill that provides tested helpers for subtitles, background blur, color grading, two-pass loudness normalization, scene-detected highlight reels, vertical conversion for shorts, clean audio-only extraction, and clip extraction, with no AI segmentation, transcription model, or external network calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers, editors, and creator-workflow agents use this skill to prepare local media assets with ffmpeg workflows such as subtitle formatting, clip extraction, loudness normalization, LUT application, highlight reel generation, vertical conversion, and audio extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local ffmpeg workflows process media files supplied by the user.

Mitigation: Run the skill only on media files you intend to process in an environment where local ffmpeg execution is acceptable.

Risk: Generated outputs may overwrite existing files at user-provided output paths.

Mitigation: Choose explicit output paths and review existing files before running workflows that write media or subtitle outputs.

Risk: Highlight reel generation temporarily stores derived clips in the system temp directory before cleanup.

Mitigation: Use the workflow only when temporary local storage of derived clips is acceptable and ensure sufficient temp-space availability.

## Reference(s):

- [Openclaw Video Editor on ClawHub](https://clawhub.ai/gopendrasharma89-tech/skills/openclaw-video-editor)
- [Publisher profile](https://clawhub.ai/user/gopendrasharma89-tech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides local ffmpeg and Python helper workflows that produce media, subtitle, audio, and clip files at user-provided output paths.]

## Skill Version(s):

6.1.0 (source: SKILL.md body and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
