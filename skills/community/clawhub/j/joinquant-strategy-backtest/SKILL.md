---
name: joinquant-strategy-backtest
version: 0.5.0
description: 聚宽(JoinQuant)策略回测代码生成框架。基于六段式骨架模板，支持截面多因子选股、时序技术指标择时两种模式，使用聚宽原生API获取数据，自动生成可直接在聚宽平台运行的回测代码。
author: weiyang
tags:
  - joinquant
  - 聚宽
  - 策略回测
  - 多因子
  - 截面策略
  - 时序策略
  - 量化
---

# 聚宽策略回测代码生成框架

> **状态：迭代构建中** — v0.5.0 移除 jqfactor 依赖，改用聚宽原生API获取因子数据。

## 适用场景

当用户需要：
- 在聚宽平台开发和回测量化策略
- 生成截面多因子选股策略代码（使用原生 `get_fundamentals` + `attribute_history`）
- 生成时序技术指标择时策略代码
- 查阅聚宽API使用方法
- 查阅聚宽因子库IC信息

## ⚠️ API文档获取方法

**聚宽官方API文档为JavaScript SPA，curl直接抓取仅返回HTML框架。**

**已验证可行的抓取方法：** 聚宽文档内部使用 `help/api/getContent?name=<节点名>` 端点加载内容，可直接curl获取：

```bash
# 获取API主文档
curl -s 'https://www.joinquant.com/help/api/getContent?name=api' \
  -H 'X-Requested-With: XMLHttpRequest' \
  -H 'Referer: https://www.joinquant.com/help/api/help'
# 返回JSON: {"data": "<html内容>"}
```

**因子库IC查询：** 直接访问聚宽因子库页面 `https://www.joinquant.com/view/factorlib/list`，查看各因子的 IC均值、分位数收益率等指标。该页面为SPA，需浏览器打开。

---

## 一、六段式骨架模板

所有聚宽策略都遵循统一的六段式结构。截面和时序两种策略类型的差异仅体现在第4段「信号模块」。

### 骨架总览

```
1. 文件头          — 标题/作者/import
2. initialize      — set_option + set_benchmark + g.* 参数定义
3. before_trading_start — 滑点/手续费（可选，注释包裹）
4. 信号模块         — 截面版：get_buy_list()；时序版：signal_stock_buy/sell()
5. handle_data     — 配资 + 信号调用 + 先卖后买执行
6. after_trading_end — 盘后日志（可选，注释包裹）
```

### 1.1 initialize 必备项

```python
def initialize(context):
    set_option('use_real_price', True)
    g.benchmark = '000300.XSHG'        # 基准
    set_benchmark(g.benchmark)
    g.N = 30                            # 持仓数量
    g.period = 20                       # 调仓周期(交易日)
    g.inv_days = 0                      # 投资天数计数器
    g.stock_index = ['000300.XSHG']     # 股票池指数
```

### 1.2 before_trading_start 模板（可选）

```python
def before_trading_start(context):
    set_slip_fee(context)

def set_slip_fee(context):
    set_slippage(FixedSlippage(0))
    dt = context.current_dt
    if dt > datetime.datetime(2013, 1, 1):
        set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    elif dt > datetime.datetime(2011, 1, 1):
        set_commission(PerTrade(buy_cost=0.001, sell_cost=0.002, min_cost=5))
    elif dt > datetime.datetime(2009, 1, 1):
        set_commission(PerTrade(buy_cost=0.002, sell_cost=0.003, min_cost=5))
    else:
        set_commission(PerTrade(buy_cost=0.003, sell_cost=0.004, min_cost=5))
```

### 1.3 handle_data 通用模板（截面版）

```python
def handle_data(context, data):
    if g.inv_days % g.period == 0:          # 调仓周期门控
        capital_unit = context.portfolio.portfolio_value / g.N
        list_to_buy = get_buy_list(context)  # 调信号模块
        list_to_sell = stocks_to_sell(context, list_to_buy)
        # 先卖后买
        for stk in list_to_sell:
            order_target_value(stk, 0)
        for stk in list_to_buy:
            order_target_value(stk, capital_unit)
    g.inv_days += 1
```

