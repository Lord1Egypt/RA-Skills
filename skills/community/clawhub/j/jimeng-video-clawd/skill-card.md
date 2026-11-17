## Description:

即梦AI视频生成工具（带声音版本），通过火山引擎API自动生成带音频的高质量视频，支持文生视频、图生视频，适用于短视频内容创作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and content teams use this skill to prompt Dreamina/Volcengine video-generation models for short videos, including text-to-video and image-to-video workflows with optional generated audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image inputs, and generation metadata are sent to an external Volcengine/Dreamina API and may incur provider charges.

Mitigation: Confirm provider use and billing expectations before invocation, and avoid sending secrets, regulated data, or confidential business material.

Risk: Broad video-generation triggers could invoke this provider when the user intended a different workflow.

Mitigation: Prefer explicit invocation for Dreamina/Volcengine video generation and review generated commands before execution.

Risk: Generated audio is AI-synthesized and may not meet exact quality, licensing, or brand requirements.

Mitigation: Review generated video and audio before publication, and use post-production or a no-audio model when precise audio control is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/jimeng-video-clawd)
- [Volcengine content generation tasks API endpoint](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown with shell command/API call examples and generated video file paths or URLs when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate external paid API calls and return MP4 video outputs with AI-generated audio depending on model selection.]

## Skill Version(s):

2.0.0 (source: server release, target metadata, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
