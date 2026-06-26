---
name: gm-quant
version: 2.1.0
description: >
  掘金量化 Python SDK 专家技能。 当用户提到掘金、gm、gm.api、掘金量化、掘金策略、掘金SDK、掘金终端、
  量化策略开发、回测、实时行情、订阅行情、历史行情、下单、委托、持仓、
  order_volume、subscribe、history、set_token、get_symbols、get_symbol_infos、
  get_history_symbol、history_n、current、last_tick、current_price、get_trading_dates、
  order_percent、order_value、order_target_volume、algo_order、
  get_orders、get_position、get_cash、bond_convertible、
  L2行情、逐笔成交、逐笔委托、schedule定时任务、 财务数据、资产负债表、利润表、现金流量表、估值指标、PE/PB/PS/股息率、
  市值、股本、流通股、成分股、行业分类、 可转债分析、转股溢价率、纯债价值、ETF成分股、基金净值、 期货合约信息、仓单数据、成交持仓排名、连续合约、
  stk_get_fundamentals、stk_get_daily_valuation、stk_get_index_constituents、
  stk_get_industry_category、stk_get_industry_constituents、stk_get_symbol_industry、
  stk_get_sector_category、stk_get_sector_constituents、stk_get_symbol_sector、
  stk_get_dividend、stk_get_ration、stk_get_adj_factor、stk_get_shareholder_num、
  stk_get_top_shareholder、stk_get_share_change、stk_abnor_change_stocks、
  stk_abnor_change_detail、stk_quota_shszhk_infos、stk_active_stock_top10_shszhk_info、
  stk_get_money_flow、stk_get_finance_audit、stk_get_finance_forecast、
  bnd_get_analysis、bnd_get_conversion_price、bnd_get_call_info、bnd_get_put_info、bnd_get_amount_change、
  fnd_get_portfolio、fnd_get_etf_constituents、fnd_get_net_value、fnd_get_adj_factor、fnd_get_dividend、fnd_get_split、fnd_get_share、
  fut_get_contract_info、fut_get_continuous_contracts、fut_get_transaction_rankings、fut_get_warehouse_receipt、
  get_open_call_auction
  时，自动加载此 skill。
---

# 掘金量化 SDK 技能 — v2.0 自然语言策略引擎

## 定位

你是**掘金量化平台的自然语言策略助手**。用户用中文描述交易想法，你负责：
1. **理解需求** → 提炼策略逻辑（标的/信号/风控）
2. **生成代码** → 输出可直接运行的完整策略 `.py` 文件
3. **执行运行** → 调用 `scripts/run_strategy.py` 一键启动回测或实盘

## 核心原则

1. **必须先 set_token**：纯数据查询（非策略 run）场景下，代码开头必须调用 `set_token('your_token')`。
2. **symbol 格式**：`交易所代码.证券代码`，如 `SHSE.600000`、`SZSE.000001`，**严格区分大小写**。
3. **gm 包通过掘金终端连接**：终端必须保持打开，否则接口会超时或报错。
4. **两种模式**：`MODE_LIVE=1`（实时/仿真）、`MODE_BACKTEST=2`（回测）；`run()` 函数启动策略。
5. **数据查询不需要 run**：仅用 `set_token` 后直接调用数据函数即可。

## 🚀 用户工作流（自然语言→运行）

### 第 0 步：确认 Strategy ID（重要！）

**每次生成策略前，必须向用户索要 `strategy_id`。**

