---
name: okx-quant-trade
description: "Comprehensive quantitative trading skill for OKX. Use when user asks to 'analyze market', 'calculate RSI', 'check EMA', 'compute bollinger bands', 'buy BTC', 'sell ETH', 'place order', 'long perp', 'short swap', 'set stop loss', 'set take profit', 'check positions', 'cancel order', 'set leverage', 'trailing stop', or any quantitative analysis + order execution task on OKX. Combines Python-based technical indicator computation (RSI, EMA 5/10/20, Bias, Bollinger Bands) with OKX CLI for actual order placement. Requires API credentials for trading operations. Do NOT use for grid/DCA bots (use okx-cex-bot)."
license: MIT
metadata:
  author: system
  version: "3.1.0"
  homepage: "https://www.okx.com"
  agent:
    requires:
      python: ">=3.8"
      packages: ["pandas", "requests", "apscheduler"]
      bins: ["okx"]
    install:
      - id: npm
        kind: node
        package: "@okx_ai/okx-trade-cli"
        bins: ["okx"]
        label: "Install okx CLI (npm)"
---

# OKX 综合量化交易系统

集「技术指标计算」与「交易委托执行」于一体的 All-in-One 量化技能。赋予 Agent 盘面分析（EMA/RSI/布林带/乖离率）和一键交易（现货、永续合约、交割合约）的双重能力。**交易操作需要 API 凭证。**

## Prerequisites

1. **Python 环境** (≥3.8) — 量化指标计算引擎：
   ```bash
   pip install pandas requests apscheduler
   ```

2. **OKX CLI** — 交易执行引擎：
   ```bash
   npm install -g @okx_ai/okx-trade-cli
   ```

3. **配置 API 凭证** — 交易操作必需：
   ```bash
   okx config init
   ```
   或设置环境变量：
   ```bash
   export OKX_API_KEY=your_key
   export OKX_SECRET_KEY=your_secret
   export OKX_PASSPHRASE=your_passphrase
   ```

4. **验证配置** — 使用模拟盘测试：
   ```bash
   okx --profile demo spot orders
   ```

## Credential & Profile Check

**在任何需要鉴权的命令前，必须执行此检查。**

### Step A — 验证凭证

```bash
okx config show       # 查看配置状态（输出已脱敏）
```

- 若返回错误或无配置：**立即停止所有操作**，引导用户运行 `okx config init`，等待配置完成后重试。
- 若已配置：继续 Step B。

### Step B — 确认 Profile (必需)

`--profile` 是**所有鉴权命令的必需参数**。禁止隐式添加 profile。

| 值 | 模式 | 资金 |
|---|---|---|
| `live` | 实盘 | 真实资金 — 操作不可逆 |
| `demo` | 模拟盘 | 虚拟资金 — 用于测试 |

**判定规则：**
1. 用户意图明确（如 "real" / "实盘" / "live" → `live`；"test" / "模拟" / "demo" → `demo`）→ 直接使用并告知：`"Using --profile live (实盘)"`
2. 上下文有历史 profile → 沿用并告知：`"Continuing with --profile demo (模拟盘) from earlier"`
3. 无法确定 → 必须询问：`"Live (实盘) or Demo (模拟盘)?"` — **等待回答后才能继续**

```bash
okx --profile live  spot place ...    # 实盘 — 真实资金
okx --profile demo  spot place ...    # 模拟盘 — 虚拟资金
```

**Rules:**
1. `--profile` 在每个鉴权命令上是**必需**的
2. 每次命令结果在回复末尾标注：`[profile: live]` 或 `[profile: demo]`
3. 不要使用 `--demo` 标志切换模式 — 统一使用 `--profile`

### Step C — 确认交易标的 (instId)

**所有命令都需要明确的交易标的。** 如果用户未指定，必须询问：
*"请明确提供您需要操作的交易标的（例如 BTC-USDT、ETH-USDT-SWAP）。"*

### 处理 401 鉴权失败

如果任何命令返回 401 / 鉴权错误：
1. **立即停止** — 不要重试同一命令
2. 告知用户："鉴权失败 (401)。您的 API 密钥可能无效或已过期。"
3. 引导用户用本地编辑器更新凭证文件：
   ```
   ~/.okx/config.toml
   ```
   更新对应 profile 下的 `api_key`、`secret_key`、`passphrase` 字段。
   **不要在聊天中粘贴新凭证。**
4. 用户确认更新后执行 `okx config show` 验证（输出已脱敏）
5. 验证通过后再重试原操作

