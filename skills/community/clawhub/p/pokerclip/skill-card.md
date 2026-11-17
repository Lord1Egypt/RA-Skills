## Description:

Automatically cuts poker tournament videos into complete hand clips in vertical 9:16 format with subtitles and unique hooks for TikTok and YouTube Shorts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicolenovan](https://clawhub.ai/user/nicolenovan)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and agents use this skill to turn long poker videos into short, publish-ready clips by detecting complete hands, selecting highlights, adding subtitles, and overlaying hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated clips, transcripts, subtitles, and JSON reports may overwrite prior files in the workspace output folder.

Mitigation: Run the skill in a dedicated workspace or back up existing clips and JSON artifacts before execution.

Risk: Automatic transcription and subtitle generation may misrepresent speech from untrusted or noisy media.

Mitigation: Review generated transcripts, subtitles, hooks, and publish reports before sharing clips publicly.

Risk: Unpinned runtime dependencies can change transcription behavior over time.

Mitigation: Use a virtual environment and pin openai-whisper and related media-processing dependencies for repeatable results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nicolenovan/skills/pokerclip)
- [Publisher Profile](https://clawhub.ai/user/nicolenovan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated video, subtitle, transcript, analysis, and publish-report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 1080x1920 H.264/AAC clips, ASS subtitles, hook overlays, transcript JSON, clips_analysis.json, and publish_report.json in the configured workspace.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
