## Description:

Use this skill when the user asks for Nano Banana Pro、图片生成、图片编辑、商品图、广告图，或要为电商、广告、营销、短剧、漫剧、带货与种草内容完成Nano Banana Pro 图片工作室。它服务电商设计师、品牌市场人员和社媒创作者：接收文字需求、参考图、品牌颜色、画幅、文字内容和用途，交付文生图、参考图编辑、批量变体、提示词和交付检查。特色是一个入口覆盖生成与编辑，优先保证主体、文字和品牌一致；需要生成素材时通过AI-HIVE OpenAPI完成配置查询、参考素材上传、价格快照、COST_FIRST/SPEED_FIRST/SUCCESS_FIRST路由、异步轮询和下载。不要把本Skill用于未授权复刻、虚假商品声明、伪造用户证言或规避平台规则。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce designers, and brand marketing teams use this skill to turn Chinese commercial image requests into visual blueprints, prompts, reference-image strategies, batch variants, runnable AI-HIVE commands, and delivery checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API client can send the user's AI-HIVE key to a configurable remote host.

Mitigation: Use only trusted AI-HIVE endpoints, avoid custom base URLs unless fully trusted, and use a dedicated limited API key.

Risk: Image-generation jobs may incur cost and may upload user media to AI-HIVE.

Mitigation: Confirm prompts, routing mode, pricing snapshot, and media authorization before submitting paid generation tasks.

Risk: Commercial images can create misleading product, brand, testimonial, copyright, or endorsement claims.

Mitigation: Require factual inputs and authorized assets, avoid protected copying or false claims, and review generated outputs before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-image-studio-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE image-generation jobs after user confirmation and can download generated files through the included helper script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