### Example

```
User: "买 0.01 BTC"
Agent: "Live (实盘) or Demo (模拟盘)?"
User: "Demo"
Agent runs: okx --profile demo spot place --instId BTC-USDT --side buy --ordType market --sz 0.01
Agent replies: "Order placed: 7890123456 (OK) — 模拟盘，未使用真实资金。[profile: demo]"
```

## Skill Routing

| 意图 | 使用技能 |
|---|---|
| 市场数据（价格、深度、资金费率） | `okx-cex-market` |
| 账户余额、P&L、持仓、费用 | `okx-cex-portfolio` |
| **量化指标分析 + 交易下单** | `okx-quant-trade`（本技能） |
| 网格 / DCA 机器人 | `okx-cex-bot` |

## Sz Handling (下单数量处理)

### 现货 & 合约 (Spot / Swap / Futures)

**当用户指定 USDT 金额** (如 "200U", "500 USDT", "$1000")：
→ 使用 `--tgtCcy quote_ccy`，将金额直接传入 `--sz`。**禁止手工换算 — 让 API 自动转换。**

```bash
# 用 1000 USDT 做多 BTC 永续
okx swap place --instId BTC-USDT-SWAP --side buy --ordType market --sz 1000 \
  --tgtCcy quote_ccy --tdMode cross --posSide long
```

**当用户指定具体数量** (如 "0.01 BTC", "2 张", "5 contracts")：
→ 直接使用 `--sz`，不加 `--tgtCcy`。

```bash
# 做多 2 张 BTC 合约
okx swap place --instId BTC-USDT-SWAP --side buy --ordType market --sz 2 \
  --tdMode cross --posSide long
```

**当用户给出无单位的数字** (合约场景)：
→ 歧义 — 必须确认：`"您输入的 X 是合约张数还是 USDT 金额？"` — 等待回答后才能继续。

⚠ **反向合约** (`*-USD-SWAP`, `*-USD-YYMMDD`)：`tgtCcy=quote_ccy` 同样适用（注意此时 `quote_ccy` = USD 而非 USDT）。始终警告："这是反向合约，保证金和盈亏以 BTC 结算，而非 USDT。"

## Quickstart

```bash
# 市价买入 0.01 BTC (现货)
okx --profile demo spot place --instId BTC-USDT --side buy --ordType market --sz 0.01

# 用 10 USDT 买入 SOL (现货，指定 USDT 金额)
okx --profile demo spot place --instId SOL-USDT --side buy --ordType market --sz 10 --tgtCcy quote_ccy

# 限价卖出 0.01 BTC (价格 $100,000)
okx --profile demo spot place --instId BTC-USDT --side sell --ordType limit --sz 0.01 --px 100000

# 做多 1 张 BTC 永续合约 (cross margin)
okx --profile demo swap place --instId BTC-USDT-SWAP --side buy --ordType market --sz 1 \
  --tdMode cross --posSide long

# 做多 1000 USDT 等值 BTC 永续 (自动转换为合约张数)
okx --profile demo swap place --instId BTC-USDT-SWAP --side buy --ordType market --sz 1000 \
  --tgtCcy quote_ccy --tdMode cross --posSide long

# 做多+附带止盈止损 (一步到位)
okx --profile demo swap place --instId BTC-USDT-SWAP --side buy --ordType market --sz 1 \
  --tdMode cross --posSide long \
  --tpTriggerPx 105000 --tpOrdPx -1 --slTriggerPx 88000 --slOrdPx -1

# 市价全平多仓
okx --profile demo swap close --instId BTC-USDT-SWAP --mgnMode cross --posSide long

# 设置 10 倍杠杆 (cross)
okx --profile demo swap leverage --instId BTC-USDT-SWAP --lever 10 --mgnMode cross

# 现货止盈止损 (OCO: 涨到 $105k 止盈，跌到 $88k 止损)
okx --profile demo spot algo place --instId BTC-USDT --side sell --ordType oco --sz 0.01 \
  --tpTriggerPx 105000 --tpOrdPx -1 \
  --slTriggerPx 88000 --slOrdPx -1

# 永续合约追踪止损 (回调 2%)
okx --profile demo swap algo trail --instId BTC-USDT-SWAP --side sell --sz 1 \
  --tdMode cross --posSide long --callbackRatio 0.02

# 现货追踪止损 (回调 3%)
okx --profile demo spot algo trail --instId BTC-USDT --side sell --sz 0.01 --callbackRatio 0.03

# 查看挂单 / 持仓
okx --profile demo spot orders
okx --profile demo swap positions
```

