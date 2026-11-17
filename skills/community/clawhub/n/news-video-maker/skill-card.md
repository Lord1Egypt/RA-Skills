## Description:

News video maker skill. Use search tools to get news, generate speech, and create video with golden subtitles. For creating news briefing videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[izorro](https://clawhub.ai/user/izorro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn current-news topics into short briefing videos with voiceover, subtitles, and a provided background image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FFmpeg command construction can expose users to unsafe local command execution if file paths are not tightly controlled.

Mitigation: Use trusted local file paths and output directories, and run FFmpeg with a fixed argument array plus strict path and subtitle-filter escaping.

Risk: The workflow searches the web and sends generated news text to a TTS tool.

Mitigation: Review the selected news content before narration and use only TTS providers appropriate for the data being processed.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [MP4 video file plus Markdown-style instructions and an FFmpeg command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses web search, TTS-generated audio, SRT-style subtitles, a user-provided background image, and FFmpeg.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
