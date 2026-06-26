---
name: meme-token-analyzer
version: 2.0.1
description: "Meme 代币财富基因检测系统。输入任意代币名称（如 PEPE、DOGE、$SHIB），基于实时 Web 情绪数据输出四维分析报告与 🌟钻石手/🌙登月/🗑️纸手/💩屎币 评级。支持主流币自动识别（BTC/ETH/SOL），无数据时不幻觉。触发词：meme 分析、代币评级、财富基因、PEPE分析、meme coin、rug check、meme token analyze、wealth gene、meme coin rating"
author: AntalphaAI
license: MIT
metadata: {"repository":"https://github.com/AntalphaAI/meme-token-analyzer","mcp":{"url":"https://mcp-skills.ai.antalpha.com/mcp","transport":"streamable-http","tools":[{"name":"meme-analyze","description":"分析 Meme 代币财富基因，输出 🌟/🌙/🗑️/💩 评级报告"}]}}
---

# Meme Token Analyzer 🚀

> **Meme 代币财富基因检测系统 V2**
> 基于 Antalpha MCP Server，接入 llm-proxy 统一管控，全面替代 Coze 方案

---

## 使用前提

需先完成 Agent 注册（获取 `agent_id`）：

```
调用 antalpha-register 工具完成注册，保存 agent_id
```

---

## 核心能力

- 🔍 **实时 Web 搜索**：Tavily API，过滤最近 30 天数据，带 AI 摘要
- 🤖 **LLM 多维分析**：四维分析框架，via llm-proxy 统一计量计费
- 💎 **财富基因评级**：四档精准评级，Degen 风格毒舌点评
- 🧠 **主流币识别**：自动检测 BTC/ETH/SOL 等并切换分析视角
- 🚫 **无幻觉设计**：无数据时明确说明，不编造价格或社区数据

---

## 触发场景

| 用户说 | 自动执行 |
|--------|----------|
| "帮我分析一下 PEPE" | `meme-analyze` |
| "DOGE 的财富基因是什么" | `meme-analyze` |
| "$SHIB 值得买吗" | `meme-analyze` |
| "这个 meme 币怎么样：BONK" | `meme-analyze` |
| "BTC 算 meme 吗" | `meme-analyze`（自动切换价值币视角） |

---

## MCP Tool 说明

### `meme-analyze`

**输入参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `token_name` | string (1–100) | Meme 或社区代币名称/符号，如 PEPE、DOGE、$SHIB、WIF |
| `agent_id` | string | 从 antalpha-register 获取的 Agent ID（'A' + 32 位十六进制，或兼容旧版 UUID） |

**输出结构：**

```json
{
  "token": "PEPE",
  "is_major_coin": false,
  "major_coin_warning": null,
  "rating": "moonshot",
  "rating_emoji": "🌙",
  "rating_label": "登月",
  "report": {
    "narrative_magic": "叙事魔力分析...",
    "community_hype": "社区炒作能力...",
    "risk_warning": "风险提示..."
  },
  "search_summary": "Tavily AI 摘要...",
  "data_freshness": "ok",
  "sources": ["https://...", "https://..."],
  "disclaimer": "本报告仅供娱乐和教育目的，不构成投资建议。"
}
```

**评级标准：**

| 评级值 | Emoji | 中文 | 含义 |
|--------|-------|------|------|
| `diamond_hand` | 🌟 | 钻石手 | 顶级叙事 + 强社区 + VC 背书，万倍潜力 |
| `moonshot` | 🌙 | 登月 | 有效叙事 + 活跃社区，百倍合理预期 |
| `paper_hand` | 🗑️ | 纸手 | 叙事薄弱，高风险 |
| `shitcoin` | 💩 | 屎币 | 无叙事无社区，立即远离 |

---

## 输出示例

```
🌙 PEPE — 登月

🎯 叙事魔力：PEPE 是互联网最具代表性的 Meme 形象，文化底蕴深厚，叙事自带传播力。
📢 社区炒作：Twitter/X 活跃度极高，持仓地址数量庞大，Degen 文化认同感强。
⚠️ 风险提示：高度投机，价格波动极大，注意仓位控制。

📊 数据新鲜度：✅ 充足

💡 本报告仅供娱乐和教育目的，不构成投资建议。DYOR。
```

---

## 注意事项

- 分析结果仅供娱乐和教育参考，不构成任何投资建议
- 主流币（BTC/ETH/SOL 等）会自动切换为价值币分析视角
- 冷门代币可能因 Web 数据不足而返回 `data_freshness: "no_data"`

---

## 技术架构

- **后端**：NestJS + Antalpha MCP Server
- **LLM**：via llm-proxy（统一计量，`fast-cheap` tier）
- **搜索**：Tavily API（30天时间过滤，带 AI 摘要）
- **版本**：v2.0.1（完全替代 Coze LangGraph 方案）

---

**Maintainer**: AntalphaAI | **License**: MIT
