# 全量模型分档明细 (Model Tiers Reference)

> 数据来源：各 provider 官方定价页 + OpenClaw 社区，2026年3月验证
> 价格单位：$ per million tokens（输入/输出）
> ⭐ = OpenClaw 社区高频推荐

---

## 🏆 高质量套餐 (Premium)

**特征**：顶级推理、最可靠工具调用、200k+ 上下文、抗 prompt 注入最强
**月费参考**：轻度 $80-150 / 中度 $200-400 / 重度 $500+

### Anthropic — Claude

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `anthropic/claude-opus-4-6` | Claude Opus 4.6 ⭐ | $15 | $75 | 200k | OpenClaw 首选，工具调用最可靠 |
| `opencode/claude-opus-4-6` | Claude Opus 4.6 (via OpenCode) | — | — | 200k | OpenCode Zen 订阅用户 |

### OpenAI — GPT

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `openai/gpt-5.1-codex` | GPT-5.1 Codex ⭐ | ~$10 | ~$30 | 1M+ | 最强代码能力 |
| `openai-codex/gpt-5.3-codex` | GPT-5.3 Codex (OAuth) | ChatGPT订阅 | — | 266k | OAuth 免 API Key |
| `openai/gpt-5.4` | GPT-5.4 | 待定 | 待定 | — | 2026.3 新发布 |

### Google — Gemini

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `google/gemini-3.1-pro-preview` | Gemini 3.1 Pro ⭐ | ~$3.5 | ~$10.5 | 2M | 最大上下文，适合长文档 |
| `google/gemini-3-pro-preview` | Gemini 3 Pro | ~$3.5 | ~$10.5 | 2M | 同上，旧别名 |
| `google/gemini-2.5-pro` | Gemini 2.5 Pro | $3.5 | $10.5 | 1M | 稳定可用版 |

### xAI — Grok

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `xai/grok-4.20` | Grok 4.20 | ~$5 | ~$15 | 131k | 最新旗舰 |
| `xai/grok-4` | Grok 4 | ~$3 | ~$10 | 131k | 强推理+实时信息 |

### Moonshot — Kimi

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `moonshot/kimi-k2.5` | Kimi K2.5 ⭐ | ~$0.5 | ~$1.5 | 128k | 中文最强旗舰，性价比高 |

### Mistral

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `mistral/mistral-large-2` | Mistral Large 2 | $3 | $9 | 128k | 欧洲合规，多语言 |

---

## ⚖️ 平衡套餐 (Balanced)

**特征**：能力与成本最优平衡，OpenClaw 社区最多人日常使用
**月费参考**：轻度 $15-30 / 中度 $40-80 / 重度 $100-200

### Anthropic — Claude

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `anthropic/claude-sonnet-4-6` | Claude Sonnet 4.6 ⭐⭐ | $3 | $15 | 200k | **OpenClaw 第一推荐**，工具调用最稳 |
| `anthropic/claude-sonnet-4-5` | Claude Sonnet 4.5 | $3 | $15 | 200k | 上一代稳定版 |
| `opencode/claude-sonnet-4-6` | Claude Sonnet (via OpenCode) | — | — | 200k | OpenCode Zen 订阅 |

### OpenAI — GPT

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `openai/gpt-4o` | GPT-4o ⭐ | $2.5 | $10 | 128k | 生态最成熟，工具丰富 |
| `openai/gpt-5.2` | GPT-5.2 | ~$5 | ~$15 | 200k | 新一代平衡款 |

### Google — Gemini

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `google/gemini-3-flash-preview` | Gemini 3 Flash ⭐ | ~$0.3 | ~$1.2 | 1M | 快速+大上下文，性价比高 |
| `google/gemini-2.5-pro` | Gemini 2.5 Pro | $3.5 | $10.5 | 1M | 稳定版旗舰 |
| `google/gemini-2.5-flash` | Gemini 2.5 Flash | $0.5 | $1.5 | 1M | 快速平衡款 |

