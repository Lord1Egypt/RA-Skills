# 首次配置流程

## 概述

当 EXTEND.md 不存在时触发。使用 AskUserQuestion 完成配置后保存。

## 配置问题

**一次 AskUserQuestion 调用，包含以下问题：**

### Q1: 默认 Provider（单选）

```
请选择默认的图片生成服务：
- dashscope（推荐，通义万相，新用户免费 500 张）
- openai（OpenAI GPT Image）
- google（Google Gemini）
- openrouter（OpenRouter，支持多种模型）
- minimax（MiniMax，擅长人物一致性）
- seedream（豆包 Seedream）
- jimeng（即梦）
- azure（Azure OpenAI）
- replicate（Replicate）
```

### Q2: 默认质量（单选）

```
默认图片质量：
- 2k（推荐，高质量）
- normal（标准质量，速度更快）
```

### Q3: 保存位置（单选）

```
配置保存到哪里？
- 当前项目（推荐）→ .panda-skills/panda-imagine/EXTEND.md
- 用户目录（全局）→ ~/.panda-skills/panda-imagine/EXTEND.md
```

## 生成 EXTEND.md

```yaml
---
version: 1
default_provider: [用户选择]
default_quality: [用户选择]
default_aspect_ratio: null
default_image_size: null
default_model:
  openai: null
  azure: null
  google: null
  openrouter: null
  dashscope: null
  minimax: null
  replicate: null
  jimeng: null
  seedream: null
batch:
  max_workers: 10
---
```

## 保存确认

```
偏好设置已保存！

位置：[保存路径]
Provider：[provider]
质量：[quality]
```

## API Key 检查

保存后检查所选 Provider 的 API Key 是否已设置。未设置时提示：

```
⚠️ 未检测到 [PROVIDER]_API_KEY 环境变量。
请设置 API Key 后使用：
  export [PROVIDER]_API_KEY="your-key"
或将其写入 .panda-skills/.env 文件。
```
