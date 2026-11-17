## Description:

使用 GPT Image 2 对现有图片进行精确、可复核的编辑，包括删除或替换物体、局部修复、改颜色材质、人物与服装调整、扩图改版和广告版本适配，并通过 AI Hive 上传原图并下载结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, ecommerce operators, and marketing teams use this skill to prepare controlled GPT Image 2 image-editing requests, run AI Hive image-editing commands, and review visual differences before approving outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source images and prompts are uploaded to AI Hive for processing.

Mitigation: Install only if you trust AI Hive, avoid uploading sensitive or unauthorized images, and obtain needed approval for edits involving people, products, or advertising claims.

Risk: API key handling and custom base URLs require review before installation.

Mitigation: Use a dedicated low-privilege AI Hive API key, keep configuration files private, and set a custom base URL only when the endpoint is fully trusted.

Risk: Downloaded output paths are under-scoped enough that accidental overwrites or misplaced files could matter.

Mitigation: Run the skill in an isolated environment and choose an output directory where downloaded files cannot overwrite important assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-image-edit)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and generated image files downloaded to a local output directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses prompts, source images, optional reference images, routing mode, batch size, model parameters, and output directory settings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