---

## 模块 1: 量化指标分析引擎 (Python)

Agent 的"眼睛"。通过 OKX 公共 API (无需鉴权) 获取 K线 并计算技术指标。

### 技术指标清单

| 指标 | 说明 | 参数 |
|---|---|---|
| EMA (5, 10, 20) | 指数移动平均线 | 周期分别为 5/10/20 |
| RSI | 相对强弱指数 (Wilder 平滑法) | 14 周期 |
| 乖离率 (Bias) | 价格偏离均线幅度 | 10 周期 MA |
| 布林带 (Bollinger Bands) | Upper / Mid / Lower | 20 周期，2 倍标准差 |

### calculator.py — 命令参考

```bash
python calculator.py --instId <id> --bar <periods...> [--limit <n>] [--profile <live|demo>] [--json]
```

| 参数 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `--instId` | Yes | - | 交易标的，如 `BTC-USDT`、`ETH-USDT-SWAP` |
| `--bar` | No | `1H` | 时间周期，可指定多个：`1H 4H 1D` |
| `--limit` | No | 100 | 获取数据条数 (最大 300) |
| `--profile` | No | `live` | `live` 或 `demo` |
| `--json` | No | false | 纯 JSON 格式输出 (Agent 解析模式) |

### Agent 调用约定 (非常重要)

**Agent 必须使用 `--json` 标志来获取机器可解析的纯净数据。**
该模式抑制所有终端日志，仅在 stdout 输出一个 JSON 对象。

```bash
# 单周期查询
python calculator.py --instId BTC-USDT --bar 1H --json

# 多周期批量查询（推荐：一次拿到 1H/4H/1D 全局视角）
python calculator.py --instId BTC-USDT --bar 1H 4H 1D --json
```

**JSON 输出结构：**
```json
{
  "instId": "BTC-USDT",
  "profile": "live",
  "timestamp": "2026-03-31 10:00:00",
  "results": [
    {
      "instId": "BTC-USDT",
      "bar": "1H",
      "profile": "live",
      "count": 5,
      "data": [
        {
          "ts": "2026-03-31 08:00:00",
          "o": 82500.0, "h": 82800.0, "l": 82300.0, "c": 82650.0,
          "ema_5": 82580.1234, "ema_10": 82420.5678, "ema_20": 82100.9012,
          "rsi": 55.32, "bias_10": 0.2834,
          "bb_mid": 82300.0, "bb_upper": 83100.0, "bb_lower": 81500.0
        }
      ]
    }
  ]
}
```

**错误时的 JSON 输出：**
```json
{
  "instId": "INVALID-PAIR",
  "bar": "1H",
  "error": "OKX API 错误 [51001]: Instrument ID does not exist",
  "data": []
}
```

### scheduler.py — 定时调度服务

后台守护进程，按固定周期自动拉取数据并计算指标：
- **周一~周五**：每 1 小时 (整点) 触发
- **周六~周日**：每 6 小时触发 (0:00, 6:00, 12:00, 18:00)
- 时区：`Asia/Shanghai`

```bash
# 单周期监控
python scheduler.py --instId BTC-USDT --bar 1H --profile live

# 多周期同时监控
python scheduler.py --instId BTC-USDT --bar 1H 4H 1D --profile demo
```

---

## 模块 2: 交易执行引擎 (OKX CLI)

Agent 的"手"。通过 `@okx_ai/okx-trade-cli` 执行真实的交易委托操作。

### Command Index

#### Spot 现货

| # | Command | Type | Description |
|---|---|---|---|
| 1 | `okx spot place` | WRITE | 下单 (market/limit/post_only/fok/ioc) |
| 2 | `okx spot cancel` | WRITE | 撤单 |
| 3 | `okx spot amend` | WRITE | 改单 (改价/改量) |
| 4 | `okx spot algo place` | WRITE | 挂止盈止损委托单 (oco/conditional) |
| 5 | `okx spot algo trail` | WRITE | 追踪止损 |
| 6 | `okx spot algo amend` | WRITE | 修改策略委托 |
| 7 | `okx spot algo cancel` | WRITE | 撤销策略委托 |
| 8 | `okx spot orders` | READ | 查看挂单 (加 `--history` 查看历史) |
| 9 | `okx spot get` | READ | 单笔订单详情 |
| 10 | `okx spot fills` | READ | 成交记录 |
| 11 | `okx spot algo orders` | READ | 策略委托列表 |

