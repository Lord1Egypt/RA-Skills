## Description:

使用 AI Hive Seedance 2.5 将美图 MOKI、美图视频或时尚商业视频流程迁移为品牌可审的镜头资产，支持文生、商品首帧、参考风格、视频改版与镜头延长；不连接美图账号，也不表示官方合作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to plan and run brand-reviewed AI video generation and editing workflows through AI Hive Seedance 2.5. It supports text-to-video, image-to-video, reference-video generation, campaign video edits, and packshot extension while preserving approved product, model, color, and layout constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, videos, audio, prompts, and task data are sent to AI Hive and its storage provider.

Mitigation: Use approved assets, avoid confidential or regulated media unless authorized, and keep task records for review.

Risk: Generated videos can drift from approved product, model, color, logo, or claim constraints.

Mitigation: Perform the documented frame-by-frame review of packaging, identity, skin tone, wardrobe, accessories, brand colors, edit joins, and post-production text areas before use.

Risk: The AI Hive credential can be exposed if AI_HIVE_API_KEY or ~/.ai-hive/config.json is mishandled.

Mitigation: Protect the API key, keep config permissions restricted, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/meitu-moki-video-generation-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, files]

**Output Format:** [Markdown guidance with inline bash commands; CLI responses are text or JSON and generated assets are downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI_HIVE_API_KEY or ~/.ai-hive/config.json for authentication; supports --output-dir and --no-download for generated task results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
