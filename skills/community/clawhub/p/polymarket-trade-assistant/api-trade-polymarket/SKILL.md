---
name: api-trade-polymarket
version: 1.0.2
description: Polymarket CLOB API 自动交易执行层。非交互式、指令驱动，支持买入/卖出（市价/限价）、撤单、余额查询、持仓查询、订单簿读取与智能定价。可被 orchestrator 或其他 skill 直接调用执行真实交易。当需要在 Polymarket 上执行实盘交易、查询余额、查看持仓、读取订单簿时使用此技能。
metadata: {"openclaw": {"emoji": "💰", "requires": {"bins": ["node", "npx"]}, "primaryEnv": "PRIVATE_KEY", "envVars": [{"name": "PRIVATE_KEY", "required": true, "description": "Polymarket wallet private key (loaded via .env.aizen)"}, {"name": "FUNDER_ADDRESS", "required": true, "description": "Polymarket funder/proxy wallet address"}, {"name": "SIGNATURE_TYPE", "required": false, "description": "Signing mode: 0=EOA, 1=Proxy (default), 2=Gnosis"}], "install": [{"id": "node", "kind": "brew", "formula": "node", "bins": ["node", "npx"], "label": "Install Node.js (brew)"}]}}
---

# Polymarket CLOB API 交易执行

非交互式交易执行层，通过 `$ARGUMENTS` 接收指令，调用 Polymarket CLOB API 完成操作并返回结构化 JSON 结果。

## 工作流

按顺序执行，不可跳过。

### 第 0 步：环境准备

```bash
cd {baseDir}/scripts && npm install 2>/dev/null
```

验证 `.env.aizen` 存在（位于 `scripts/` 目录下）。若不存在，提示用户参照 `.env.aizen.example` 创建。

### 第 1 步：解析指令

从 `$ARGUMENTS` 中提取操作类型和参数。支持的操作：

| 操作 | 格式 |
|------|------|
| 买入 | `buy --market <slug> --direction Yes\|No --amount <usd> [--order-type market\|limit] [--price <p>]` |
| 卖出 | `sell --market <slug> --direction Yes\|No --shares <n> [--order-type market\|limit] [--price <p>]` |
| 撤单 | `cancel --order-id <id>` 或 `cancel --all` |
| 余额 | `balance` |
| 持仓 | `positions` |
| 订单簿 | `orderbook --market <slug> --direction Yes\|No` |

### 第 2 步：市场解析（买入/卖出/订单簿操作需要）

当指令包含 `--market <slug>`，需要将 market slug 和 direction 转换为 CLOB token ID：

1. 通过 Polymarket Gamma API 查询市场信息：
   ```
   GET https://gamma-api.polymarket.com/events?slug=<slug>
   ```
2. 从返回的 market 数据中，根据 `--direction` 找到对应 outcome 的 `clobTokenId`
3. 如果 API 查询失败，提示用户直接提供 `--token-id`

### 第 3 步：预检查（买入/卖出操作需要）

**余额检查：**
```bash
cd {baseDir}/scripts && npx tsx balance.ts
```

验证 USDC 余额充足。

**订单簿读取（限价单需要）：**
```bash
cd {baseDir}/scripts && npx tsx orderbook.ts --token-id <id> --side BUY|SELL --urgency medium
```

如果用户未指定价格但选择限价单，使用返回的 `smart_price` 作为限价。

**风控验证：**
- 单笔金额不超过 $500（安全上限）
- 价格在 best_bid 和 best_ask 范围内合理
- 余额足够覆盖交易

### 第 4 步：执行操作

根据操作类型调用对应脚本：

**买入/卖出：**
```bash
# 市价单 (FOK)
cd {baseDir}/scripts && npx tsx trade.ts --token-id <id> --side BUY|SELL --order-type FOK --amount <usd>

# 限价单 (GTC)
cd {baseDir}/scripts && npx tsx trade.ts --token-id <id> --side BUY|SELL --order-type GTC --price <p> --size <shares>
```

**撤单：**
```bash
cd {baseDir}/scripts && npx tsx cancel.ts --order-id <id>
cd {baseDir}/scripts && npx tsx cancel.ts --all
```

**余额查询：**
```bash
cd {baseDir}/scripts && npx tsx balance.ts
```

**持仓查询：**
```bash
cd {baseDir}/scripts && npx tsx positions.ts
```

**订单簿：**
```bash
cd {baseDir}/scripts && npx tsx orderbook.ts --token-id <id> [--side BUY|SELL] [--urgency low|medium|high] [--depth 5]
```

### 第 5 步：更新组合状态

如果执行了买入/卖出操作且成功，更新 `~/polymarket-reports/portfolio.json`：

- `status=matched/filled` → 添加到 `positions`，扣减 `cash_balance`
- `status=live` → 添加到 `pending_orders`，记录 `real_order_id`
- 撤单成功 → 从 `pending_orders` 移除，恢复 `cash_balance`

### 第 6 步：输出结果

将脚本输出的 JSON 直接返回给调用者。所有脚本输出格式统一包含 `status` 字段。

## 错误处理

- 环境缺失 → 返回 `{"error": "...", "status": "config_error"}`
- 参数错误 → 返回 `{"error": "...", "status": "arg_error"}`
- API 失败 → 返回 `{"error": "...", "status": "execution_error"}`
- 执行出错时自动调用 `cancelAll()` 清理

## 参考文件

- [references/clob-trading-api.md](references/clob-trading-api.md) — CLOB API 端点文档
- [references/env-setup.md](references/env-setup.md) — .env.aizen 配置指南
