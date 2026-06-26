---
name: poly-master
description: "Polymarket prediction market skill by Antalpha AI. Discover trending markets, browse event predictions, invest in outcomes, copy-trade top traders, track portfolio & PnL. V3: Antalpha wallet data, trader win-rate enrichment, event money-flow heat, and Poly Master hedge strategy. Trigger: polymarket, prediction market, 预测市场, poly, copy trade, 跟单, wallet profile, 钱包画像, smart money, hedge strategy, 对冲策略, arbitrage, 套利"
version: 3.0.2
metadata: {"mcp":{"url":"https://mcp-skills.ai.antalpha.com/mcp","transport":"streamable-http"},"clawdbot":{"emoji":"🎯"}}
---

# Poly Master v3 — Polymarket 预测市场 + Poly Master 对冲策略

> Powered by **Antalpha AI** — Polymarket 聚合交易、跟单与 LLM 驱动对冲套利

---

## Overview

Poly Master v3 在交易、跟单和对冲策略基础上，新增 **Antalpha 深度数据层**。Agent 可以在用户跟单、查看持仓、评估巨鲸信号、分析市场热度时，用更真实的钱包胜率、PnL、已结算市场数量和事件资金热度辅助解释。

### V3 核心能力

| 能力 | 说明 |
|------|------|
| 🔮 **对冲策略扫描** | LLM 分析市场逻辑蕴含关系，输出 T1/T2/T3 分级套利信号 |
| 🔎 **市场全文搜索** | `poly-master-search-market` 多语言搜索长尾市场（事件/球队/候选人/slug） |
| 🧠 **Antalpha 钱包画像** | 查询钱包 PnL、胜率、最大盈利、已结算市场活动 |
| 👥 **真实交易员榜单** | `poly-master-traders` 返回真实 `winRate` 与 `settledMarkets` |
| 🔥 **事件资金热度** | `poly-trending` / `poly-intel` 可展示 totalVolume、uniqueTraders、top holders |
| 🏗️ **Builder Program 接入** | 所有 CLOB 订单通过 Polymarket Builder Program 路由，享受优先执行和免 Gas 操作 |
| ⛽ **免 Gas 操作** | Relayer 代付链上 Gas，降低交易摩擦 |

---

## Architecture

```
User ←→ AI Agent ←→ Antalpha MCP Server ←→ Polymarket APIs
                          ↕
              ┌───────────┼──────────────┐
              ▼           ▼              ▼
       PolyMasterStrategy  LlmProxy    BuilderModule
       (对冲扫描引擎)   (计量计费)   (X-Builder-Key)
              ↕           ↕              ↕
         Gamma/CLOB    OpenAI API   CLOB/Relayer
```

- **Zero custody**: 私钥不离开用户钱包
- **MCP Protocol**: Streamable HTTP (MCP 2024-11-05)
- **Chain**: Polygon Mainnet (Chain ID 137)
- **Currency**: USDC.e (`0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`)
- **Supported Wallets**: MetaMask, OKX Wallet, Trust Wallet, TokenPocket

---

## MCP Tools Reference

### Registration（首次必须）
| Tool | Description |
|------|-------------|
| `antalpha-register` | 注册 agent，返回 `agent_id` + `api_key`。仅调用一次，持久化两个值。 |

### Market Discovery
| Tool | Parameters | Description |
|------|-----------|-------------|
| `poly-trending` | `agent_id`, `limit?`, `category?` | 热门市场（按 24h 成交量），缓存命中时可附加 Antalpha 资金热度 |
| `poly-new` | `agent_id`, `limit?`, `hours?`, `category?` | 最近创建的市场 |
| `poly-market-info` | `agent_id`, `market_id` | 市场完整信息：价格/成交量/Token ID/结果列表 |
| `poly-master-search-market` | `agent_id`, `query`, `lang?`, `limit?`, `min_liquidity?`, `include_closed?` | 自由文本搜索市场（按名称/球队/国家/候选人/事件标题/slug）。当 `poly-trending`/`poly-new` 未返回用户问到的具体事件（尤其多结果事件下的长尾结果）时调用此工具。支持 zh-CN/zh-TW/en/ja/ko，内部翻译后查询 |

