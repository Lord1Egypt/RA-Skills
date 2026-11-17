## Description:

为快手电商、快手小店、直播间和磁力金牛生成与编辑信任型商品演示、主播口碑、工厂实拍及带货视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants, marketing teams, and agents use this skill to generate and edit Kuaishou ecommerce videos for product demos, live-commerce previews, factory-source content, and paid creative variants while preserving truthful claims and visible evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a stored AI Hive API key with a configured API host, which creates credential exposure risk if the base URL is changed by untrusted input.

Mitigation: Use only the documented AI Hive base URL, avoid untrusted --base-url or AI_HIVE_BASE_URL values, keep API keys in an isolated environment, and review uploaded media before sending it to the configured service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/kuaishou-ecommerce-video-generation-editing)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can submit generation tasks, query task status, and download generated media through the configured AI Hive service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
