# MNS CLI 命令参考

本文档详细描述 MNS CLI 的所有命令、参数和用法。

## 命令概览

| 命令 | 用途 | 异步 |
|------|------|------|
| `init` | 初始化配置文件和数据库 | 否 |
| `config` | 查看/修改配置 | 否 |
| `cash` | 现金余额管理 | 否 |
| `portfolio` | 查看持仓概览 | 否 |
| `add` | 新增资产到持仓池 | 否 |
| `buy` | 记录买入交易 | 否 |
| `sell` | 记录卖出交易 | 否 |
| `price` | 更新资产当前价格 | 否 |
| `sentiment` | 查看当前恐贪指数 | 是 |
| `report` | 生成策略报告 | 是 |
| `history` | 查看交易历史 | 否 |
| `backtest` | 策略回测 | 否 |
| `update-prices` | 自动更新所有资产价格 | 是 |

---

## `init`

**语法**: `mns init [-f, --force]`

**功能**: 初始化配置文件和数据库。

**参数**:
- `-f, --force`: 跳过确认提示，强制覆盖已有数据

**行为说明**:
- 如果检测到已有配置文件或数据库，会提示用户确认后再覆盖
- 使用 `--force` 参数可跳过确认直接覆盖

**示例**:
```bash
# 普通初始化（如有数据会提示确认）
mns init

# 强制初始化（跳过确认）
mns init --force
```

**输出示例（已有数据时）**:
```
⚠️  检测到已有数据：

继续将覆盖上述文件，数据将丢失。是否继续？[y/N]: y
✓ 初始化完成
  配置文件: ~/.mns/config.toml
  数据库: ~/.mns/mns.db
  报告目录: ./reports
```

**注意**: 
- 报告目录默认为当前目录下的 `reports/`，可通过配置修改
- 输入 `y` 或 `yes` 确认覆盖，其他任何输入都会取消操作

---

## `config`

**语法**: `mns config [KEY] [VALUE]`

**功能**: 查看或修改配置项。支持 dot-path 语法访问嵌套配置。

### 查看所有配置
```bash
mns config
```

输出 TOML 格式的完整配置。

### 查看特定配置项
```bash
mns config thresholds.fear
mns config buy_ratio.extreme_fear
mns config sell_ratio.extreme_greed_target_high
```

输出:
```
thresholds.fear = 45
buy_ratio.extreme_fear = 60.0
sell_ratio.extreme_greed_target_high = 50.0
```

### 修改配置项
```bash
mns config thresholds.greed 75
mns config buy_ratio.fear 30.0
```

**支持的配置路径**:

| 路径 | 说明 | 默认值 |
|------|------|--------|
| `settings.annualized_target_low` | 年化止盈下限(%) | 10.0 |
| `settings.annualized_target_high` | 年化止盈上限(%) | 15.0 |
| `settings.min_holding_days` | 最小持仓天数 | 45 |
| `settings.min_absolute_profit_days` | 绝对收益最小天数 | 120 |
| `settings.max_contrarian_weight` | 最大逆向权重 | 2.0 |
| `settings.report_output_dir` | 报告输出目录 | ./reports |
| `allocation.us_stocks` | 美股配置比例(%) | 55.0 |
| `allocation.cn_stocks` | A股配置比例(%) | 25.0 |
| `allocation.counter_cyclical` | 逆周期配置比例(%) | 20.0 |
| `thresholds.extreme_fear` | 极度恐慌阈值 | 30.0 |
| `thresholds.fear` | 恐慌阈值 | 45.0 |
| `thresholds.neutral` | 中性阈值 | 55.0 |
| `thresholds.greed` | 贪婪阈值 | 70.0 |
| `buy_ratio.extreme_fear` | 极度恐慌买入比例(%) | 60.0 |
| `buy_ratio.fear` | 恐慌买入比例(%) | 35.0 |
| `buy_ratio.neutral` | 中性买入比例(%) | 0.0 |
| `buy_ratio.greed` | 贪婪买入比例(%) | 0.0 |
| `sell_ratio.extreme_greed_target_high` | 极度贪婪+高收益卖出(%) | 50.0 |
| `sell_ratio.extreme_greed_target_low` | 极度贪婪+低收益卖出(%) | 30.0 |
| `sell_ratio.extreme_greed_below_target` | 极度贪婪+未达标卖出(%) | 20.0 |
| `sell_ratio.greed_target_high` | 贪婪+高收益卖出(%) | 40.0 |
| `sell_ratio.greed_target_low` | 贪婪+低收益卖出(%) | 25.0 |
| `sell_ratio.neutral_target_high` | 中性+高收益卖出(%) | 15.0 |

