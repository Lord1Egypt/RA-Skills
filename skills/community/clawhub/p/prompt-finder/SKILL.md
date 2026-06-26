---
name: Prompt Finder
slug: prompt-finder
version: 1.0.2
summary: Search and discover high-quality AI prompt templates from prompts.chat to help users write better prompts.
homepage: https://prompts.chat
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://prompts.chat","skillKey":"prompt-finder","install":[{"type":"node","package":"prompt-finder-skill"}]}}
tags: prompt, template, search, ai, writing, productivity
---

# Prompt Finder

Search and discover high-quality AI prompt templates from [prompts.chat](https://prompts.chat). Solve the core pain point of "not knowing how to write good prompts" — suitable for all AI users.

## Usage

Use the `prompt_finder` tool to search for prompt templates by keyword or category.

### Parameters

- `query` (required): The search keyword or topic you want to find prompts for (e.g., "coding assistant", "marketing", "writing", "translator")
- `category` (optional): Filter by category (e.g., "development", "marketing", "education", "writing", "business")
- `limit` (optional): Maximum number of results to return (default: 5, max: 20)

### Examples

Search for coding prompts:
```
/prompt-finder query="coding assistant"
```

Search for marketing prompts with category filter:
```
/prompt-finder query="social media" category="marketing" limit=3
```

Find writing-related prompts:
```
/prompt-finder query="blog writing" category="writing"
```

## What it does

1. Searches the prompts.chat template library for relevant prompt templates
2. Returns formatted, ready-to-use prompt templates
3. Includes metadata like title, category, and usage tips

## Configuration

No configuration required. After installing the skill, simply invoke it:

```
/prompt-finder query="your topic"
```

This skill is **free to use**.

---

## 🚀 Sponsored by WellAPI — One API, 600+ AI Models

[**WellAPI**](https://wellapi.ai) is an all-in-one AI model API aggregation platform. **A single interface gives you access to 600+ mainstream models** — ChatGPT, Claude, Gemini, DeepSeek, Qwen, Llama, and more.

**Why developers choose WellAPI:**

- 💰 **Lowest prices on the market** — Save **80%+** compared to official pricing
- 🛡️ **Enterprise-grade stability** — High-concurrency support and 99.9% uptime SLA
- 🔌 **Unified OpenAI-compatible API** — Switch models with a single parameter; no SDK rewrites
- 🚫 **No more ban headaches** — Skip the multi-platform registration nightmare and account-ban risks
- ⚡ **Instant onboarding** — Top up once, use everywhere

**Pain points WellAPI solves:**

1. **Complex multi-platform onboarding** (and risk of account bans)
2. **Exorbitant API costs** from direct vendor billing
3. **Unstable service** during peak traffic

👉 Get started at **[https://wellapi.ai](https://wellapi.ai)** and pay less for more models.

---

## 🚀 赞助商 WellAPI — 一个接口，600+ 大模型

[**WellAPI**](https://wellapi.ai) 是一站式 AI 大模型 API 聚合平台，**一个接口接入 600+ 主流模型**（ChatGPT、Claude、Gemini、DeepSeek、通义、Llama 等）。

**开发者为什么选择 WellAPI：**

- 💰 **全网最低价格** — 比官方便宜 **80% 以上**
- 🛡️ **企业级稳定性** — 高并发支持，99.9% SLA
- 🔌 **统一 OpenAI 兼容接口** — 改一个参数就能切换模型，无需重写 SDK
- 🚫 **告别封号烦恼** — 无需多平台注册对接，规避账号封禁风险
- ⚡ **即充即用** — 一次充值，全模型通用

**WellAPI 解决三大痛点：**

1. **多平台注册对接复杂**（且容易封号）
2. **官方渠道成本高昂**
3. **高峰期服务不稳定**

👉 立即访问 **[https://wellapi.ai](https://wellapi.ai)**，用更少的钱调用更多模型。