### xAI — Grok

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `xai/grok-4-fast` | Grok 4 Fast ⭐ | $0.8 | $2 | 131k | 快速版，性价比好 |
| `xai/grok-4.1-fast` | Grok 4.1 Fast | $0.8 | $2 | 131k | 同上，新版 |
| `xai/grok-code-fast` | Grok Code Fast | $0.5 | $1.5 | 131k | 代码专项 |

### DeepSeek

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `deepseek/deepseek-r1` | DeepSeek R1 ⭐ | $0.55 | $2.19 | 128k | 推理+代码，极高性价比 |
| `deepseek/deepseek-v3.2` | DeepSeek V3.2 ⭐ | $0.28 | $0.42 | 128k | 日常主力，最流行预算选择 |
| `deepseek/deepseek-v3.1` | DeepSeek V3.1 | $0.28 | $0.42 | 128k | 上一版本 |

### Moonshot — Kimi

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `moonshot/kimi-k2` | Kimi K2 | ~$0.3 | ~$1 | 128k | 中文强，中档价位 |

### MiniMax

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `minimax/m2.5` | MiniMax M2.5 ⭐ | ~$0.3 | ~$1.1 | 1M | 超长上下文，中文友好 |
| `minimax/m2.1` | MiniMax M2.1 | ~$0.2 | ~$0.8 | 1M | 稳定前代 |

### Zhipu — GLM

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `zai/glm-5` | GLM-5 ⭐ | ~$0.5 | ~$1.5 | 128k | 最新旗舰，中文专优 |
| `zai/glm-4.7` | GLM-4.7 | ~$0.3 | ~$0.9 | 128k | 稳定主力 |

### Qwen（阿里）

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `qwen/qwen3-max` | Qwen3 Max | ~$0.5 | ~$1.5 | 128k | 综合旗舰 |
| `qwen/qwen3-coder` | Qwen3 Coder | ~$0.5 | ~$2 | 128k | 代码专项 |
| `qwen/qwen3.5-397b` | Qwen3.5 397B | ~$1 | ~$3 | 32k | 超大参数量 |

### Ollama（本地部署）

| 模型 ID | 名称 | 费用 | 上下文 | 亮点 |
|--------|------|------|--------|------|
| `ollama/llama-3.3-70b` | Llama 3.3 70B ⭐ | $0 | 128k | 本地最强，需好硬件 |
| `ollama/qwen3-coder` | Qwen3 Coder (本地) | $0 | 32k | 本地代码专用 |
| `ollama/mistral-large` | Mistral Large (本地) | $0 | 128k | 本地多语言 |

---

## 💰 经济套餐 (Economy)

**特征**：极低成本，适合高频简单任务、心跳、后台工作。质量有取舍。
**月费参考**：轻中度 $5-15 / 重度通常 <$30

### Anthropic — Claude

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `anthropic/claude-haiku-4-5` | Claude Haiku 4.5 ⭐ | $0.8 | $4 | 200k | 最快 Claude，工具调用仍可靠 |
| `anthropic/claude-haiku-3-5` | Claude Haiku 3.5 | $0.8 | $4 | 200k | 上一代，更稳定 |

### OpenAI — GPT

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `openai/gpt-4o-mini` | GPT-4o mini ⭐⭐ | $0.15 | $0.60 | 128k | **经济首选**，100条消息/天约$2-4/月 |
| `openai/gpt-4.1-mini` | GPT-4.1 mini | ~$0.15 | ~$0.60 | 1M | 超长上下文经济款 |

### Google — Gemini

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `google/gemini-3.1-flash-lite-preview` | Gemini 3.1 Flash-Lite ⭐ | $0.05 | $0.20 | 1M | **最便宜可靠云端模型之一** |
| `google/gemini-2.5-flash` | Gemini 2.5 Flash | $0.5 | $1.5 | 1M | 快速，大上下文 |
| `google/gemini-2.0-flash` | Gemini 2.0 Flash | ~$0.1 | ~$0.4 | 1M | 最快响应，<200ms TTFT |