### Direct Trading
| Tool | Parameters | Description |
|------|-----------|-------------|
| `poly-buy` | `agent_id`, `market_id`, `outcome`, `amount_usdc`, `wallet_address`, `proxy_wallet`, `price?` | 买入结果代币。不含 `price` = 市价单；含 `price` = 限价单 |
| `poly-sell` | `agent_id`, `market_id`, `outcome`, `size`, `wallet_address`, `proxy_wallet` | 卖出结果代币 |
| `poly-confirm` | `agent_id`, `order_id` | 查询订单签名状态 + CLOB 成交状态（`pending_signature` / `submitted` / `matched` / `failed`），同时自动修复 signed 但未更新为 submitted 的订单 |
| `poly-master-orders` | `agent_id`, `status?`, `limit?` | 订单列表，支持按状态过滤（`pending_signature`/`submitted`/`matched`/`failed`/`cancelled`） |
| `poly-history` | `agent_id`, `proxy_wallet`, `limit?` | 链上历史成交记录（来自 Polymarket data API） |

### Copy Trading
| Tool | Parameters | Description |
|------|-----------|-------------|
| `poly-master-traders` | `agent_id`, `limit?`, `sort_by?` | 顶级交易员列表，v3 可返回真实 `winRate` 与 `settledMarkets` |
| `poly-master-follow` | `agent_id`, `address`, `copyRatio` | 跟随/取消跟随交易员，设置跟单比例（0.1 = 10%） |
| `poly-master-status` | `agent_id` | 跟单状态：已关注交易员 + 最近跟单订单 |
| `poly-master-risk` | `agent_id`, `stopLossPercent?`, `takeProfitPercent?`, `maxPositionPerMarket?`, `maxTotal?` | 查看/更新风控参数 |
| `poly-master-pnl` | `agent_id`, `period?` | PnL 报告（day/week/month），按交易员分组 |
| `poly-master-orders` | `agent_id`, `status?`, `limit?` | 跟单/普通订单列表 |

### Portfolio
| Tool | Parameters | Description |
|------|-----------|-------------|
| `poly-positions` | `agent_id`, `proxy_wallet` | 当前持仓：成本/市值/未实现 PnL；缓存命中时附加 Antalpha 钱包数据 |
| `poly-history` | `agent_id`, `proxy_wallet`, `limit?` | 交易历史记录 |
| `poly-master-orders` | `agent_id`, `status?`, `limit?` | 查未成交/挂单：用 `status` 过滤（如 `status: "submitted"`） |

---

## V3 Antalpha Data Tools

### 什么时候使用 `poly-intel`

| 用户意图 | 推荐 action | 用户示例 |
|----------|-------------|----------|
| 跟单前判断钱包质量 | `wallet-profile` | “这个钱包 0xABC... 值得跟单吗？” |
| 找表现最稳定的交易员 | `leaderboard` | “按胜率和已结算市场数看顶级交易员。” |
| 看某事件背后是谁在持仓 | `top-holders` | “这个 event_id 的 top holders 是谁？” |
| 看全局资金热点 | `hotspots` | “现在 Polymarket 哪些事件资金最热？” |
| 看网络级活动 | `network-stats` | “给我一个 Polymarket 网络活动概览。” |

### `poly-intel` 参数规则

| Action | Required parameters | 说明 |
|--------|---------------------|------|
| `wallet-profile` | `address` | 钱包画像：PnL、胜率、最大盈利、已结算市场 |
| `leaderboard` | none | 交易员榜单 |
| `top-holders` | `event_id` | 事件级 top holders |
| `hotspots` | none | 全局热点事件 |
| `network-stats` | none | 网络活动概览 |

### 数据可用性解释

`poly-intel` 和被富化的老工具都会返回 `meta`。Agent 必须按以下方式解释：