#### Swap 永续合约

| # | Command | Type | Description |
|---|---|---|---|
| 12 | `okx swap place` | WRITE | 下单 |
| 13 | `okx swap cancel` | WRITE | 撤单 |
| 14 | `okx swap amend` | WRITE | 改单 |
| 15 | `okx swap close` | WRITE | 市价全平仓 |
| 16 | `okx swap leverage` | WRITE | 设置杠杆 |
| 17 | `okx swap algo place` | WRITE | 挂止盈止损 (oco/conditional) |
| 18 | `okx swap algo trail` | WRITE | 追踪止损 |
| 19 | `okx swap algo amend` | WRITE | 修改策略委托 |
| 20 | `okx swap algo cancel` | WRITE | 撤销策略委托 |
| 21 | `okx swap positions` | READ | 查看持仓 |
| 22 | `okx swap orders` | READ | 查看挂单 |
| 23 | `okx swap get` | READ | 单笔订单详情 |
| 24 | `okx swap fills` | READ | 成交记录 |
| 25 | `okx swap get-leverage` | READ | 查看当前杠杆 |
| 26 | `okx swap algo orders` | READ | 策略委托列表 |

#### Futures 交割合约

| # | Command | Type | Description |
|---|---|---|---|
| 27 | `okx futures place` | WRITE | 下单 |
| 28 | `okx futures cancel` | WRITE | 撤单 |
| 29 | `okx futures amend` | WRITE | 改单 |
| 30 | `okx futures close` | WRITE | 市价全平仓 |
| 31 | `okx futures leverage` | WRITE | 设置杠杆 |
| 32 | `okx futures algo place` | WRITE | 挂止盈止损 |
| 33 | `okx futures algo trail` | WRITE | 追踪止损 |
| 34 | `okx futures algo amend` | WRITE | 修改策略委托 |
| 35 | `okx futures algo cancel` | WRITE | 撤销策略委托 |
| 36 | `okx futures positions` | READ | 查看持仓 |
| 37 | `okx futures orders` | READ | 查看挂单 |
| 38 | `okx futures get` | READ | 单笔订单详情 |
| 39 | `okx futures fills` | READ | 成交记录 |
| 40 | `okx futures get-leverage` | READ | 查看当前杠杆 |
| 41 | `okx futures algo orders` | READ | 策略委托列表 |

### Order Type Reference

| `--ordType` | 说明 | 需要 `--px` |
|---|---|---|
| `market` | 以最优价立即成交 | No |
| `limit` | 以指定价格或更优成交 | Yes |
| `post_only` | 限价单；若成为 taker 则自动取消 | Yes |
| `fok` | 全部立即成交或取消 (Fill-or-Kill) | Yes |
| `ioc` | 可用部分立即成交，剩余取消 (Immediate-or-Cancel) | Yes |
| `conditional` | 策略单：单边止盈或止损 | No (需设 trigger px) |
| `oco` | 策略单：止盈 + 止损 (一个触发另一个取消) | No (两个 trigger px) |
| `move_order_stop` | 追踪止损 | No (需设 callback) |

---

### CLI Command Reference — 关键命令详解

#### Spot — Place Order

```bash
okx spot place --instId <id> --side <buy|sell> --ordType <type> --sz <n> \
  [--tgtCcy <base_ccy|quote_ccy>] [--px <price>] \
  [--tpTriggerPx <p>] [--tpOrdPx <p|-1>] \
  [--slTriggerPx <p>] [--slOrdPx <p|-1>] \
  [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--instId` | Yes | - | 现货标的 (如 `BTC-USDT`) |
| `--side` | Yes | - | `buy` 或 `sell` |
| `--ordType` | Yes | - | `market`, `limit`, `post_only`, `fok`, `ioc` |
| `--sz` | Yes | - | 下单数量 — 单位取决于 `--tgtCcy` |
| `--tgtCcy` | No | base_ccy | `base_ccy`: sz 为基础币种数量；`quote_ccy`: sz 为计价币种金额 (如 USDT) |
| `--px` | Cond. | - | 价格 — `limit`/`post_only`/`fok`/`ioc` 必填 |
| `--tpTriggerPx` | No | - | 附带止盈触发价 |
| `--tpOrdPx` | No | - | 止盈委托价；使用 `-1` 表示市价执行 |
| `--slTriggerPx` | No | - | 附带止损触发价 |
| `--slOrdPx` | No | - | 止损委托价；使用 `-1` 表示市价执行 |

