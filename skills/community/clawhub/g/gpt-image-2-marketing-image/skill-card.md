## Description:

使用 GPT Image 2 按营销漏斗制作一整套 Campaign 图片，包括品牌认知KV、发布会视觉、落地页Hero、邮件头图、社交素材、线下Banner和会员沟通。Use this skill for GPT Image 2 marketing images、品牌Campaign、整合营销、产品上市、活动海报、EDM、landing page、社媒内容、CRM和多渠道营销资产；通过 AI Hive 生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, ecommerce, CRM, and campaign teams use this skill to plan source-of-truth campaign requirements and generate channel-specific GPT Image 2 marketing assets through AI Hive. It is intended for brand awareness, launch, landing page, email, social, offline banner, and retention visuals that preserve product facts and approved brand assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom AI Hive base URL can receive the user's bearer API key.

Mitigation: Use the official AI Hive endpoint and set AI_HIVE_BASE_URL or --base-url only for servers the user controls.

Risk: Reference images are uploaded to the AI Hive service.

Mitigation: Upload only approved assets and confirm rights for third-party people, trademarks, campaign materials, and partner brands before generation.

Risk: Generated files are downloaded to ~/Downloads/AiHive by default.

Mitigation: Review the output directory before use and choose a controlled location with --output-dir when handling sensitive campaign assets.

Risk: Installing dependencies from an unpinned environment can introduce supply-chain exposure.

Mitigation: Install requests from a trusted pinned environment before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-marketing-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; downloaded generated image files when execution succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses prompts, optional reference images, batch size, routing mode, model parameters, and output directory settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