- `meta.cached=true` + `meta.dataAvailable=true`：可以正常总结深度数据字段。
- `meta.dataAvailable=false`：说明目前没有可用 Polymarket 深度活动，不要把它说成“安全”或“风险低”。
- `meta.queuedForEnrichment=true`：告诉用户后台正在补全，建议稍后再问；同时展示当前已有的 Polymarket/Gamma 数据。

### 钱包画像输出建议

```
🧠 Polymarket 钱包画像 — {address}

📊 胜率：{winRate}%（基于已结算市场）
🏁 已结算市场：{settledMarkets}
💰 总 PnL：{totalPnl}
🏆 最大盈利：{question} / {outcome} / {pnl}
🐋 巨鲸标签：{isWhale}

解读：{用 2-3 句话说明是否值得继续观察、是否适合跟单、信息是否完整}

由 Antalpha AI 提供聚合服务
```

---

## V3 Poly Master Strategy Tools

> **策略原理**：Poly Master 基于逻辑蕴含而非市场相关性寻找套利机会。若 "A=YES 必然导致 B=YES"，则存在接近无风险的双腿对冲结构（totalCost < 1）。

### 策略工具
| Tool | Parameters | Description |
|------|-----------|-------------|
| `poly-master-strategy-scan` | `agent_id`, `limit?`, `min_tier?` | 触发一轮市场扫描，返回按覆盖率排序的对冲信号列表；**每条信号已含完整详情**（双腿 position、targetPrice/coverPrice、totalCost、coverage、expectedProfit、availableSize、tier、reasoning），无需再单独查询 |

### 信号结构说明

```
HedgeSignal {
  targetMarketId    # 目标市场 ID
  targetPosition    # "YES" | "NO"
  coverMarketId     # 对冲市场 ID
  coverPosition     # "YES" | "NO"
  metrics {
    targetPrice     # 目标腿价格（string, 精度保留）
    coverPrice      # 对冲腿价格（string）
    totalCost       # 两腿总成本，必须 < 1.0
    availableSize   # 最小可交易流动性（盘口最小挂单量）
    expectedProfit  # 预期利润（1 - totalCost）
    coverage        # 覆盖率，必须 ≥ 0.85
    tier            # "T1" (≥0.95) | "T2" (≥0.90) | "T3" (≥0.85)
  }
  reasoning         # LLM 推理依据（自然语言）
  builderAttributed # true = 已携带 Builder 归因头
}
```

### Tier 分级解读

| Tier | Coverage | 说明 |
|------|----------|------|
| T1 | ≥ 0.95 | 极强逻辑蕴含，几乎无风险 |
| T2 | ≥ 0.90 | 强逻辑蕴含，低风险 |
| T3 | ≥ 0.85 | 中等蕴含，需关注流动性 |

---

## Agent Instructions

### 1. 首次使用

```
1. 调用 antalpha-register → 获取 agent_id + api_key
2. 持久化 agent_id 和 api_key（后续所有调用均需要）
3. 询问用户钱包地址 (wallet_address) 和代理钱包地址 (proxy_wallet)
```

### 2. 普通交易流程

```
poly-trending / poly-new → 发现市场
poly-market-info → 查看详情
poly-buy / poly-sell → 生成签名链接
展示订单预览格式（含二维码）→ 用户在钱包内打开签名
```

### 3. Antalpha 数据辅助流程

当用户说“这个钱包怎么样”“这个交易员值得跟吗”“这个市场背后资金热不热”“这个巨鲸有 Polymarket 表现吗”时，优先使用 v3 数据能力：

```
钱包/交易员评估：
poly-intel({ action: "wallet-profile", address })
→ 若 dataAvailable=true，总结 winRate / settledMarkets / totalPnl / biggestWin
→ 若 queuedForEnrichment=true，说明后台正在补全，先给已有信息

榜单/跟单评估：
poly-master-traders({ agent_id, sort_by: "winRate" })
→ 展示 winRate 与 settledMarkets，强调 settledMarkets 是已结算市场数，不是交易笔数

热门市场分析：
poly-trending({ agent_id, limit })
→ 如返回 Antalpha 资金热度，补充 totalVolume / uniqueTraders
```