---

#### Swap — Place Order

```bash
okx swap place --instId <id> --side <buy|sell> --ordType <type> --sz <n> \
  --tdMode <cross|isolated> \
  [--tgtCcy <base_ccy|quote_ccy>] \
  [--posSide <long|short>] [--px <price>] \
  [--tpTriggerPx <p>] [--tpOrdPx <p|-1>] \
  [--slTriggerPx <p>] [--slOrdPx <p|-1>] \
  [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--instId` | Yes | - | 永续标的 (如 `BTC-USDT-SWAP`) |
| `--side` | Yes | - | `buy` 或 `sell` |
| `--ordType` | Yes | - | `market`, `limit`, `post_only`, `fok`, `ioc` |
| `--sz` | Yes | - | 下单数量 — 单位取决于 `--tgtCcy` |
| `--tdMode` | Yes | - | `cross` 全仓 或 `isolated` 逐仓 |
| `--tgtCcy` | No | base_ccy | `base_ccy`: sz 为合约张数；`quote_ccy`: sz 为 USDT 金额 |
| `--posSide` | Cond. | - | 双向持仓模式必填：`long` 或 `short` |
| `--px` | Cond. | - | 价格 — 限价单必填 |
| `--tpTriggerPx` | No | - | 附带止盈触发价 |
| `--slTriggerPx` | No | - | 附带止损触发价 |

---

#### Swap — Close Position

```bash
okx swap close --instId <id> --mgnMode <cross|isolated> \
  [--posSide <long|short>] [--autoCxl] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--instId` | Yes | - | 永续标的 |
| `--mgnMode` | Yes | - | `cross` 或 `isolated` |
| `--posSide` | Cond. | - | 双向持仓模式必填：`long` 或 `short` |
| `--autoCxl` | No | false | 平仓前自动撤销未成交订单 |

市价**全平**整个仓位。

---

#### Swap — Set Leverage

```bash
okx swap leverage --instId <id> --lever <n> --mgnMode <cross|isolated> \
  [--posSide <long|short>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--lever` | Yes | - | 杠杆倍数 (如 `10`) |
| `--mgnMode` | Yes | - | `cross` 或 `isolated` |

⚠ **Stock tokens** (如 `TSLA-USDT-SWAP`)：最大杠杆 **5x**，超出会被交易所拒绝。

---

#### Spot / Swap — Place Trailing Stop

```bash
# 现货追踪止损 (不需要 tdMode 和 posSide)
okx spot algo trail --instId <id> --side <buy|sell> --sz <n> \
  [--callbackRatio <r>] [--callbackSpread <s>] [--activePx <p>] [--json]

# 合约追踪止损
okx swap algo trail --instId <id> --side <buy|sell> --sz <n> \
  --tdMode <cross|isolated> [--posSide <long|short>] \
  [--callbackRatio <r>] [--callbackSpread <s>] [--activePx <p>] [--json]
```

| Param | Required | Description |
|---|---|---|
| `--callbackRatio` | Cond. | 回调比率 (如 `0.02` = 2%)；与 `--callbackSpread` 互斥 |
| `--callbackSpread` | Cond. | 回调固定价差；与 `--callbackRatio` 互斥 |
| `--activePx` | No | 追踪止损激活价 |

---

#### Other Common Commands

```bash
# 撤单
okx spot cancel --instId <id> --ordId <id> [--json]
okx swap cancel --instId <id> --ordId <id> [--json]

# 改单
okx spot amend --instId <id> --ordId <id> [--newSz <n>] [--newPx <p>] [--json]
okx swap amend --instId <id> --ordId <id> [--newSz <n>] [--newPx <p>] [--json]

# 查看挂单 (默认: 活跃单；加 --history 查看历史)
okx spot orders [--instId <id>] [--history] [--json]
okx swap orders [--instId <id>] [--history] [--json]

# 查看持仓
okx swap positions [<instId>] [--json]
okx futures positions [<instId>] [--json]

# 查看成交记录
okx spot fills [--instId <id>] [--ordId <id>] [--json]
okx swap fills [--instId <id>] [--ordId <id>] [--json]

# 查看杠杆
okx swap get-leverage --instId <id> --mgnMode <cross|isolated> [--json]

# 策略委托列表
okx spot algo orders [--instId <id>] [--history] [--ordType <type>] [--json]
okx swap algo orders [--instId <id>] [--history] [--ordType <type>] [--json]
```

---

## Operation Flow

### Step 0 — Credential & Profile Check

