---
name: danger-auto-trade-polymarket
version: 1.0.2
description: DANGER：Polymarket 全自动交易编排器。无需人工确认，AI 自主完成市场扫描、概率评估、仓位计算和实盘下单。一句话触发完整交易链路。当用户要求自动交易、全自动下单、danger trade、auto trade Polymarket 时使用此技能。
metadata: {"openclaw": {"emoji": "⚠️", "requires": {"bins": ["node", "npx", "python3"]}, "primaryEnv": "PRIVATE_KEY", "envVars": [{"name": "PRIVATE_KEY", "required": true, "description": "Polymarket wallet private key"}, {"name": "FUNDER_ADDRESS", "required": true, "description": "Polymarket funder/proxy wallet address"}]}}
---

# DANGER: Polymarket 全自动交易编排器

全自动「扫描 -> 评估 -> 决策 -> 下单」链路。无需人工确认，AI 自主完成所有决策和交易执行。

**警告：此 skill 会使用真金白银执行实盘交易。使用 `--dry-run` 可仅模拟不下单。**

## 工作流

按顺序执行，不可跳过。共 8 步（第 0-7 步）。

### 第 0 步：环境与风控初始化

1. 确保 api-trade-polymarket 脚本可用：
   ```bash
   cd {baseDir}/../api-trade-polymarket/scripts && npm install 2>/dev/null
   ```

2. 检查余额：
   ```bash
   cd {baseDir}/../api-trade-polymarket/scripts && npx tsx balance.ts
   ```

3. 读取 `~/polymarket-reports/portfolio.json`，计算当前总资产：
   - `total_assets = cash_balance + sum(positions[].current_value)`
   - 如果 `portfolio.json` 不存在，用余额作为 `total_assets`，初始化空 portfolio 结构
   - 如果余额 < $10 且无持仓，报错退出

4. 解析 `$ARGUMENTS` 中的风控参数（未指定则用默认值）：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--max-per-trade <usd>` | 单笔交易上限 | $50 |
| `--max-total <usd>` | 本次运行总交易上限 | $150 |
| `--max-positions <n>` | 最多同时持仓数 | 10 |
| `--dry-run` | 仅模拟，不实际下单 | false |
| `--mode pulse\|review\|full` | 操作模式 | full |

**操作模式说明：**
- `pulse` — 仅扫描新机会并下单（跳过第 1 步）
- `review` — 仅审查现有持仓并执行 sell/rotate（跳过第 2-5 步）
- `full` — 先 review 再 pulse，完整链路

5. 打印风控参数摘要，确认初始化完成。

### 第 1 步：Portfolio Review（review/full 模式）

审查现有持仓，决定 hold/sell/rotate。直接执行 portfolio-review 方法论（不调用 skill）。

**1.1 读取持仓**

读取 `~/polymarket-reports/portfolio.json` 中的 `positions[]`。如果无持仓，跳到第 2 步。

**1.2 逐仓评估**

对每个持仓执行：

1. 通过 WebSearch 获取该市场的最新信息（2-3 次搜索），更新概率估算 `p_now`
2. 获取当前价格：
   ```bash
   cd {baseDir}/../api-trade-polymarket/scripts && npx tsx orderbook.ts --token-id <token_id> --side SELL --urgency medium
   ```
   从返回结果提取 `smart_price` 作为 `c_now`
3. 计算关键指标：
   ```
   edge = p_now - c_now
   daily_expected_return = (p_now - c_now) / (c_now * d_remaining)
   ```

**1.3 应用决策树**

| 条件 | 决策 |
|------|------|
| edge <= 0 | **SELL** — edge 已消失 |
| 原始 thesis 已被推翻 | **SELL** — 基本面变化 |
| daily_ER < 0.02% 且有更好机会 | **ROTATE** — 标记为待卖 |
| 单仓位 > 总资产 25% | **TRIM** — 减仓至 15% |
| 否则 | **HOLD** |

**1.4 执行卖出**

对每个 SELL/TRIM 决策：

1. 确定卖出数量：
   - SELL → 全部 shares
   - TRIM → 减至目标比例的 shares
2. 获取卖出智能价格：
   ```bash
   cd {baseDir}/../api-trade-polymarket/scripts && npx tsx orderbook.ts --token-id <token_id> --side SELL --urgency medium
   ```
3. 执行卖出（如果非 `--dry-run`）：
   ```
   调用 api-trade-polymarket skill: sell --market <slug> --direction <dir> --shares <n> --order-type limit --price <smart_price>
   ```
   如果是 `--dry-run`，仅打印将要执行的命令。
4. 记录执行结果（成功/失败/挂单）

**1.5 记录 review 结果**

将所有持仓的评估结果和决策记录到内存中，用于第 6 步报告。

### 第 2 步：Market Pulse 扫描（pulse/full 模式）

调用 `polymarket-market-pulse` skill 扫描新机会：

```
使用 Skill tool 调用 polymarket-market-pulse
```

这会执行完整的 market pulse 流程：
1. 扫描 Polymarket 热门市场
2. AI 评估概率 + 计算 Edge
3. 生成 `~/polymarket-reports/market-pulse-{date}.md` 报告
4. 追加到 `recommendation-history.md`

### 第 3 步：解析 Pulse 报告

1. 使用 Glob 工具找到最新的 `~/polymarket-reports/market-pulse-*.md` 文件
2. 读取报告，提取每个推荐的：
   - 市场 slug / event_slug
   - 推荐方向（Yes/No）
   - 推荐价格（entry price）
   - 建议仓位金额
   - Edge 和置信度（High/Medium-High/Medium/Low）
   - clobTokenId（如果报告中有）

3. 过滤已持有市场：
   - 读取 `portfolio.json` 的 `positions[]`
   - 按 event_slug 匹配，去除已持有的市场
   - 跳过 Edge < 5% 的推荐

### 第 4 步：自动仓位计算

对每个通过筛选的新推荐，计算最终交易金额：

```
资金管理规则（按顺序应用，取最小值）：

