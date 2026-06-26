# longbridge

English | [中文](#中文)

---

## English

A command-line tool built on the [LongPort OpenAPI](https://open.longportapp.com/) Python SDK. Supports real-time quotes, account positions, order management, and market data. Ships with a `SKILL.md` for direct integration as a Claude Code Skill.

---

### Features

- **Quotes**: Real-time prices, order book, trade ticks, candlesticks, static info
- **Account**: Balance & net assets, stock positions, fund positions
- **Orders**: Today's / historical orders (read-only); limit buy/sell, cancel (requires trade permission)
- **Market**: Market temperature, capital flow, capital distribution, option chain

---

### Authentication

Apply for an API Key at [open.longportapp.com](https://open.longportapp.com/), then configure credentials using either method below.

#### Method 1: .env file (recommended)

Create a `.env` file in the current directory or home directory (`~/.env`):

```bash
LONGBRIDGE_APP_KEY=your_app_key
LONGBRIDGE_APP_SECRET=your_app_secret
LONGBRIDGE_ACCESS_TOKEN=your_access_token

# Optional: enable trading (default is read-only)
LONGBRIDGE_TRADE_ENABLED=true
```

Search order: **current directory** → **home directory**. Values in `.env` do **not** override existing system environment variables (system env takes precedence).

#### Method 3: Multiple accounts with `--profile`

Use named profile files to switch between accounts (e.g., paper trading vs live):

```bash
# Create .paper.env and .live.env in the current or home directory
# Each file contains the credentials for that account

longbridge --profile paper balance
longbridge --profile live positions
```

The `--profile paper` flag loads `.paper.env` instead of `.env`. If the file is not found, an error is raised.

#### Method 2: Shell environment variables

```bash
export LONGBRIDGE_APP_KEY="your_app_key"
export LONGBRIDGE_APP_SECRET="your_app_secret"
export LONGBRIDGE_ACCESS_TOKEN="your_access_token"
```

Add to `~/.zshrc` or `~/.bashrc` for persistence.

| Variable | Required | Description |
|----------|----------|-------------|
| `LONGBRIDGE_APP_KEY` | ✅ | App Key |
| `LONGBRIDGE_APP_SECRET` | ✅ | App Secret |
| `LONGBRIDGE_ACCESS_TOKEN` | ✅ | Access Token |
| `LONGBRIDGE_TRADE_ENABLED` | Optional | Set to `true` to enable trading (default: read-only) |

---

### Read-only Mode & Trade Permission

**Default is read-only**: `buy`, `sell`, `cancel` are disabled unless `LONGBRIDGE_TRADE_ENABLED=true` is set:

```
Error: 当前为只读模式，下单/撤单操作已禁用。
如需开启交易权限，请设置环境变量：
  export LONGBRIDGE_TRADE_ENABLED=true
⚠️  开启后请确保操作正确，下单指令将直接提交至长桥交易系统。
```

Read commands (`orders`, `history-orders`, `positions`, etc.) are always available without extra configuration.

---

### Usage

All commands support `--json` for machine-readable output.

#### Quotes

```bash
# Real-time quotes (multiple symbols)
longbridge quote AAPL.US 700.HK
longbridge quote AAPL.US --json

# Order book (top 5 bid/ask)
longbridge depth 700.HK

# Trade ticks
longbridge trades 700.HK --count 20

# Candlesticks
# period: 1m 5m 15m 30m 60m day week month quarter year
longbridge candlesticks AAPL.US day --count 30
longbridge candlesticks 700.HK 60m --count 100 --json

# Static security info
longbridge info AAPL.US 700.HK
```

#### Account & Positions

```bash
longbridge balance
longbridge balance --json

longbridge positions

longbridge funds
```

#### Order Management

```bash
# Read-only — no trade permission required
longbridge orders
longbridge history-orders --start 2026-01-01 --end 2026-03-14

# Requires LONGBRIDGE_TRADE_ENABLED=true

# Limit buy (confirmation prompt before execution)
longbridge buy AAPL.US --qty 100 --price 180.0

# Limit sell (confirmation prompt)
longbridge sell 700.HK --qty 500 --price 320.0

# Cancel order (confirmation prompt)
longbridge cancel 701234567890

# Skip confirmation for programmatic / scripted use
longbridge buy AAPL.US --qty 100 --price 180.0 --yes
longbridge sell 700.HK --qty 500 --price 320.0 -y
```

#### Market Data

```bash
# Market temperature (US / HK / CN / SG)
longbridge temperature US

# Capital flow
longbridge capital-flow 700.HK

# Capital distribution (large / medium / small orders)
longbridge capital-dist 700.HK

# Option chain expiry dates
longbridge option-chain AAPL.US
```

---

### AI Agent Integration

#### OpenClaw Skill

Copy `SKILL.md` to your OpenClaw skills directory to register it as a Clawdbot Skill:

```bash
mkdir -p ~/.openclaw/skills/longbridge-cli
cp SKILL.md ~/.openclaw/skills/longbridge-cli/SKILL.md
```

Once installed, Claude can invoke longbridge-cli commands automatically when you ask about account balances, positions, quotes, or orders.

#### Usage as a Skill

This project includes `SKILL.md` and can be registered as a Clawdbot Skill for AI-driven workflows. All commands support `--json` for structured output:

```bash
longbridge positions --json
longbridge quote AAPL.US 700.HK --json
longbridge orders --json
```

Example JSON output (`longbridge quote AAPL.US --json`):

```json
[
  {
    "symbol": "AAPL.US",
    "last_done": 213.49,
    "open": 211.50,
    "high": 214.20,
    "low": 210.30,
    "volume": 52345678,
    "turnover": 11162345678.0,
    "change_rate": 0.94,
    "prev_close": 211.51
  }
]
```

---

### Symbol Format

| Market | Format | Examples |
|--------|--------|---------|
| US | `TICKER.US` | `AAPL.US`, `NVDA.US` |
| HK | `4-digit code.HK` | `0700.HK`, `9988.HK` |

---

### Project Structure

```
longbridge-cli/
├── longbridge_cli/
│   ├── __init__.py
│   ├── __main__.py          # python -m entry point
│   ├── cli.py               # Click root command group
│   ├── config.py            # Config initialization
│   ├── formatters.py        # Unified text/json output
│   └── commands/
│       ├── quote.py         # Quote commands
│       ├── account.py       # Account & positions
│       ├── order.py         # Order management
│       └── market.py        # Market data
├── SKILL.md                 # Claude Code Skill document
├── _meta.json               # Skill registration
├── LICENSE
├── requirements.txt
└── pyproject.toml
```

---

### Dependencies

```
longbridge    # LongPort official Python SDK
click>=8.0   # CLI framework
rich>=13.0   # Terminal output formatting
```

---

### Notes

- **Read-only mode**: `buy`/`sell`/`cancel` require `LONGBRIDGE_TRADE_ENABLED=true`
- **Trade confirmation**: Even with trade permission enabled, all write commands prompt for confirmation before executing. Use `--yes` / `-y` to skip the prompt for scripted or programmatic use
- **Multi-account profiles**: Use `longbridge --profile <name>` to load `.<name>.env` credentials (e.g., `--profile paper` loads `.paper.env`). Useful for switching between paper trading and live accounts
- **HK symbol format**: Must use 4-digit format, e.g. `0700.HK` (leading zero required)
- **Error handling**: SDK exceptions are caught and displayed as friendly messages
- **Decimal serialization**: Decimal values are automatically converted to float in JSON output
- **.env precedence**: System environment variables take precedence over `.env` file values (system env is not overwritten)

---

### License

MIT

---

## 中文

基于[长桥 LongPort OpenAPI](https://open.longportapp.com/) Python SDK 的命令行工具，支持行情查询、账户持仓、订单管理、市场数据。封装为 Claude Code Skill，可直接被 AI Agent 调用。

---

### 功能概览

- **行情**：实时报价、盘口、逐笔成交、K 线、标的信息
- **账户**：余额净资产、股票持仓、基金持仓
- **订单**：今日/历史订单查询（只读）；限价买入/卖出、撤单（需开启交易权限）
- **市场**：市场温度、资金流向、资金分布、期权链

---

### 认证配置

在长桥开放平台 [open.longportapp.com](https://open.longportapp.com/) 申请 API Key 后，通过以下任一方式配置凭证。

#### 方式 1：.env 文件（推荐）

在当前目录或用户主目录创建 `.env` 文件：

```bash
LONGBRIDGE_APP_KEY=your_app_key
LONGBRIDGE_APP_SECRET=your_app_secret
LONGBRIDGE_ACCESS_TOKEN=your_access_token

# 可选：开启交易权限，默认为只读模式，不允许交易下单
LONGBRIDGE_TRADE_ENABLED=true
```

查找顺序：**当前工作目录** → **用户主目录**，`.env` 中的值**不会**覆盖已有的系统环境变量（系统环境变量优先）。

#### 方式 3：多账户 `--profile` 切换

使用具名 profile 文件切换账户（如模拟盘与实盘）：

```bash
# 在当前目录或主目录分别创建 .paper.env 和 .live.env
# 每个文件填写对应账户的凭证

longbridge --profile paper balance
longbridge --profile live positions
```

`--profile paper` 会加载 `.paper.env` 而不是 `.env`。若文件不存在则报错。

#### 方式 2：Shell 环境变量

```bash
export LONGBRIDGE_APP_KEY="your_app_key"
export LONGBRIDGE_APP_SECRET="your_app_secret"
export LONGBRIDGE_ACCESS_TOKEN="your_access_token"
```

写入 `~/.zshrc` 或 `~/.bashrc` 永久生效。

| 环境变量 | 必填 | 说明 |
|----------|------|------|
| `LONGBRIDGE_APP_KEY` | ✅ | 应用 App Key |
| `LONGBRIDGE_APP_SECRET` | ✅ | 应用 App Secret |
| `LONGBRIDGE_ACCESS_TOKEN` | ✅ | 用户访问 Token |
| `LONGBRIDGE_TRADE_ENABLED` | 可选 | 设为 `true` 开启交易权限（默认只读） |

---

### 只读模式与交易权限

**默认为只读模式**：`buy`、`sell`、`cancel` 命令在未配置交易权限时会被拒绝：

```
Error: 当前为只读模式，下单/撤单操作已禁用。
如需开启交易权限，请设置环境变量：
  export LONGBRIDGE_TRADE_ENABLED=true
⚠️  开启后请确保操作正确，下单指令将直接提交至长桥交易系统。
```

查询类命令（`orders`、`history-orders`、`positions` 等）不受限制，无需额外配置。

---

### 使用方法

所有命令均支持 `--json` 选项输出机器可读的 JSON 格式。

#### 行情

```bash
# 实时报价（支持批量）
longbridge quote AAPL.US 700.HK
longbridge quote AAPL.US --json

# 盘口（买5卖5）
longbridge depth 700.HK

# 逐笔成交
longbridge trades 700.HK --count 20

# K 线（period 可选：1m 5m 15m 30m 60m day week month quarter year）
longbridge candlesticks AAPL.US day --count 30
longbridge candlesticks 700.HK 60m --count 100 --json

# 标的静态信息
longbridge info AAPL.US 700.HK
```

#### 账户与持仓

```bash
longbridge balance
longbridge balance --json

longbridge positions

longbridge funds
```

#### 订单管理

```bash
# 只读，无需交易权限
longbridge orders
longbridge history-orders --start 2026-01-01 --end 2026-03-14

# 以下命令需设置 LONGBRIDGE_TRADE_ENABLED=true

# 限价买入（执行前有确认提示）
longbridge buy AAPL.US --qty 100 --price 180.0

# 限价卖出（执行前有确认提示）
longbridge sell 700.HK --qty 500 --price 320.0

# 撤销订单（执行前有确认提示）
longbridge cancel 701234567890

# 跳过确认提示（程序化/脚本调用时使用）
longbridge buy AAPL.US --qty 100 --price 180.0 --yes
longbridge sell 700.HK --qty 500 --price 320.0 -y
```

#### 市场数据

```bash
# 市场温度（US / HK / CN / SG）
longbridge temperature US

# 资金流向
longbridge capital-flow 700.HK

# 资金分布（大单/中单/小单）
longbridge capital-dist 700.HK

# 期权链到期日
longbridge option-chain AAPL.US
```

---

### AI Agent 集成

#### OpenClaw Skill 接入

将 `SKILL.md` 复制到 OpenClaw skills 目录，即可注册为 Clawdbot Skill：

```bash
mkdir -p ~/.openclaw/skills/longbridge-cli
cp SKILL.md ~/.openclaw/skills/longbridge-cli/SKILL.md
```

安装后，当你询问账户余额、持仓、行情、订单等问题时，Claude 会自动调用 longbridge-cli 命令。

#### 作为 Skill 使用

本项目包含 `SKILL.md`，可直接注册为 Clawdbot Skill 供 AI 调用。所有命令均支持 `--json`，输出结构化数据，方便 AI 解析：

```bash
longbridge positions --json
longbridge quote AAPL.US 700.HK --json
longbridge orders --json
```

JSON 输出示例（`longbridge quote AAPL.US --json`）：

```json
[
  {
    "symbol": "AAPL.US",
    "last_done": 213.49,
    "open": 211.50,
    "high": 214.20,
    "low": 210.30,
    "volume": 52345678,
    "turnover": 11162345678.0,
    "change_rate": 0.94,
    "prev_close": 211.51
  }
]
```

---

### 代码标的格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 美股 | `代码.US` | `AAPL.US`, `NVDA.US` |
| 港股 | `4位代码.HK` | `0700.HK`, `9988.HK` |

---

### 项目结构

```
longbridge-cli/
├── longbridge_cli/
│   ├── __init__.py
│   ├── __main__.py          # python -m 入口
│   ├── cli.py               # Click 根命令组
│   ├── config.py            # Config 初始化
│   ├── formatters.py        # text/json 统一输出
│   └── commands/
│       ├── quote.py         # 行情命令
│       ├── account.py       # 账户与持仓
│       ├── order.py         # 订单管理
│       └── market.py        # 市场数据
├── SKILL.md                 # Claude Code Skill 文档
├── _meta.json               # Skill 注册信息
├── LICENSE
├── requirements.txt
└── pyproject.toml
```

---

### 依赖

```
longbridge    # 长桥官方 Python SDK
click>=8.0   # CLI 框架
rich>=13.0   # 终端美化输出
```

---

### 注意事项

- **只读模式**：默认禁止 `buy`/`sell`/`cancel`，需设置 `LONGBRIDGE_TRADE_ENABLED=true` 才能下单
- **下单/撤单**：开启交易权限后，执行前仍有二次确认提示，防止误操作。脚本/程序化调用可加 `--yes` 或 `-y` 跳过确认
- **多账户切换**：使用 `longbridge --profile <名称>` 加载 `.<名称>.env` 凭证文件（如 `--profile paper` 加载 `.paper.env`），方便在模拟盘与实盘之间切换
- **港股代码**：必须使用 4 位格式，如 `0700.HK`（不能省略前导零）
- **错误处理**：SDK 异常会转换为友好提示，不暴露原始堆栈
- **Decimal 序列化**：JSON 输出中 Decimal 类型自动转为 float
- **.env 优先级**：系统环境变量优先级高于 `.env` 文件，已存在的环境变量不会被 `.env` 覆盖

---

### License

MIT
