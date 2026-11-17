## Description:

A Chinese-language OpenClaw skill for self-media creators that connects Feishu Bitable with hot-list topic generation, publishing-data tracking, monthly review reports, and content-calendar management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a799549967-lang](https://clawhub.ai/user/a799549967-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External self-media creators and content operators use this skill to plan Chinese-platform content, store publishing workflow data in Feishu Bitable, and generate performance reviews and overdue-draft reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu App Secret exposure could allow unintended access if pasted into an insecure chat or retained in logs.

Mitigation: Use a secure secret setting when available, avoid sharing the secret in ordinary chat, and rotate any secret that may already have been exposed.

Risk: Read/write Feishu Bitable access can modify the user's content database.

Mitigation: Use a dedicated Feishu app with least-privilege access limited to the intended Bitable and review permissions before installation.

Risk: Hot-list-derived topic suggestions and review reports may be stale, incomplete, or misleading.

Mitigation: Review generated records, topic recommendations, and monthly analysis before publishing content or making business decisions.

Risk: Third-party hot-list APIs may be unavailable or unstable.

Mitigation: Fall back to other available hot-list sources or the user's historical Feishu data and disclose when a hot-list source could not be used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a799549967-lang/skills/notion-content-hub-cn)
- [Publisher profile](https://clawhub.ai/user/a799549967-lang)
- [Feishu Open Platform](https://open.feishu.cn)
- [Zhihu hot-list endpoint](https://tenapi.cn/v2/zhihuhot)
- [Weibo hot-search endpoint](https://v2.xxapi.cn/api/weibohot)
- [Baidu hot-search endpoint](https://tenapi.cn/v2/baiduhot)
- [Toutiao hot-list endpoint](https://tenapi.cn/v2/toutiaohotnew)
- [Douyin hot-list endpoint](https://tenapi.cn/v2/douyinhot)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Chinese Markdown guidance, topic plans, review reports, setup instructions, and Feishu Bitable record updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Feishu App ID, App Secret, and Bitable URL; may call third-party hot-list APIs and Feishu Bitable APIs.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