### xAI — Grok

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `xai/grok-4.1-mini` | Grok 4.1 mini | $0.20 | $0.50 | 131k | 75x 便宜于 Opus |
| `xai/grok-3-mini` | Grok 3 Mini | ~$0.15 | ~$0.60 | 131k | 上一代经济款 |
| `xai/grok-3-mini-fast` | Grok 3 Mini Fast | ~$0.1 | ~$0.4 | 131k | 最快轻量版 |

### DeepSeek

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `deepseek/deepseek-v3.2` | DeepSeek V3.2 ⭐⭐ | $0.28 | $0.42 | 128k | **云端最便宜主力**，心跳仅$0.14/月 |
| `deepseek/deepseek-v3` | DeepSeek V3 | $0.27 | $1.10 | 64k | 老版本，仍可用 |

### MiniMax

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `minimax/m2.5-lightning` | M2.5 Lightning ⭐ | ~$0.1 | ~$0.3 | 1M | 极速，超长上下文 |
| `minimax/m2.1-lightning` | M2.1 Lightning | ~$0.08 | ~$0.2 | 1M | 最便宜长上下文 |

### Zhipu — GLM（含免费）

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `zai/glm-4.7-flash` | GLM-4.7 Flash | ~$0.05 | ~$0.15 | 128k | 极低成本中文模型 |
| `kilocode/glm-5-free` | GLM-5 Free ⭐ | $0 | $0 | 128k | 通过 Kilocode 免费使用 |
| `kilocode/minimax-m2.5-free` | M2.5 Free ⭐ | $0 | $0 | 1M | 通过 Kilocode 免费使用 |

### Qwen

| 模型 ID | 名称 | 输入价 | 输出价 | 上下文 | 亮点 |
|--------|------|--------|--------|--------|------|
| `qwen/qwen3-coder-plus` | Qwen3 Coder Plus | ~$0.2 | ~$0.6 | 128k | 经济代码款 |
| `qwen/qwen2.5-coder-32b` | Qwen2.5 Coder 32B | ~$0.15 | ~$0.4 | 128k | 开源部署或API |

### Ollama（本地，零成本）

| 模型 ID | 名称 | 费用 | 上下文 | 亮点 |
|--------|------|------|--------|------|
| `ollama/llama-3.2-3b` | Llama 3.2 3B | $0 | 128k | 最轻量，CPU 可跑 |
| `ollama/llama-3.1-8b` | Llama 3.1 8B | $0 | 128k | 轻量通用 |
| `ollama/qwen2.5-coder-7b` | Qwen2.5 Coder 7B | $0 | 32k | 本地代码小模型 |
| `ollama/deepseek-coder-v2` | DeepSeek Coder V2 (本地) | $0 | 64k | 本地代码专用 |
| `ollama/mistral-small` | Mistral Small (本地) | $0 | 32k | 轻量本地通用 |

---

## 价格速查对比

| 档位 | 代表模型 | 输出价（/M） | 心跳月费 | 日常任务月费 |
|------|---------|------------|---------|------------|
| 高质量 | Claude Opus 4.6 | $75 | ~$130 | $200-400 |
| 高质量 | GPT-5.1 Codex | ~$30 | ~$50 | $80-200 |
| 平衡 | Claude Sonnet 4.6 | $15 | $4.32 | $15-80 |
| 平衡 | DeepSeek R1 | $2.19 | $0.63 | $2-15 |
| 经济 | GPT-4o mini | $0.60 | $0.17 | $2-4 |
| 经济 | DeepSeek V3.2 | $0.42 | $0.14 | $0.80-2 |
| 经济 | Gemini Flash-Lite | $0.20 | $0.06 | $0.40-1 |
| 免费 | GLM-5 Free（Kilocode）| $0 | $0 | $0 |
| 免费 | Ollama 本地模型 | $0 | $0 | $0 |

---

## OpenClaw 配置片段参考

```json
// 三档混合配置示例（openclaw.json）
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-6",
        "fallback": "openai/gpt-4o",
        "economy": "google/gemini-3.1-flash-lite-preview"
      }
    }
  }
}
```
