## Description:

使用阿里云百炼 HappyHorse 模型生成视频，支持图生视频（首帧/尾帧控制）和文生视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to plan and generate short videos through Alibaba Cloud Bailian DashScope HappyHorse, using either text prompts or first-frame and last-frame image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an exposed DashScope API key that the skill can automatically use for external paid requests.

Mitigation: Remove and rotate the exposed key before installation, and require users to provide their own API key through a secure mechanism.

Risk: The skill can submit video-generation jobs to Alibaba DashScope and share prompts or image URLs with that external service.

Mitigation: Require explicit user confirmation before job submission and avoid sending private prompts, image URLs, or sensitive media.

Risk: The skill can download generated videos and write files to local paths.

Mitigation: Restrict downloads to trusted video URLs and safe output paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cindypapa/skills/happyhorse-video-creator)
- [Declared project homepage](https://github.com/Cindypapa/happyhorse-video-creator)
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/)
- [DashScope video synthesis endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, API Calls, Files]

**Output Format:** [Markdown guidance with Python code examples and generated video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit asynchronous DashScope video-generation jobs, poll task status, and download generated MP4 files.]

## Skill Version(s):

1.1.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
