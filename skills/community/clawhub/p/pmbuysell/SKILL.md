---
name: pm-polymarket-trade
description: Executes Polymarket (pmbuysell) trade/balance via CLI or Python API. Use when the user or model needs to trade or query balances/positions. Auto-redeem is a separate paid addon (pmbuysell_redeem).
---

# Polymarket 交易快速调用 (pmbuysell)

在用户或模型需要执行 Polymarket 买卖、多账号下单或程序化调用 pmbuysell 时使用本 Skill。

## 运行位置（主流写法）

本技能文档里所有命令都默认在 **项目根目录**（也就是包含 `pmbuysell/` 目录的那个目录）执行。

如果你当前目录不是项目根，请先切换到你的实际路径，例如：

```bash
cd <your-project-root>
```

## 快速调用方式

### 方式零：初始化配置（生成 `.env` 模板）

AI 智能体可以先执行一次初始化，确保有一个确定的配置文件路径可编辑：

```bash
python -m pmbuysell.skills.init_cli
```

生成位置固定为：`pmbuysell/.env`（若已存在则不会覆盖；需要覆盖可加 `--force`）。

初始化后可做一次配置自检（会列出缺失项）：

```bash
python -m pmbuysell.skills.check_config_cli
```

### 方式一：CLI 一键下单（推荐模型调用）

在 **项目根目录** 下执行，以便 `pmbuysell` 作为包被找到：

```bash
python -m pmbuysell.skills.trade_cli --account ACC1 --action buy --slug tc-updown-5m-1772452800 --side down --amount 10
```

自动 slug（按当前 5m/15m 桶）：

```bash
python -m pmbuysell.skills.trade_cli --account ACC1 --action buy --slug-mode auto --symbol tc --timeframe 5m --side down --amount 10
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--account` | 是 | 账号 ID，如 ACC1（需在 .env 的 PM_ACCOUNT_IDS 及 ACC1_PRIVATE_KEY/ACC1_FUNDER 中配置） |
| `--action` | 是 | `buy` 或 `sell` |
| `--slug` | 手动时必填 | 市场 slug，如 `tc-updown-5m-1772452800` |
| `--slug-mode` | 否 | `manual`（默认）或 `auto`；auto 时用 `--symbol`、`--timeframe` 生成当前桶 slug |
| `--symbol` | auto 时 | 标的，如 `tc`、`btc`，默认 `tc` |
| `--timeframe` | auto 时 | `5m` 或 `15m`，默认 `5m` |
| `--side` | 是 | `up` 或 `down` |
| `--amount` | 是 | 买入：USDC 金额；卖出：token 数量；当买入且 amount=0 时会按余额规则自动计算下注金额 |

输出为 JSON（字段可能随功能演进略有增减）：

- `ok`: 是否成功
- `message`: 失败原因或成功提示
- `usdc_balance`: 交易后/查询到的余额（可能为 null）
- `order_message`: 结构化成交/下单信息（可能为 null）
- `requested_amount`: 你传入的 amount 原值
- `auto_amount`: 当 `buy` 且 `amount=0` 时，按余额规则自动计算出的买入金额

`ok` 为 false 时 CLI 退出码为 1。

### 方式一补充：CLI 查询余额 / 持仓

查询 USDC 余额：

```bash
python -m pmbuysell.skills.balance_cli --account ACC1
```

查询指定 slug 的 up/down 持仓（同时返回 USDC）：

```bash
python -m pmbuysell.skills.balance_cli --account ACC1 --slug tc-updown-5m-1772452800
```

### 自动结算（redeem）— Pro 付费模块

免费版提供接口入口，调用时仅提示需购买 Pro 付费：

```bash
python -m pmbuysell.skills.auto_redeem_cli --account ACC1 --dry-run
```

返回示例：`{"ok": false, "message": "自动结算为 Pro 版本功能，请购买", ...}`

购买 Pro 后安装并调用：

```bash
pip install pmbuysell_redeem
python -m pmbuysell_redeem.cli --account ACC1 --dry-run
```

redeem 相关配置自检（供 Pro 用户预校验）：

```bash
python -m pmbuysell.skills.check_config_cli --account ACC1 --require-redeem
```

### 方式二：Python 函数调用（在代码中直接调用）

在同一项目环境中：

```python
from pmbuysell.skills.multi_account import market_buy, market_sell, get_balance

# 市价买入
result = market_buy("ACC1", "tc-updown-5m-1772452800", "down", 10.0)

# 市价卖出
result = market_sell("ACC1", "tc-updown-5m-1772452800", "up", 5.0)

# 查询余额
result = get_balance("ACC1", slug="tc-updown-5m-1772452800")
```

返回 `dict`：`{"ok": bool, "message": str | None, "usdc_balance": float | None, "order_message": dict | None}`（trade）；`{"ok": bool, "usdc": float, "conditional": {...} | None, "message": str | None}`（balance）。

## 环境与依赖

- 需在 `pmbuysell` 目录下存在 `.env`（可参考 `.env.example`），配置 `PM_ACCOUNT_IDS`、`ACCx_PRIVATE_KEY`、`ACCx_FUNDER`。
- **安装依赖**（任选其一，在项目根目录执行）：
  - 仅使用本 Skill：`pip install -r pmbuysell/skills/requirements.txt`
  - 使用完整项目（含 Flask 等）：`pip install -r pmbuysell/requirements.txt`

## 账号配置样例（复制到 `pmbuysell/.env`）

### 方式 A（推荐）：扁平变量，多账号可读性更好

```dotenv
# 声明有哪些账号
PM_ACCOUNT_IDS=ACC1,ACC2

# 每个账号需要：私钥 + funder（pm 的代理地址 / Safe 地址）
ACC1_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_1
ACC1_FUNDER=0xYOUR_FUNDER_ADDRESS_1

ACC2_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_2
ACC2_FUNDER=0xYOUR_FUNDER_ADDRESS_2
```

### 方式 B（可选）：JSON 一行配置（适合直接注入环境变量）

```dotenv
PM_ACCOUNTS_JSON={"ACC1":{"private_key":"0xYOUR_PRIVATE_KEY_1","funder":"0xYOUR_FUNDER_ADDRESS_1"},"ACC2":{"private_key":"0xYOUR_PRIVATE_KEY_2","funder":"0xYOUR_FUNDER_ADDRESS_2"}}
```

## 模型调用检查清单

1. 确认在 **项目根目录** 下执行 CLI，或当前环境能 `import pmbuysell`。
2. 确认 `account` 已在 .env 中配置。
3. 手动 slug 时：`slug` 格式为 `{symbol}-updown-{5m|15m}-{桶起始时间戳}`。
4. 自动 slug 时：只支持 `timeframe` 为 `5m` 或 `15m`。
5. 根据返回的 `ok` 与 `message` 判断是否成功；失败时 `message` 常含余额、市场关闭、无匹配等提示。