---

## 二、截面多因子策略模板

> **数据获取方式：** 使用聚宽原生API（`get_fundamentals` + `attribute_history`）获取因子数据，不依赖 jqfactor 包。

### 2.1 信号模块

```python
import math
import datetime

def get_buy_list(context):
    # 1. 从指数成分获取候选股票池
    stock_list = []
    for ix_ in g.stock_index:
        stock_list.extend(get_index_stocks(ix_, date=context.previous_date))
    stock_list = list(set(stock_list))  # 去重

    # 2. 获取基本面因子（通过 get_fundamentals）
    # ⚠️ get_fundamentals 使用 query 对象，返回当日截面数据
    # valuation 表字段: code, market_cap, pe_ratio, pb_ratio, ps_ratio, turnover_ratio ...
    # indicator 表字段: code, roe, roa, gross_profit_margin, net_profit_margin, inc_net_profit_year_on_year ...
    q = query(
        valuation.code,
        valuation.market_cap,             # 总市值(亿元)
        valuation.pe_ratio,               # 市盈率
        valuation.pb_ratio,               # 市净率
        valuation.ps_ratio,               # 市销率
        valuation.turnover_ratio,         # 换手率(%)
        indicator.roe,                    # ROE
        indicator.roa,                    # ROA
        indicator.gross_profit_margin,    # 毛利率
        indicator.net_profit_margin,      # 净利率
        indicator.inc_net_profit_year_on_year,  # 净利润同比增速
    ).filter(valuation.code.in_(stock_list))
    df_fund = get_fundamentals(q, date=context.previous_date).dropna(subset=['market_cap'])

    # 3. 计算衍生因子
    # BP (book_to_price_ratio) = 1/PB，IC>0 正向
    # EP (earnings_to_price) = 1/PE，IC>0 正向
    # SP (sales_to_price) = 1/PS，IC>0 正向
    df_fund['BP'] = 1.0 / df_fund['pb_ratio'].replace(0, np.nan)
    df_fund['EP'] = 1.0 / df_fund['pe_ratio'].replace(0, np.nan)
    df_fund['SP'] = 1.0 / df_fund['ps_ratio'].replace(0, np.nan)
    # PEG = PE / 净利润增速，IC<0 负向（低PEG=好）
    df_fund['PEG'] = df_fund['pe_ratio'] / df_fund['inc_net_profit_year_on_year'].replace(0, np.nan)

    # 4. 获取量价因子（通过 attribute_history 计算换手率均值）
    # ⚠️ attribute_history 每只股票单独调用，大量股票时较慢
    #    替代方案：用 get_price 批量获取后计算
    vol20_list = {}
    for code in df_fund['code'].values:
        try:
            hist = attribute_history(code, 20, '1d', ['volume', 'money'])
            # 20日平均换手率 = 20日平均成交额 / 流通市值（简化：用成交额代理）
            vol20_list[code] = hist['money'].mean()
        except:
            vol20_list[code] = np.nan
    df_fund['VOL20_proxy'] = df_fund['code'].map(vol20_list)

    # 5. 构建因子DataFrame
    # 选择要使用的因子列
    factor_cols = ['BP', 'EP', 'roe', 'gross_profit_margin', 'PEG', 'VOL20_proxy']
    df_factors = df_fund.set_index('code')[factor_cols].copy()

    # 6. 去极值 + 标准化
    df_factors = mad_remove_extreme(factor_cols, df_factors, multiplier=5)
    df_factors = zscore_standardize(factor_cols, df_factors)

    # 7. 因子合成（等权，IC方向加权）
    # IC>0 → 正向(+)，IC<0 → 负向(-)
    # BP: IC>0 (+), EP: IC>0 (+), roe: IC>0 (+)
    # gross_profit_margin: IC>0 (+), PEG: IC<0 (-), VOL20_proxy: IC<0 (-)
    df_factors['composite'] = (
        +df_factors['BP']
        + df_factors['EP']
        + df_factors['roe']
        + df_factors['gross_profit_margin']
        - df_factors['PEG']
        - df_factors['VOL20_proxy']
    )

    # 8. 排序取Top N
    df_factors = df_factors.sort_values(by='composite', ascending=False)
    return list(df_factors.dropna(subset=['composite']).head(g.N).index)

# 中位数去极值(MAD法)
def mad_remove_extreme(factor_list, df_, multiplier=5):
    for x_ in factor_list:
        median_ = df_[x_].quantile(0.5)
        dis2media = np.abs(df_[x_] - median_)
        dis_media = dis2media.quantile(0.5)
        up_limit = median_ + multiplier * dis_media
        down_limit = median_ - multiplier * dis_media
        df_[x_] = df_[x_].clip(down_limit, up_limit)
    return df_

# 截面标准化(Z-score)
def zscore_standardize(factor_list, df_):
    for x_ in factor_list:
        std = df_[x_].std()
        if std == 0 or np.isnan(std):
            df_[x_] = 0.0
        else:
            df_[x_] = (df_[x_] - df_[x_].mean()) / std
    return df_

# 卖出清单
def stocks_to_sell(context, list_to_buy):
    list_to_sell = []
    for stock_sell in context.portfolio.positions:
        if stock_sell not in list_to_buy:
            list_to_sell.append(stock_sell)
    return list_to_sell
```

