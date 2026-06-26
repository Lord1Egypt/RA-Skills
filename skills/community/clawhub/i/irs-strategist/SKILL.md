---
name: irs-strategist
description: This skill should be used when the user needs to write, review, or debug trading strategies using the IRS (SunnyQuant Investment Research System) framework. It provides complete knowledge of the CommonStrategy lifecycle, quote subscription, order placement algorithms, strategy parameters, chart visualization, sub-strategies, and common patterns. Trigger when users mention IRS, SunnyQuant, CommonStrategy, or ask to write/modify C# trading strategy code in this framework.
---

# IRS Strategy Development Skill

IRS（开发代号 SunnyQuant）是一个基于 C#/.NET 的量化投研系统，支持策略编写、回测（IRS.Lab）和实盘交易（IRS.Trader）。

## 适用场景

- 用户需要编写新的交易策略，或修改现有策略。
- 用户需要调试策略代码，解决编译错误或运行时错误。
- 用户需要进行回测或模拟交易，以验证策略的有效性。

## 项目结构

使用 `dotnet new irs -n MyStrategy` 创建新策略项目，结构如下：

```
MyStrategy/
├── MyStrategy/            # 策略代码（核心，在此编写策略）
│   ├── MyStrategy.cs
│   └── MyStrategy.csproj
├── MyStrategy.Lab/        # 回测项目（WinForm UI，Windows专用）
├── MyStrategy.Lab.Xplat/  # 回测项目（Blazor UI，跨平台）
├── MyStrategy.Lab.Console/ # 回测控制台（无UI，跨平台）
├── MyStrategy.Trader/     # 实盘/模拟交易项目
└── Directory.Packages.props  # 升级IRS版本在此修改 <IRSVersion>
```

> 如果用户的环境没有dotnet sdk，请引导用户安装最新版的 .NET SDK（https://dotnet.microsoft.com/download）
> 没有特殊说明的时候，推荐用户使用`Jetbrains Rider`打开`MyStrategy.sln`进行后续的开发，如果用户未安装`Jetbrains Rider`，提示用户安装`Jetbrains Rider`。
> 如果提示没有安装irs模板，可以通过下面命令安装`dotnet new install SGD.InvestorResearchSystem --nuget-source https://nuget.shengguanda.com/v3/index.json --force`. 如果提示nuget.shengguanda.com访问失败，则提示用户，该模板需要访问盛冠达内网才可以访问。

## 启动策略

如果用户只想查看回测结果，你可以询问用户必要的参数(回测起止日期)，修改 `MyStrategy.Lab.Console` 项目的启动参数，启动该项目，回测结果会输出在控制台。其他参数比如开收盘时间，多账号多币种配置等，你可以根据策略的需要自行添加，拿不准的可以询问用户。

如果用户想要自己启动回测或者是模拟交易，你可以引导用户运行 `MyStrategy.Lab.Xplat` 或 `MyStrategy.Trader` 项目，并提供用户相关的问题解答。

## 策略生命周期

所有策略继承 `CommonStrategy`，运行流程：

```
Init → BeforeTrading → OnQuoteArrive/OnCandleArrive → AfterTrading → AfterSettlement → (循环) → Finished
```

| 回调方法 | 触发时机 | 关键说明 |
|---------|---------|---------|
| `Init()` / `InitAsync()` | 整个运行期只调用一次 | 初始化变量、获取准备数据 |
| `BeforeTrading()` | 每交易日开始前调用一次 | **必须在此订阅行情**（订阅每日清空） |
| `OnQuoteArrive(QuoteData q, bool outDated)` | Tick 数据到达时 | `outDated=true` 表示盘中重启补推的历史数据 |
| `OnCandleArrive(Instrument, CandleType, CandleData, bool outDated)` | K线数据到达时 | 同上，用 `outDated` 区分历史与实时 |
| `AfterTrading()` | 每日交易结束后（结算前） | 可查当日交易记录、持仓 |
| `AfterSettlement()` | 结算完成后 | 分红配股校准后数据 |
| `Finished()` | 策略运行结束 | 释放资源 |

> `IsTest` 属性：`true` = 回测模式，`false` = 实盘/模拟（两者无法区分）