执行 "Credential & Profile Check" 部分中的 Step A → Step B → Step C。

### Step 1 — 识别标的类型和操作

**Spot** (instId 格式: `BTC-USDT`)：
- 下/撤/改单 → `okx spot place/cancel/amend`
- 止盈止损 → `okx spot algo place/amend/cancel`
- 追踪止损 → `okx spot algo trail`
- 查询 → `okx spot orders/get/fills/algo orders`

**Swap/Perpetual** (instId 格式: `BTC-USDT-SWAP`)：
- 下/撤/改单 → `okx swap place/cancel/amend`
- 平仓 → `okx swap close`
- 杠杆 → `okx swap leverage` / `okx swap get-leverage`
- 止盈止损 → `okx swap algo place/amend/cancel`
- 追踪止损 → `okx swap algo trail`
- 查询 → `okx swap positions/orders/get/fills/get-leverage/algo orders`

**Futures/Delivery** (instId 格式: `BTC-USDT-<YYMMDD>`)：
- 下/撤/改单 → `okx futures place/cancel/amend`
- 平仓 → `okx futures close`
- 杠杆 → `okx futures leverage` / `okx futures get-leverage`
- 止盈止损 → `okx futures algo place/amend/cancel`
- 追踪止损 → `okx futures algo trail`
- 查询 → `okx futures orders/positions/fills/get/get-leverage/algo orders`

### Step 2 — 确认参数后执行

**读取命令** (orders, positions, fills, get, get-leverage, algo orders)：直接执行，标注 profile。

- `--history` 标志：默认显示活跃/挂起订单；仅在用户明确要求历史时使用
- `--ordType` 策略类型：`conditional` = 单边止盈或止损；`oco` = 止盈 + 止损一起
- `--tdMode` 合约保证金模式：`cross` 全仓 或 `isolated` 逐仓
- `--posSide` 双向持仓：`long` 或 `short`；单向模式省略

**写入命令** (place, cancel, amend, close, leverage, algo)：需两项确认：

1. **Profile** — 在 Step 0 中确定
2. **参数确认** — 向用户确认关键订单参数后再执行：
   - Spot place：确认 `--instId`, `--side`, `--ordType`, `--sz` (用户指定 USDT 金额时附加 `--tgtCcy quote_ccy` — 禁止手工换算)
   - Swap/Futures place：确认 `--instId`, `--side`, `--sz`, `--tdMode` (用户指定 USDT 金额时附加 `--tgtCcy quote_ccy` — 禁止手工换算)；双向模式确认 `--posSide`
   - Close：确认 `--instId`, `--mgnMode`, `--posSide`；全平整个仓位
   - Leverage：确认新杠杆倍数及对现有仓位的影响；不得超过交易所上限
   - Algo TP/SL：确认触发价；使用 `--tpOrdPx -1` 表示触发后市价执行
   - Algo trail：确认 `--callbackRatio` 或 `--callbackSpread`

### Step 3 — 写入后验证

| 操作 | 验证命令 |
|---|---|
| `spot place` | `okx spot orders` 或 `okx spot fills` (市价单) |
| `swap place` | `okx swap orders` 或 `okx swap positions` |
| `swap close` | `okx swap positions` — 确认仓位数量为 0 |
| `futures place` | `okx futures orders` 或 `okx futures positions` |
| `futures close` | `okx futures positions` — 确认仓位数量为 0 |
| spot/swap/futures algo | 对应的 `algo orders` — 确认策略生效 |
| 任何 cancel | 对应的 `orders` — 确认订单已消失 |

---

## 模块 3: 量化决策工作流 (SOP)

将分析与交易串联成闭环，让 Agent 完成"看盘 → 研判 → 出手"的完整链路。

### 标准工作流程

```
Step 1: 确认参数
  ├── 交易标的 (instId)
  ├── 运行环境 (profile: live/demo)
  └── 策略规则 (与用户确认或基于自身判断)

Step 2: 获取盘口数据
  └── python calculator.py --instId <PAIR> --bar 1H 4H 1D --profile <PROFILE> --json

Step 3: 信号研判
  ├── 解析 JSON 中 results 数组的各周期数据
  ├── 取最后一根已确认 K线 的指标值
  └── 对比策略规则（如 RSI < 30 且价格 < bb_lower）

Step 4: 执行决策
  ├── 不满足 → 告知用户当前指标值，按兵不动
  └── 满足 → 执行对应 CLI 命令下单

Step 5: 执行后验证
  └── 调用 positions/orders/fills 确认订单状态
```