1. 基础上限 = min(建议金额, --max-per-trade, total_assets * 5%)

2. 置信度调整：
   - High 或 Medium-High → 放宽到 total_assets * 8%
   - Medium 或 Low → 维持 total_assets * 5%

3. 流动性约束：
   - 获取 orderbook 的 2% 滑点深度（buy_capacity.max_cost_usd）
   - 不超过该深度的 10%

4. 总敞口约束：
   - 所有现有持仓 + 本次所有新交易 <= total_assets * 50%
   - 如超出则按比例缩减新交易金额

5. Edge 加权缩放：
   - Edge > 20%: 用满上限
   - Edge 10-20%: 上限 * 60%
   - Edge 5-10%: 上限 * 30%
   - Edge < 5%: 跳过该推荐

6. 最小交易检查：金额 < $10 则跳过

7. 累计检查：本次运行所有买入累计不超过 --max-total
   如剩余额度不足，按 Edge 优先级截断
```

### 第 5 步：自动执行交易（pulse/full 模式）

按 Edge 从高到低排序，依次执行：

对每个推荐：

**5.1 获取智能价格**
```bash
cd {baseDir}/../api-trade-polymarket/scripts && npx tsx orderbook.ts --token-id <token_id> --side BUY --urgency medium
```
提取 `smart_price` 和流动性数据。

**5.2 计算份数**
```
shares = floor(amount / smart_price)
```

**5.3 执行下单**

如果是 `--dry-run` 模式，打印将要执行的命令，跳过实际下单：
```
[DRY-RUN] 将执行: api-trade-polymarket buy --market <slug> --direction <dir> --order-type limit --price <price> --amount <usd>
```

如果非 dry-run，调用 api-trade-polymarket skill 执行：
```
调用 api-trade-polymarket skill: buy --market <slug> --direction <dir> --order-type limit --price <smart_price> --amount <usd>
```

**5.4 处理返回结果**

解析返回 JSON：
- `status=matched` 或 `status=filled` → 记录成功，累加已用金额
- `status=live` → 挂单中，记录 orderID，累加已用金额
- `status=error` → 记录失败原因，继续下一个（单笔失败不影响后续）

**5.5 更新累计金额**

每笔成功后更新累计交易金额，确保不超过 `--max-total`。

### 第 6 步：生成执行报告

使用 Write 工具生成报告：

**文件路径：** `~/polymarket-reports/auto-trade-{YYYY-MM-DD}-{HHMMSS}.md`

**报告模板：**

```markdown
# Auto-Trade Execution Report