## 行情订阅

```csharp
// 在 BeforeTrading 中订阅
SubMarketData(Instrument.FromCode("000300.SSE"));   // Tick
SubCandleData(Instrument.FromCode("000300.SSE"), CandleType.Minute); // K线

// 接收 Tick
public override void OnQuoteArrive(QuoteData q, bool outDated) { }

// 接收 K线
public override void OnCandleArrive(Instrument instrument, CandleType type, CandleData candle, bool outDated) { }
```

**Instrument 创建**：

所有可以交易的标的都可以通过 `Instrument.FromCode("代码")` 创建，代码格式为 `证券代码.交易所后缀`，如 `000300.SSE`（沪深300）。港股代码后缀为 `.HKEX`，如 `00019.HKEX`。期货代码通常不带后缀，如 `IF2307`。

```csharp
var stock = Instrument.FromCode("000300.SSE");
var future = Instrument.FromCode("IF2307");
var hk = Instrument.HKEX("00019");
```

**历史数据查询**（一般不需要查当日）：

```csharp
var ticks = DataUtils.GetTicks(PreTradingDay, Instrument.FromCode("000300.SSE"));
var candles = DataUtils.GetCandles(Instrument.FromCode("000300.SSE"), CandleType.Minute, PreTradingDay, PreTradingDay);
```

## 算法下单

所有下单均通过算法单（AlgoOrder）完成。必须在策略类上添加对应的 `[UseXxxAlgo]` 特性标记。

详细算法用法见 `references/algorithms.md`。

### 下单流程回调

```csharp
public override void OnCreateAlgoOrder(AlgoOrder algoOrder) { /* 算法单是否被接受 */ }
public override void OnRtnAlgoOrder(AlgoOrder algoOrder) { /* 算法单状态更新 */ }
public override void OnRtnSubOrder(SubOrderInfo subOrder) { /* 子单委托回报 */ }
public override void OnRtnSubOrderTrade(SubOrderTrade trade) { /* 子单成交回报 */ }
```

### 资金与持仓

```csharp
// 资金（异步，不要频繁调用）
var asset = await this.GetAssetsAsync(Accounts[0].AccountId);

// 持仓（内存操作，可频繁调用）
var posVol = this.GetPositionVolume(accountId, code);
var pos = GetPositions(accountId, code);
// pos.TodayLong / TodayShort / HistoryLong / HistoryShort / TotalShort

// 最小变动价位
var tickPrice = GetTickPrice("IF2106");
```

## 策略参数（回测参数调优）

```csharp
[RangeParams<int>(Name = "MA周期", Begin = 5, End = 30, Step = 5)]
public int MaPeriod { get; set; }

[RangeParams<double>(Name = "止损比例", Begin = 0.01, End = 0.05, Step = 0.01)]
public double StopLoss { get; set; }

[ValueListParams<string>(Name = "合约", ValueList = new[] { "IF", "IH", "IC" })]
public string ContractType { get; set; } = "IF";

[MultiplierParams<long>(Name = "等比参数", Begin = 1, End = 100, Multiplier = 2)]
public long Param { get; set; }

[EnumParams<TradeType>(Name = "交易类型")]
public TradeType Type { get; set; }
```

## 定时任务

```csharp
public override void BeforeTrading()
{
    this.AddTimerTask("换仓", TradingDay.AddHours(9), () =>
    {
        // 到时间执行
    }, cancellationToken);
}
```

> 注意：定时任务收盘后未执行将被取消；如果策略盘中重启，需要自行判断是否补下订单。

## K线指标（Stock.Indicators）

```csharp
List<CandleData> _candles = new();

// 在 OnCandleArrive 中积累数据
_candles.Add(candle);

var sma10 = _candles.GetSma(10).ToArray();
var latestMa10 = sma10[^1].Sma;   // 最新值在最后

var macd = _candles.GetMacd().ToArray();
var kdj  = _candles.GetStoch();
var rsi  = _candles.GetRsi();
// 更多：https://dotnet.stockindicators.dev/indicators/
```

> `GetSma()` 结果正向排列，最新在 `[^1]`。注意边界：N个K线计算MA(N)只有1个结果。

