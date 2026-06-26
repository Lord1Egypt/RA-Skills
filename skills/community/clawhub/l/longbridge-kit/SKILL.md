---
name: longbridge
version: 1.0.2
description: |
  长桥 LongPort OpenAPI CLI 工具，提供股票行情查询、账户持仓、订单管理、市场数据四大功能。
  当用户提到"长桥"、"LongPort"、"longbridge"，或要求查看股票报价、实时行情、K线、盘口、
  逐笔成交、账户余额、持仓、基金持仓、下单、买入、卖出、撤单、今日订单、历史订单、
  资金流向、资金分布、市场温度、期权链时，使用此 skill。即使用户只是随口问"看看苹果股价"、
  "我的持仓怎么样"、"帮我下个单"，也应触发此 skill。
metadata: {"clawdbot":{"emoji":"📊","os":["darwin","linux"],"requires":{"bins":["python3","uv"],"env":["LONGBRIDGE_APP_KEY","LONGBRIDGE_APP_SECRET","LONGBRIDGE_ACCESS_TOKEN"]}}}
---

# 长桥 OpenAPI CLI 工具

通过 `longbridge` CLI 命令调用长桥 OpenAPI，覆盖行情查询、账户持仓、订单管理、市场数据四大模块。

## 前置条件

### 环境变量

需设置以下环境变量（可在 `~/.zshrc` 或 `~/.bashrc` 中配置）：

```bash
export LONGBRIDGE_APP_KEY="your_app_key"
export LONGBRIDGE_APP_SECRET="your_app_secret"
export LONGBRIDGE_ACCESS_TOKEN="your_access_token"

# 可选：开启交易权限（默认只读，禁止 buy/sell/cancel）
# export LONGBRIDGE_TRADE_ENABLED=false
```

也可以在当前目录或主目录创建 `.env` 文件（系统环境变量优先级更高，不会被 `.env` 覆盖）。

多账户切换：使用 `--profile <名称>` 加载 `.<名称>.env` 文件，例如：

```bash
longbridge --profile paper balance   # 加载 .paper.env
longbridge --profile live positions  # 加载 .live.env
```

### 安装

先检测是否已安装：

```bash
which longbridge
```

- 若输出路径（如 `/Users/xxx/.local/bin/longbridge`），说明已安装，跳过安装步骤。
- 若未找到，从本 skill 目录安装（`SKILL_DIR` 为本文件所在目录）：

```bash
uv tool install "$SKILL_DIR"
```

验证安装：

```bash
longbridge --help
```

## 使用方式

所有命令均支持 `--json` 选项输出 JSON 格式。

### 行情模块

```bash
# 实时报价（支持多个标的）
longbridge quote AAPL.US 700.HK
longbridge quote AAPL.US --json

# 盘口（买5卖5）
longbridge depth 700.HK

# 逐笔成交
longbridge trades 700.HK --count 20

# K 线（period 可选：1m 5m 15m 30m 60m day week month quarter year）
longbridge candlesticks AAPL.US day --count 30
longbridge candlesticks 700.HK 60m --count 100

# 标的静态信息
longbridge info 700.HK AAPL.US
```

### 账户模块

```bash
# 账户余额与净资产
longbridge balance

# 股票持仓
longbridge positions
longbridge positions --json

# 基金持仓
longbridge funds
```

### 订单模块

```bash
# 今日订单（只读，无需交易权限）
longbridge orders

# 历史订单（只读，无需交易权限）
longbridge history-orders --start 2026-01-01 --end 2026-03-14

# 以下命令需设置 LONGBRIDGE_TRADE_ENABLED=true

# 限价买入（会有确认提示，防止误操作）
longbridge buy AAPL.US --qty 100 --price 180.0

# 限价卖出（会有确认提示）
longbridge sell 700.HK --qty 500 --price 320.0

# 撤销订单（会有确认提示）
longbridge cancel 701234567890

# 跳过确认提示（AI Agent 程序化调用时推荐加 --yes）
longbridge buy AAPL.US --qty 100 --price 180.0 --yes
longbridge sell 700.HK --qty 500 --price 320.0 -y
```

### 市场数据模块

```bash
# 市场温度（US/HK/CN/SG）
longbridge temperature US
longbridge temperature HK

# 资金流向
longbridge capital-flow 700.HK

# 资金分布（大单/中单/小单）
longbridge capital-dist 700.HK

# 期权链到期日列表
longbridge option-chain AAPL.US
```

## 注意事项

- **下单/撤单命令**：`buy`、`sell`、`cancel` 均有确认提示，确认后才会执行，防止误操作。AI Agent 程序化调用时请加 `--yes` 或 `-y` 跳过确认
- **港股代码格式**：使用 4 位 + `.HK` 后缀，如 `0700.HK`、`9988.HK`
- **美股代码格式**：使用股票代码 + `.US` 后缀，如 `AAPL.US`、`NVDA.US`
- **JSON 输出**：所有命令加 `--json` 可输出机器可读的 JSON 格式，便于 AI 解析
- **错误处理**：SDK 异常会输出友好提示，不暴露原始堆栈
