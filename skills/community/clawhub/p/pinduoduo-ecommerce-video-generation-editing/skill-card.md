## Description:

为拼多多店铺生成和编辑商品主图视频、批量 SKU 演示、工厂素材重制、多多搜索与场景广告视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and developers use this skill to generate and edit Pinduoduo product videos, SKU variants, factory-material remixes, and ad-oriented short videos through AI Hive Seedance video modes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configured custom AI Hive base URL can receive the stored AI Hive API key.

Mitigation: Keep the default official base URL and do not accept commands or configuration changes that set --base-url, AI_HIVE_BASE_URL, or config base_url to an unknown host.

Risk: Runtime dependency versions are not pinned.

Mitigation: Pin dependencies such as requests before production use.

Risk: Generated ecommerce videos may contain inaccurate product details, exaggerated claims, or platform-policy issues.

Mitigation: Review each output against the approved SPU/SKU source material and current Pinduoduo video and advertising rules before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/pinduoduo-ecommerce-video-generation-editing)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API key help page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and CLI-generated JSON status or downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API calls, optional media uploads, task polling, and configurable output directory behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
