---
name: polymarket-paper-trading
version: 1.0.2
description: Polymarket 交易回测与组合管理。读取 market-pulse 报告推荐，交互式询问下单方式（市价/智能限价/自定义限价/跳过），执行资金管理与仓位计算，自动追踪持仓损益，生成收益分析与反思报告。支持纸上交易和实盘两种模式。当用户提到 Polymarket 回测、纸上交易、下单、组合管理、收益分析、仓位回顾时使用此技能。
metadata: {"openclaw": {"emoji": "📝", "requires": {"bins": ["python3", "node", "npx"]}, "primaryEnv": "PRIVATE_KEY", "envVars": [{"name": "PRIVATE_KEY", "required": true, "description": "Polymarket wallet private key (loaded via .env.aizen)"}, {"name": "FUNDER_ADDRESS", "required": true, "description": "Polymarket funder/proxy wallet address"}, {"name": "SIGNATURE_TYPE", "required": false, "description": "Signing mode: 0=EOA, 1=Proxy (default), 2=Gnosis"}]}}
---

# Polymarket 交易回测

基于 market-pulse 报告的推荐仓位，执行交易（纸上或实盘），追踪组合损益，生成收益分析与反思。

## 双模式

- **纸上交易**（默认）：模拟成交，无需钱包，用于策略验证
- **实盘**：通过 `@polymarket/clob-client` 下单到 Polymarket CLOB，需配置 `.env.aizen`

## 工作流

按顺序执行以下步骤，不可跳过。

### 第 0 步：环境检查

```bash
pip install -r scripts/requirements.txt 2>/dev/null
```

若为实盘模式，还需：
```bash
cd scripts && npm install 2>/dev/null
```

检查 `.env.aizen` 是否存在（包含 `PRIVATE_KEY`, `FUNDER_ADDRESS`, `SIGNATURE_TYPE`）。

### 第 1 步：加载组合状态

读取 `~/polymarket-reports/portfolio.json`。

若文件不存在，使用 AskQuestion 询问用户：
1. 初始资金金额（选项：$1,000 / $5,000 / $10,000 / 自定义）
2. 交易模式（纸上交易 / 实盘）

然后创建新组合，使用 Write 工具写入 `~/polymarket-reports/portfolio.json`。格式见 [references/portfolio-schema.md](references/portfolio-schema.md)。

### 第 2 步：自动回顾已有仓位

如果组合中有持仓或挂单，执行以下操作：

**获取当前价格：**
```bash
python scripts/fetch_prices.py ~/polymarket-reports/portfolio.json
```

脚本输出每个持仓的当前价格和结算状态。

**处理已结算市场：**
- `closed=true` 且最终价格为 0 或 1 的市场 → 计算实现损益
- 公式：`pnl = shares * (exit_price - entry_price)`，其中 exit_price 为 1.0（赢）或 0.0（输）
- 将已结算仓位从 `positions` 移入 `settled_trades`
- 归还现金：`cash_balance += shares * exit_price`

**检查挂单成交：**
```bash
python scripts/check_orders.py ~/polymarket-reports/portfolio.json
```

- 纸上模式：当前价格穿越限价 → 视为成交，移入 `positions`
- 实盘模式：通过 CLOB API 查询订单状态

**显示组合摘要（向用户展示）：**

| 指标 | 值 |
|------|-----|
| 总资产 | cash + 持仓市值 |
| 现金 | cash_balance |
| 未实现损益 | 持仓市值 - 持仓成本 |
| 已实现损益 | 已结算交易的总 PnL |
| 胜率 | 盈利交易数 / 已结算交易数 |
| 活跃仓位 | N 个 |
| 挂单 | N 个 |

然后更新 `portfolio.json`。

### 第 3 步：解析 Pulse 报告

用户需提供 pulse 报告路径。若未提供，列出 `~/polymarket-reports/market-pulse-*.md` 文件让用户选择。

```bash
python scripts/parse_pulse.py <pulse_report_path>
```

脚本输出 JSON，每个推荐包含：question, url, event_slug, direction, recommended_price, size_range, edge, confidence, liquidity_tier。

过滤掉已在 `positions` 或 `pending_orders` 中的市场（按 event_slug 匹配），避免重复建仓。

### 第 4 步：交互式下单决策

对每个新推荐，先展示摘要：

```
市场：{question}
方向：买入 {direction}
Edge：{edge}% | 置信度：{confidence}
当前价格：${price} | 建议规模：{size_range}
流动性等级：{liquidity_tier}
```

