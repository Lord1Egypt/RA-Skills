## Description:

使用 Nano Banana Pro 生成包含指定中文、英文、数字和短文案的图片，并按字符、层级、位置和品牌版式逐项复核。Use this skill for Nano Banana Pro exact text in images、AI海报文字、中文文字图片、广告标题、促销图、信息图、社媒封面、双语视觉和带字电商图；通过 AI Hive 生成或基于底图编辑。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, marketers, and developers use this skill to generate or edit image assets that contain approved Chinese, English, numeric, or short marketing text, then verify visible characters and layout before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if a custom base URL or AI_HIVE_BASE_URL points to an untrusted endpoint.

Mitigation: Keep the default AI Hive endpoint unless you control and trust the replacement endpoint.

Risk: Reference images and other selected files are uploaded to the service during generation or editing workflows.

Mitigation: Upload only files intended for the service and use a limited-scope API key when available.

Risk: Output downloads may be unexpectedly large or unsuitable for direct publication.

Mitigation: Monitor downloaded outputs and inspect generated files before sharing or publishing them.

Risk: Generated image text can contain incorrect, added, missing, or distorted characters, especially in price, legal, medical, or promotional copy.

Mitigation: Perform character-level review against the approved copy list; for non-tolerant text, generate a text-free base image and place approved text in design software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-exact-text-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files, JSON]

**Output Format:** [Markdown guidance with inline bash commands; runtime commands can return JSON task data and downloaded image or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an AI Hive API key and accepts prompts, optional reference images, batch size, routing mode, model parameters, and output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
