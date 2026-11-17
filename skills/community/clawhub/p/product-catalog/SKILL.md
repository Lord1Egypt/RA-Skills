---
name: product-catalog
description: "使用场景: 用户需要维护SKU产品库、显式绑定图片、确认中英文内容并生成和更新可核对PDF目录时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.1.0",
        "openclaw": {
            "emoji": "📊",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "PRODUCT_CATALOG_API_KEY",
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
                    "name": "PRODUCT_CATALOG_API_KEY",
                    "required": false,
                    "description": "AI Skills 平台产品目录 API 密钥。"
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

# 多语言产品目录

## Skill 简介

维护长期私有产品库，按 SKU 明确绑定素材，人工确认译文及价格后冻结目录；用两套固定模板生成 PDF、逐页预览和可追溯清单。生成项目保留30天，库中在用素材保留至用户删除。产品默认关闭，真实模型、私有 S3 和部署验收通过后方可启用。

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

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.PRODUCT_CATALOG_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `PRODUCT_CATALOG_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## OpenClaw 使用流程

用户直接提供产品表、产品图片和目标语言，不要求先下载网页模板。Agent 在具备相应文件读取能力时整理产品编号、名称、规格、价格及图片对应关系；无法读取时使用已支持的表格上传接口或询问用户，不能捏造内容。缺少币种、计价单位、图片对应或译文确认时先补齐。

原表按图片文件名引用时，先上传每张图并记录“原文件名—asset_id”，按明确对应关系写入产品；不把网页模板导入路由当成 OpenClaw API。API 的表格映射使用素材 ID，而不是自动按图片顺序配图。

开始时读 OPERATIONS 与 HTTP-REQUESTS，费用读 API-KEY，确认与质量边界读 BEHAVIOR-RULES。Agent 负责整理和提出建议，用户负责逐产品核对图文、价格及译文；不能自行勾选批准。

## Agent 执行规则

1. `catalog.inspect` 检查并保存库修订；图片先上传，逐 SKU 显式选择 asset_id，不按文件顺序或模型猜测绑图。
2. `catalog.translate` 可选，调用平台模型后只得到待确认候选；禁止使用宿主模型伪装平台翻译结果。也可提交用户自备译文。
3. 用户核对名称、规格、价格、币种、单位、译文和主图后，执行 `catalog.review` 冻结单语言目录，再执行 `catalog.generate`。源文变化使旧译文待复核；未经确认不得生成。
4. 改价、换图或改规格先保存新库版本，再确认、生成；`catalog.compare` 仅比较同库同语言的确认目录；`catalog.export` 免费导出成功目录的源数据和交付包。
5. 任何质量不通过、SKU缺失、字体或图片加载失败都不能描述为完整交付。不得擅自删产品、截断描述、改事实、无限缩字或替用户确认。

## 参考资料

按任务读取，无需预读全部资料。

- [API密钥与计费](https://ai-skills.open-idea.net/skill-docs/product-catalog/API-KEY.md)
- [HTTP请求、上传与轮询](https://ai-skills.open-idea.net/skill-docs/product-catalog/HTTP-REQUESTS.md)
- [操作参数与产品样例](https://ai-skills.open-idea.net/skill-docs/product-catalog/OPERATIONS.md)
- [授权、私有存储与质量边界](https://ai-skills.open-idea.net/skill-docs/product-catalog/BEHAVIOR-RULES.md)