### 2.2 因子合成规则

- IC > 0 的因子：正向加权（`+w * factor`）
- IC < 0 的因子：负向加权（`-w * factor`），即引入负号
- 等权组合：所有因子权重绝对值相同（`w=1`）
- **IC查询方法：** 访问聚宽因子库页面 `https://www.joinquant.com/view/factorlib/list` 查看各因子的IC均值和分位数收益率

### 2.3 原生API因子对照表

> **以下因子均可通过聚宽原生API获取，无需 jqfactor 包。**
> **IC方向请通过因子库页面验证：** `https://www.joinquant.com/view/factorlib/list`

| 因子 | 获取方式 | API字段/计算 | 典型IC方向 | 含义 |
|------|----------|-------------|-----------|------|
| BP (1/PB) | get_fundamentals | `1/valuation.pb_ratio` | 正 | 账面市值比，高BP=低PB=好 |
| EP (1/PE) | get_fundamentals | `1/valuation.pe_ratio` | 正 | 利润市值比，EP效应 |
| SP (1/PS) | get_fundamentals | `1/valuation.ps_ratio` | 正 | 营收市值比 |
| PEG | get_fundamentals | `pe_ratio / inc_net_profit_year_on_year` | 负 | 市盈率相对盈利增长比率 |
| ROE | get_fundamentals | `indicator.roe` | 正 | 权益回报率 |
| ROA | get_fundamentals | `indicator.roa` | 正 | 资产回报率 |
| 毛利率 | get_fundamentals | `indicator.gross_profit_margin` | 正 | 销售毛利率 |
| 净利率 | get_fundamentals | `indicator.net_profit_margin` | 正 | 销售净利率 |
| 净利润增速 | get_fundamentals | `indicator.inc_net_profit_year_on_year` | 正 | 净利润同比增长率 |
| 营收增速 | get_fundamentals | `indicator.inc_operating_revenue_year_on_year` | 正 | 营业收入同比增长率 |
| 总市值 | get_fundamentals | `valuation.market_cap` | 负 | 小市值效应 |
| 换手率 | get_fundamentals | `valuation.turnover_ratio` | 负 | 短期换手率 |
| 20日均换手 | attribute_history | `volume.mean(20)` | 负 | 中期换手率代理 |
| 20日波动率 | attribute_history | `close.pct_change().std(20)` | 负 | 短期波动率 |
| 动量(20日) | attribute_history | `close.pct_change(20)` | 正/负 | 短期收益动量 |

---

## 三、时序技术指标择时模板

### 3.1 信号模块

