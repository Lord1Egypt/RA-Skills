## Description:

Generates illustrated Markdown articles from local video files or online video URLs by downloading media when needed, transcribing speech, capturing video frames, matching frames to subtitle timing, and drafting the article.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chentx1243](https://clawhub.ai/user/chentx1243)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and external users use this skill to turn video content into image-supported articles, blog posts, summaries, or reports. It is especially suited to workflows that need local transcripts, selected frames, and timeline-aligned Markdown output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader may merge and delete unrelated audio or media files in the selected output folder.

Mitigation: Use a fresh empty output directory for each download and avoid pointing the downloader at directories that contain private, original, or important media.

Risk: The workflow can download remote videos, install media and transcription dependencies, and write large local outputs.

Mitigation: Run it in an isolated Python environment with pinned dependencies, review download sources, and reserve sufficient local storage before processing media.

Risk: The workflow may process private or sensitive media into transcripts, subtitles, frames, and article drafts.

Mitigation: Process only media you are authorized to use and store generated TXT, SRT, image, JSON, and Markdown outputs in locations with appropriate access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chentx1243/skills/maple-video-article)
- [Video downloader usage guide](artifact/references/video-downloader使用说明.md)
- [Video-to-text usage guide](artifact/references/video-to-txt使用说明/video2txt使用说明.md)
- [Video frame capture usage guide](artifact/references/video-frame-capture使用说明/使用说明.md)
- [Video frame capture supplemental notes](artifact/references/video-frame-capture使用说明/补充说明.md)
- [General article format reference](artifact/assets/通用文本格式参考.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown article output with local image references, plus workflow guidance, shell commands, transcripts, subtitles, frame captures, and timeline-mapping files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The primary public artifact is a video-derived Markdown article; intermediate local outputs may include TXT, SRT, JSON, image frames, downloaded media files, and temporary timeline-matching text.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