**示例 - 完整参数调优**:
```bash
# 调整买入比例
mns config buy_ratio.extreme_fear 60.0
mns config buy_ratio.fear 25.0
mns config buy_ratio.neutral 10.0

# 调整卖出矩阵
mns config sell_ratio.extreme_greed_target_high 60.0
mns config sell_ratio.greed_target_high 50.0

# 调整止盈线
mns config settings.annualized_target_low 12.0
mns config settings.annualized_target_high 18.0

# 调整逆向权重上限
mns config settings.max_contrarian_weight 1.5
```

---

## `cash`

**语法**: `mns cash [ACTION]`

**功能**: 查看或设置现金余额。

### 查看余额
```bash
mns cash
```

输出:
```
现金余额: ¥125430.50
```

### 设置现金余额
```bash
mns cash set 100000
```

### 增加现金
```bash
mns cash add 5000
```

**注意**:
- `set` 会覆盖当前余额
- `add` 在当前余额基础上增加
- 金额不能为负数

---

## `portfolio`

**语法**: `mns portfolio`

**功能**: 显示当前持仓概览，包括：
- 资产代码和名称
- 持仓份额和成本价
- 当前价格（需通过 `price` 命令更新）
- 持仓市值和盈亏
- 年化收益率（基于持有天数）

**示例输出**:
```
┌───────┬────────────┬──────────┬──────────┬─────────────┬─────────────┬────────────┐
│ 代码  │   名称     │  份额    │ 成本价   │ 当前价      │  市值       │ 年化收益   │
├───────┼────────────┼──────────┼──────────┼─────────────┼─────────────┼────────────┤
│ QQQ   │ 纳指100    │ 150.0    │ 450.00   │ 460.50      │ 69075.00    │  +8.2%     │
│ SH600 │ 浦发银行   │ 500.0    │ 12.30    │ 12.80       │ 6400.00     │ +15.3%     │
└───────┴────────────┴──────────┴──────────┴─────────────┴─────────────┴────────────┘

总市值: ¥75475.00
现金余额: ¥24685.50
总资产: ¥100160.50
```

**注意事项**:
- 年化收益计算公式: `(current / cost) ^ (365 / holding_days) - 1`
- 如果持有天数小于配置的 `min_holding_days`，年化收益显示为 `N/A`
- 当前价格需要定期通过 `price` 命令更新

---

## `add`

**语法**: `mns add <CODE> <NAME> <CATEGORY>`

**功能**: 新增资产到持仓池，后续可通过 `buy` 命令买入。

**参数**:
- `CODE`: 资产代码（如 `QQQ`, `SH600000`, `AAPL`）
- `NAME`: 资产名称（任意描述性字符串）
- `CATEGORY`: 类别，预设可选值：
  - `us_stocks` - 美股
  - `cn_stocks` - A股
  - `counter_cyclical` - 逆周期资产

**示例**:
```bash
mns add QQQ "纳指100" us_stocks
mns add SH600000 "浦发银行" cn_stocks
mns add GLD "黄金ETF" counter_cyclical
```

**注意**:
- 资产代码在数据库中必须唯一
- 添加后立即用 `buy` 记录初始买入

---

## `buy`

**语法**: `mns buy <CODE> <SHARES> <PRICE>`

**功能**: 记录买入交易，增加持仓份额。

**参数**:
- `CODE`: 资产代码（必须已通过 `add` 添加）
- `SHARES`: 买入份额（支持小数，如股票可支持碎股）
- `PRICE`: 买入单价（元/股）

**示例**:
```bash
# 买入 100 股 QQQ，单价 450.50 元
mns buy QQQ 100 450.50

# 买入 50 份黄金 ETF，单价 180.00 元
mns buy GLD 50 180.00
```

**行为**:
- 现金余额相应减少
- 持仓成本价重新计算（加权平均）
- 交易记录存入 `transactions` 表

---

## `sell`

**语法**: `mns sell <CODE> <SHARES> <PRICE>`

**功能**: 记录卖出交易，减少持仓份额。

**参数**:
- `CODE`: 资产代码
- `SHARES`: 卖出份额（不能超过当前持仓）
- `PRICE`: 卖出单价