```python
import talib

def signal_stock_sell(context):
    sell = [0] * len(g.security)
    for i in range(len(g.security)):
        (ma_long_pre, ma_long_now) = get_EMA(context, g.security[i], g.N_sell_slow)
        (ma_short_pre, ma_short_now) = get_EMA(context, g.security[i], g.N_sell_fast)
        # 死叉：短下穿长 + 有持仓
        if ma_short_now < ma_long_now and ma_short_pre > ma_long_pre \
                and context.portfolio.positions[g.security[i]].sellable_amount > 0:
            sell[i] = 1
    return sell

def signal_stock_buy(context):
    buy = [0] * len(g.security)
    for i in range(len(g.security)):
        (ma_long_pre, ma_long_now) = get_EMA(context, g.security[i], g.N_buy_slow)
        (ma_short_pre, ma_short_now) = get_EMA(context, g.security[i], g.N_buy_fast)
        # 金叉：短上穿长 + 无持仓
        if ma_short_now > ma_long_now and ma_short_pre < ma_long_pre \
                and context.portfolio.positions[g.security[i]].sellable_amount == 0:
            buy[i] = 1
    return buy

def get_EMA(context, code, days):
    a = get_price(code, start_date='2005-01-04',
                  end_date=context.previous_date).close
    ema = talib.EMA(a, days)
    return ema[-2], ema[-1]
```

### 3.2 时序模板 handle_data

```python
def handle_data(context, data):
    capital_unit = context.portfolio.portfolio_value / g.N
    toSell = signal_stock_sell(context)
    toBuy = signal_stock_buy(context)
    # 先卖后买
    for i in range(len(g.security)):
        if toSell[i] == 1:
            order_target_value(g.security[i], 0)
    for i in range(len(g.security)):
        if toBuy[i] == 1:
            order_target_value(g.security[i], capital_unit)
```

### 3.3 时序模板 initialize

```python
def initialize(context):
    set_option('use_real_price', True)
    g.benchmark = '000300.XSHG'
    set_benchmark(g.benchmark)
    # 交易标的列表
    g.security = ['000300.XSHG', '000905.XSHG', '000852.XSHG']
    g.N = len(g.security)
    # EMA均线参数
    g.N_buy_fast = 5
    g.N_buy_slow = 20
    g.N_sell_fast = 5
    g.N_sell_slow = 20
```

---

## 四、因子选择与IC查询

### 4.1 因子选择流程

当用户没有明确策略思路时，按以下流程推荐因子：

1. **查阅因子库IC：** 访问聚宽因子库页面 `https://www.joinquant.com/view/factorlib/list`
2. **筛选规则**：
   - 获取每个因子的 **IC均值** 和 **分位数收益率**
   - 如果 IC > 0：看**最大分位数收益率**（Top quantile收益越高越好）
   - 如果 IC < 0：看**最小分位数收益率**（Bottom quantile收益越低越好，负向使用）
3. **排序选取**：按 IC绝对值 × 分位数收益幅度 综合排序，取 Top 2-3 个因子
4. **确定获取方式**：查「2.3 原生API因子对照表」，确认因子可通过 `get_fundamentals` 或 `attribute_history` 获取
5. **等权组合**：
   - IC > 0 的因子 → 正向加权（`+factor`）
   - IC < 0 的因子 → 负向加权（`-factor`）
6. **生成代码**：自动填入截面多因子模板（第二节），生成完整可回测代码

### 4.2 因子库访问方法

**聚宽因子库页面：** `https://www.joinquant.com/view/factorlib/list`

- 该页面展示所有因子的IC均值、分位数收益率、IC胜率等评估指标
- 页面为SPA，需用浏览器打开查看
- Agent无法直接抓取该页面数据（需要前端鉴权参数）
- **操作方式**：用户在浏览器打开因子库页面 → 查看因子IC → 将因子名和IC数据告知Agent → Agent据此选择因子并生成代码

### 4.3 常见因子参考表（原生API可获取）

> **IC方向请通过因子库页面验证：** `https://www.joinquant.com/view/factorlib/list`