### Cross-Skill Workflow 示例

#### 指标驱动自动开仓
> 用户: "帮我以模拟盘盯一下 BTC，如果 RSI 低于 30 并且跌破布林带下轨就做多 1 张"

```
1. okx-quant-trade    → python calculator.py --instId BTC-USDT --bar 1H --profile demo --json
                         → 获取技术指标 JSON
2. Agent 解析:        → rsi=28.45, c=81200.0, bb_lower=81500.0
3. Agent 判断:        → RSI(28.45) < 30 ✓ 且 c(81200) < bb_lower(81500) ✓ → 信号触发
        ↓ 向用户确认执行参数
4. okx-cex-portfolio  → okx account balance USDT               → 确认保证金充足
5. okx-quant-trade    → okx --profile demo swap place --instId BTC-USDT-SWAP \
                          --side buy --ordType market --sz 1 --tdMode cross --posSide long
6. okx-quant-trade    → okx --profile demo swap positions      → 确认持仓
7. Agent 汇报:        → "BTC-USDT-SWAP 做多 1 张已成交。[profile: demo]"
```

#### 现货市价买入
> 用户: "买入 500 USDT 的 ETH (模拟盘)"

```
1. okx-cex-portfolio  → okx account balance USDT               → 确认可用资金 ≥ 500
        ↓ 确认
2. okx-quant-trade    → okx --profile demo spot place --instId ETH-USDT \
                          --side buy --ordType market --sz 500 --tgtCcy quote_ccy
3. okx-quant-trade    → okx --profile demo spot fills --instId ETH-USDT  → 确认成交
```

---

## Input / Output Examples

**"帮我看看 BTC 当前的技术面"**
```bash
python calculator.py --instId BTC-USDT --bar 1H 4H 1D --json
# → JSON: 三个周期的 EMA/RSI/BB/Bias 数据
```

**"市价买入 0.05 BTC"**
```bash
okx --profile demo spot place --instId BTC-USDT --side buy --ordType market --sz 0.05
# → Order placed: 7890123456 (OK) [profile: demo]
```

**"做多 10 张 BTC 永续，止盈 $105k 止损 $88k"**
```bash
okx --profile demo swap place --instId BTC-USDT-SWAP --side buy --ordType market --sz 10 \
  --tdMode cross --posSide long \
  --tpTriggerPx 105000 --tpOrdPx -1 --slTriggerPx 88000 --slOrdPx -1
# → Order placed: 7890123459 (OK) — TP/SL attached [profile: demo]
```

**"平掉我的 ETH 永续多仓"**
```bash
okx --profile demo swap close --instId ETH-USDT-SWAP --mgnMode cross --posSide long
# → Position closed: ETH-USDT-SWAP long [profile: demo]
```

**"设 BTC 永续杠杆 5 倍"**
```bash
okx --profile demo swap leverage --instId BTC-USDT-SWAP --lever 5 --mgnMode cross
# → Leverage set: 5x BTC-USDT-SWAP [profile: demo]
```

**"查看我当前的持仓"**
```bash
okx --profile demo swap positions
# → table: instId, side, size, avgPx, upl, uplRatio, lever [profile: demo]
```

**"给我 BTC 多仓加个 2% 追踪止损"**
```bash
okx --profile demo swap algo trail --instId BTC-USDT-SWAP --side sell --sz 10 \
  --tdMode cross --posSide long --callbackRatio 0.02
# → Trailing stop placed: TRAIL123 (OK) [profile: demo]
```

---

## Rate Limits (接口调用频率限制)

### 公共 API (calculator.py 使用)

| 接口 | 限速 | 说明 |
|---|---|---|
| `GET /api/v5/market/candles` | 40 次 / 2 秒 | K线数据获取，按 IP 限速 |
| `GET /api/v5/market/ticker` | 20 次 / 2 秒 | 行情快照 |
| `GET /api/v5/market/tickers` | 20 次 / 2 秒 | 全市场行情 |
| `GET /api/v5/public/instruments` | 20 次 / 2 秒 | 产品信息 |
| `GET /api/v5/public/mark-price` | 10 次 / 2 秒 | 标记价格 |

> ⚠ **多周期批量调用时**，`calculator.py --bar 1H 4H 1D` 会对同一标的连续发起 3 次 `/market/candles` 请求。
> 即使在最高调用频率下（40 次/2 秒），这也完全在安全范围内。
> 但如果 Agent 在短时间内对多个标的进行批量扫描（如同时分析 10+ 个币种），应当增加请求间隔以避免触发限速。