**示例**:
```bash
# 卖出 30 股 QQQ，单价 455.00 元
mns sell QQQ 30 455.00

# 清仓某资产
mns sell SH600000 500 13.20
```

**行为**:
- 现金余额相应增加
- 持仓份额减少，成本价保持不变（剩余份额）
- 交易记录存入 `transactions` 表

---

## `price`

**语法**: `mns price <CODE> [PRICE]`

**功能**: 查看或更新单个资产的当前价格。

### 查看当前价格
```bash
mns price QQQ
```

输出:
```
QQQ (纳指100): ¥460.50
```

### 更新当前价格
```bash
mns price QQQ 460.50
```

**注意**:
- 每次更新价格会更新对应持仓的 `current_price` 和 `current_at` 字段
- 不更新价格会导致 `portfolio` 和 `report` 显示的市值不准确
- 如需批量更新所有资产价格，请使用 `update-prices` 命令

---

## `update-prices`

**语法**: `mns update-prices`

**功能**: 自动更新所有持仓资产的当前价格。

**行为说明**:
- 遍历所有有持仓的资产
- 尝试从网络获取最新价格（需要网络连接）
- 更新数据库中的 `current_price` 字段
- 此命令为异步命令

**示例**:
```bash
mns update-prices
```

**输出示例**:
```
正在更新所有资产价格...
✓ QQQ: 460.50
✓ SH600000: 12.80
✓ GLD: 182.35
已完成 3 个资产的价格更新
```

**注意**:
- 需要网络连接
- 部分资产可能无法获取价格（如 A 股需要特定数据源）
- 建议在执行 `report` 前先运行此命令

---

## `sentiment`

**语法**: `mns sentiment`

**功能**: 从 CNN 官网获取最新的 Fear & Greed Index 数据。

**示例**:
```bash
mns sentiment
```

输出:
```
CNN Fear & Greed Index: 42 (Fear)
Previous Close: 38
1 Week Ago: 35
1 Month Ago: 28
```

**注意**:
- 此命令是异步的，需要网络访问
- 如果 API 不可用，可能返回错误
- 数据来自 CNN 官方 API 端点

---

## `report`

**语法**: `mns report`

**功能**: 生成今日策略报告，包含：
1. 当前恐贪指数和情绪判断
2. 买入建议（基于可用现金和 contrarian 分配）
3. 卖出建议（基于年化收益和绝对收益）
4. 持仓摘要和风险警告（浮亏过大）
5. 现金预测（按建议执行后）

**示例**:
```bash
mns report
```

**输出节选**:
```
╔═══════════════════════════════════════════════════════════════╗
║           MNS 逆向投资策略报告 - 2026-04-21                     ║
╚═══════════════════════════════════════════════════════════════╝

📊 市场情绪 (CNN Fear & Greed)
┌─────────────────────────────────────┐
│ 当前指数: 42 (Fear)                  │
│ 状态解读: 市场处于恐慌区间，建议逐步  │
│         买入                          │
└─────────────────────────────────────┘

💰 买入建议 (可用现金: ¥25000)
┌─────────────────────────────────────┐
│ QQQ (Fear 区间权重: 1.2)             │
│  建议买入: ¥12000 (50 股 @ ¥240)    │
│                                     │
│ SH600000 (Fear 区间权重: 1.5)        │
│  建议买入: ¥13000 (1042 股 @ ¥12.5) │
└─────────────────────────────────────┘

⚠️  卖出建议
┌─────────────────────────────────────┐
│ 暂无满足卖出条件的持仓              │
└─────────────────────────────────────┘

🚨 风险警告
┌─────────────────────────────────────┐
│ [无]                                │
└─────────────────────────────────────┘
```

**注意**:
- 异步命令，需要网络获取恐贪指数
- 报告同时保存到报告目录（默认 `./reports/`）
- 买入/卖出建议仅供参考，agent 需根据实际执行顺序调整

---

## `history`

**语法**: `mns history [--limit N]`

**功能**: 查看最近的交易历史。

**参数**:
- `--limit N`: 显示条数，默认 20

**示例**:
```bash
# 查看最近 20 条
mns history

# 查看最近 50 条
mns history --limit 50
```