| 因子 | 获取方式 | 典型IC方向 | 含义 |
|------|----------|-----------|------|
| BP (1/PB) | get_fundamentals | 正 | 账面市值比，高BP=低PB=好 |
| EP (1/PE) | get_fundamentals | 正 | 利润市值比，EP效应 |
| SP (1/PS) | get_fundamentals | 正 | 营收市值比 |
| PEG | get_fundamentals | 负 | 市盈率相对盈利增长比率，越低越好 |
| ROE | get_fundamentals | 正 | 权益回报率 |
| ROA | get_fundamentals | 正 | 资产回报率 |
| 毛利率 | get_fundamentals | 正 | 销售毛利率 |
| 净利率 | get_fundamentals | 正 | 销售净利率 |
| 净利润增速 | get_fundamentals | 正 | 净利润同比增长率 |
| 营收增速 | get_fundamentals | 正 | 营业收入同比增长率 |
| 总市值 | get_fundamentals | 负 | 小市值效应 |
| 换手率 | get_fundamentals | 负 | 短期换手率 |
| 20日均换手 | attribute_history | 负 | 中期换手率代理 |
| 20日波动率 | attribute_history | 负 | 短期波动率 |
| 动量(20日) | attribute_history | 正/负 | 短期收益动量 |

**⚠️ 因子名注意：**
- 聚宽因子库页面中的因子名（如 `book_to_price_ratio`）对应的是 jqfactor 包的因子code
- 使用原生API时，需要自行计算对应因子（如 BP = 1/`valuation.pb_ratio`）
- 查看因子库IC时，用因子名搜索；编写代码时，用原生API字段计算

**⚠️ 倒数比率因子的IC方向翻转：**
- `PB`（市净率）：IC<0（低PB=好）→ 因子合成用负号 `-PB`
- `BP`（1/PB）：IC>0（高BP=低PB=好）→ 因子合成用正号 `+BP`
- 同理：`EP`(1/PE) IC>0正号 vs `PE` IC<0负号；`SP`(1/PS) IC>0正号 vs `PS` IC<0负号
- **规则**：凡是倒数比率因子（BP/EP/SP），IC方向一律为**正**（高比率=低估=好），因子合成用正号

---

## 五、代码生成工作流

### 5.0 核心设计原则：纯因子选股

**生成多因子策略时，默认只生成纯因子选股逻辑，不加额外模块。**

纯因子选股的完整流程：
```
取指数成分股 → get_fundamentals取基本面因子 → attribute_history取量价因子
→ 去极值(MAD) → 标准化(Z-score) → 因子合成 → 排序取TopN → 等权调仓
```

**不加的东西（除非用户明确要求）：**
- ❌ 止损模块（个股止损/组合止损）
- ❌ ST/新股/停牌过滤（filter_stocks）
- ❌ 行业中性化
- ❌ 市值中性化
- ❌ 仓位优化/风险预算

**保留的东西（因子选股的核心组成部分）：**
- ✅ `get_fundamentals` 的 `dropna` 防御（技术必须，非风控）
- ✅ MAD去极值 + Z-score标准化（因子处理必须步骤）
- ✅ 因子合成方向（IC正→+，IC负→-）
- ✅ 调仓周期门控
- ✅ 先卖后买执行顺序

> 当用户说"加止损"/"过滤ST"/"行业中性"等明确需求时，再在纯因子选股基础上叠加对应模块。

### 5.1 用户输入 → 代码生成流程

```
用户需求
   │
   ├── 有明确因子/策略思路？
   │     ├── 是 → 选择模板（截面/时序）→ 填入因子/参数 → 生成纯因子选股代码
   │     └── 否 → 因子推荐流程
   │               ├── 用户打开因子库页面查看IC（https://www.joinquant.com/view/factorlib/list）
   │               ├── 按IC+分位数收益筛选Top 2-3因子
   │               ├── 确定原生API获取方式（get_fundamentals / attribute_history）
   │               ├── 确定加权方向（IC正→+，IC负→-）
   │               └── 填入截面模板 → 生成纯因子选股代码
   │
   ├── 策略类型？
   │     ├── 截面多因子 → 使用第二节模板（纯因子选股，原生API）
   │     └── 时序择时   → 使用第三节模板
   │
   ├── 用户是否明确要求额外模块？
   │     ├── 否 → 生成纯因子选股代码，结束
   │     └── 是 → 在纯因子选股基础上叠加用户要求的模块（止损/过滤/中性化等）
   │
   └── 生成完整代码（六段式骨架 + 信号模块 + 注释）
```

