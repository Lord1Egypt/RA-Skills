## Description:

使用 GPT Image 2 通过 AI Hive 生成直播带货图片物料，包括预约预热海报、直播封面、直播间背景、商品讲解卡、福利节点图、导播转场和回放封面。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, livestream operators, and developers use this skill to generate livestream commerce image assets and supporting AI Hive commands across pre-live, live, and replay stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores and uses an AI Hive API key and can send that key to a configured API endpoint.

Mitigation: Use the default AI Hive endpoint unless you intentionally trust a custom endpoint, protect ~/.ai-hive/config.json, and review the skill before installing it with a real API key.

Risk: Uploaded files may contain sensitive or unintended content.

Mitigation: Upload only approved livestream image assets and avoid non-image or sensitive files.

Risk: Unpinned dependencies can change behavior after installation.

Mitigation: Pin and review dependencies before installation in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-livestream-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Image files]

**Output Format:** [Markdown guidance with inline bash commands and generated image files from AI Hive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI_HIVE_API_KEY, optional local reference images, aspect ratio parameters, and a local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