**输出**:
```
最近交易记录 (按时间倒序):
┌─────────────────┬───────┬────────┬──────┬────────┬──────────┐
│ 时间            │ 类型  │ 资产   │ 份额 │ 价格   │ 金额     │
├─────────────────┼───────┼────────┼──────┼────────┼──────────┤
│ 2025-06-15 10:30│ buy   │ QQQ    │ 50   │ 448.50 │ 22425.00 │
│ 2025-06-14 14:20│ sell  │ SH600  │ 100  │ 13.00  │ 1300.00  │
│ 2025-06-14 09:15│ price │ QQQ    │ -    │ 445.00 │ -        │
└─────────────────┴───────┴────────┴──────┴────────┴──────────┘
```

**类型说明**:
- `buy` - 买入交易
- `sell` - 卖出交易
- `price` - 价格更新记录

---

## `backtest`

**语法**: `mns backtest [SUBCOMMAND]`

**功能**: 策略回测相关命令，基于历史数据验证策略表现。

### 子命令

#### `backtest run`
运行回测。

**语法**: `mns backtest run [-c, --config <PATH>] [-C, --compare <PATHS>]`

**参数**:
- `-c, --config <PATH>`: 配置文件路径，省略则使用默认配置
- `-C, --compare <PATHS>`: 对比多个配置文件，逗号分隔

**示例**:
```bash
# 使用默认配置运行回测
mns backtest run

# 指定配置文件
mns backtest run --config ./my_strategy.toml

# 对比多个策略配置
mns backtest run --compare config1.toml,config2.toml,config3.toml
```

#### `backtest params`
查看可调参数列表。

**语法**: `mns backtest params`

**示例**:
```bash
mns backtest params
```

**输出示例**:
```
可调参数列表:
┌─────────────────────────────┬────────────────┬─────────────────┐
│ 参数名                       │ 默认值          │ 说明             │
├─────────────────────────────┼────────────────┼─────────────────┤
│ buy_ratio.extreme_fear      │ 50.0           │ 极度恐慌买入比例  │
│ buy_ratio.fear             │ 30.0           │ 恐慌买入比例     │
│ ...                        │ ...            │ ...             │
└─────────────────────────────┴────────────────┴─────────────────┘
```

---

## 通用 Exit Code

| Code | 含义 |
|------|------|
| 0    | 成功 |
| 1    | 通用错误（配置错误、参数错误、数据库错误等） |
| 2    | 网络错误（仅影响 `sentiment`/`report`/`update-prices`） |

---

## 数据存储位置

MNS 数据存储在用户主目录下的 `.mns` 文件夹：

| 文件 | 路径 | 说明 |
|------|------|------|
| 配置文件 | `~/.mns/config.toml` | TOML 格式的策略配置 |
| 数据库 | `~/.mns/mns.db` | SQLite 数据库 |
| 报告目录 | `./reports/` | 默认报告输出目录（可配置） |

---

## 数据库 Schema 参考

主要表结构：

### `cash`
- `id` INTEGER PRIMARY KEY
- `balance` REAL NOT NULL
- `updated_at` TIMESTAMP

### `positions`
- `id` INTEGER PRIMARY KEY
- `code` TEXT NOT NULL UNIQUE
- `name` TEXT NOT NULL
- `category` TEXT NOT NULL
- `shares` REAL NOT NULL
- `cost_price` REAL NOT NULL
- `current_price` REAL NOT NULL
- `first_buy_date` TEXT NOT NULL
- `updated_at` TIMESTAMP
- `created_at` TIMESTAMP

### `transactions`
- `id` INTEGER PRIMARY KEY
- `type` TEXT NOT NULL ('buy' | 'sell' | 'price')
- `code` TEXT NOT NULL
- `shares` REAL
- `price` REAL
- `amount` REAL
- `created_at` TIMESTAMP

---

## 错误信息速查

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `未知的配置项` | 配置路径错误或不存在 | 用 `config` 查看有效的配置项 |
| `现金余额不能为负数` | `cash set` 参数 < 0 | 检查金额参数 |
| `资产代码不存在` | `buy`/`sell`/`price` 使用未添加的代码 | 先用 `add` 添加资产 |
| `卖出份额超过持仓` | `sell` 参数 > 当前持仓 | 检查持仓数量 |
| `API error: ...` | CNN API 不可用 | 稍后重试或检查网络 |
| `Database is locked` | 并发访问数据库 | 确保同一时间只有一个进程操作 |

---

**最后更新**: 2026-04-21
