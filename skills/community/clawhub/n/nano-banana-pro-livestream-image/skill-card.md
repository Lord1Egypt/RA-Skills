## Description:

使用 Nano Banana Pro 建立主播、商品与直播间风格一致的直播视觉套件，覆盖开播封面、主播主视觉、场景背景、品类转场、商品卡和多平台直播封面，并通过 AI Hive 生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Commerce operators, creators, and agent-assisted design teams use this skill to prepare consistent livestream selling visuals, including host-and-product key art, background layers, category transitions, product cards, and platform-specific covers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an AI Hive API key and may store it in a local configuration file.

Mitigation: Keep the API key file protected, prefer environment variables when appropriate, and delete or rotate the key when it is no longer needed.

Risk: Selected reference images are uploaded to AI Hive for generation.

Mitigation: Only upload media that is approved for use with AI Hive and avoid sensitive or restricted images.

Risk: Generated livestream visuals can include inaccurate product, brand, pricing, promotion, or layout details if prompts are not reviewed.

Mitigation: Review generated assets against approved source material and add operational text, prices, inventory, and promotions from authoritative business sources.

Risk: The helper depends on the Python requests package and network calls to AI Hive.

Mitigation: Use a virtual environment and consider pinning dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-livestream-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files, JSON]

**Output Format:** [Markdown guidance with bash commands; generated image files and task JSON from AI Hive when commands are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Nano Banana Pro via AI Hive, supports reference images, batch generation, aspect-ratio parameters, routing mode, output directory selection, media upload, task polling, and optional no-download task submission.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
