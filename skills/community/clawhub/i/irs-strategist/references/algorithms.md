# IRS 算法详细参考

## 算法概览

IRS 内置多种算法，策略类上必须添加对应的 `[UseXxxAlgo]` 特性。

| 算法 | 特性标记 | 适用场景 |
|------|---------|---------|
| 子单算法 | `[UseSubOrderAlgo]` | 直接下普通委托，最基础 |
| 追单算法 | `[UseChasingAlgo]` | 按对手价追单，自动追价 |
| Twap算法 | `[UseTwapAlgo]` | 时间加权拆单，降低冲击 |
| 配对算法 | `[UsePairAlgo]` | 双腿价差交易 |

> 使用融券卖出、期货等特殊场景时，需确认所用算法支持。

---

## 1. 子单算法（SubOrder）

最简单的算法，直接向柜台发送普通委托。

> **建议优先考虑追单/Twap算法，子单算法仅在它们无法满足需求时使用。**

```csharp
[UseSubOrderAlgo]
public class MyStrategy : CommonStrategy
{
    public override void OnCandleArrive(Instrument instrument, CandleType type, CandleData candle, bool outDated)
    {
        if (outDated) return;
        // 按最新价买入1手
        this.MarketOrder(instrument.Code, instrument.Exchange, BUY, OPEN, 1, candle.Close);
        // 简便方法
        // this.BuyOpen(code, volume, price);
        // this.SellClose(code, volume, price);
    }

    public override void OnRtnAlgoOrder(AlgoOrder algoOrder)
    {
        if (algoOrder is SubOrder subOrder)
        {
            // 处理子单回报
        }
    }

    public override void OnRtnSubOrderTrade(SubOrderTrade trade)
    {
        // 处理成交回报
    }
}
```

---

## 2. 追单算法（Chasing）

算法自动向对手价发单，未成交则撤单继续追最新对手价，直到成交。

- 支持自动处理零碎股（持仓只剩零碎股时）
- 融券卖出时按最新价报单

```csharp
[UseChasingAlgo]
public class MyStrategy : CommonStrategy
{
    public override void OnCandleArrive(Instrument instrument, CandleType type, CandleData candle, bool outDated)
    {
        if (outDated) return;

        // 基础用法：买入10手
        var orderId = this.ChasingBuy(instrument.Code, 10);

        // 设置拆单（每次最多3手）
        var orderId2 = this.ChasingBuy(instrument.Code, 10, batchVolume: 3);

        // 指定开平方向
        var orderId3 = this.ChasingBuy(instrument.Code, 10, offset: Offset.Open);

        // 查询/撤销
        var order = this.GetChasingOrder(orderId);
        this.CancelChasingOrder(orderId);
    }
}
```

### CustomProperties 参数

```csharp
// 不平今品种（适用于期货，用锁仓代替平今）
this.ChasingBuy(code, 10, customProperties: new Dictionary<string, string>
{
    [nameof(ChasingParameter.CloseTodayExceptCommodities)] = "ag,au,pb"
});

// 失败自动重试
this.ChasingBuy(code, 10, customProperties: new Dictionary<string, string>
{
    [nameof(ChasingParameter.RetryErrorMessages)] = "自成交,资金不足"
});
```

> **注意**：中金所股指期货（IF/IC/IH/IM）总是不平今，无需特殊设置。

---

## 3. Twap 算法

将交易拆分为一段时间内均匀执行，降低市场冲击。

支持两种实现：
- **SgdTwap**：支持期货、港股，不支持融券/VWAP
- **QndTwap**：支持股票融券卖出，不支持期货/港股，支持VWAP

```csharp
[UseTwapAlgo]
public class MyStrategy : CommonStrategy
{
    public override void OnCandleArrive(Instrument instrument, CandleType type, CandleData candle, bool outDated)
    {
        if (outDated) return;

        // 简便用法：120秒内买入100手
        this.TwapBuy(instrument, 100, 120);

        // 完整参数用法
        var orderId = this.SubmitTwapOrder(new TwapAlgoParameter()
        {
            AccountVolumes = new[]
            {
                new AccountVolume { Volume = 100, AccountRefId = Accounts[0].AccountId }
            },
            BeginTime = GetTradingDay().Add(new TimeSpan(9, 30, 0)),
            Code = instrument.Code,
            ExchangeId = instrument.Exchange,
            Direction = "BUY",
            Duration = TimeSpan.FromSeconds(120),
            MinChasingIntervalSeconds = 2,
            MinuteLimitVolumeRate = 0.1,
            CloseTodayExceptCommodities = Array.Empty<string>(),
            RetryErrorMessages = Array.Empty<string>(),
        });

        var order = this.GetTwapAlgoOrder(orderId);
    }
}
```

### SgdTwap CustomProperties