### 5.2 代码生成检查清单

- [ ] `initialize` 包含 `set_option`, `set_benchmark`, 所有 `g.*` 参数
- [ ] `handle_data` 包含调仓周期门控（截面策略）或每日信号检查（时序策略）
- [ ] 先卖后买顺序
- [ ] `order_target_value` 而非 `order`（自动计算差额）
- [ ] 因子去极值 + 标准化（截面策略）
- [ ] 因子合成方向正确（IC正→+，IC负→-）
- [ ] **基本面因子用 `get_fundamentals`，量价因子用 `attribute_history`**
- [ ] **纯因子选股：无止损/无ST过滤/无中性化（除非用户明确要求）**
- [ ] 可选模块（before_trading_start / after_trading_end）用注释包裹
- [ ] 文件头包含标题、作者、import
- [ ] 代码可直接复制到聚宽平台运行

---

## 六、聚宽API速查

### 6.1 策略框架函数

| 函数 | 用途 | 调用时机 |
|------|------|---------|
| `initialize(context)` | 全局初始化 | 回测开始前一次 |
| `before_trading_start(context)` | 盘前准备 | 每日开盘前 |
| `handle_data(context, data)` | 交易执行 | 每日交易时段 |
| `after_trading_end(context)` | 盘后处理 | 每日收盘后 |
| `process_initialize(context)` | 进程初始化 | 进程启动时 |

### 6.2 设置函数

| 函数 | 用途 |
|------|------|
| `set_option('use_real_price', True)` | 使用真实价格 |
| `set_benchmark(code)` | 设置基准 |
| `set_commission(PerTrade(...))` | 设置手续费 |
| `set_slippage(FixedSlippage(0))` | 设置滑点 |

### 6.3 下单函数

| 函数 | 用途 |
|------|------|
| `order(security, amount)` | 按股数下单 |
| `order_value(security, value)` | 按金额下单 |
| `order_target(security, target_amount)` | 调至目标股数 |
| `order_target_value(security, target_value)` | 调至目标金额 |
| `order_target_percent(security, percent)` | 调至目标百分比 |
| `cancel_order(order)` | 撤单 |

### 6.4 数据函数

| 函数 | 用途 |
|------|------|
| `get_price(code, start_date, end_date)` | 获取历史行情 |
| `get_bars(code, count, unit)` | 获取K线数据 |
| `attribute_history(code, count, unit, fields)` | 获取个股历史数据（单只，返回DataFrame） |
| `get_fundamentals(query_object, date)` | 查询财务数据（截面，返回DataFrame） |
| `get_index_stocks(index, date)` | 获取指数成分股 |
| `get_security_info(code)` | 获取证券信息 |
| `get_industry(security)` | 获取行业分类 |
| `get_current_data()` | 获取实时行情快照 |
| `get_all_securities(types=['stock'])` | 所有股票列表 |
| `get_trade_days(start_date, end_date)` | 交易日历 |

### 6.5 get_fundamentals 常用表与字段

| 表名 | 常用字段 | 用途 |
|------|----------|------|
| `valuation` | code, market_cap, pe_ratio, pb_ratio, ps_ratio, turnover_ratio, capitalization, circulating_cap | 估值与市值 |
| `indicator` | code, roe, roa, gross_profit_margin, net_profit_margin, inc_net_profit_year_on_year, inc_operating_revenue_year_on_year, eps | 财务指标 |
| `balance` | code, total_assets, total_liability, total_owner_equities | 资产负债表 |
| `cash_flow` | code, net_operate_cash_flow, net_invest_cash_flow, net_finance_cash_flow | 现金流量表 |
| `income` | code, total_operating_revenue, net_profit, operating_profit | 利润表 |

**使用示例：**
```python
# 查询沪深300成分股的PE和ROE
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    indicator.roe
).filter(valuation.code.in_(stock_list))
df = get_fundamentals(q, date=context.previous_date)
```

### 6.6 上下文对象