## 图表可视化

```csharp
// 全局图（整个运行期数据在一张图）
Executor.GetOrAddGraph("每日资金").PutPoint("收益", TradingDay, value);

// 日内图（每日清空）
Executor.GetOrAddDailyGraph("日内价差").PutPoint("价差", time, value);

// K线图
Executor.GetOrAddGraph("Main").PutCandle(candle);

// 副图（如MACD）
Executor.GetOrAddGraph("Main").GetSubGraph("MACD").PutPoint("MACD", candle.BeginTime, macdValue, color: Color.Blue);
Executor.GetOrAddGraph("Main").GetSubGraph("MACD").PutPoint("Histogram", candle.BeginTime, histVal, histogram: true);

// 标记箭头
Executor.GetOrAddGraph("Main").GetSubGraph("MACD").PutMarker(candle.BeginTime, upArrow: true);
```

## 多账号策略

启动策略的时候，可以为不同的账号添加标签，以便标记该账号的功能，然后在策略中通过标签获取账号ID，进行数据隔离和差异化处理。

```csharp
public override void Init()
{
    var futureAccountId = Accounts.FirstOrDefault(o => o.Tag.Contains("Future"))?.AccountId
        ?? throw new Exception("no future account");
    var stockAccountId = Accounts.FirstOrDefault(o => o.Tag.Contains("Stock"))?.AccountId
        ?? throw new Exception("no stock account");
}
```

## 子策略（SubStrategy）

将多个策略组合为父子结构，子策略数据独立隔离（持仓、委托、行情），但共享资金。这个功能属于高级功能，在用户明确要求的情况下使用。

```csharp
// 父策略
[UseSubOrderAlgo]
[UseChasingAlgo]
public class ParentStrategy : CommonStrategy
{
    public override void Init()
    {
        AddSubStrategy<SubA>("label_a");
        AddSubStrategy<SubB>("label_b", x => { x.SomeParam = 123; });
    }
}

// 子策略
[UseChasingAlgo]
public class SubA : CommonStrategy { /* 与普通策略写法一致 */ }
```

> - 父策略需标记所有子策略使用的算法特性
> - 子策略只支持一级嵌套
> - 避免多个子策略交易同一标的（会导致开平逻辑复杂）

## 策略标签（StrategyLabel）

用于多策略共用同一账号时隔离数据，这个功能通常在实盘下有用，在回测中通常不需要使用。

```csharp
// 下单时自动带上策略标签
// 获取策略资金
var asset = GetStrategyAsset(MainAccountId);
var preBalance = Accounts.First(x => x.AccountId == MainAccountId).GetPreBalance();

// 禁用标签过滤（查全账号数据）
public override void Init() { DisableFilterDataByStrategyLabel = true; }

// 为其他策略标签下单
this.BuyOpen(code, vol, price,
    customProperties: new Dictionary<string, string>() { [CustomProperty.StrategyLabel] = otherLabel });
```

## 数据获取

IRS 使用两类数据源：**147基础数据**（行情核心）**聚源数据库**（研究用基本面/合约信息）。

完整的数据获取文档详见 `references/data.md`，以下为常用速查。

### 历史行情（DataUtils）

```csharp
// Tick 历史（一般不查当日）
var ticks = DataUtils.GetTicks(PreTradingDay, Instrument.FromCode("000300.SSE"));

// K线历史
var candles = DataUtils.GetCandles(
    Instrument.FromCode("000300.SSE"), CandleType.Minute, PreTradingDay, PreTradingDay);

// 日线
var daily = GetDailyData(PreTradingDay, Instrument.FromCode("000300.SSE"));
// daily.Candle.Open/High/Low/Close, daily.UpperLimit, daily.LowerLimit
```

### 主力合约

```csharp
// 获取某品种某天的主力合约代码
var mains = DataUtils.GetMainContracts(PreTradingDay, "IF");
// mains[0] => "IF2503"
```

### 交易日历

```csharp
bool isTrading = IsTradingDay(someDate);  // 按策略当前日历
DateTime[] days = CommonStrategy.GetTradingDays(startDate, endDate);
```

### 汇率

