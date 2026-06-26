## Description: <br>
Generates Markdown articles with aligned text and images from local video files or video URLs by downloading media, transcribing speech, capturing frames, matching frames to subtitle timestamps, and drafting the article. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chentx1243](https://clawhub.ai/user/chentx1243) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content operators use this skill to convert videos into illustrated Markdown articles, blog posts, public-account drafts, summaries, or reports. It is intended for workflows where transcript text and sampled frames need to stay aligned by timeline rather than image interpretation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill mostly does the advertised video-to-article workflow, but its downloader can automatically overwrite or delete files in the chosen output folder. <br>
Mitigation: Review before installing. Use a fresh empty output folder for each download, avoid pointing it at important media directories, expect dependency and Whisper model downloads, and delete generated transcripts, frames, and downloaded videos after processing sensitive content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chentx1243/maple-video-article) <br>
- [Publisher profile](https://clawhub.ai/user/chentx1243) <br>
- [Video downloader instructions](artifact/references/video-downloader使用说明.md) <br>
- [Video frame capture instructions](artifact/references/video-frame-capture使用说明/使用说明.md) <br>
- [Video frame capture supplemental notes](artifact/references/video-frame-capture使用说明/补充说明.md) <br>
- [Video-to-text instructions](artifact/references/video-to-txt使用说明/video2txt使用说明.md) <br>
- [General article format reference](artifact/assets/通用文本格式参考.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown article with image references, plus local transcript, subtitle, frame, and timeline files generated during processing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The final article is saved as a Markdown file near the source video; intermediate outputs may include downloaded videos, .txt transcripts, .srt subtitles, captured frame images, result.json, and a timeline-matched draft file.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
