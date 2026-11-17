## Description:

OpenClaw video pipeline expands a user brief into a three-shot storyboard, saves it as storyboard/storyboard.json, and runs a Python script that calls Zhipu CogVideoX-3 three times to produce 10-second clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilaus](https://clawhub.ai/user/ilaus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn a short video brief into a three-segment storyboard and then generate three CogVideoX-3 video clips. It is suited for OpenClaw workflows involving storyboards, 30-second short films, or storyboard-to-video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can send the ZHIPUAI_API_KEY and storyboard prompts to any endpoint configured through BIGMODEL_API_BASE.

Mitigation: Use the default official Zhipu HTTPS API host unless the alternate endpoint is fully trusted, and review the skill before installing it in a project.

Risk: The workflow requires a Zhipu API key to submit video-generation jobs.

Mitigation: Keep ZHIPUAI_API_KEY in the environment only and do not commit API keys or generated credentials to source control.

Risk: The workflow returns three separate 10-second clips rather than a single finished 30-second video.

Mitigation: Plan a post-production step, such as video editing software or ffmpeg, to concatenate and review the generated clips.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilaus/skills/openclaw-video-pipeline)
- [CogVideoX-3 model guide](https://docs.bigmodel.cn/cn/guide/models/video-generation/cogvideox-3)
- [Zhipu video generation async API](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%E5%BC%82%E6%AD%A5)
- [Zhipu async result API](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E6%9F%A5%E8%AF%A2%E5%BC%82%E6%AD%A5%E7%BB%93%E6%9E%9C)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON storyboard content, shell commands, video URLs, optional MP4 files, and a final JSON summary from the script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates exactly three 10-second CogVideoX-3 generation requests; generated clips require separate post-production concatenation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
