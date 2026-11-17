---
name: meeting-minutes-action-items
description: "使用场景: 用户要求从会议文字或文档生成纪要、决策、行动项和可交付报告时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.2.0",
        "openclaw": {
            "emoji": "🗒️",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "MEETING_MINUTES_ACTION_ITEMS_API_KEY",
            "requires": {
                "bins": ["curl"]
            },
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "通用平台 Key；与产品专用变量任选其一。"
                },
                {
                    "name": "MEETING_MINUTES_ACTION_ITEMS_API_KEY",
                    "required": false,
                    "description": "AI Skills 平台会议纪要 API 密钥。"
                },
                {
                    "name": "AI_SKILLS_API_URL",
                    "required": false,
                    "description": "可选 API 根地址。"
                }
            ]
        }
    }
---

# 会议纪要与行动项

## Skill 简介

会议纪要与行动项 Skill 从文本或 TXT、MD、VTT、SRT、DOCX、PDF 生成摘要、决策、行动项、风险和待确认事项。每个关键结论关联原文证据；缺失负责人或日期会标记为待确认，不会替参会者编造承诺。

## 平台入口与注册

1. 打开 [AI Skills 平台](https://ai-skills.open-idea.net/)，新用户进入 [注册页面](https://ai-skills.open-idea.net/register)，已有账号进入 [登录页面](https://ai-skills.open-idea.net/login)。
2. 登录后进入 [产品管理](https://ai-skills.open-idea.net/dashboard/products) 开通本 Skill，再到 [API 密钥管理](https://ai-skills.open-idea.net/dashboard/keys) 创建密钥。

## Skill 安装与配置

当前控制台直接创建通用 Key，无需选择产品；每个账号最多保留一把未撤销的通用 Key，已有时直接复制复用，更换时先撤销旧 Key。下列产品选择说明适用于旧版控制台。

1. 在 [API 密钥管理](https://ai-skills.open-idea.net/dashboard/keys)中选择已开通的产品，创建并复制 API 密钥。
2. 在 OpenClaw 中安装本 Skill。
3. 将复制的密钥配置到本 Skill 的 API 密钥环境变量，然后重启 Gateway：

```sh
openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"
openclaw gateway restart
```

推荐创建账号通用 Key，以上全局变量只需配置一次即可供各 Skill 使用；仍需在产品管理中开通目标产品。原有产品专用 Key 仅能调用对应产品。

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.MEETING_MINUTES_ACTION_ITEMS_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `MEETING_MINUTES_ACTION_ITEMS_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## Agent 执行规则

1. 使用 `meeting.analyze`（整理会议纪要）提交 `transcript` 或一个文件，二者不可同时提交；必须带 IANA `timezone`。
2. 原文未明确的负责人、期限、决策状态标记为待确认；不根据常识或参会者职位猜测。
3. 每项决策和行动项保留证据摘录与位置；对证据不足的输出降低置信度或放入待确认列表。
4. 用户需要交付物时再调用 `meeting.export`（导出会议交付物），格式限 `markdown`、`docx`、`pdf`。

## 完成标准

- 持续轮询到 `succeeded`、`partial` 或 `failed`，结果不确定时不重复分析。
- 重试使用原 `Idempotency-Key`；不同业务动作生成新 UUID。
- 最终区分已确认决策、行动项、风险和待确认事项，并只向当前用户交付私有 `artifacts`。

## 参考资料

按当前任务读取对应资料；无需预读全部文档。

- [API 密钥配置与价格](https://ai-skills.open-idea.net/skill-docs/meeting-minutes-action-items/API-KEY.md)
- [HTTP 请求、上传与任务轮询](https://ai-skills.open-idea.net/skill-docs/meeting-minutes-action-items/HTTP-REQUESTS.md)
- [操作字段与结果](https://ai-skills.open-idea.net/skill-docs/meeting-minutes-action-items/OPERATIONS.md)
- [证据、承诺与人工复核规则](https://ai-skills.open-idea.net/skill-docs/meeting-minutes-action-items/BEHAVIOR-RULES.md)