然后使用 AskQuestion 询问用户下单方式：

| 选项 | 说明 |
|------|------|
| 市价单 | 按当前 best ask 立即成交（适合短期/高波动） |
| 智能限价 | 自动计算优化价格（见下方逻辑） |
| 自定义限价 | 用户指定价格（再次询问价格） |
| 跳过 | 不交易此推荐 |

**智能限价计算：**

获取实时订单簿：
```bash
python scripts/fetch_orderbook.py <clob_token_id>
```

复用 pulse skill 的 `fetch_orderbook.py`（位于 `{baseDir}/../polymarket-market-pulse-zh/scripts/fetch_orderbook.py`，若不存在则用 CLOB API 手动获取）。

计算公式：
```
limit_price = best_bid + spread * urgency_factor
```

紧迫度因子：
- 短期市场（< 7 天结算）→ urgency = 0.5
- 中期市场（7-30 天）→ urgency = 0.3
- 长期市场（> 30 天）→ urgency = 0.2

向用户展示建议价格及理由后确认。

### 第 5 步：资金管理与仓位计算

对用户确认交易的每个推荐，计算最终仓位：

**约束规则：**
1. **单笔上限**：总资产 × 5%（高置信度放宽到 8%）
2. **单市场上限**：总资产 × 15%（含已有同市场仓位）
3. **总敞口上限**：总资产 × 50%
4. **流动性约束**：不超过 2% 滑点深度的 10%（来自 pulse 报告）
5. **Edge 加权**：
   - Edge > 20%：用满单笔上限
   - Edge 10-20%：单笔上限 × 60%
   - Edge 5-10%：单笔上限 × 30%
6. **最小交易**：$10

取上述约束的最小值作为最终金额。计算份数：`shares = floor(amount / price)`。

向用户展示最终仓位详情：
```
下单金额：${amount}
份数：{shares} 份 @ ${price}
占总资产：{pct}%
```

确认后执行。

### 第 6 步：执行下单

**纸上模式：** 直接更新 portfolio.json：
- 市价单 → 添加到 `positions`，扣减 `cash_balance`
- 限价单 → 添加到 `pending_orders`

**实盘模式：** 调用下单脚本：

市价单（FOK）：
```bash
npx tsx scripts/place_order.ts --token-id <id> --side BUY --type FOK --amount <shares>
```

限价单（GTC）：
```bash
npx tsx scripts/place_order.ts --token-id <id> --side BUY --type GTC --price <price> --size <shares>
```

脚本输出 JSON：`{ orderID, status, filledPrice, filledSize, latency_ms }`。

根据返回结果更新 portfolio.json：
- `status=matched/filled` → 添加到 `positions`
- `status=live` → 添加到 `pending_orders`，记录 `real_order_id`
- `status=error` → 向用户报告错误，不修改组合

### 第 7 步：生成收益分析报告

每次运行自动生成报告。使用 Write 工具保存到：
```
~/polymarket-reports/performance-{YYYY-MM-DD}-{HHMMSS}.md
```

报告格式见 [references/output-template.md](references/output-template.md)。

**绩效指标**（自动计算）：
- 总资产 & 收益率
- 已实现 / 未实现损益
- 胜率
- 平均 Edge vs 实际结果偏差
- 最佳 / 最差交易

**仓位明细表**（每个持仓一行）：
- 进场价、当前价、损益%、持有天数、原始 Edge

**反思模块**（由 AI 撰写，这是最核心的部分）：
- 哪些预测准确？关键原因？
- 哪些预测失败？失败原因（信息不足 / 过度自信 / 市场变化）？
- 各类别表现（政治 vs 加密 vs AI）
- Longshot Bias 策略回顾
- Edge 校准分析：AI 预估 Edge 与实际价格变动的相关性
- 下一步调整建议

反思要求：
1. 必须引用具体数据（不能空泛）
2. 对失败案例必须提出可操作的改进
3. 整体论调应诚实，不美化结果

## 故障排除

- **parse_pulse.py 解析失败**：报告格式可能变化，手动读取报告并提取数据
- **fetch_prices.py 超时**：降低并发请求数或增加重试
- **实盘下单失败**：检查 `.env.aizen` 配置和钱包余额，运行 smoke test
- **portfolio.json 损坏**：从 `trade_history` 重建

## 参考文件

- [references/portfolio-schema.md](references/portfolio-schema.md) — 组合 JSON 格式
- [references/output-template.md](references/output-template.md) — 收益报告模板