```csharp
// 分钟成交量限制比例（默认0.1=10%）
this.TwapBuy(code, 100, 120, customProperties: new Dictionary<string, string>
{
    [nameof(SgdTwapParameter.MinuteLimitVolumeRate)] = "0.1",
    [nameof(SgdTwapParameter.DisableMinuteLimit)] = "false",      // 是否禁用分钟限制
    [nameof(SgdTwapParameter.AllowTradeAfterEnd)] = "true",        // 超时是否继续
    [nameof(SgdTwapParameter.AllowTakeAtLimit)] = "false",         // 涨跌停是否打单
    [nameof(SgdTwapParameter.MinChasingIntervalSeconds)] = "2",    // 最小追单间隔(秒)
    [nameof(SgdTwapParameter.PreferMinBatchVolume)] = "2000",      // 每次最小下单量
    [nameof(SgdTwapParameter.Offset)] = "Open",                    // 开平方向
    [nameof(SgdTwapParameter.CloseTodayExceptCommodities)] = "ag,au",
});
```

### QndTwap CustomProperties

```csharp
// AlgoType: "Twap" 或 "Vwap"
// MaxAmountPerMinute: 每分钟最大金额（0=不限）
// MaxCancelRate: 撤单率控制（0=不限）
// MinOrderAmount: 最小下单金额（默认3000）
// AllowTradeAfterEnd: 超时是否继续（默认true）
// AllowTradeAtLimit: 涨跌停是否继续（默认false）
```

---

## 4. 配对算法（Pair）

双腿价差交易，根据实时行情计算价差，满足条件后同时下两腿单。

**算法原理**：
1. 计算实时价差（第一腿价格 vs 第二腿对手价）
2. 满足价差条件时，挂第一腿，等待成交
3. 第一腿成交后，追单或挂单完成第二腿

```csharp
[UsePairAlgo]
public class MyStrategy : CommonStrategy
{
    // 价差计算器（字符串与方法内容保持一致，否则编译失败）
    const string BuySpreadCalculator = "return q1 - q2;";
    const string SellSpreadCalculator = "return q1 - q2;";

    public double? CalculateBuySpread(double q1, double q2, double[] parameter) => q1 - q2;
    public double? CalculateSellSpread(double q1, double q2, double[] parameter) => q1 - q2;

    public override void OnCandleArrive(Instrument instrument, CandleType type, CandleData candle, bool outDated)
    {
        if (outDated) return;

        double buyWantedSpread = -0.5; // 希望的买入价差

        // 提交配对单
        var orderId = this.SubmitPairOrder(
            Main.Code, Second.Code,
            BUY,
            volume1: 1, volume2: 1,
            BuySpreadCalculator, SellSpreadCalculator,
            buyWantedSpread
        );

        // 修改价差
        this.ModifyPairOrderWantedSpread(orderId, newSpread);

        // 撤销
        this.CancelPairOrder(orderId);
    }
}
```

### Pair CustomProperties

```csharp
var orderId = this.SubmitPairOrder(code1, code2, BUY, 1, 1, buyCalc, sellCalc, wantedSpread,
    customProperties: new Dictionary<string, string>
    {
        [nameof(PairAlgoParameter.SecondLegPlace)] = "true",          // 第二腿挂单执行（默认false=追单）
        [nameof(PairAlgoParameter.Code2StopLossRate)] = "0.1",        // 第二腿挂单止损率（%，需SecondLegPlace=true）
        [nameof(PairAlgoParameter.MinSubmitCancelSeconds)] = "2",     // 最小撤单间隔(秒)
        [nameof(PairAlgoParameter.QuotaMaxDelaySeconds)] = "10",      // 行情最大延迟(秒)
        [nameof(PairAlgoParameter.QuoteMaxDiffSeconds)] = "5",        // 两腿行情最大时差(秒)
        [nameof(PairAlgoParameter.SecondLegBatchVolume)] = "10",      // 第二腿分批下单量
        [nameof(PairAlgoParameter.PreferCode1ShortSell)] = "false",   // 第一腿优先融券卖出
        [nameof(PairAlgoParameter.CheckStockAvailable)] = "true",     // 检查股票可卖数量
        [nameof(PairAlgoParameter.CloseTodayExceptCommodities)] = "ag,au",
        [nameof(PairAlgoParameter.RetryErrorMessage)] = "自成交",
        ["RetryIntervalSeconds"] = "5",                               // 重试间隔(秒)
    });
```

> **注意**：`BuySpreadCalculator` 字符串内容必须与 `CalculateBuySpread` 方法实现完全一致，否则会出现 `CS0103` 编译错误。

---

## AlgoOrderId 与 AlgoClientId

- `AlgoClientId`：IRS 本地生成的母单唯一标志，下单时立即可用，`SubmitXxxOrder` 的返回值
- `AlgoOrderId`：算法平台生成，需在 `OnCreateAlgoOrder` 回报后才能获取

所有撤单/修改操作使用 `AlgoClientId`（即下单接口的返回值）。

---

## 融券额度配置（配对算法）

回测中默认每票有 100 万融券额度。实盘需维护配置文件：

```csv title="Config/CreditAmountInfos.csv"
Account,Code,Total,Used
account01,000623,10000,0
account02,000623,10000,0
```
