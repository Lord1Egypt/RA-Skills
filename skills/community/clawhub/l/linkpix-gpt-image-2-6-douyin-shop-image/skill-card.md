## Description:

用户指定 GPT Image 2.6 / 智慧模型2.6，要做抖店商品首图、抖音商城主图、短视频封面或直播间贴片时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

抖音电商内容创作者和店铺运营人员可用此技能，为商品主图、短视频带货封面和直播间贴片准备图片生成提示，并通过青虎 AI 提交生成任务。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Reference images are uploaded to Qinghu AI, and a configured endpoint override can change where requests are sent.

Mitigation: Use only reference images you are comfortable sending to the service, and verify any QHKIT_BASE_HOST override before submitting a task.

Risk: Image generation uses credits, and the installed global qhkit CLI is a third-party dependency whose code was outside this artifact review.

Mitigation: Review the estimate and confirm before generation; check the CLI package and version before installing or updating it.

## Reference(s):


## Skill Output:

**Output Type(s):** [Images, Text, Markdown, JSON configuration, Shell commands, Guidance]

**Output Format:** [Generated image files, JSON task and result files, and Markdown or text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts are limited to 5,000 characters; image dimensions, quality, language, and count depend on the selected model options.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
