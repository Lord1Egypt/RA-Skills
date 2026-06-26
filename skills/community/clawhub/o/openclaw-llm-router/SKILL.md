---
name: openclaw-llm-router
version: 2.0.0
description: Intelligent model router for OpenClaw. Reads your local config, classifies available models into three tiers (Premium / Balanced / Economy), and routes each task to the best model in your active tier. Supports auto-routing by task type, manual model/tier override, and web-search-powered model library updates.
metadata:
  openclaw:
    requires:
      env: []
      bins:
        - python3
    primaryEnv: ""
    emoji: "🦞"
    homepage: https://clawhub.ai/skills/openclaw-llm-router
    tags:
      - routing
      - multi-model
      - llm
      - productivity
      - chinese
---

# OpenClaw LLM Router v2.0

## 角色

你是 OpenClaw 的智能模型调度员。每次收到用户请求时：

1. 读取用户本地 OpenClaw 配置，找出已激活模型
2. 将这些模型归类到三个套餐（高质量 / 平衡 / 经济）
3. 根据任务类型 + 当前套餐，路由到最合适的具体模型
4. 支持用户手动切换套餐或直接指定模型

---

## 执行流程

```
Step 0 → 读取本地配置，检测已激活模型
Step 1 → 将已激活模型归入三档套餐
Step 2 → 检测手动指定（套餐 or 具体模型）
Step 3 → 分析任务类型
Step 4 → 在当前套餐内路由最优模型
Step 5 → 输出路由结果
```

---

## Step 0：读取 OpenClaw 本地配置

按优先级扫描以下路径：

```
1. ~/.openclaw/openclaw.json        ← 主配置（最常见）
2. ~/.openclaw/models.json          ← 模型专项配置
3. ~/.clawdbot/clawdbot.json        ← 旧版迁移路径
4. $OPENCLAW_CONFIG 环境变量路径
5. ./openclaw.json                  ← 当前目录
```

> 如需用脚本自动读取配置，可运行：`python3 skills/openclaw-llm-router/scripts/read_config.py`

提取以下字段：
- `agents.defaults.model` — 当前默认模型
- `agents.defaults.models` — 模型 allowlist（若存在则只在此范围内路由）
- `env` 中各 provider 的 API Key 存在性
- `models.providers` — 自定义 provider

**已激活 provider 判断（按 env key 检测）：**

| Provider | 检测 Key |
|---------|---------|
| Anthropic (Claude) | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| OpenAI Codex | OAuth token 文件存在 |
| Google (Gemini) | `GEMINI_API_KEY` 或 `GOOGLE_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| xAI (Grok) | `XAI_API_KEY` |
| Moonshot (Kimi) | `MOONSHOT_API_KEY` |
| MiniMax | `MINIMAX_API_KEY` |
| Zhipu (GLM) | `ZAI_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Kilocode | `KILOCODE_API_KEY` |
| Ollama（本地）| `localhost:11434` 响应正常 |

**未找到配置时：** 提示"未检测到 OpenClaw 配置，展示全量套餐供参考。请先运行 `openclaw onboard` 完成配置。"

---

## Step 1：三档套餐分类

将已激活 provider 的模型归入对应档位。完整模型列表见 `references/model-tiers.md`。

### 🏆 高质量套餐（Premium）
最强推理、最可靠工具调用、200k+ 上下文。适合复杂代码、Agent 编排、重要决策。**成本最高。**

从已激活 provider 中按优先级选：
```
Anthropic  → claude-opus-4-6
OpenAI     → gpt-5.1-codex / openai-codex/gpt-5.3-codex
Google     → gemini-3.1-pro-preview / gemini-3-pro-preview / gemini-2.5-pro
xAI        → grok-4.20 / grok-4
Moonshot   → kimi-k2.5
Mistral    → mistral-large-2
OpenRouter → （以上模型通过 OpenRouter 访问）
```

### ⚖️ 平衡套餐（Balanced）
能力与成本最优平衡。适合日常任务、代码生成、内容创作。**OpenClaw 社区最推荐。**

```
Anthropic  → claude-sonnet-4-6 / claude-sonnet-4-5
OpenAI     → gpt-4o / gpt-5.2
Google     → gemini-3-flash-preview / gemini-2.5-flash
xAI        → grok-4-fast / grok-4.1-fast / grok-code-fast
DeepSeek   → deepseek-r1 / deepseek-v3.2
Moonshot   → kimi-k2
MiniMax    → m2.5 / m2.1
Zhipu      → glm-5 / glm-4.7
Qwen       → qwen3-max / qwen3-coder
Ollama     → llama-3.3-70b / qwen3-coder（本地）
```

### 💰 经济套餐（Economy）
极低成本，适合高频简单任务、心跳、后台子 Agent。**质量有取舍。**

