## Description:

为快手电商、快手小店、直播间和磁力金牛生成与编辑商品卡、主播同框、源头工厂、直播贴片及广告图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, designers, and agent users use this skill to generate or edit Kuaishou ecommerce product cards, host-and-product images, factory proof visuals, livestream overlays, and ad test images from authorized reference materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes credential-bearing API calls to user-configurable AI Hive endpoints.

Mitigation: Use it only with a trusted AI Hive service and publisher, avoid custom base_url values, and protect AI_HIVE_BASE_URL plus ~/.ai-hive/config.json from unauthorized changes.

Risk: Running init can store an API key locally.

Mitigation: Keep the local configuration file private, prefer environment variables or secured local config, and rotate the key if exposure is suspected.

Risk: Selected reference media may be uploaded to the AI Hive service.

Mitigation: Upload only media the user is authorized to process and review service trust, policy, and data-handling expectations before use.

Risk: Generated ecommerce images could misstate product claims, pricing, sales volume, certification, origin, factory scale, or platform UI details.

Mitigation: Keep claims, prices, sales numbers, certifications, and platform UI additions outside model generation unless approved source material supports them, then review against current Kuaishou ecommerce and ad rules before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/kuaishou-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and generated image task outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-selected reference media to AI Hive, submit image-generation tasks, poll task status, and download generated image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
