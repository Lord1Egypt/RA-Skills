## Description:

将本地视频或公开视频链接转写为文字，并可按自定义提示生成总结、改写、提取或翻译内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、访谈整理人员及课程或会议记录者可用此技能转写本地视频或公开视频，并按提示生成摘要、整理稿、改写文案或翻译。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video URLs and redirects may reach private-network resources that could then be uploaded for transcription.

Mitigation: Block private-network access for the initial URL and every redirect, or run with equivalent network isolation; use only approved public sources.

Risk: Recordings are sent to an external transcription service, and local temporary video copies may be created.

Mitigation: Confirm approved upload destinations and retention terms before processing confidential recordings, and account for temporary local copies.

Risk: Service use may incur usage-based charges.

Mitigation: Review current service pricing and expected processing volume before submitting videos.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-video-script-doc)
- [Guaikei official website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Plain text on standard output; content follows the requested transcript or transformation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cleaned transcripts, summaries, rewrites, extracted quotes, shot breakdowns, or translations; output language and structure depend on the request.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
