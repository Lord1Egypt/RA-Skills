## Description:

AI视频创作 skill for text-to-video and image-to-video generation through the Juhe video API, with configurable resolution, duration, aspect ratio for text prompts, job polling, and optional MP4 download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate short videos from text prompts or animate an image into a video, then retrieve an online video link or a local MP4 file. It is suited for creative video drafts, social clips, product visuals, and other prompt-driven video generation workflows that can use the Juhe service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs or base64 image content, optional audio URLs, and the Juhe API key are sent to the Juhe video service.

Mitigation: Use the skill only when that data sharing is acceptable, prefer the JUHE_VIDEO_KEY environment variable over command-line keys, and avoid committing scripts/.env.

Risk: Generated videos are saved locally by default, which can place files in an unintended directory.

Mitigation: Choose the output directory deliberately or use --no-download when only an online link is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-video-generate)
- [Publisher profile](https://clawhub.ai/user/juhemcp)
- [Juhe AI Video Creation API documentation](https://www.juhe.cn/docs/api/id/827)
- [Juhe data service](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Juhe task status text, an online video URL when generation succeeds, and a local MP4 file by default unless download is disabled.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