```csharp
// 查人民币汇率
CurrencyRateManager.Default.TryGetRate("HKD",Date, out double rate);

// 回测时设置临时汇率
CurrencyRateManager.Default.SetTempFixedRate("HKD", 0.92);


```

### 分红送股

```csharp
// 获取分红序列（用于除权处理），来源：factor/bonus.csv
var dividends = GetStockDividend(Instrument.FromCode("000001.SZSE"));

// 当日实际发生的分红在 AfterSettlement 中获取
// dailyInfo.AccountDailyInfos[MainAccountId].StockCashDividend / StockDividend / StockExtension
// 注意：所有行情数据均为未除权数据
```

### ETF申赎

```csharp
// 获取ETF成分清单
var components = DataUtils.GetEtfComponentInfos(Instrument.FromCode("588030"), PreTradingDay);
// 获取申赎参数
var purRedInfo = DataUtils.GetEtfPurRedInfo(Instrument.FromCode("588030"), PreTradingDay);

// 聚源查成分清单细节（MF_ETFPRComponents）
// 含现金替代标志(1-允许/2-必须/3-禁止/4-退补)、替代金额、溢/折价比例等
```

### 停牌

```csharp
if (Instrument.FromCode("600036").IsSuspend(PreTradingDay)) { /* 停牌 */ }
// 数据来源：聚源 LC_SuspendResumption 表
```

### 数据库访问（FreeSql）

```csharp
// 聚源数据（通用写法）
var data = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.FutContractMain>()
    .Where(o => o.ContractCode.StartsWith("IF"))
    .OrderBy(o => o.DeliveryDate)
    .ToList();
```

> 聚源数据字典在线：https://dd.gildata.com/（szsgdsjk01 / gildata@123），本地版本见 `references/data.md` 中的「常用表速查」。


## 融资融券

```csharp
// 融券卖出（下单价需 >= 最新价）
this.ShortSell(code, 1000, lastTick.LastPrice);

// 获取融券持仓
var pos = GetPositions(MainAccountId, code);
// pos.TotalShort / TodayShort / HistoryShort

// 获取融券额度 (回测固定100w额度，实盘不支持查询)
var quota = GetMarginQuota(MainAccountId, code);

// 买券还券
this.BuyAndRepayStock(code, 1000, lastTick.AskPrice1);

// 融资买入
this.MarginBuy(code, 1000, lastTick.LastPrice);
```

## 手续费设置

| 标的种类 | 默认手续费 |
|---------|-----------|
| 国内股票/港股通 | 买0.0002，卖0.0007 |
| 国内ETF | 买0.0006，卖0.0006 |
| 国内ETF期权 | 每手1.5元 |
| 国内期货 | 按配置文件 |

```csharp
// 调整单个标的
this.ConfigTradeFee(Instrument.FromCode("IF2306"), TradeFeeConfig.RateFeeConfig(0.0001));
// 调整全部股票
this.ConfigStockTradeFee(TradeFeeConfig.RateFeeConfig(0.0001, 0.0006));
```

## 下单数量规则

| 标的类型 | 下单量单位 | 最小量 | 倍数 |
|---------|----------|--------|------|
| A股股票 | 股数 | 100 | 100 |
| 科创板 | 股数 | 200 | 1 |
| 上海可转债 | 手数（1手=10张） | 1 | 1 |
| 深圳可转债 | 张数 | 10 | 10 |
| 期货 | 手数 | 1（部分品种不同） | 1 |

```csharp
// 获取下单规则
var maxVol = instrument.GetMaxSubmitVolume();
var minVol = instrument.GetMinSubmitVolume();
var multiple = instrument.GetSubmitMultiple();
var volumeMultiple = instrument.GetVolumeMultiple(); // 合约乘数
```

## References 文档

- 详细算法用法（子单/追单/Twap/配对）：请读取 `references/algorithms.md`
- 策略完整代码示例：请读取 `references/examples.md`
- 数据获取完整参考（日线/Tick/K线/主力合约/交易日/汇率/分红/ETF申赎/聚源表速查）：请读取 `references/data.md`
- 基类CommonStrategy的所有方法和属性：<https://irs_doc.shengguanda.com/docs/api/IRS.Common/CommonStrategy>
