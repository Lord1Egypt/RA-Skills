# IRS 策略完整代码示例

## 示例1：MA 金叉死叉策略（基础结构模板）

```csharp
using IRS.Common;
using IRS.Common.Core;
using Skender.Stock.Indicators;

[DisplayName("MA金叉死叉策略")]
[UseChasingAlgo]
public class MaCrossStrategy : CommonStrategy
{
    [RangeParams<int>(Name = "快线周期", Begin = 5, End = 20, Step = 5)]
    public int FastPeriod { get; set; } = 10;

    [RangeParams<int>(Name = "慢线周期", Begin = 20, End = 60, Step = 10)]
    public int SlowPeriod { get; set; } = 40;

    private Instrument _main = null!;
    private List<CandleData> _candles = new();

    public override void Init()
    {
        _main = Instrument.FromCode("IF2309");
    }

    public override void BeforeTrading()
    {
        SubCandleData(_main, CandleType.Minute);
    }

    public override void OnCandleArrive(Instrument instrument, CandleType type, CandleData candle, bool outDated)
    {
        _candles.Add(candle);

        // 画图
        Executor.GetOrAddGraph("Main").PutCandle(candle);

        if (_candles.Count < SlowPeriod + 1) return;

        var fastSma = _candles.GetSma(FastPeriod).ToArray();
        var slowSma = _candles.GetSma(SlowPeriod).ToArray();

        var fastNow = fastSma[^1].Sma;
        var fastPrev = fastSma[^2].Sma;
        var slowNow = slowSma[^1].Sma;
        var slowPrev = slowSma[^2].Sma;

        if (fastNow is null || fastPrev is null || slowNow is null || slowPrev is null) return;

        // 画均线
        Executor.GetOrAddGraph("Main").PutPoint("Fast", candle.BeginTime, fastNow.Value, color: Color.Orange);
        Executor.GetOrAddGraph("Main").PutPoint("Slow", candle.BeginTime, slowNow.Value, color: Color.Blue);

        if (outDated) return; // 历史补推数据不下单

        var pos = GetPositionVolume(Accounts[0].AccountId, _main.Code);

        // 金叉：快线上穿慢线
        if (fastPrev.Value < slowPrev.Value && fastNow.Value > slowNow.Value && pos == 0)
        {
            this.ChasingBuy(_main.Code, 1);
            LogInfo($"金叉信号 Fast={fastNow:F2} Slow={slowNow:F2}");
        }
        // 死叉：快线下穿慢线
        else if (fastPrev.Value > slowPrev.Value && fastNow.Value < slowNow.Value && pos > 0)
        {
            this.ChasingSell(_main.Code, pos);
            LogInfo($"死叉信号 Fast={fastNow:F2} Slow={slowNow:F2}");
        }
    }

    public override void AfterTrading()
    {
        var pos = GetPositionVolume(Accounts[0].AccountId, _main.Code);
        LogInfo($"今日结束持仓: {pos}");
    }
}
```

---

## 示例2：期现套利策略（双账号 + 配对算法）

```csharp
[DisplayName("股指期现套利")]
[UsePairAlgo]
public class IndexArbiStrategy : CommonStrategy
{
    private string _futureAccountId = null!;
    private string _stockAccountId = null!;
    private Instrument _future = null!;
    private Instrument _etf = null!;

    [RangeParams<double>(Name = "开仓价差", Begin = -2.0, End = 0, Step = 0.2)]
    public double BuyWantedSpread { get; set; } = -1.0;

    [RangeParams<double>(Name = "平仓价差", Begin = 0, End = 2.0, Step = 0.2)]
    public double SellWantedSpread { get; set; } = 1.0;

    // 价差计算器（字符串必须与方法实现一致）
    const string BuySpreadCalc = "return q1 - q2;";
    const string SellSpreadCalc = "return q1 - q2;";
    public double? CalculateBuySpread(double q1, double q2, double[] p) => q1 - q2;
    public double? CalculateSellSpread(double q1, double q2, double[] p) => q1 - q2;

    public override void Init()
    {
        _futureAccountId = Accounts.FirstOrDefault(o => o.Tag.Contains("Future"))?.AccountId
            ?? throw new Exception("需要一个标记为 Future 的账号");
        _stockAccountId = Accounts.FirstOrDefault(o => o.Tag.Contains("Stock"))?.AccountId
            ?? throw new Exception("需要一个标记为 Stock 的账号");

        _future = Instrument.FromCode("IF2309");
        _etf = Instrument.FromCode("510300.SSE");
    }

    public override void BeforeTrading()
    {
        SubMarketData(_future);
        SubMarketData(_etf);
    }

    private string? _openOrderId = null;
    private bool _hasPosition = false;

    public override void OnQuoteArrive(QuoteData q, bool outDated)
    {
        if (outDated) return;
        if (_hasPosition || _openOrderId != null) return;

        // 开仓：买期货 + 卖ETF（当价差足够低时）
        _openOrderId = this.SubmitPairOrder(
            _future.Code, _etf.Code,
            BUY,
            volume1: 1, volume2: 100,
            BuySpreadCalc, SellSpreadCalc,
            BuyWantedSpread
        );
    }

    public override void OnRtnAlgoOrder(AlgoOrder algoOrder)
    {
        if (algoOrder.AlgoClientId == _openOrderId
            && algoOrder.Status == AlgoOrderStatus.Completed)
        {
            _hasPosition = true;
            _openOrderId = null;
            LogInfo("开仓完成");
        }
    }
}
```