### 交易 API (OKX CLI 使用)

| 操作类型 | 限速 | 说明 |
|---|---|---|
| 下单 / 撤单 / 改单 | 60 次 / 2 秒 | 按 UID，所有标的共享额度 |
| 批量下单 | 300 次 / 2 秒 | 仅限做市商 |
| 查询订单/持仓 | 20 次 / 2 秒 | 按 UID |

> ⚠ **最佳实践：**
> - 避免在循环中快速连续下单，每次操作后至少等待 100ms
> - 量化 SOP 流程中的每步操作之间，建议间隔 500ms~1s
> - 如遇 `429 Too Many Requests` 错误，自动暂停 2 秒后重试
> - 调度服务 (`scheduler.py`) 的最小触发间隔已设计为 1 小时，远低于限速上限

---

## Edge Cases

### Spot 现货
- **市价单 sz 单位**：默认为基础币种 (如 BTC 数量)。若用户指定 USDT 金额，用 `--tgtCcy quote_ccy` — **禁止手工换算**
- **余额不足**：下单前先查 `okx account balance`
- **价格参数**：`market` 不需要 `--px`；`limit` / `post_only` / `fok` / `ioc` 必须带 `--px`
- **Algo oco**：同时提供 `tpTriggerPx` 和 `slTriggerPx`；价格 `-1` 表示触发后市价执行
- **fills vs orders**：`fills` 显示已执行的成交；`orders --history` 显示所有订单含已取消
- **追踪止损**：使用 `--callbackRatio` (相对，如 `0.02`) 或 `--callbackSpread` (绝对价差)，不能同时使用；现货不需要 `--tdMode` 和 `--posSide`
- **策略方向**：`--side` 必须与仓位方向相反（持多 → `sell` algo；持空 → `buy` algo）

### Swap 永续合约
- **sz 单位**：合约张数，或使用 `--tgtCcy quote_ccy` 时为 USDT 金额。用户指定 USDT 金额时直接传入 — **禁止手工换算**
- **线性 vs 反向**：`BTC-USDT-SWAP` (USDT 结算) vs `BTC-USD-SWAP` (BTC 结算)。反向合约必须警告保证金和盈亏以 BTC 结算
- **posSide**：双向持仓模式 (`long_short_mode`) 必须指定；单向模式 (`net` mode) 省略
- **tdMode**：`cross` 全仓，`isolated` 逐仓
- **全平仓**：`swap close` 全平整个仓位；部分平仓使用 `swap place --reduceOnly`
- **杠杆上限**：因标的和账户等级而异，超限会被交易所拒绝
- **Stock tokens** (如 TSLA, NVDA)：最大杠杆 **5x**，必须带 `--posSide`，仅在美股交易时段交易

### Futures 交割合约
- **instId 格式**：`BTC-USDT-<YYMMDD>` (如 `BTC-USDT-260328`，2026年3月28日到期)
- **线性 vs 反向**：`BTC-USDT-<YYMMDD>` 线性；`BTC-USD-<YYMMDD>` 反向 (BTC 结算)
- **到期风险**：合约到期日自动交割结算，切勿无意持仓过期
- **全平仓**：`futures close` — 同 `swap close` 语义

---

## Global Notes

- 所有写入命令需要有效凭证 (`~/.okx/config.toml` 或环境变量)
- `--profile <name>` 在所有鉴权命令上是**必需**的；参见 "Credential & Profile Check" 部分
- 每次命令结果需附带 `[profile: <name>]` 标签
- `--json` 返回 OKX API v5 原始响应
- 持仓模式 (`net` vs `long_short_mode`) 决定是否需要 `--posSide`
- **tgtCcy 规则 (spot/swap/futures)**：用户指定计价币种金额 (如 "30 USDT") → MUST 使用 `--tgtCcy quote_ccy` 并将 USDT 金额作为 `--sz` 传入。**严禁**手工计算基础币种数量或合约张数 — 让 API 处理转换。用户指定基础币种数量或合约张数时 → 省略 `--tgtCcy`
- **订单金额偏差安全规则**：若订单执行金额与用户期望有显著偏差（如因 minSz 或转换导致），必须**立即停止**并告知用户，**禁止自动调整**订单数量
- **禁止追补订单**：订单执行后，若实际成交金额与用户请求有实质性差异，**立即停止**。告知用户实际成交量和差异，**不得**自行追加订单弥补，等待用户明确指令
