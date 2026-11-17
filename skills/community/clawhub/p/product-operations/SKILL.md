---
name: product-operations
description: "使用场景: 用户要求通过平台制定运营计划、复盘真实数据或获取上线检查清单时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.3.0",
        "openclaw": {
            "emoji": "📈",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "PRODUCT_OPERATIONS_API_KEY",
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "通用平台 Key；与产品专用变量任选其一。"
                },
                {
                    "name": "PRODUCT_OPERATIONS_API_KEY",
                    "required": false,
                    "description": "兼容产品专用 Key；设置时优先使用。"
                }
            ]
        }
    }
---

# 产品运营

## Skill 简介

产品运营助手把目标转换为带日期、负责人、优先级和验收指标的任务计划，并使用后端公式计算点击率、漏斗转化率、目标完成率、转化成本、增长率和 ROI。它也能生成上线检查清单，并将计划或复盘导出为 CSV、Excel、Markdown；运营计划还可导出系统日历文件。

## 平台入口与注册

1. 打开 [AI Skills 平台](https://ai-skills.open-idea.net/)，新用户进入 [注册页面](https://ai-skills.open-idea.net/register)，已有账号进入 [登录页面](https://ai-skills.open-idea.net/login)。
2. 登录后进入 [产品管理](https://ai-skills.open-idea.net/dashboard/products) 开通本 Skill，再到 [API 密钥管理](https://ai-skills.open-idea.net/dashboard/keys) 创建并复制 API 密钥。

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

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.PRODUCT_OPERATIONS_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `PRODUCT_OPERATIONS_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## Skill 使用

1. 制定新计划时，收集产品名称、明确目标、日期范围、执行渠道、预算和团队人数，调用“制定运营计划”操作 `operation.plan`。
2. 复盘时只使用用户提供的真实数据。可读取用户指定的 CSV 或 XLSX，在本地提取曝光、访问、线索、转化、收入和成本后调用“复盘运营数据”操作 `operation.review`；不得上传原始文件或自行补造缺失数据。
3. 用户要求上线准备或运营风险检查时，调用免费的“获取运营检查清单”操作 `operation.checklist`；普通计划或复盘无需额外调用。
4. 用户需要文件时，对成功的计划或复盘任务调用“导出运营结果”操作 `operation.export`。只能使用当前用户、当前 Skill 的成功来源任务 ID。
5. 指标结果由平台确定性计算。解释结论时区分原始数据、计算结果和行动建议，不把相关性写成因果关系。

## 完成标准

- 在用户已授权范围内完成请求；收到异步任务时持续轮询任务状态，按 HTTP-REQUESTS.md 的终态与等待上限停止。未规定上限时，开始轮询前设定有限等待预算；超时保留任务 ID、最后状态与查询方式，不宣称成功或失败、不重复提交。
- 429/503 等可恢复错误按参考规则有限退避；同一逻辑请求复用原 `Idempotency-Key` 和相同输入。结果不确定或规则要求人工核对时停止自动重试；已授权范围内的安全续查无需重复确认。
- 多文件或多步骤任务完成后逐项交付结果；部分失败、仍在处理或等待人工核对的项目分别说明，并给出下一步。

## 参考资料

按当前任务读取对应资料；无需预读全部文档。

- 首次配置或排查鉴权时：[API 密钥配置](https://ai-skills.open-idea.net/skill-docs/product-operations/API-KEY.md)
- 调用 API 前，确认请求、响应与重试规则：[HTTP 请求与任务轮询](https://ai-skills.open-idea.net/skill-docs/product-operations/HTTP-REQUESTS.md)
- 选择当前操作后，查其字段与结果：[操作与字段说明](https://ai-skills.open-idea.net/skill-docs/product-operations/OPERATIONS.md)
- 执行前，确认本次授权、安全与结果解释边界：[指标与行为规则](https://ai-skills.open-idea.net/skill-docs/product-operations/BEHAVIOR-RULES.md)
