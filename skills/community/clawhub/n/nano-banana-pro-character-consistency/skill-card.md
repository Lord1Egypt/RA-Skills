## Description:

使用 Nano Banana Pro 在广告、社媒、短故事、虚拟模特和品牌 Campaign 中保持同一商业人物的脸、年龄、发型、体型、服装与身份连续。Use this skill for Nano Banana Pro character consistency、一致人物、虚拟模特、品牌代言人、数字人图片、连续场景、换装、表情动作表和系列广告；通过 AI Hive 使用人物参考图生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to generate commercial character-consistent Nano Banana Pro image campaigns from approved reference images. It supports outfit variants, multi-scene campaign images, expression and gesture sheets, and ad layout variants while preserving approved identity details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI Hive API key can be sent to a configured API endpoint if the base URL is changed.

Mitigation: Use the default official HTTPS base URL, and set AI_HIVE_BASE_URL or --base-url only for endpoints you fully trust.

Risk: Reference images passed to the helper are uploaded to AI Hive for image generation.

Mitigation: Upload only approved images with the required rights and consent, and keep records of allowed identity, channel, region, term, and use.

Risk: Global dependency installation can affect the user's Python environment.

Mitigation: Install requests in a virtual environment when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-character-consistency)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and helper-generated image files from AI Hive tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses explicit reference-image uploads, batch counts, aspect ratio settings, route selection, and a local output directory.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