**用户提示语示例：**
- “帮我判断这个钱包是否值得跟单：0xABC...”
- “列出胜率高且已结算市场多的 Polymarket 交易员。”
- “这个市场有哪些 top holders？”
- “这个巨鲸在 Polymarket 上有历史盈利吗？”

### 4. Poly Master 对冲策略流程（只读分析）

> ⚠️ **当前 MCP 仅支持对冲机会的扫描与分析；实盘执行（双腿下单）尚未通过 MCP 开放。** 待后端上线执行能力后再补充下单流程。请勿向用户承诺可经本 skill 自动完成对冲下单。

```
步骤 1: 调用 poly-master-strategy-scan({ agent_id, limit: 5 })
        → 返回按覆盖率排序的信号列表，每条信号已含完整详情
          （双腿 target/cover position、targetPrice/coverPrice、totalCost、
           coverage、expectedProfit、availableSize、tier、reasoning）

步骤 2: 展示信号列表（按 Tier 分组，显示 totalCost/coverage/tier/expectedProfit）
        → scan 输出即为信号详情，无需再单独查询单条信号
```

**⚠️ 展示与解读规则：**
- `totalCost ≥ 1` 的信号无套利空间，应明确标注「不具备套利条件」
- `availableSize` 为当前盘口最小可成交流动性，需提示用户实际可执行规模受限于此
- `coverage` / `tier` 越高逻辑蕴含越强；T3 信号需特别提示流动性风险
- 不得向用户承诺「无风险」，仅以 `expectedProfit = 1 − totalCost` 客观呈现理论利润

### 5. Portfolio 查询（备用公开 API）

当 `poly-positions` 未部署时：
```
GET https://data-api.polymarket.com/positions?user={proxy_wallet}
```

---

## Mandatory Output Formats

### 订单预览格式（所有 poly-buy / poly-sell 必须使用）

⚠️ **硬性规则**：所有字段值必须来自 MCP 响应，不允许填写硬编码数据。

```
📋 {market}
🎯 方向：{side} {outcome}
💰 价格：${price}/份
📦 数量：{size} 份
💵 总计：${totalUsdc} USDC
📊 滑点：{slippage}%
🔗 签名页面：{signUrl}
[二维码图片 — 必须生成并附带]

由 Antalpha AI 提供聚合交易服务
```

发送前检查：✅ 7 行都有 ✅ 二维码已生成 ✅ 品牌 footer ✅ 无额外注释

### 对冲信号列表格式

```
🔮 Poly Master 对冲信号 — {扫描时间}

共发现 {n} 个信号

⭐⭐⭐ T1 信号（Coverage ≥ 0.95）
━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣ Signal #{id}
   📌 目标：{targetMarketQuestion} → {targetPosition}
   🔗 对冲：{coverMarketQuestion} → {coverPosition}
   💰 总成本：{totalCost} USDC（利润空间：{expectedProfit} USDC）
   📊 覆盖率：{coverage} | 可用流动性：{availableSize} USDC
   💡 {reasoning}

⭐⭐ T2 信号 / ⭐ T3 信号
...

由 Antalpha AI Poly Master 策略引擎提供
```

### 对冲执行格式（两腿）

```
⚡ 对冲执行 — Signal #{id}

🦵 第一腿（Target）
📋 {targetMarket}
🎯 方向：BUY {targetPosition}
💰 价格：${targetPrice}/份 | 数量：{size} 份
🔗 签名页面：{signUrl_leg1}
[二维码 1]

🦵 第二腿（Cover）
📋 {coverMarket}
🎯 方向：BUY {coverPosition}
💰 价格：${coverPrice}/份 | 数量：{size} 份
🔗 签名页面：{signUrl_leg2}
[二维码 2]

⚠️ 请先完成第一腿签名，再签第二腿

由 Antalpha AI Poly Master 策略引擎提供
```

