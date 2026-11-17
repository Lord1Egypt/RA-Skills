## Description:

面向农产品品牌和门店，生成受众卖点策略、30天内容日历、图片与短视频脚本提示词、AI-HIVE任务记录和复盘指标，并要求用户核验事实、素材权利和预算后再执行生成任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External agricultural brands, local merchants, marketing operators, and supporting developers use this skill to plan and produce image, short-video, and content-marketing assets for agricultural products. It helps structure facts, audience claims, platform-specific prompts, AI-HIVE generation tasks, task records, and review checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API keys may be stored in plaintext local configuration if the init flow is used.

Mitigation: Prefer providing AI_HIVE_API_KEY through the environment and avoid init unless plaintext storage in ~/.ai-hive/config.json is acceptable.

Risk: A custom API base URL could receive the AI-HIVE API key.

Mitigation: Use the default AI-HIVE endpoint or set a custom base URL only when the endpoint is fully trusted.

Risk: Uploaded media may contain unauthorized product, person, logo, video, or music assets.

Mitigation: Upload only media the user is authorized to send to AI-HIVE, and require source confirmation before generation.

Risk: Agricultural marketing claims can misrepresent origin, production, testing, nutrition, efficacy, pricing, or traceability.

Mitigation: Treat uncertain facts as pending verification, keep AI-generated visuals labeled as generated or illustrative, and require human review before publication.

## Reference(s):

- [农产品品牌图片视频内容营销行业手册](references/industry-playbook.md)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/industry-agri-product-brand-marketing-ai-hive)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with JSON records and bash/Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create JSON marketing briefs, AI-HIVE image or video tasks, downloaded media files, and ffmpeg-edited videos when the generated commands are executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