`strategy_id` 是策略在掘金终端中的唯一标识。填写后：
- 回测结果**持久化**到掘金终端后台
- 用户登录 [掘金终端网页](https://www.myquant.cn) → 策略列表 → 查看完整的**绩效分析图表**
  （收益曲线、回撤分析、夏普比率、持仓明细等）

> **交互方式**：如果用户没有主动提供 strategy_id，在生成代码前询问：
> "请给我一个 **strategy_id**（英文/数字/下划线），用于在掘金终端标识这个策略。
> 填完后你可以在终端网页上看到绩效分析图表。例如：`ma_cross_600519`、`momentum_v1`"

| 场景 | 处理方式 |
|------|---------|
| 用户提供了 strategy_id | 直接使用 |
| 用户没提供 | **必须追问**，不能自己编造一个默认值后静默使用 |
| 用户说"随便起一个" | 根据策略特征起一个有意义的名字（如 `dual_ma_kweichow`） |

### 第一步：理解用户意图

当用户用自然语言描述策略时，按以下维度提取信息：

| 维度 | 需确认的信息 | 默认值（如未明确说明） |
|------|-------------|---------------------|
| **strategy_id** | 策略在掘金终端的标识（**必须用户提供，见第0步**） | 无默认，必须询问 |
| **标的池** | 哪些股票/指数？ | 沪深300成分股 |
| **时间频率** | 日线/分钟线/tick？ | 日线 `1d` |
| **买入信号** | 什么条件买入？（均线/指标/事件） | 必须明确，不能猜测 |
| **卖出信号** | 什么条件卖出？ | 必须明确，不能猜测 |
| **仓位管理** | 全仓/固定金额/比例/等权 | 等权分配 |
| **止损止盈** | 有无？阈值多少？ | 无 |
| **回测区间** | 开始~结束日期 | 最近1年 |
| **初始资金** | 多少钱？ | 100万 |
| **运行模式** | 回测还是实盘？ | 先回测 |

> ⚠️ **如果用户描述模糊（如"帮我做个赚钱的策略"），必须追问具体条件后再生成代码。**

### 第二步：生成策略文件

使用下方**标准策略模板**生成完整 `.py` 文件，保存到用户的输出目录：

```python
"""
策略名称：{name}
策略描述：{description}
生成时间：{date}
"""

import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from gm.api import *

# ============================================================
# 配置区 —— 用户可通过修改此处调整策略参数
# ============================================================
SYMBOLS = 'SHSE.600519,SZSE.000001'      # 标的（逗号分隔）
FREQUENCY = '1d'                          # K线周期：1d/60s/300s/tick
COUNT = 20                                # 订阅K线数量（context.data滑窗大小）

# 交易参数
ORDER_TYPE = OrderType_Market              # 下单方式：Market(市价) / Limit(限价)
POSITION_PCT = 0.2                        # 单只股票仓位占比（0~1）

# 回测参数
BACKTEST_START = '2024-01-02 09:30:00'
BACKTEST_END   = '2025-12-31 15:30:00'
INITIAL_CASH   = 1000000                  # 初始资金
COMMISSION     = 0.00025                  # 手续费率
SLIPPAGE       = 0.001                    # 滑点


# ============================================================
# 策略逻辑
# ============================================================

def init(context):
    """初始化：订阅行情"""
    log.info(f'策略启动 | 标的:{SYMBOLS} | 周期:{FREQUENCY}')
    subscribe(symbols=SYMBOLS, frequency=FREQUENCY, count=COUNT)

    # 存储策略状态
    context.last_signal = {}  # {symbol: last_signal_time}


def on_bar(context, bars):
    """每根K线触发"""
    for bar in bars:
        symbol = bar['symbol']
        try:
            _handle_bar(context, symbol)
        except Exception as e:
            log.error(f'处理{symbol}异常: {e}')


def on_tick(context, tick):
    """tick级别回调（如订阅了tick会走这里）"""
    pass


def _handle_bar(context, symbol):
    """单只标的策略逻辑"""

    # 1. 获取历史数据（滑窗内）—— 注意返回 DataFrame
    data = context.data(symbol=symbol, frequency=FREQUENCY, count=COUNT)
    if data is None or len(data) < COUNT:
        return

    # 2. 获取当前持仓 —— get_position() 不带参数，返回全部持仓列表
    all_positions = get_position()
    position = None
    if all_positions:
        for p in all_positions:
            sym = p.get('symbol') if isinstance(p, dict) else (p.symbol if hasattr(p, 'symbol') else None)
            if sym == symbol:
                position = p
                break

    # ========================================
    # 【策略核心】在此处实现买卖信号
    # ========================================

    # 示例：双均线策略
    close = data['close'].tolist()
    ma_short = sum(close[-5:]) / 5    # MA5
    ma_long  = sum(close[-20:]) / 20  # MA20
    prev_ma5 = sum(close[-6:-1]) / 5 if len(close) >= 6 else ma_short
    prev_ma20 = sum(close[-26:-6]) / 20 if len(close) >= 27 else ma_long

    buy_signal  = (prev_ma5 <= prev_ma20) and (ma_short > ma_long)
    sell_signal = (prev_ma5 >= prev_ma20) and (ma_short < ma_long)

    # ========================================
    # 3. 执行交易
    # ========================================

    current_price = close[-1]
    cash_info = get_cash()

    if buy_signal and not position:
        # 买入：按仓位比例计算金额
        available = cash_info.available
        order_value = available * POSITION_PCT
        if order_value > 10000:  # 最少1万元
            volume = int(order_value / current_price / 100) * 100  # A股必须100股整数倍
            order_volume(symbol, volume,
                         side=OrderSide_Buy,
                         position_effect=PositionEffect_Open,
                         order_type=ORDER_TYPE)
            print(f'[买入] {symbol} 价格={current_price:.2f} 数量={volume}')

    elif sell_signal and position:
        # 卖出：清仓该标的（注意用 position_side 不是 position_effect）
        order_target_volume(symbol, 0,
                            position_side=PositionSide_Long,
                            order_type=ORDER_TYPE)
        print(f'[卖出] {symbol} 价格={current_price:.2f}')


def handle_error(context, error_code, error_msg, **kwargs):
    """错误处理"""
    log.error(f'策略异常 [{error_code}]: {msg}')


# ============================================================
# 启动入口
# ============================================================
if __name__ == '__main__':
    # 从环境变量读取参数（由 run_strategy.py 传入）
    TOKEN = os.environ.get('GM_TOKEN', '') or ''
    MODE = os.environ.get('GM_RUN_MODE', 'backtest')
    STRATEGY_ID = os.environ.get('GM_STRATEGY_ID', '') or 'my_strategy'
    START = os.environ.get('GM_BACKTEST_START', BACKTEST_START)
    END = os.environ.get('GM_BACKTEST_END', BACKTEST_END)
    CASH = float(os.environ.get('GM_INITIAL_CASH', str(INITIAL_CASH)))

    mode = MODE_LIVE if MODE.lower() in ('live', 'realtime') else MODE_BACKTEST

    run(
        strategy_id=STRATEGY_ID,
        filename=__file__[:__file__.rfind('.')] if '.' in __file__ else __file__,
        mode=mode,
        token=TOKEN,
        backtest_start_time=START,
        backtest_end_time=END,
        backtest_initial_cash=CASH,
        backtest_commission_ratio=COMMISSION,
        backtest_slippage_ratio=SLIPPAGE,
        backtest_adjust=ADJUST_PREV,
    )
```

### 第三步：执行策略

使用运行器脚本一键执行：

```bash
python scripts/run_strategy.py --strategy <策略文件路径> --strategy-id <你的策略ID> [--mode backtest|live] [--token YOUR_TOKEN]
```

> **`--strategy-id` 必填**：填写后回测结果会持久化到掘金终端，登录终端网页即可查看绩效分析图表（收益曲线、回撤、夏普比率等）。
> 如果不填，回测结果仅在控制台输出，不会保存到终端。

运行器脚本路径：`C:\Users\wjz\.workbuddy\skills\gm-quant\scripts\run_strategy.py`

## 参考文档索引

详细 API 文档位于 `references/` 目录下：

| 文件 | 内容 |
|------|------|
| `01-quick-start.md` | 快速开始、策略架构、运行模式 |
| `02-core-functions.md` | `run`、`set_token`、`stop`、`schedule`、`timer` |
| `03-subscribe-events.md` | `subscribe`、`unsubscribe`、`on_tick`、`on_bar`、`on_l2*` |
| `04-market-data.md` | `current`、`last_tick`、`current_price`、`history`、`history_n`、`context.data` |
| `05-l2-data.md` | L2 行情查询接口（付费） |
| `06-symbol-info.md` | 标的信息查询 API |
| `07-trading-dates.md` | 交易日历 API |
| `08-order-api.md` | 下单 API 全集 |
| `09-algo-order.md` | 算法单 API |
| `10-account-query.md` | 账户查询 API |
| `11-bond-convertible.md` | 可转债交易 API |
| `12-dataobjects.md` | 数据对象字段定义 |
| `13-enums.md` | 枚举常量速查 |
| `14-context.md` | context 对象 |
| `15-user-guide.md` | 用户指南（常见问题） |
| `16-premium-data-apis.md` | 增值数据 API 速查合集（股票/基金/转债/期货） |
| `17-financial-data-fields.md` | 财务数据字段定义 |
| `18-stock-premium-apis.md` | 股票增值数据 API 完整文档（行业/板块/分红/龙虎榜/沪深港通/资金流向等） |
| `19-fund-premium-apis.md` | 基金增值数据 API 完整文档（ETF成分股/净值/资产组合/规模等） |
| `20-cb-premium-apis.md` | 可转债增值数据 API 完整文档（转股价/赎回/回售/分析指标等） |
| `21-futures-premium-apis.md` | 期货增值数据 API 完整文档（品种信息/成交持仓排名/仓单/连续合约映射等） |

## 交易 API 补充

### 融资融券（信用交易）

融资融券交易需在信用账户下操作，使用 `credit_` 前缀函数：

```python
# 融资买入（借入资金买证券）
credit_buying_on_margin(symbol, volume, price=0, order_type=OrderType_Market, position_effect=PositionEffect_Open)

# 融券卖出（借入证券卖出）
credit_short_selling(symbol, volume, price=0, order_type=OrderType_Market, position_effect=PositionEffect_Open)

# 买券还券（买入证券归还融券）
credit_buying_on_repayment(symbol, volume, price=0, order_type=OrderType_Market)

# 卖券还款（卖出证券归还融资）
credit_selling_on_repayment(symbol, volume, price=0, order_type=OrderType_Market)

# 直接还款（用现金直接归还融资）
credit_direct_repayment(amount)

# 直接还券（用持仓直接归还融券）
credit_direct_return_securities(symbol, volume)

# 信用账户查询
credit_get_collateral_instruments()    # 查询可担保证券
credit_get_borrowable_instruments()    # 查询可融券证券
credit_get_collateral_ratio(symbol)    # 查询担保折算率
credit_get_concentrate_limit(symbol)   # 查询集中度限制
credit_get_margin_ratio(symbol)        # 查询融资融券保证金比例
credit_get_max_volume(symbol, side)    # 查询最大可借数量
```

> ⚠️ 融资融券功能需要开通信用账户，且掘金终端需切换到信用交易模式。

### 批量下单

```python
# 批量下单 — 一次提交多笔委托，减少网络往返
orders = [
    {'symbol': 'SHSE.600519', 'volume': 100, 'side': OrderSide_Buy, 'position_effect': PositionEffect_Open, 'order_type': OrderType_Market},
    {'symbol': 'SZSE.000001', 'volume': 200, 'side': OrderSide_Buy, 'position_effect': PositionEffect_Open, 'order_type': OrderType_Market},
]
order_batch(orders)
```

> `order_batch` 返回订单ID列表，与 `order_volume` 返回值一致。

### 撤单

```python
# 撤销指定委托
order_cancel(cl_ord_id)         # cl_ord_id 从 get_orders() 或 on_order_status 回调中获取

# 撤销全部未成交委托
order_cancel_all()

# 查询未成交委托
get_unfinished_orders()
```

> `order_cancel` 的参数是 `cl_ord_id`（客户端订单ID），**不是** `order_id`。可以从 `on_order_status` 回调的 `order.cl_ord_id` 字段或 `get_unfinished_orders()` 返回值中获取。

### 特殊交易函数

```python
# 新股申购
ipo_buy(symbol, volume, price=0, order_type=OrderType_Limit)

# ETF 申购/赎回（场内基金）
fund_etf_buy(symbol, volume, price=0, order_type=OrderType_Market)       # ETF 申购
fund_etf_redemption(symbol, volume, price=0, order_type=OrderType_Market) # ETF 赎回

# 场外基金
fund_subscribing(symbol, volume, price=0)   # 场外基金认购
fund_buy(symbol, volume, price=0)           # 场外基金申购
fund_redemption(symbol, volume, price=0)    # 场外基金赎回

# 国债逆回购
bond_reverse_repurchase_agreement(symbol, volume, price=0, order_type=OrderType_Limit)
```

> ⚠️ 国债逆回购的 `volume` 单位是**张**（1张=1000元面值），`price` 是年化利率（如 2.5 表示年化 2.5%）。

### 动态参数（终端 UI 可调）

在 `init()` 中用 `add_parameter` 注册参数后，用户可在掘金终端 UI 上实时调整策略参数，无需改代码重启：

```python
def init(context):
    add_parameter(key='ma_short', value=5, min=1, max=100, step=1, name='短期均线周期')
    add_parameter(key='ma_long', value=20, min=1, max=200, step=1, name='长期均线周期')
    add_parameter(key='stop_loss_pct', value=0.05, min=0.01, max=0.5, step=0.01, name='止损比例')

# 用户在终端修改参数时触发回调
def on_parameter(context, parameter):
    key = parameter['key']
    value = parameter['value']
    log.info(f'参数变更: {key} = {value}')
    if key == 'ma_short':
        context.ma_short_period = value

# 策略中读取当前参数值
def on_bar(context, bars):
    ma_short = get_parameter(key='ma_short')
    ma_long = get_parameter(key='ma_long')
```

### 连接事件

适用于实盘/仿真模式，可用于断线重连逻辑或告警通知（回测模式下不会触发）：

```python
def on_market_data_connected(context):
    log.info('行情服务已连接')

def on_market_data_disconnected(context):
    log.info('行情服务已断开')

def on_trade_data_connected(context):
    log.info('交易服务已连接')

def on_trade_data_disconnected(context):
    log.info('交易服务已断开')
```

### 交易所代码表

| 代码 | 交易所 | 示例 |
|------|--------|------|
| SHSE | 上海证券交易所 | SHSE.600000 |
| SZSE | 深圳证券交易所 | SZSE.000001 |
| CFFEX | 中国金融期货交易所 | CFFEX.IF2506 |
| SHFE | 上海期货交易所 | SHFE.ag2506 |
| DCE | 大连商品交易所 | DCE.m2509 |
| CZCE | 郑州商品交易所 | CZCE.CF501 |
| INE | 上海国际能源交易中心 | INE.sc2506 |
| GFEX | 广州期货交易所 | GFEX.si2508 |

### 枚举常量表（速查）

```python
# ---- 订单状态 OrderStatus ----
OrderStatus_New = 1                # 新建
OrderStatus_PartiallyFilled = 3    # 部分成交
OrderStatus_Filled = 4             # 全部成交
OrderStatus_Canceled = 5           # 已撤
OrderStatus_Rejected = 7           # 拒绝
OrderStatus_Cancelling = 8         # 待撤
# 注意：回测中可能出现未记录状态码 10（内部中间态），需兼容处理

# ---- 订单类型 OrderType ----
OrderType_Market = 1               # 市价单
OrderType_Limit = 2                # 限价单

# ---- 买卖方向 OrderSide ----
OrderSide_Buy = 1
OrderSide_Sell = 2

# ---- 开平仓 PositionEffect（order_volume 用）----
PositionEffect_Open = 1            # 开仓
PositionEffect_Close = 2           # 平仓
PositionEffect_CloseToday = 3      # 平今
PositionEffect_CloseYesterday = 4  # 平昨

# ---- 持仓方向 PositionSide（order_target_* 用）----
PositionSide_Long = 1
PositionSide_Short = 2

# ---- 复权方式 AdjustType ----
ADJUST_NONE = 0                    # 不复权
ADJUST_PREV = 1                    # 前复权（回测常用）
ADJUST_POST = 2                    # 后复权

# ---- 运行模式 ----
MODE_LIVE = 1                      # 实时/仿真
MODE_BACKTEST = 2                  # 回测
```

### 数据频率与运行模式

**K线频率（frequency）**：

| 值 | 说明 |
|----|------|
| `tick` | 逐笔 |
| `60s` | 1分钟 |
| `300s` | 5分钟 |
| `900s` | 15分钟 |
| `1800s` | 30分钟 |
| `3600s` | 1小时 |
| `1d` | 日线 |

**运行模式**：

| 值 | 说明 |
|----|------|
| `MODE_LIVE = 1` | 实时/仿真模式，行情实时推送 |
| `MODE_BACKTEST = 2` | 回测模式，数据按时间序列回放 |

### ~~基本面数据（已下线）~~

> ⚠️ `get_fundamentals()` / `get_fundamentals_n()` 已下线，请使用 `stk_get_fundamentals_*_pt` 系列替代。

### 新股申购

```python
# 查询新股申购额度
ipo_get_quota(exchange='SHSE')        # 返回沪市/深市可用额度

# 查询可申购新股列表
ipo_get_instruments(trade_date='2025-01-15')  # 指定交易日的可申购新股

# 查询申购配号
ipo_get_match_number(symbol='SHSE.688001')

# 查询中签信息
ipo_get_lot_info(symbol='SHSE.688001')
```

### 分红数据

```python
# 查询分红送配数据（时序）
get_dividend(symbol='SHSE.600519', start_date='2020-01-01', end_date='2025-12-31', df=True)
# 返回字段：ex_date(除权日), record_date(登记日), pay_date(发放日), cash_div(每股派息),
#           bonus_share_r(送股比例), transfer_share_r(转增比例)
```

### L2 历史数据查询

```python
# L2 逐笔成交
get_history_l2_transaction(symbol, start_time, end_time, fields=None, df=True)

# L2 逐笔委托
get_history_l2_order(symbol, start_time, end_time, fields=None, df=True)

# L2 队列（买卖盘口）
get_history_l2_queue(symbol, start_time, end_time, fields=None, df=True)
```

> ⚠️ L2 数据接口为付费功能，仅特定券商可用，需要开通相应权限。

## 进阶策略示例

### 配对交易（均值回归）

```python
def init(context):
    context.pair = ('SHSE.600036', 'SZSE.000001')  # 招行 vs 平安
    subscribe(symbols=','.join(context.pair), frequency='1d', count=60)
    context.half_life = 20
    context.entry_z = 2.0
    context.exit_z = 0.5

def on_bar(context, bars):
    s1, s2 = context.pair
    d1 = context.data(symbol=s1, frequency='1d', count=60)
    d2 = context.data(symbol=s2, frequency='1d', count=60)
    if d1 is None or d2 is None or len(d1) < 30:
        return

    spread = d1['close'].values / d2['close'].values
    mean = spread[-context.half_life:].mean()
    std = spread[-context.half_life:].std()
    zscore = (spread[-1] - mean) / std if std > 0 else 0

    if zscore > context.entry_z and _get_position_volume(context, s1) == 0:
        order_target_percent(s1, -0.5, position_side=PositionSide_Short, order_type=OrderType_Market)
        order_target_percent(s2, 0.5, position_side=PositionSide_Long, order_type=OrderType_Market)
    elif zscore < -context.entry_z and _get_position_volume(context, s2) == 0:
        order_target_percent(s1, 0.5, position_side=PositionSide_Long, order_type=OrderType_Market)
        order_target_percent(s2, -0.5, position_side=PositionSide_Short, order_type=OrderType_Market)
    elif abs(zscore) < context.exit_z:
        for sym in context.pair:
            order_target_volume(sym, 0, position_side=PositionSide_Long, order_type=OrderType_Market)
            order_target_volume(sym, 0, position_side=PositionSide_Short, order_type=OrderType_Market)
```

### CTA 海龟交易法

```python
def init(context):
    subscribe(symbols='SHFE.ag2506', frequency='1d', count=55)
    context.atr_period = 20
    context.entry_period = 20
    context.exit_period = 10
    context.unit_risk = 0.01  # 每笔最大亏损占总资金1%

def on_bar(context, bars):
    data = context.data(symbol='SHFE.ag2506', frequency='1d', count=55)
    if data is None or len(data) < 55:
        return

    high, low, close = data['high'].values, data['low'].values, data['close'].values
    tr = [max(high[i]-low[i], abs(high[i]-close[i-1]), abs(low[i]-close[i-1])) for i in range(1, len(close))]
    atr = sum(tr[-context.atr_period:]) / context.atr_period

    entry_high = max(high[-context.entry_period:-1])
    exit_low = min(low[-context.exit_period:-1])
    curr = close[-1]

    cash = get_cash()
    unit = int(cash.available * context.unit_risk / atr / 1000) * 1000
    pos = _get_position_volume(context, 'SHFE.ag2506')

    if curr > entry_high and pos == 0:
        order_volume('SHFE.ag2506', unit, side=OrderSide_Buy,
                     position_effect=PositionEffect_Open, order_type=OrderType_Market)
    elif curr < exit_low and pos > 0:
        order_volume('SHFE.ag2506', pos, side=OrderSide_Sell,
                     position_effect=PositionEffect_Close, order_type=OrderType_Market)
```

### 风控模块（可嵌入任意策略）

```python
class RiskManager:
    """通用风控：止损/止盈/最大持仓/回撤控制"""

    def __init__(self, stop_loss_pct=0.05, take_profit_pct=0.10,
                 max_position_pct=0.3, max_drawdown_pct=0.15):
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.max_position_pct = max_position_pct
        self.max_drawdown_pct = max_drawdown_pct
        self.peak_value = 0

    def check_stop_loss(self, entry_price, current_price, side='long'):
        if side == 'long':
            return (current_price - entry_price) / entry_price < -self.stop_loss_pct
        return (entry_price - current_price) / entry_price < -self.stop_loss_pct

    def check_take_profit(self, entry_price, current_price, side='long'):
        if side == 'long':
            return (current_price - entry_price) / entry_price > self.take_profit_pct
        return (entry_price - current_price) / entry_price > self.take_profit_pct

    def check_drawdown(self):
        cash = get_cash()
        total = cash.nav if hasattr(cash, 'nav') else cash.available
        self.peak_value = max(self.peak_value, total)
        dd = (self.peak_value - total) / self.peak_value if self.peak_value > 0 else 0
        return dd > self.max_drawdown_pct

    def check_position_limit(self, symbol_value, total_value):
        return (symbol_value / total_value) > self.max_position_pct
```

### 行业轮动（动量因子 + schedule 定时调仓）

```python
def init(context):
    context.sectors = {
        'SHSE.512000': '券商', 'SHSE.512010': '医药', 'SHSE.512660': '军工',
        'SHSE.512800': '银行', 'SHSE.512690': '白酒', 'SHSE.515030': '新能源',
    }
    context.top_n = 2
    subscribe(symbols=','.join(context.sectors.keys()), frequency='1d', count=22)
    schedule(rebalance, frequency='1d', time_rule='15:05')

def rebalance(context, bar_dict):
    momentum = {}
    for sym in context.sectors:
        data = context.data(symbol=sym, frequency='1d', count=22)
        if data is not None and len(data) >= 20:
            momentum[sym] = data['close'].iloc[-1] / data['close'].iloc[-20] - 1

    ranked = sorted(momentum.items(), key=lambda x: x[1], reverse=True)
    targets = [s[0] for s in ranked[:context.top_n]]

    for sym in context.sectors:
        if sym in targets:
            order_target_percent(sym, 1.0 / context.top_n,
                                 position_side=PositionSide_Long, order_type=OrderType_Market)
        else:
            order_target_volume(sym, 0,
                                position_side=PositionSide_Long, order_type=OrderType_Market)
```

## API 参数补充说明

### current() 回测 vs 实盘字段差异

```python
data = current(symbols='SHSE.600519,SZSE.000001')
# 通用字段：symbol, open, high, low, close, volume, amount, frequency, timestamp
# 实盘额外字段：bid_price/bid_volume(买价买量), ask_price/ask_volume(卖价卖量),
#               last_price(最新价), num_trades(成交笔数)
```

> ⚠️ 回测模式下 `current()` 只能查询已订阅标的，实盘模式可查询任意标的。

**⚠️ current() 实时模式调用频次限制（2026-05-19 起）**：
- 5分钟内最多调用 **100 次**
- 24小时内最多调用 **1000 次**
- **2026-06-01 起**：单次查询标的数量上限调整为 **50 个**

### last_tick — 查询已订阅的最新 Tick（推荐替代 current）

不受 `current()` 调用频次限制，返回数据更精简高效。

```python
last_tick(symbols, fields="", include_call_auction=False)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| symbols | str or list | 标的代码，多个用英文逗号隔开或列表格式 |
| fields | str | 返回字段，默认所有 |
| include_call_auction | bool | 是否支持集合竞价(09:15-09:25)取数，默认 False |

**返回值**：`list[dict]`，每项包含 `symbol`、`price`、`created_at` 等字段

```python
from gm.api import *
set_token('YOUR_TOKEN')

subscribe(symbols='SZSE.000001,SHSE.600000', frequency='tick')
result = last_tick(symbols='SZSE.000001,SHSE.600000', fields='symbol,price,open,created_at')
for item in result:
    print(item['symbol'], item['price'])
```

> ⚠️ 输入的 `symbols` **必须先通过 `subscribe` 订阅 tick 行情**；若未订阅，返回空数据。

### current_price — 查询当前最新价（更轻量替代 current）

仅返回最新价，不受 `current()` 调用频次限制。

```python
current_price(symbols)
```

| 参数 | 类型 | 说明 |
|------|------|------|
| symbols | str or list | 标的代码，多个用英文逗号隔开或列表格式 |

**返回值**：`list[dict]`，每项包含 `symbol`、`price`、`created_at`

```python
from gm.api import *
set_token('YOUR_TOKEN')

result = current_price(symbols='SZSE.000001,SHSE.600000')
print(result[0]['symbol'], result[0]['price'])
```

### fut_get_continuous_contracts — 查询连续合约对应的真实合约

```python
fut_get_continuous_contracts(csymbol, start_date="", end_date="")
```

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:----:|:-----:|------|
| csymbol | str | Y | 无 | 连续合约代码，只能输入一个。支持主力/次主力/前5个月份/加权指数 |
| start_date | str | N | "" | 开始日期 %Y-%m-%d，默认最新交易日 |
| end_date | str | N | "" | 结束日期 %Y-%m-%d，默认最新交易日 |

**csymbol 连续合约后缀规则**：

| 后缀 | 含义 | 示例 |
|:----:|------|------|
| 无 | 主力连续 | `CFFEX.IM` |
| 22 | 次主力连续 | `CFFEX.IM22` |
| 00 | 当月连续 | `CFFEX.IM00` |
| 01 | 下月连续 | `CFFEX.IM01` |
| 02 | 下季连续 | `CFFEX.IM02` |
| 03 | 隔季连续 | `CFFEX.IM03` |
| 99 | 加权指数 | `CFFEX.IM99` |

```python
from gm.api import *
set_token('YOUR_TOKEN')

# 查询中证1000主力连续合约2025年真实合约
df = fut_get_continuous_contracts('CFFEX.IM', start_date='2025-01-01', end_date='2025-12-31')
print(df)
```

### history() 补充参数

```python
history(symbol, frequency, start_time=None, end_time=None, count=None,
        fields=None, skip_suspended=True, fill_missing=None, df=True)

# skip_suspended=True（默认）：跳过停牌日
# skip_suspended=False：保留停牌日，数据字段用 NaN 填充

# fill_missing='pre'：用前值填充缺失
# fill_missing='post'：用后值填充缺失
# fill_missing=None（默认）：不填充
```

### subscribe() wait_group 参数

```python
# 多标的等待同步：所有标的bar都到达后才触发一次 on_bar
subscribe(symbols='SHSE.600519,SZSE.000001', frequency='60s', count=20,
          wait_group=True)

# 默认 wait_group=False：每个标的bar到达时单独触发
```

> 多标的同频率策略建议开启 `wait_group=True`，避免部分标的先触发导致数据不齐。

### order_value / order_percent / order_target_percent

```python
# order_value — 按金额下单（自动取整到100股倍数）
order_value(symbol='SHSE.600519', value=50000, side=OrderSide_Buy,
            position_effect=PositionEffect_Open, order_type=OrderType_Market)

# order_percent — 按总资产百分比下单
order_percent(symbol='SHSE.600519', percent=0.1, side=OrderSide_Buy,
              position_effect=PositionEffect_Open, order_type=OrderType_Market)
# percent=0.1 表示用总资产的10%买入

# order_target_percent — 调仓到目标占比（ETF 调仓推荐）
order_target_percent(symbol='SHSE.512000', percent=0.15,
                     position_side=PositionSide_Long, order_type=OrderType_Market)
# 调整到占总资产15%，不足买入，超出卖出
```

### 成交回报查询

```python
get_execution_reports(cl_ord_id=None, symbol=None, start_time=None,
                      end_time=None, position_side=None, limit=None, df=True)
# cl_ord_id: 指定订单ID
# symbol: 指定标的
# limit: 返回条数限制
```

## 常见问题 & 注意事项

- `history()` 的 `df` 参数默认 `True` 返回 DataFrame，`False` 返回 `list[dict]`
- 单次查询最多返回 33000 条数据
- L2 数据接口（`get_history_l2*`）仅特定付费券商可用
- `subscribe` 中 `count` 决定 `context.data` 的滑窗大小
- 回测模式下 `init` 不支持交易操作
- 虚拟合约（主力连续合约）仅在回测模式下可用，如 `SHFE.RB`
- `get_trading_dates` 查交易日历时，`exchange` 参数用交易所代码如 `'SHSE'`
- `run()` 参数名是 `strategy_id` 和 `filename`（模块名，不是文件路径！）
- A 股最小下单单位为 100 股（1手），`order_volume` 必须是 100 的整数倍
- `order_value` 会自动取整到 100 股倍数

## 踩坑经验（实测验证）

**以下坑点已通过实际运行验证，生成代码时必须遵守：**

1. **`run()` 参数名**：是 `strategy_id` + `filename`（模块名，不带 .py 后缀），不是 `strategy_name` / `file_path`
2. **`log()` 用法**：`log(msg, source)` 是普通函数，**不是** logger 对象。不要用 `log.info()`。推荐直接用 `print()`
3. **`context.data()` 返回值**：返回的是 **DataFrame**（不是 dict list），用 `data['close'].tolist()` 访问数据列
4. **`get_position()` 不带参数**：调用 `get_position()` 获取全部持仓列表，然后遍历查找目标 symbol 的持仓。不支持 `get_position(symbol=xxx)`
5. **`order_target_volume()` 参数**：不需要 `side` 参数；用 `position_side=PositionSide_Long`（不是 `position_effect=PositionEffect_Close`）
6. **`order_volume()` 买入参数**：需要 `side=OrderSide_Buy` + `position_effect=PositionEffect_Open`
7. **Windows 编码**：脚本开头必须加 `sys.stdout = io.TextIOWrapper(...)` 否则中文 emoji 报错
8. **A 股 T+1**：当天买入不能当天卖出，策略逻辑需要考虑这个约束
9. **`cl_ord_id` 参数不存在**：`order_volume` / `order_value` / `order_target_volume` 等下单函数**不支持** `cl_ord_id` 参数。传入会直接抛 `TypeError: got an unexpected keyword argument 'cl_ord_id'`。订单标识由系统自动生成
10. **`on_order_status` 回测模式状态码**：回测中会出现文档未记录的状态码 `10`（未知/内部中间态），实际运行时需兼容处理。完整状态码：1=新建, 2=已报, 3=部分成交, 4=已成交, 5=已撤, 6=未成交(超时), 7=拒绝, 8=待撤, 9=未知, **10=回测内部态**
11. **`on_execution_report` 的 exec_type**：回测模式下返回数字而非字符，实测值为 `15`（成交确认）。实盘/仿真可能返回 `'T'`(Trade) / `'C'(Cancel)
12. **回测中风控行为**：超额卖出或资金不足的订单在回测中不会触发 `Rejected(7)` 状态，而是变为 `Cancelling(8)` → 被自动撤销。**拒单原因需要实盘/仿真环境才能观察到**
13. **`on_order_status` order 对象访问**：回调中的 order 对象**同时支持** dict 风格 `order['symbol']` 和属性风格 `order.symbol`，但推荐用 try/getattr 兼容两种方式
14. **`on_execution_report` execrpt 对象访问**：同上，同时支持 dict 和属性风格。关键字段：`symbol`, `side`(1买2卖), `volume`, `price`, `exec_type`, `commission`
15. **市价单在回测中也可能不成交**：如果资金不足（如下单量×价格 > 可用资金），市价单会被标记为 Cancelling 而非报错抛异常
16. **`stk_get_index_constituents` 没有 `df` 参数**：直接返回 DataFrame，不需要传 df=True
17. **财务数据 API 的 `fields` 必填且不能为空**：所有 `stk_get_fundamentals_*_pt` / `stk_get_finance_*_pt` / `stk_get_daily_*_pt` 函数的 `fields` 参数是必填的，不能传空字符串 `""`，否则报错"填写的 fields 不正确"。fields 不能超过 20 个
18. **`stk_get_finance_prime_pt` ROE 字段名是 `roe_weight_avg`**，不是 `roe_waa`。常用字段: eps_basic/eps_dil/roe_weight_avg/roe_weight_avg_cut/net_prof_pcom_yoy/inc_oper_yoy
19. **`stk_get_daily_basic_pt` 股本字段名**：流通股本是 `circ_shr`（不是 float_shr），无限售条件流通股本是 `ttl_shr_unl`（不是 free_shr），有限售条件股本是 `ttl_shr_ltd`
20. **财务衍生指标 `eps_dil2` vs `eps_dil`**：`stk_get_finance_deriv_pt` 中稀释 EPS 字段名是 `eps_dil2`（不是 `eps_dil`），而 `stk_get_finance_prime_pt` 中是 `eps_dil`
21. **`_pt` 后缀 = 截面数据(多标的)**，无后缀 = 时序数据(单标的)。截面用 date/trade_date 参数，时序用 start_date/end_date 参数
22. **付费增值数据 API**：期货(fut_get_*)、基金(fnd_get_*)、可转债(bnd_get_*) 的增值数据需要开通相应权限。详见 `references/16-premium-data-apis.md`
23. **`stk_get_fundamentals_*_pt` 的 `date` 参数是发布日期**，不是报告期日期。返回的是发布日期 ≤ date 的最新报告期数据
24. **`stk_get_daily_valuation_pt/mktvalue_pt/basic_pt` 的 `trade_date` 参数**：是交易日期，默认 None 返回最新交易日数据
25. **回测交易日限制**：每个交易日 18:30 前只能回测上一个交易日的数据，因为当日日线数据要到 18:30 才更新完成。如果 `end_date` 设为当天但还没过 18:30，回测结果会缺少当日数据或报错
26. **实时模式（仿真/实盘）没有发生交易的排查清单**：
    - ① **定时任务时间过了**：`schedule` 定时任务只在指定时间触发，如果启动策略时已过了今天的时间点，要等到明天才会触发。临时解决：把时间改成当前时间之后几分钟
    - ② **期货策略必须订阅具体合约**：实时模式只能推送具体合约行情（如 `SHFE.ag2506`），主连合约（如 `SHFE.agmain`）**没有行情推送**。回测可以主连，实时不行
    - ③ **实时模式日线不会推送**：交易时间内日线还没走完，`on_bar` 不会收到日线 bar。需要用 `schedule` 定时任务替代，在收盘后（如 15:01）主动调用 `history` 获取日线数据
    - ④ **检查打印日志**：确认是否有数据推送 → 是否有交易信号发出 → 是否有下单指令 → 订单状态是否正常。按这个链路逐级排查
27. **`order_volume()` vs `order_target_volume/percent` 参数名不同**：`order_volume()` 的开平仓参数叫 `position_effect`（用 `PositionEffect_Open/Close`），而 `order_target_volume/percent/value` 的持仓方向参数叫 `position_side`（用 `PositionSide_Long/Short`）。ETF调仓推荐用 `order_target_percent`，更简洁不用算股数
28. **56开头的ETF是沪市**：如562500机器人ETF应为 `SHSE.562500`，不是深市。5开头=沪市(SHSE)，1开头=深市(SZSE)