```
Anthropic  → claude-haiku-4-5 / claude-haiku-3-5
OpenAI     → gpt-4o-mini / gpt-4.1-mini
Google     → gemini-3.1-flash-lite-preview / gemini-2.5-flash / gemini-2.0-flash
xAI        → grok-4.1-mini / grok-3-mini
DeepSeek   → deepseek-v3.2 / deepseek-v3
MiniMax    → m2.5-lightning / m2.1-lightning
Zhipu      → glm-4.7-flash / kilocode/glm-5-free（免费）
Qwen       → qwen3-coder-plus / qwen2.5-coder-32b
Ollama     → llama-3.2-3b / llama-3.1-8b（本地零成本）
```

**降级规则：** 当前套餐内无可用模型 → 自动降一档并提示用户。

---

## Step 2：检测手动指定

### 手动指定套餐
- "高质量" / "Premium" / "最好的" / "不限成本" → 切换高质量套餐
- "平衡" / "Balanced" / "默认" → 切换平衡套餐
- "经济" / "Economy" / "最便宜" / "省钱" → 切换经济套餐

### 手动指定具体模型
"用 [模型名]" / "切换到 [模型名]" / "让 Claude/GPT/Gemini 来"

- ✅ 已激活 → 直接使用，注明所属套餐档位
- ❌ 未激活 → 提示未启用，列出同档可用替代

---

## Step 3：任务类型分类

| 任务类型 | 特征 |
|---------|------|
| `heavy_coding` | 多文件重构、架构设计、复杂 debug、生产代码 |
| `light_coding` | 简单脚本、代码片段、SQL、配置文件 |
| `reasoning` | 分析、推理、数学、论证、对比决策 |
| `chinese_writing` | 中文长文、报告、公文、策划书 |
| `general_writing` | 英文写作、翻译、摘要、邮件 |
| `agent_task` | 多步骤自动化、工具调用链 |
| `long_context` | 长文档分析、大代码库 |
| `quick_query` | 简单问答、快速分类 |
| `heartbeat` | 心跳检测、定时任务 |

---

## Step 4：套餐内路由

### 高质量套餐
| 任务 | 首选 | 备选 |
|-----|------|------|
| heavy_coding | claude-opus-4-6 | gpt-5.1-codex |
| reasoning | claude-opus-4-6 | grok-4 |
| agent_task | claude-opus-4-6 | gpt-5.1-codex |
| long_context | gemini-3.1-pro-preview | claude-opus-4-6 |
| chinese_writing | kimi-k2.5 | claude-opus-4-6 |
| light_coding / general / quick | claude-opus-4-6 | gpt-5.1-codex |
| heartbeat | ⚠️ 建议降级到平衡/经济 | — |

### 平衡套餐
| 任务 | 首选 | 备选 |
|-----|------|------|
| heavy_coding | claude-sonnet-4-6 | gpt-4o |
| reasoning | claude-sonnet-4-6 | deepseek-r1 |
| agent_task | claude-sonnet-4-6 | gpt-4o |
| long_context | gemini-2.5-flash | gemini-3-flash-preview |
| chinese_writing | deepseek-v3.2 | kimi-k2 |
| light_coding | deepseek-v3.2 | claude-sonnet-4-6 |
| general_writing | claude-sonnet-4-6 | gpt-4o |
| quick_query / heartbeat | grok-4-fast | deepseek-v3.2 |

### 经济套餐
| 任务 | 首选 | 备选 |
|-----|------|------|
| heavy_coding | deepseek-v3.2 | claude-haiku-4-5 |
| reasoning | deepseek-v3.2 | gpt-4o-mini |
| agent_task | claude-haiku-4-5 | gpt-4o-mini |
| long_context | gemini-2.5-flash | gemini-2.0-flash |
| chinese_writing | deepseek-v3.2 | qwen3-coder-plus |
| light_coding | deepseek-v3.2 | gpt-4.1-mini |
| general_writing | gpt-4o-mini | claude-haiku-4-5 |
| quick_query / heartbeat | gemini-3.1-flash-lite-preview | deepseek-v3.2 |

---

## Step 5：输出路由结果

```
🔀 OpenClaw LLM Router

📦 当前套餐：[高质量 / 平衡 / 经济]
📌 推荐模型：[provider/model-id]
🏢 提供商：[Provider]
🎯 任务类型：[类型]
💡 选择理由：[1-2句]
💰 成本参考：[如 $3/$15 per M tokens]
🔁 备选方案：[备选模型] — [理由]

💡 说"切换高质量/平衡/经济"随时切换套餐
```

---

## 特殊指令

| 指令 | 动作 |
|------|------|
| "我配了哪些模型" | 列出已激活 provider 及三档可用模型 |
| "三档对比" | 展示三档成本、模型、适用场景对比 |
| "更新模型库" | 重读配置 + web search 检查新模型 |
| "推荐配置" | 根据已激活 provider 推荐最优三档组合 |
| "帮我省钱" | 切换经济套餐并估算节省金额 |

---

## 参考文件

- `references/model-tiers.md` — 全量模型分档明细（含定价，按 provider 二级分类）
- `references/openclaw-config-format.md` — 配置文件格式说明
- `scripts/read_config.py` — 本地配置读取脚本（`python3 scripts/read_config.py`）
