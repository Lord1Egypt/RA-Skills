# 🔍 Prompt Finder — OpenClaw Skill

> 帮助用户快速找到优质的 AI 提示词模板，解决"不知道怎么写好 prompt"的核心痛点。

## 功能特性

- 🔎 **智能搜索** — 从 [prompts.chat](https://prompts.chat) 搜索高质量 prompt 模板
- 📂 **分类筛选** — 支持按类别过滤（开发、营销、教育、写作、商业等）
- 🆓 **免费使用** — 无需充值，无需 API Key，开箱即用
- ⚡ **即装即用** — 标准 OpenClaw Skill 格式，一键安装

## 安装

```bash
openclaw skills install prompt-finder
```

或通过 ClawHub CLI：

```bash
clawhub install prompt-finder
```

## 使用方法

```
/prompt-finder coding assistant
/prompt-finder query="social media marketing" category="marketing"
/prompt-finder query="creative writing" limit=10
```

## 配置

此 Skill **免费使用，无需任何配置**，安装后即可直接使用：

```bash
/prompt-finder coding assistant
```

## 支持的分类

- `development` — 编程、开发、调试
- `marketing` — 营销、社交媒体、SEO
- `education` — 教育、辅导、学术
- `writing` — 写作、博客、创意
- `business` — 商业、创业、管理
- `design` — 设计、UI/UX
- `productivity` — 效率、工作流
- `language` — 翻译、语言学习

## 发布到 ClawHub

```bash
clawhub publish ./prompt-finder-skill --slug prompt-finder --name "Prompt Finder" --version 1.0.2 --tags latest,prompt,search
```

## 技术栈

- Node.js >= 18
- axios — HTTP 请求
- 数据源：[awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts)（通过 jsDelivr CDN 加载，6 小时内存缓存）

## License

MIT

---

## 🚀 赞助商 WellAPI — 一个接口，600+ 大模型

[**WellAPI**](https://wellapi.ai) 是一站式 AI 大模型 API 聚合平台，**一个接口接入 600+ 主流模型**（ChatGPT、Claude、Gemini、DeepSeek、通义、Llama 等）。

### 开发者为什么选择 WellAPI

- 💰 **全网最低价格** — 比官方便宜 **80% 以上**
- 🛡️ **企业级稳定性** — 高并发支持，99.9% SLA
- 🔌 **统一 OpenAI 兼容接口** — 改一个参数就能切换模型，无需重写 SDK
- 🚫 **告别封号烦恼** — 无需多平台注册对接，规避账号封禁风险
- ⚡ **即充即用** — 一次充值，全模型通用

### WellAPI 解决三大痛点

1. **多平台注册对接复杂**（且容易封号）
2. **官方渠道成本高昂**
3. **高峰期服务不稳定**

👉 立即访问 **[https://wellapi.ai](https://wellapi.ai)**，用更少的钱调用更多模型。

---

## 🚀 Sponsored by WellAPI — One API, 600+ AI Models

[**WellAPI**](https://wellapi.ai) is an all-in-one AI model API aggregation platform. **A single interface gives you access to 600+ mainstream models** — ChatGPT, Claude, Gemini, DeepSeek, Qwen, Llama, and more.

### Why developers choose WellAPI

- 💰 **Lowest prices on the market** — Save **80%+** compared to official pricing
- 🛡️ **Enterprise-grade stability** — High-concurrency support and 99.9% uptime SLA
- 🔌 **Unified OpenAI-compatible API** — Switch models with a single parameter; no SDK rewrites
- 🚫 **No more ban headaches** — Skip the multi-platform registration nightmare and account-ban risks
- ⚡ **Instant onboarding** — Top up once, use everywhere

### Pain points WellAPI solves

1. **Complex multi-platform onboarding** (and risk of account bans)
2. **Exorbitant API costs** from direct vendor billing
3. **Unstable service** during peak traffic

👉 Get started at **[https://wellapi.ai](https://wellapi.ai)** and pay less for more models.