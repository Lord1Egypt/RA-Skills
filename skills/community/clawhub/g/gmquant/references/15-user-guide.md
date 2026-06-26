# 掘金量化 + WorkBuddy 使用手册

> 从零开始，用自然语言开发量化策略，完成回测、仿真、实盘

---

## 目录

1. [整体架构](#1-整体架构)
2. [安装掘金终端](#2-安装掘金终端)
3. [安装 WorkBuddy](#3-安装-workbuddy)
4. [安装 gm-quant Skill](#4-安装-gm-quant-skill)
5. [获取掘金 Token](#5-获取掘金-token)
6. [5 分钟快速体验：第一个回测](#6-5-分钟快速体验第一个回测)
7. [策略开发详解](#7-策略开发详解)
8. [运行回测](#8-运行回测)
9. [启动仿真交易](#9-启动仿真交易)
10. [启动实盘交易](#10-启动实盘交易)
11. [在微信中操作](#11-在微信中操作)
12. [常见问题排查](#12-常见问题排查)
13. [附录：API 速查](#附录api-速查)

---

## 1. 整体架构

```
┌─────────────┐     自然语言      ┌──────────────┐     代码生成      ┌──────────────┐
│   微信/PC    │ ──────────────→  │  WorkBuddy   │ ──────────────→  │  策略 .py     │
│  (你的入口)   │  "帮我写个均线策略" │  (AI 助手)    │  完整可运行代码    │  (标准模板)    │
└─────────────┘                   └──────────────┘                   └──────┬───────┘
                                                                          │
                                          run_strategy.py                 │
                                               │                          │
                                               ▼                          ▼
                                    ┌──────────────────────┐
                                    │    掘金终端 (GM)      │
                                    │  ┌──────┐ ┌──────┐   │
                                    │  │ 回测  │ │ 实盘  │   │
                                    │  │ 引擎  │ │ 引擎  │   │
                                    │  └──────┘ └──────┘   │
                                    └──────────────────────┘
```

**核心流程**：你在 WorkBuddy 里用中文说"我想做个均线策略"→ AI 自动生成代码 → 一键回测/仿真/实盘

---

## 2. 安装掘金终端

### 2.1 下载安装

1. 访问掘金官网：**https://www.myquant.cn**
2. 点击"下载终端"，选择 Windows 版本
3. 安装到默认路径（如 `D:\掘金终端\`）
4. 启动终端，**注册账号并登录**

### 2.2 安装 Python SDK

掘金终端自带 Python 环境，但建议用自己管理的 Python：

```bash
# 确认 Python 版本（3.9+）
python --version

# 安装掘金 SDK
pip install gm -U

# 验证安装
python -c "from gm.api import *; print('GM SDK OK')"
```

### 2.3 验证终端连接

```python
from gm.api import *
set_token('你的token')  # 先随便填，下一节获取
```

> ⚠️ **关键**：掘金终端必须保持打开状态，所有 API 调用都依赖终端连接

---

## 3. 安装 WorkBuddy

### 3.1 安装 VS Code 扩展

1. 打开 VS Code
2. 在扩展商店搜索 **"Coding Copilot"**（腾讯云出品）
3. 点击安装
4. 安装完成后侧边栏会出现 WorkBuddy 图标

### 3.2 首次启动

1. 点击侧边栏 WorkBuddy 图标
2. 按提示登录（微信扫码或账号登录）
3. 进入对话界面

### 3.3 创建工作区

1. 在本地创建一个项目文件夹，如 `D:\quant-workspace\`
2. 在 VS Code 中 `File → Open Folder` 打开这个文件夹
3. WorkBuddy 会自动关联当前工作区

---

## 4. 安装 gm-quant Skill

### 方式一：让 AI 自动安装（推荐）

在 WorkBuddy 对话中直接说：

> "帮我安装掘金量化 skill"

AI 会自动搜索并安装 `gm-quant` skill。

### 方式二：手动安装

将 skill 文件夹复制到：

```
%USERPROFILE%\.workbuddy\skills\gm-quant\
```

目录结构：

```
gm-quant/
├── SKILL.md                    # 技能定义（AI 核心指令）
├── README.md                   # 说明文档
├── scripts/
│   ├── run_strategy.py         # 策略运行器（统一入口）
│   ├── strategy_ma_cross.py    # 示例：均线策略
│   ├── strategy_etf_momentum.py# 示例：ETF动量轮动
│   └── ...
└── references/
    ├── 01-quick-start.md       # 快速开始
    ├── 02-core-functions.md    # 核心函数
    ├── 04-market-data.md       # 行情数据
    ├── 08-order-api.md         # 交易接口
    └── ...
```

### 验证 Skill 安装

在 WorkBuddy 中说：

> "你有什么掘金量化的能力？"

如果 AI 回复了掘金相关的功能介绍，说明 skill 已生效。

---

## 5. 获取掘金 Token

Token 是策略连接掘金终端的凭证，**必须获取才能运行策略**。

### 获取步骤

1. 打开掘金终端，登录账号
2. 点击右上角头像 → **"我的 Token"**
3. 复制 Token 字符串（类似 `c2a347464c31056c84165dff766750fbf2ec67b4`）

### 保存 Token

将 Token 写入环境变量，避免每次手动输入：

**Windows（PowerShell 临时设置）**：
```powershell
$env:GM_TOKEN = "你的token"
```

**Windows（永久设置）**：
```powershell
[System.Environment]::SetEnvironmentVariable("GM_TOKEN", "你的token", "User")
```

> 💡 设置后重启 VS Code，WorkBuddy 就能自动读取

---

## 6. 5 分钟快速体验：第一个回测

打开 WorkBuddy，直接输入：

```
帮我写一个双均线策略，标的茅台，MA5上穿MA20买入，下穿卖出，
回测最近1年，初始资金100万，策略ID用 ma_test_001
```

AI 会自动：
1. 生成完整的策略代码
2. 保存到 `scripts/` 目录
3. 使用 `run_strategy.py` 执行回测

**你只需要说一句话，剩下的全自动。**

回测完成后，AI 会输出绩效报告：

```
累计收益: +12.3%
年化收益: 15.6%
夏普比率: 0.85
最大回撤: 8.2%
胜率: 58.3%
```

---

## 7. 策略开发详解

### 7.1 策略模板结构

每个策略都遵循标准模板：

```python
"""策略说明"""
import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from gm.api import *

# === 配置区（修改参数在这里）===
SYMBOLS = 'SHSE.600519'
FREQUENCY = '1d'
BACKTEST_START = '2024-01-02 09:30:00'
BACKTEST_END   = '2025-12-31 15:30:00'
INITIAL_CASH   = 1000000

# === 初始化 ===
def init(context):
    subscribe(symbols=SYMBOLS, frequency=FREQUENCY, count=30)

# === K线回调 ===
def on_bar(context, bars):
    # 在这里写策略逻辑
    pass

# === 启动入口 ===
if __name__ == '__main__':
    TOKEN = os.environ.get('GM_TOKEN', '') or '你的token'
    run(strategy_id='your_strategy_id', filename='your_file',
        mode=MODE_BACKTEST, token=TOKEN,
        backtest_start_time=BACKTEST_START,
        backtest_end_time=BACKTEST_END,
        backtest_initial_cash=INITIAL_CASH,
        backtest_commission_ratio=0.00025,
        backtest_slippage_ratio=0.001,
        backtest_adjust=ADJUST_PREV)
```

### 7.2 标的代码格式

| 市场 | 代码前缀 | 示例 |
|------|---------|------|
| 上交所 | `SHSE.` | `SHSE.600519`（茅台）、`SHSE.510300`（沪深300ETF） |
| 深交所 | `SZSE.` | `SZSE.000001`（平安）、`SZSE.159949`（创业板50ETF） |

> ⚠️ ETF 的交易所：5 开头是沪市（SHSE），1 开头是深市（SZSE）

### 7.3 常用下单方式

```python
# 1. 按目标比例调仓（最推荐，简单好用）
order_target_percent(symbol='SHSE.600519', percent=0.3,
                     position_side=PositionSide_Long, order_type=OrderType_Market)

# 2. 按目标数量调仓（会自动算差值，只下增量单）
order_target_volume(symbol='SHSE.600519', volume=1000,
                    position_side=PositionSide_Long, order_type=OrderType_Market)

# 3. 按指定量下单（注意参数名是 position_effect，不是 position_side！）
order_volume(symbol='SHSE.600519', volume=200, side=OrderSide_Buy,
             order_type=OrderType_Market, position_effect=PositionEffect_Open)

# 4. 清仓：目标数量设为 0
order_target_volume(symbol='SHSE.600519', volume=0,
                    position_side=PositionSide_Long, order_type=OrderType_Market)
```

### 7.4 定时任务（替代日线回调）

```python
def init(context):
    # 每天 14:50 执行
    schedule(schedule_func=afternoon_trade, date_rule='1d', time_rule='14:50:00')

def afternoon_trade(context):
    # 在这里获取日线数据、执行交易
    data = context.data(symbol='SHSE.600519', frequency='1d', count=30)
    # ...
```

### 7.5 策略类型选择

| 策略类型 | 适用场景 | 核心函数 |
|---------|---------|---------|
| 日线驱动 | 中低频，日K线信号 | `on_bar` + `subscribe(frequency='1d')` |
| 定时任务 | 每天固定时间执行 | `schedule(time_rule='14:50:00')` |
| 分钟驱动 | 日内高频 | `on_bar` + `subscribe(frequency='60s')` |
| Tick驱动 | 超高频 | `on_tick` + `subscribe(frequency='tick')` |

---

## 8. 运行回测

### 8.1 用 WorkBuddy 运行（最简单）

直接告诉 AI：

```
用策略ID abc123 跑回测，回测今年1月到4月，日线
```

AI 会自动执行 `run_strategy.py` 并返回结果。

### 8.2 手动运行

```bash
cd %USERPROFILE%\.workbuddy\skills\gm-quant\scripts

python run_strategy.py \
    --strategy strategy_ma_cross.py \
    --strategy-id my_ma_strategy \
    --mode backtest \
    --token 你的token \
    --start "2024-01-02 09:30:00" \
    --end "2025-12-31 15:30:00"
```

### 8.3 查看回测结果

**终端网页查看（推荐）**：

1. 登录 https://www.myquant.cn
2. 进入"策略研究" → "我的策略"
3. 找到你的策略ID，点击查看
4. 可查看：收益曲线、回撤分析、持仓明细、交易记录

**命令行输出**：回测结束时会打印核心指标

### 8.4 回测注意事项

- ⚠️ **交易日 18:30 前**只能回测到上一个交易日的数据（当日日线 18:30 才更新）
- 回测时用 `ADJUST_PREV` 前复权，避免除权缺口
- 初始资金建议 100 万以上，太小可能因为股数不足 100 无法下单
- 手续费率默认 0.025%，滑点默认 0.1%

---

## 9. 启动仿真交易

### 9.1 前提条件

- 掘金终端已登录并保持打开
- 已获取仿真账户 ID（在掘金终端"交易"页面查看）

### 9.2 用 WorkBuddy 启动

```
把刚才的均线策略切换到仿真模式运行，账户ID是 xxx
```

AI 会自动修改运行模式并启动。

### 9.3 手动启动

```bash
python run_strategy.py \
    --strategy strategy_ma_cross.py \
    --strategy-id my_ma_strategy \
    --mode live \
    --token 你的token \
    --account-id 仿真账户ID
```

### 9.4 仿真注意事项

- 仿真使用真实行情，模拟撮合成交
- **定时任务时间过了要等第二天**——如果 14:50 的任务，15:00 才启动，今天不会触发
- **期货策略必须订阅具体合约**，主连合约没有行情推送
- **实时模式日线不推送**——交易时间内日线没走完，`on_bar` 不会收到日线。需要用 `schedule` 替代
- 建议先仿真至少 1 周再考虑实盘

---

## 10. 启动实盘交易

### 10.1 前提条件

- 已完成仿真测试，策略表现符合预期
- 掘金终端已绑定券商账户（在终端"交易"→"实盘"中绑定）
- 已获取实盘账户 ID

### 10.2 用 WorkBuddy 启动

```
把策略切换到实盘，账户ID是 xxx，确认策略逻辑无误
```

### 10.3 手动启动

```bash
python run_strategy.py \
    --strategy strategy_ma_cross.py \
    --strategy-id my_ma_strategy \
    --mode live \
    --token 你的token \
    --account-id 实盘账户ID
```

### 10.4 ⚠️ 实盘安全检查清单

在切换实盘前，务必确认：

- [ ] 策略已在仿真环境运行至少 1 周
- [ ] 策略逻辑已确认无误（特别是止损/止盈逻辑）
- [ ] 仓位管理已设置（避免全仓单只标的）
- [ ] 已设置风控规则（单日最大亏损等）
- [ ] 掘金终端保持运行且网络稳定
- [ ] 理解策略的风险特征和最大回撤

> 🚨 **实盘交易有真实资金风险，请谨慎操作！**

---

## 11. 在微信中操作

WorkBuddy 支持通过微信与 AI 交互，实现移动端策略管理。

### 11.1 绑定微信

1. 在 WorkBuddy 对话界面，点击右上角设置
2. 选择"绑定微信"
3. 扫码绑定

### 11.2 微信中使用

绑定后，你可以直接在微信中发消息给 WorkBuddy：

**开发策略**：
```
帮我写一个ETF轮动策略，20日动量选前3名，每周二调仓
```

**运行回测**：
```
用策略ID xxx 跑一下回测，最近3个月
```

**查看结果**：
```
回测结果怎么样？收益多少？
```

**启动仿真**：
```
把策略切到仿真模式，账户ID是 xxx
```

**查行情**：
```
茅台现在多少钱？PE多少？
```

### 11.3 微端限制

- 微信中无法直接查看图表（掘金终端网页查看）
- 长代码输出会被截断，建议说"把代码保存到文件"
- 回测运行时间较长时，微信消息可能延迟

---

## 12. 常见问题排查

### Q: 运行报错 "无效的token"

**原因**：Token 未设置或已过期

**解决**：
1. 确认掘金终端已登录
2. 重新获取 Token
3. 设置环境变量 `GM_TOKEN`

### Q: 实时模式（仿真/实盘）没有发生交易

**排查清单**：

| # | 检查项 | 解决方式 |
|---|--------|---------|
| 1 | 定时任务时间过了 | 等第二天，或改时间为当前之后几分钟 |
| 2 | 期货策略订阅了主连合约 | 实时模式必须订阅具体合约（如 `SHFE.ag2506`），主连没有行情 |
| 3 | 日线不推送 | 实时模式日线没走完不会推送，用 `schedule` 定时任务替代 |
| 4 | 打印日志 | 检查：数据推送 → 信号 → 下单 → 状态，逐级排查 |

### Q: 回测报错 "填写的 fields 不正确"

**原因**：财务数据 API 的 `fields` 参数必填，不能传空字符串

**解决**：传入具体字段名，且不超过 20 个。参考字段速查表 `references/17-financial-data-fields.md`

### Q: 下单报错 "position_side" 参数不对

**原因**：`order_volume()` 用 `position_effect`，`order_target_volume/percent` 用 `position_side`

**解决**：
```python
# order_volume → position_effect
order_volume(..., position_effect=PositionEffect_Open)

# order_target_volume/percent → position_side
order_target_volume(..., position_side=PositionSide_Long)
```

### Q: 回测收益为0，没有任何交易

**可能原因**：
1. 标的代码写错（大小写、交易所前缀）
2. 回测区间内没有触发信号
3. 资金不足导致无法下单（ETF 股票最小 100 股）
4. 18:30 前回测当天数据未更新

### Q: 562500 机器人ETF 找不到

**原因**：56 开头是沪市 ETF

**解决**：使用 `SHSE.562500`，不是 `SZSE.562500`

---

## 附录：API 速查

### 常用数据函数

| 函数 | 用途 | 示例 |
|------|------|------|
| `history()` | 获取历史K线 | `history(symbol='SHSE.600519', frequency='1d', count=30)` |
| `history_n()` | 获取最近N根K线 | `history_n(symbol='SHSE.600519', frequency='1d', count=10)` |
| `current()` | 获取最新行情 | `current(symbols='SHSE.600519')` |
| `get_fundamentals()` | 财务数据 | `stk_get_fundamentals_balance_pt(symbols='SHSE.600519', fields='fix_ast,ttl_ast')` |
| `get_trading_dates()` | 交易日历 | `get_trading_dates(exchange='SHSE', start_date='2024-01-01')` |
| `get_symbols()` | 标的信息 | `get_symbols(sec_types=SEC_TYPE_STOCK, exchanges='SHSE')` |

### 常用交易函数

| 函数 | 用途 | 关键参数 |
|------|------|---------|
| `order_volume()` | 按量下单 | `symbol, volume, side, order_type, position_effect` |
| `order_target_volume()` | 调仓到目标量 | `symbol, volume, position_side, order_type` |
| `order_target_percent()` | 调仓到目标比例 | `symbol, percent, position_side, order_type` |
| `order_percent()` | 按总资产比例买 | `symbol, percent, side, order_type, position_effect` |
| `get_position()` | 查询持仓 | 无参返回全部持仓 |
| `get_cash()` | 查询资金 | 返回 available/nav 等 |
| `get_orders()` | 查询委托 | 返回当日所有委托 |

### 常用枚举

| 枚举 | 值 | 说明 |
|------|---|------|
| `OrderSide_Buy` | 1 | 买入 |
| `OrderSide_Sell` | 2 | 卖出 |
| `OrderType_Market` | 2 | 市价单 |
| `OrderType_Limit` | 1 | 限价单 |
| `PositionSide_Long` | 1 | 多头 |
| `PositionSide_Short` | 2 | 空头 |
| `PositionEffect_Open` | 1 | 开仓 |
| `PositionEffect_Close` | 3 | 平仓 |
| `MODE_BACKTEST` | 2 | 回测模式 |
| `MODE_LIVE` | 1 | 实时模式 |
| `ADJUST_PREV` | 1 | 前复权 |

### 财务数据字段速查

| 类别 | API | 常用字段 |
|------|-----|---------|
| 资产负债表 | `stk_get_fundamentals_balance_pt` | fix_ast, ttl_ast, ttl_liab, ttl_eqy, mny_cptl |
| 利润表 | `stk_get_fundamentals_income_pt` | inc_oper, ttl_inc_oper, net_prof, net_prof_pcom |
| 现金流量表 | `stk_get_fundamentals_cashflow_pt` | net_cf_oper, net_cf_inv, net_cf_fin |
| 财务主要指标 | `stk_get_finance_prime_pt` | eps_basic, eps_dil, roe_weight_avg, bps_sh |
| 估值指标 | `stk_get_daily_valuation_pt` | pe_ttm, pb_mrq, ps_ttm, dy_ttm |
| 市值指标 | `stk_get_daily_mktvalue_pt` | tot_mv, a_mv, ev |
| 基础指标 | `stk_get_daily_basic_pt` | tclose, turnrate, ttl_shr, circ_shr |

> ⚠️ 所有 `_pt` 后缀函数：`fields` 必填且不能为空，不超过 20 个字段

---

**手册版本**：v1.0 | 更新日期：2026-04-17 | 适用于 gm-quant skill v2.0
