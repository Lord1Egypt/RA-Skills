---
name: Harena
description: "AI 交易信息工作台 | AI Trading Intelligence Workbench. 24/7 市场监控、新闻分析、交易信号、智能预警，通过 MCP 协议接入 Claude/OpenClaw 等 AI 助手。触发词：市场分析、每日简报、交易信号、突发事件、行情监控、trading signals、market briefing、alerts、crypto analysis、stock analysis."
version: 0.3.3
author: Harena Team
metadata:
  openclaw:
    requires:
      env:
        - HARENA_API_KEY
    primaryEnv: HARENA_API_KEY
    emoji: "📊"
    homepage: https://harena.world
---

# Harena — AI 交易信息工作台 | AI Trading Intelligence

为你的 AI 助手提供实时金融市场数据、个性化新闻分析、交易信号和智能预警能力。覆盖加密货币和美股市场。

Give your AI assistant real-time access to financial market data, personalized news analysis, trading signals, and smart alerts — covering crypto and US stocks.

## 重要：使用 MCP 工具，不要猜 API 路径

**所有操作都通过 MCP 工具完成，不要用 curl 或 HTTP 请求调用 API。** Harena 的功能通过 MCP 协议暴露为 12 个工具，直接调用即可。

## 注册新账号 | Register (通过 MCP 工具)

注册不需要 API Key，使用两个 MCP 工具完成：

1. **调用 `get_questionnaire` 工具**（无需参数）→ 获取 4 道注册问卷
2. 向用户提问，收集答案
3. **调用 `submit_questionnaire` 工具**（传入 answers）→ 返回 `user_id` 和 `api_key`
4. 后续工具调用传入获得的 `api_key`

**不要用 curl 或 HTTP 请求注册，直接用 MCP 工具。**

## 获取 API Key（已有账号）