| 属性 | 用途 |
|------|------|
| `context.current_dt` | 当前回测时间 |
| `context.previous_date` | 上一交易日 |
| `context.portfolio.available_cash` | 可用资金 |
| `context.portfolio.portfolio_value` | 总资产 |
| `context.portfolio.positions` | 持仓字典 |
| `context.portfolio.positions[stk].sellable_amount` | 可卖数量 |
| `g.*` | 全局自定义变量 |

### 6.7 定时调度

| 函数 | 用途 |
|------|------|
| `run_daily(func, time)` | 每日定时执行 |
| `run_weekly(func, weekday, time)` | 每周定时执行 |
| `run_monthly(func, monthday, time)` | 每月定时执行 |

### 6.8 证券代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 深圳股票 | `.XSHE` | `000001.XSHE`（平安银行） |
| 上海股票 | `.XSHG` | `600519.XSHG`（贵州茅台） |
| 指数 | `.XSHG`/`.XSHE` | `000300.XSHG`（沪深300） |
| 场内基金 | `.XSHG`/`.XSHE` | `510300.XSHG`（沪深300ETF） |

---

## 七、坑点提醒

1. **成交金额限制**：若下单金额超过当日实际成交额，只能成交部分（ETF常见）
2. **最低成交单位**：聚宽默认最低100股，建议个股回测金额≥100万、指数≥1000万
3. **`talib`** 在聚宽平台预装，本地环境需自行安装
4. **`context.previous_date`** 是上一交易日（非前一天），用于取因子值避免未来数据
5. **`pd.DataFrame.append`** 在pandas 2.0+已废弃，聚宽平台内pandas版本可能较旧仍可用
6. **`order_target_value`** 会自动计算差额下单，比手动计算买卖数量更简洁
7. **持仓状态跟踪**：时序策略中需在买卖信号中同步更新持仓状态
8. **`set_option` vs `set_options`（易错，已实测踩坑）**：聚宽API中两个函数都存在但调用方式不同：
   - `set_option('use_real_price', True)` — 单数形式，接收 `(key, value)` 键值对，设置单个选项 ✅
   - `set_options({'use_real_price': True, 'avoid_future_data': True})` — 复数形式，接收 dict 批量设置
   - **常见错误**：`set_options('use_real_price', True)` — 把键值对传给复数形式，不会报错但设置不生效 ❌
   - **建议**：统一使用 `set_option`（单数）逐项设置，避免混淆
9. **ClawHub发布脱敏**：发布前必须扫描所有文件中的IP/密码/token，替换为 `<YOUR_PLACEHOLDER>`。ClawHub安全扫描会自动标记含硬编码凭证的skill为 `suspicious (DO_NOT_INSTALL)`
10. **⚠️ `get_fundamentals` 返回值处理**：
    - `get_fundamentals(q, date=...)` 返回DataFrame，每行一只股票
    - 必须用 `dropna()` 过滤缺失值，否则后续计算会出错
    - `valuation.pb_ratio` 为0时会导致 `1/PB` 除零错误，需用 `.replace(0, np.nan)` 保护
    - `indicator` 表中部分字段可能为NaN（新上市/财务数据未更新），需防御性处理
11. **⚠️ `attribute_history` 性能限制**：
    - 每只股票单独调用，大量股票时循环很慢（300只股票×20日数据≈3-5秒）
    - 替代方案：用 `get_price` 批量获取后自行计算
    - `attribute_history(code, count, unit, fields)` 的 `unit` 参数为 `'1d'`（日线）或 `'1m'`（分钟线）
12. **⚠️ 倒数比率因子的IC方向翻转**：聚宽因子库对估值类因子使用**倒数比率**命名（BP=1/PB, EP=1/PE, SP=1/PS），而非直接比率。这意味着IC方向会翻转：
    - `PB`（市净率）：IC<0（低PB=好）→ 因子合成用 **负号** `-PB`
    - `BP`（1/PB）：IC>0（高BP=低PB=好）→ 因子合成用 **正号** `+BP`
    - 同理：`EP`(1/PE) IC>0正号 vs `PE` IC<0负号；`SP`(1/PS) IC>0正号 vs `PS` IC<0负号
    - **常见错误**：把`PB`改成`BP`后忘记翻转IC方向符号，导致因子合成方向完全反转，选出的股票与预期相反
    - **规则**：凡是倒数比率因子（BP/EP/SP），IC方向一律为**正**（高比率=低估=好），因子合成用正号

