## Description:

Infographic Image turns topics, long-form text, reports, meeting notes, or instructions into Chinese image-generation prompts and can optionally render the resulting infographic with DashScope Qwen image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yeyitech](https://clawhub.ai/user/yeyitech)

### License/Terms of Use:


## Use Case:

Developers, content teams, and agents use this skill to convert topics, articles, reports, or meeting notes into Chinese infographic and story-comic prompts. It can run as a prompt-only workflow or call DashScope to render and save the final image locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source text submitted to the workflow may be sent to DashScope for prompt inference or image generation.

Mitigation: Do not process confidential documents unless the user has approved sending that content to DashScope.

Risk: Generated prompt payloads and image files can be written to local paths selected by the user or by the skill defaults.

Mitigation: Choose output paths deliberately and review generated files before sharing or reusing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yeyitech/skills/infographic-image)
- [DashScope API Base](https://dashscope.aliyuncs.com)
- [Infographic Meta Prompt](references/meta-prompt.md)
- [Comic Story Meta Prompt](references/meta-prompts-comic-story.md)
- [Frosted Whiteboard Meta Prompt](references/meta-prompts-frosted-whiteboard.md)
- [Spatial Gallery Meta Prompt](references/meta-prompts-spatial-gallery.md)
- [Clean Editorial Style](references/styles/clean-editorial.md)
- [Comic Story Style](references/styles/comic-story.md)
- [Default Style](references/styles/default.md)
- [Frosted Whiteboard Style](references/styles/frosted-whiteboard.md)
- [Spatial Gallery Style](references/styles/spatial-gallery.md)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Console text, optional JSON prompt payload, and optional image file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only dry runs are supported; image rendering saves files locally and requires DASHSCOPE_API_KEY.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