---

## 示例3：定时换仓（Twap + 定时任务）

```csharp
[DisplayName("定时Twap换仓")]
[UseTwapAlgo]
public class TimedRebalanceStrategy : CommonStrategy
{
    [ValueListParams<string>(Name = "目标标的", ValueList = new[] { "510300.SSE", "510500.SSE" })]
    public string TargetCode { get; set; } = "510300.SSE";

    [RangeParams<int>(Name = "目标仓位（手）", Begin = 100, End = 1000, Step = 100)]
    public int TargetVolume { get; set; } = 500;

    private Instrument _target = null!;
    private readonly CancellationTokenSource _cts = new();

    public override void Init()
    {
        _target = Instrument.FromCode(TargetCode);
    }

    public override void BeforeTrading()
    {
        SubMarketData(_target);

        // 每天 9:31 开始换仓，Twap 执行 30 分钟
        this.AddTimerTask("Twap换仓", TradingDay.AddHours(9).AddMinutes(31), () =>
        {
            var pos = GetPositionVolume(Accounts[0].AccountId, _target.Code);
            var diff = TargetVolume - (int)pos;

            if (diff > 0)
            {
                this.TwapBuy(_target, diff, 1800);
                LogInfo($"开始Twap买入 {diff} 手");
            }
            else if (diff < 0)
            {
                this.TwapSell(_target, -diff, 1800);
                LogInfo($"开始Twap卖出 {-diff} 手");
            }
        }, _cts.Token);
    }
}
```

---

## 示例4：子策略组合（多策略共用账号）

```csharp
// 子策略A：追涨策略
[UseChasingAlgo]
public class MomentumSubStrategy : CommonStrategy
{
    [ValueListParams<string>(ValueList = [])]
    public Instrument Instrument { get; set; } = null!;

    public override void BeforeTrading()
    {
        SubMarketData(Instrument);
    }

    public override void OnQuoteArrive(QuoteData q, bool outDated)
    {
        if (outDated || q.Instrument != Instrument) return;
        // 策略逻辑...
    }
}

// 父策略：组合两个子策略
[UseChasingAlgo]
public class CombinedStrategy : CommonStrategy
{
    public override void Init()
    {
        // 为每个标的创建独立的子策略实例
        AddSubStrategy<MomentumSubStrategy>("momentum_if", x =>
        {
            x.Instrument = Instrument.FromCode("IF2309");
        });
        AddSubStrategy<MomentumSubStrategy>("momentum_ic", x =>
        {
            x.Instrument = Instrument.FromCode("IC2309");
        });
    }
}
```

---

## 常见写法模式

### 避免重复下单

```csharp
private string? _activeOrderId = null;

// 检查是否有未完成的母单
private bool HasActiveOrder()
{
    if (_activeOrderId == null) return false;
    var order = this.GetChasingOrder(_activeOrderId);
    return order != null && !order.IsFinished;
}
```

### outDated 的正确处理

```csharp
public override void OnCandleArrive(Instrument instrument, CandleType type, CandleData candle, bool outDated)
{
    // 始终积累数据用于指标计算
    _candles.Add(candle);
    
    // outDated 时只更新状态，不下单
    if (outDated) return;
    
    // 以下是需要实时触发的交易逻辑
}
```

### 多标的行情区分

```csharp
public override void OnQuoteArrive(QuoteData q, bool outDated)
{
    if (q.Instrument == _mainInstrument)
    {
        // 处理主标的行情
    }
    else if (q.Instrument == _secondInstrument)
    {
        // 处理次标的行情
    }
}

public override void OnCandleArrive(Instrument instrument, CandleType type, CandleData candle, bool outDated)
{
    if (instrument == _mainInstrument && type == CandleType.Minute)
    {
        // 处理主标的分钟K线
    }
}
```