13. **⚠️ `get_price(panel=False)` 列名兼容性**：聚宽 `get_price` 在 `panel=False`（默认）模式下返回 DataFrame，列名是 **security code 字符串**（如 `'000001.XSHE'`），而非 `'close'`/`'open'` 等字段名。这与很多教程和示例代码的假设不同：
    - `get_price('000001.XSHE', count=5, end_date='2024-01-01', fields=['close'], panel=False)` → DataFrame，**列名是 `['000001.XSHE']`**，不是 `['close']`
    - 如果 `fields=['close', 'open']` 且多只股票，返回的是行=日期、列=code 的 DataFrame（每个 field 一个）
    - **常见错误**：`df['close']` 取列 → KeyError。实际应按 code 取列：`df['000001.XSHE']`，或用 `panel=True` 返回 Panel（已废弃不推荐）
    - **正确写法（单股单字段）**：`df.iloc[:, 0]` 或 `df[df.columns[0]]`
    - **正确写法（多股批量取close）**：`get_price(stock_list, count=20, end_date=context.current_dt, fields=['close'])` → 返回 DataFrame，列名=股票代码，行=日期。`df[stock_code]` 取某只股票的收盘价序列
    - **替代方案**：优先使用 `attribute_history(security, count, '1d', 'close')` 获取单股历史数据，返回 Series，无列名歧义

## 更新日志

### v0.5.1
- **新增：** 坑点#13 — `get_price(panel=False)` 列名是 security code 而非字段名，易致 KeyError

### v0.5.0
- **重大变更：** 移除 jqfactor 包依赖（无license无法使用），截面多因子模板改用聚宽原生API（`get_fundamentals` + `attribute_history`）
- **新增：** `get_fundamentals` 常用表与字段速查（6.5节）
- **新增：** 原生API因子对照表（2.3节），列出15个可通过原生API获取的因子及计算方式
- **更新：** 因子IC查询改为直接访问因子库页面 `https://www.joinquant.com/view/factorlib/list`
- **移除：** `references/jqfactor_library.md`（jqfactor专属因子库参考）
- **移除：** `from jqfactor import get_factor_values` 及相关代码
- **移除：** 坑点#12-#14（均围绕 `get_factor_values` 的行为，不再适用）
- **移除：** 因子IC查询代码（原4.4节，依赖 jqfactor）
- **移除：** 模板文件 `three_factor_strategy.py`、`multifactor_5factor_strategy.py`（依赖 jqfactor）
- **新增：** 坑点#10-#11（`get_fundamentals` 返回值处理 + `attribute_history` 性能限制）

### v0.4.2
- **修复（关键）：** 坑点#14 — `get_factor_values` 不支持 `count` 参数，必须用 `start_date`+`end_date` 字符串格式
- **修复：** 截面信号模板 `count=1, end_date=...` → `start_date`/`end_date` 字符串
- **修复：** 因子值提取 `iloc[:, 0]` → `iloc[:, -1]`
- **修复：** IC查询代码同步修正
- **修复：** API速查表 `get_factor_values` 签名更新

### v0.4.1
- **新增：** 核心设计原则「纯因子选股」
- **更新：** 代码生成流程增加"用户是否明确要求额外模块"判断分支
- **更新：** 检查清单增加纯因子选股校验项

### v0.4.0
- **新增：** 坑点#12 — `get_factor_values` 静默丢弃因子行为及防御模式
- **修复：** 截面信号模块模板更新为防御性写法

### v0.3.0
- **修复：** 因子参考表8个错误因子名全部修正
- **新增：** 错误因子名→正确因子code映射表
- **新增：** `references/jqfactor_library.md`（已于v0.5.0移除）

### v0.2.0
- 新增：六段式骨架模板
- 新增：截面多因子策略模板
- 新增：时序技术指标择时模板
- 新增：因子推荐模块
- 新增：代码生成工作流
- 保留：聚宽API速查
- 保留：坑点提醒

### v0.1.0
- 初始创建