**时间：** {timestamp UTC}
**模式：** {pulse|review|full}
**风控参数：** max_per_trade=${X}, max_total=${Y}, max_positions=${Z}
**Dry-Run：** {是/否}

## Portfolio Review 结果

| 市场 | 方向 | 买入价 | 现价 | p_now | Edge | Daily ER | 决策 | 原因 | 执行结果 |
|------|------|--------|------|-------|------|----------|------|------|----------|

（review/full 模式才有此节）

## 新建仓位

| # | 市场 | 方向 | Edge | 置信度 | 金额 | 价格 | 份数 | 状态 | OrderID |
|---|------|------|------|--------|------|------|------|------|---------|

（pulse/full 模式才有此节）

## 执行摘要

- 卖出: N 笔, 总计 $X
- 买入: N 笔, 总计 $Y
- 失败: N 笔
- 剩余现金: $Z
- 总持仓: N 个市场
- 总敞口: XX% of total_assets

## 风控检查

- [x/!] 单笔未超 $MAX_PER_TRADE
- [x/!] 本次总额未超 $MAX_TOTAL
- [x/!] 持仓数未超 MAX_POSITIONS
- [x/!] 总敞口 < 50% of total_assets
```

### 第 7 步：更新 portfolio.json

确保所有变更写入 `~/polymarket-reports/portfolio.json`：

1. **新增仓位**（买入成功）→ 添加到 `positions[]`：
   ```json
   {
     "market": "<slug>",
     "event_slug": "<event_slug>",
     "direction": "Yes|No",
     "shares": <n>,
     "entry_price": <price>,
     "current_price": <price>,
     "current_value": <value>,
     "token_id": "<clobTokenId>",
     "opened_at": "<timestamp>",
     "source": "auto-trade"
   }
   ```

2. **挂单**（status=live）→ 添加到 `pending_orders[]`：
   ```json
   {
     "order_id": "<id>",
     "market": "<slug>",
     "direction": "Yes|No",
     "side": "BUY|SELL",
     "price": <price>,
     "amount": <usd>,
     "created_at": "<timestamp>"
   }
   ```

3. **卖出成功** → 从 `positions[]` 移除，添加到 `trade_history[]`：
   ```json
   {
     "market": "<slug>",
     "direction": "Yes|No",
     "side": "SELL",
     "shares": <n>,
     "entry_price": <price>,
     "exit_price": <price>,
     "pnl": <usd>,
     "closed_at": "<timestamp>"
   }
   ```

4. 更新顶层字段：
   - `cash_balance` — 从余额查询获取最新值
   - `total_assets` — cash + 持仓市值
   - `updated_at` — 当前 UTC 时间戳

5. 如果是 `--dry-run` 模式，不写入 portfolio.json，仅在报告中标注模拟结果。

## 错误处理

- **环境缺失**（scripts 不存在、.env.aizen 缺失）→ 报错退出，不执行任何交易
- **余额不足**（< $10 且无持仓）→ 报错退出
- **单笔交易失败** → 记录错误，继续执行下一笔（不中断流程）
- **Market Pulse skill 失败** → 报错退出（pulse/full 模式），review 模式不受影响
- **portfolio.json 写入失败** → 重试一次，仍失败则将数据打印到报告中供手动恢复
- **所有交易完成后**，无论成功失败，都生成执行报告（第 6 步）

## 参考文件

- [references/risk-controls.md](references/risk-controls.md) — 风控规则详细文档
