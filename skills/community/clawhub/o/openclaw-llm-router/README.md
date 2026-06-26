# 🦞 OpenClaw LLM Router

**智能多模型路由器** — 自动读取你的 OpenClaw 配置，将可用模型分为三个套餐，按任务类型路由到最合适的模型。

[![ClawHub](https://img.shields.io/badge/ClawHub-openclaw--llm--router-blue)](https://clawhub.ai/skills/openclaw-llm-router)
[![Version](https://img.shields.io/badge/version-2.0.0-green)](https://clawhub.ai/skills/openclaw-llm-router)
[![License](https://img.shields.io/badge/license-MIT--0-lightgrey)](https://clawhub.ai/skills/openclaw-llm-router)

---

## 安装

```bash
clawdhub install openclaw-llm-router
```

安装后**重启 OpenClaw** 使 skill 生效，然后验证：

```bash
openclaw skills list --eligible | grep llm-router
```

---

## 三档套餐

| 套餐 | 代表模型 | 输出价/M | 适合 |
|------|---------|---------|------|
| 🏆 高质量 | Claude Opus 4.6 | $75 | 复杂代码、Agent、重要决策 |
| ⚖️ 平衡 | Claude Sonnet 4.6 | $15 | 日常任务、内容创作（**推荐**）|
| 💰 经济 | GPT-4o mini / DeepSeek V3.2 | $0.42–0.60 | 心跳、快速问答、后台任务 |

---

## 使用方法

### 自动路由
直接提问，路由器自动选择套餐内最优模型：
```
帮我重构这个 Python 模块
→ 🏆 高质量 → claude-opus-4-6（heavy_coding 任务）
```

### 切换套餐
```
切换经济套餐
用平衡模式帮我写一份报告
最好的模型来分析这段代码
```

### 手动指定模型
```
用 DeepSeek 帮我写这篇中文文章
让 GPT-4o 来做这个分析
```

### 查看已配置模型
```
我配了哪些模型
三档套餐对比
```

---

## 支持的 Provider

| Provider | 套餐覆盖 | 检测方式 |
|---------|---------|---------|
| Anthropic (Claude) | 全三档 | `ANTHROPIC_API_KEY` |
| OpenAI (GPT) | 全三档 | `OPENAI_API_KEY` |
| OpenAI Codex | 高质量 | OAuth token |
| Google (Gemini) | 全三档 | `GEMINI_API_KEY` |
| DeepSeek | 平衡 + 经济 | `DEEPSEEK_API_KEY` |
| xAI (Grok) | 全三档 | `XAI_API_KEY` |
| Moonshot (Kimi) | 高质量 + 平衡 | `MOONSHOT_API_KEY` |
| MiniMax | 平衡 + 经济 | `MINIMAX_API_KEY` |
| Zhipu (GLM) | 平衡 + 经济 | `ZAI_API_KEY` |
| Mistral | 高质量 | `MISTRAL_API_KEY` |
| OpenRouter | 全三档（代理）| `OPENROUTER_API_KEY` |
| Kilocode | 全三档（代理）| `KILOCODE_API_KEY` |
| Ollama（本地）| 平衡 + 经济 | localhost:11434 |

---

## 本地配置诊断

```bash
python3 ~/.openclaw/skills/openclaw-llm-router/scripts/read_config.py
```

输出示例：
```
🦞 OpenClaw LLM Router — 配置读取
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 配置文件: ~/.openclaw/openclaw.json

已激活 Providers（3）: anthropic, google, deepseek

🏆 高质量套餐（1 个可用）:
  • anthropic/claude-opus-4-6

⚖️ 平衡套餐（4 个可用）:
  • anthropic/claude-sonnet-4-6
  • google/gemini-3-flash-preview
  • deepseek/deepseek-r1
  • deepseek/deepseek-v3.2

💰 经济套餐（4 个可用）:
  • anthropic/claude-haiku-4-5
  • google/gemini-3.1-flash-lite-preview
  • google/gemini-2.5-flash
  • deepseek/deepseek-v3.2
```

---

## 文件结构

```
openclaw-llm-router/
├── SKILL.md                          # 核心路由逻辑（OpenClaw 加载此文件）
├── README.md                         # 本文档
├── scripts/
│   └── read_config.py                # 配置读取诊断脚本
└── references/
    ├── model-tiers.md                # 全量模型分档明细（含定价）
    └── openclaw-config-format.md     # 配置文件格式说明
```

---

## 更新日志

### v2.0.0
- 全新三档套餐体系（高质量 / 平衡 / 经济）
- 覆盖 13 个 provider、70+ 个模型，含 2026年3月最新定价
- 自动读取 OpenClaw 本地配置，只从已激活模型中路由
- 新增 `read_config.py` 诊断脚本
- 支持 Kilocode 免费模型（GLM-5 Free、MiniMax M2.5 Free）

### v1.0.0
- 初始版本（基础路由逻辑）

---

## 作者

**forrest** — [forrestinfo@gmail.com](mailto:forrestinfo@gmail.com)

> 📄 MIT-0 License — 可自由使用、修改、商用，无需署名
