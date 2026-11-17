---
name: procurement-optimizer
description: "使用场景: 用户要求将采购需求、供应商报价或原始表格整理为采购拆单方案，按包装、交期、容量与运费计算整数分配时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.1.0",
        "openclaw": {
            "emoji": "📄",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "PROCUREMENT_OPTIMIZER_API_KEY",
            "requires": {
                "bins": [
                    "curl"
                ]
            },
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "通用平台 Key；与产品专用变量任选其一。"
                },
                {
                    "name": "PROCUREMENT_OPTIMIZER_API_KEY",
                    "required": false,
                    "description": "平台产品专用 Key。"
                },
                {
                    "name": "AI_SKILLS_API_URL",
                    "required": false,
                    "description": "可选站点根地址，不带 /api/v1；默认 https://ai-skills.open-idea.net。"
                }
            ]
        }
    }
---

# 采购拆单优化

## Skill 简介

采购需求和供应商报价需要按包装、交期、容量与运费计算整数拆单方案时。平台初始关闭，真实依赖与授权样本验收后由管理员开放；不可将夹具测试当成真实质量证明。

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

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.PROCUREMENT_OPTIMIZER_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `PROCUREMENT_OPTIMIZER_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## Skill 使用

直接从用户提供的需求说明、报价、聊天记录或原始 CSV/XLSX 整理数据；不要求用户先套平台模板。原文足够时由 OpenClaw 组织 `data` JSON；保留来源表格时上传并确认列映射。缺少单位、币种、含税口径、报价有效期等信息时只追问影响求解的缺项，字段与样例见操作参考。

执行 `purchase.inspect` → 人工确认摘要 → `purchase.review` → `purchase.solve` → `purchase.export`。先读操作参考选择直接 JSON、原表上传或已有项目续做分支；执行前读请求参考。预检与确认免费，求解按报告收费；收费前读费用参考，取得当前版本与费用授权，不通过收费调用探价。

仅支持 CNY 统一含税、单收货地址和整数件数；不猜测单位换算，不超买，不擅自下单。确认必须绑定当前版本，求解使用确认回执原值；网络结果未知先查原任务并复用原 `Idempotency-Key`。仅 `verified=true` 的 OPTIMAL/FEASIBLE 是可导出的方案，FEASIBLE 未证明最优。

## 完成标准

交付可核查的分配、商品额、运费、总额、求解/复核状态和实际费用；无解或未验证结果如实说明。导出产生私有 artifacts 元数据；当前 API 不返回下载链接，使用当前用户工作台任务页交付，不能承诺 Agent 直接下载。

私有项目从创建起保留 30 天，修订不延长期限。仅处理用户授权资料；敏感文件、密钥与签名 URL 不写日志，不默认用于训练、演示或反馈。删除或到期后停止引用与下载，重新上传需重新确认；不自动公开或分享产物。授权和确认细节见行为参考。

## 参考资料

按任务读取：

- [平台密钥与费用](https://ai-skills.open-idea.net/skill-docs/procurement-optimizer/API-KEY.md)
- [上传、请求与轮询](https://ai-skills.open-idea.net/skill-docs/procurement-optimizer/HTTP-REQUESTS.md)
- [操作字段](https://ai-skills.open-idea.net/skill-docs/procurement-optimizer/OPERATIONS.md)
- [授权与人工确认](https://ai-skills.open-idea.net/skill-docs/procurement-optimizer/BEHAVIOR-RULES.md)