如果已有账号，可通过网页获取 Key：访问 [www.harena.world/install](https://www.harena.world/install)

设置环境变量：

```bash
export HARENA_API_KEY="your-key-here"
```

## MCP 连接配置 | Connect via MCP

**Claude Desktop:**

Settings → Developer → MCP Servers:

```json
{
  "mcpServers": {
    "harena": {
      "url": "https://www.harena.world/mcp/sse",
      "headers": { "X-API-Key": "$HARENA_API_KEY" }
    }
  }
}
```

**Claude Code:**

```bash
claude mcp add harena https://www.harena.world/mcp/sse --transport sse --header "X-API-Key: $HARENA_API_KEY"
```

**OpenClaw:**

```bash
npx clawhub@latest install harena
export HARENA_API_KEY="your-key-here"
```

## 重要规则 | Important Rules

1. **始终使用 MCP 工具**，不要用 curl/fetch/HTTP 请求调用任何 Harena API
2. **注册新账号**：调用 `get_questionnaire` → 收集答案 → 调用 `submit_questionnaire`
3. **所有认证工具**需要传 `api_key` 参数（注册后获得的 key）
4. **不要猜测 API 路径**，所有功能都通过下方列出的 MCP 工具完成

## 可用工具 | Available Tools (12)

### 市场数据与分析 | Market Data & Analysis

| 工具 Tool | 说明 Description |
|-----------|-----------------|
| `get_daily_briefing` | 个性化每日简报 — 持仓价格、市场概览、恐惧贪婪指数、涨跌排行、精选新闻 |
| `get_alerts` | 突发事件 — 价格异动(>5%)、极端市场情绪、DeFi TVL 暴跌、强交易信号 |
| `analyze_symbol` | 深度分析 — 综合近期新闻和交易信号，通过 LLM 生成分析报告 |
| `get_topic_feed` | 主题资讯 — 按主题过滤新闻流（DeFi、AI概念、Meme币、半导体、宏观等） |

### 投资组合管理 | Portfolio Management

| 工具 Tool | 说明 Description |
|-----------|-----------------|
| `manage_watchlist` | 管理关注列表 — 添加/删除/查看关注标的（BTC、ETH、NVDA 等） |
| `get_topics` | 浏览主题 — 按市场筛选可用主题 |
| `manage_topics` | 订阅管理 — 订阅/取消订阅主题分类 |

### 个人设置 | Profile & Settings

| 工具 Tool | 说明 Description |
|-----------|-----------------|
| `get_profile` | 查看交易风格、风险偏好、关注市场 |
| `set_profile` | 更新个人偏好 — AI 据此个性化推荐内容 |
| `check_subscription` | 查看订阅方案和每日用量 |

### 注册 | Register (无需 API Key | No Auth Needed)

| 工具 Tool | 说明 Description |
|-----------|-----------------|
| `get_questionnaire` | 注册第 1 步 — 获取注册问卷（关注市场、交易风格、风险偏好），无需 api_key |
| `submit_questionnaire` | 注册第 2 步 — 提交答案，创建账号，返回 user_id 和 api_key，无需 api_key |

## 执行流程 | How It Works

```
1. AI 助手调用 Harena MCP 工具（如 get_daily_briefing）
2. Harena 后端验证 API Key，检查用量配额
3. 从 10+ 数据源实时聚合数据（CoinGecko、Bloomberg、Reuters、DeFiLlama 等）
4. AI 引擎分析处理，结合用户画像个性化排序
5. 返回结构化 JSON 结果
6. AI 助手解读结果，用自然语言回复用户
```

## 输出示例 | Output Examples

**`get_daily_briefing` 返回：**

```json
{
  "watchlist": [
    {"symbol": "BTC", "title": "BTC 24h: $67,234 ↑3.2%", "time_ago": "5 分钟前"}
  ],
  "market_overview": {"title": "全球市场概览", "summary": "加密市场总市值...", "time_ago": "10 分钟前"},
  "fear_greed": {"title": "恐惧贪婪指数：72", "summary": "市场情绪：贪婪"},
  "top_news": [
    {"id": 1, "title": "Fed 维持利率不变", "source": "reuters", "sentiment": "positive"}
  ],
  "topic_sections": [{"name": "DeFi", "news": [...]}],
  "defi_updates": [{"title": "Aave TVL 突破 $20B"}]
}
```

**`get_alerts` 返回：**

```json
{
  "alerts": [
    {
      "id": "price-BTC",
      "type": "price",
      "level": "high",
      "direction": "up",
      "title": "BTC 24h 涨幅 8.5%",
      "symbol": "BTC",
      "time_ago": "2 分钟前"
    }
  ],
  "ai_analysis": "BTC 突破关键阻力位，市场情绪转向贪婪...",
  "analysis_generated_at": "2026-04-14T10:00:00Z"
}
```

## 错误处理 | Error Handling

| 错误 Error | 说明 Description | 处理 Action |
|-----------|-----------------|------------|
| `API key required` | 未传 api_key 参数 | 在工具调用中包含 api_key |
| `Invalid API key` | Key 不存在 | 检查 Key 是否正确，或重新生成 |
| `Account is inactive` | 账户已停用 | 联系管理员 |
| `Daily quota exceeded` | 每日调用次数超限 | 等待次日重置，或升级到 Pro |
| `Rate limit (429)` | 请求过于频繁 | 等待后重试 |

## 数据源 | Data Sources (10+)

CoinGecko · CoinMarketCap · Bloomberg · Reuters · DeFiLlama · SEC Filings · Yahoo Finance · TradingView · 链上数据 · Reddit · 社交媒体

## 覆盖市场 | Markets

- **加密货币 Crypto**: BTC、ETH、SOL 等 100+ 币种
- **美股 US Stocks**: NVDA、TSLA、AAPL 等
- **宏观 Macro**: 美联储、CPI、GDP、利率

## 定价 | Pricing

| | 免费版 Free | Pro |
|---|---|---|
| 每日简报 | ✓ | ✓ |
| 基础交易信号 | ✓ | ✓ |
| 新闻聚合 | ✓ | ✓ |
| 自定义关注列表 | ✓ (最多10个) | ✓ (无限) |
| MCP 接入 | ✓ | ✓ |
| 无限 AI 分析 | — | ✓ |
| 实时预警 | — | ✓ |
| 优先 API 调用 | — | ✓ |

## 安全声明 | Security

- **只读操作** — 不触发任何交易下单
- **API Key 认证** — 每个用户独立 Key，权限隔离
- **加密传输** — 所有数据通过 HTTPS 传输
- **不存储交易账户** — 仅收集关注列表用于个性化

## 示例对话 | Example Prompts

- "今天加密市场怎么样？" / "What's happening in crypto today?"
- "有没有突发事件？" / "Any breaking alerts?"
- "分析一下 NVDA" / "Analyze NVDA for me"
- "帮我关注 BTC 和 ETH" / "Add BTC and ETH to my watchlist"
- "最新的 DeFi 动态" / "Show me DeFi news"
- "恐惧贪婪指数是多少？" / "What's the fear and greed index?"
- "订阅 AI 和半导体主题" / "Subscribe to AI and semiconductor topics"

## 链接 | Links

- 官网 Website: [harena.world](https://harena.world)
- 安装引导 Install: [harena.world/install](https://www.harena.world/install)
- MCP 文档 Docs: [harena.world/mcp/docs](https://www.harena.world/mcp/docs)
- 服务发现 Discovery: [harena.world/.well-known/mcp.json](https://www.harena.world/.well-known/mcp.json)
