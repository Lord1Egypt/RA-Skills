## Description: <br>
使用阿里云百炼 HappyHorse 模型生成视频，支持图生视频（首帧/尾帧控制）和文生视频。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindypapa](https://clawhub.ai/user/cindypapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agents use this skill to generate short videos through Alibaba Cloud Bailian DashScope HappyHorse from text prompts, first-frame images, or first-and-last-frame image controls. It helps collect video requirements, confirm prompts and duration, call the video generation API, poll task status, and return the generated video file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release embeds and automatically uses a shared DashScope API key, creating account, billing, and abuse risks. <br>
Mitigation: Install only a version that removes the embedded key and requires each user to provide their own DashScope API key through a secure configuration path. <br>
Risk: Prompts and media URLs are sent to Alibaba DashScope for video generation. <br>
Mitigation: Do not submit confidential prompts, private media URLs, or proprietary assets unless external processing by DashScope is acceptable. <br>
Risk: Generated videos are downloaded to the local OpenClaw workspace and may contain sensitive or proprietary content. <br>
Mitigation: Review output paths and retention practices, restrict workspace access, and remove sensitive generated files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/cindypapa/happyhorse-video-creator) <br>
- [Project homepage](https://github.com/Cindypapa/happyhorse-video-creator) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/) <br>
- [DashScope video synthesis API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, API call parameters, status messages, and generated video file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated videos are downloaded as MP4 files when DashScope tasks succeed; prompts and media URLs are sent to Alibaba DashScope.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