### Portfolio 格式

```
🎯 Polymarket 持仓报告

1️⃣ {event_title}
   方向：{outcome}
   持仓：{size} 份 | 均价 ${avg_price}
   现价：${cur_price} | 市值 ${current_value}
   盈亏：${pnl} ({pnl_percent}%)
   到期：{end_date}

📊 汇总：总投入 ${total_cost} | 市值 ${total_value} | 盈亏 ${total_pnl} ({total_pnl_percent}%)

由 Antalpha AI 提供聚合服务
```

---

## Risk Defaults

| Parameter | Default | Description |
|-----------|---------|-------------|
| Slippage Tolerance | 5% | 市价单最大价格偏差 |
| Daily Bet Limit | $2,000 | 每日最大交易额 |
| Per-Market Limit | $500 | 单市场最大仓位 |
| Large Order Threshold | $1,000 | 需显式确认 |
| Copy Trading Stop-Loss | 20% | 自动暂停阈值 |
| Poly Master Min Coverage | 0.85 | T3 最低覆盖率（低于此不展示） |
| Poly Master Max Position | availableSize | 不超过盘口最小流动性 |

---

## Builder Program

PolyMaster V3 所有 CLOB 订单均通过 Polymarket Builder Program 路由：

- **X-Builder-Key**：每笔订单必须携带（缺失则拒单）
- **Relayer**：用户享受免 Gas 链上操作（需 Safe/Proxy 钱包）

---

## How Signing Works

1. 🔔 Agent 通过 MCP 生成签名 URL
2. 🌐 用户在钱包内置浏览器（MetaMask/OKX/Trust/TokenPocket）打开链接
3. 🔐 页面展示订单详情（市场/方向/价格/数量）
4. ✅ 用户点击"签名" — 钱包弹出 EIP-712 类型化数据签名
5. 📤 签名提交到服务器，订单发往 Polymarket CLOB

**安全保障**：私钥不离开钱包，签名页面仅请求特定订单数据的签名。

---

## Polymarket SDK Reference（后端集成参考）

- **EIP-712 domain.name**: `"Polymarket CTF Exchange"`（不是 "ClobExchange"）
- **signatureType**: `2`（POLY_GNOSIS_SAFE）— 用户通过 GnosisSafe 代理钱包交易
- **maker**: proxy wallet | **signer**: EOA wallet
- **HMAC owner**: API Key（非钱包地址）
- **API Key**: 一次性 `createApiKey()`，后续用 `deriveApiKey()`
- **USDC.e (Polygon)**: `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`

---

## Brand Attribution（必须）

⚠️ 所有用户可见输出必须以品牌 footer 结尾：

- 中文：`由 Antalpha AI 提供聚合服务`
- 英文：`Powered by Antalpha AI`

适用范围：市场列表、订单预览、持仓报告、PnL 报告、跟单状态、交易员排名、对冲信号列表、策略看板 —— **无例外**。

---

## Files

```
poly-master/
├── SKILL.md              # Agent 指令（本文件）
├── README.md             # 项目对外说明
├── docs/
│   └── quickstart.md     # 用户快速上手
├── references/
│   └── trade-page.html   # 浏览器签名页模板
└── scripts/              # 本地测试脚本
```

---

Built by [Antalpha AI](https://ai.antalpha.com) | MCP: `https://mcp-skills.ai.antalpha.com/mcp` | v3.0.2

---

## Changelog

- **v3.0.2** — 与当前 MCP 服务对齐（精选面向用户版）：新增市场发现工具 `poly-master-search-market`；移除内部计量/演练工具 `poly-master-strategy-metrics`、`poly-master-strategy-dry-run`（及对应策略看板章节）；校正 `poly-positions` / `poly-history` 参数为 `proxy_wallet`，`poly-master-orders` 去除 `wallet_address`、补 `limit` 与状态枚举。
