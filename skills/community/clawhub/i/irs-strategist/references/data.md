# IRS 数据获取参考

## 数据源体系

IRS 使用三类数据源：

| 数据源               | 用途                                    | 地址                                              |
| -------------------- | --------------------------------------- | ------------------------------------------------- |
| **147基础数据**      | Tick/K线/日线/分红等核心行情            | `\\192.168.1.147\sgd-data\data`（IDC用 `.2.147`） |
| **RedisQuota**       | 实盘盘中重启时补推当日历史行情          | `192.168.1.132:6378` / `192.168.1.133:6378`       |
| **聚源数据库(JYDB)** | 财务/基本面/合约信息/交易日历等研究数据 | SqlServer `192.168.1.129`                         |

修改147数据路径：
```csharp
DataSourcesOptions.Default.BasePath = @"\\192.168.2.147\sgd-data\data";
// 或设置环境变量：DATA_SOURCE_BASE_PATH
```

修改聚源连接串：
```csharp
SqlHelperOptions.JYDBConnectionString = "Server=192.168.1.129;Database=JYDB;User Id=Traders;Password=abcd4321;Encrypt=false;TrustServerCertificate=True";
```

---

## 一、历史行情数据（DataUtils）

> **重要**：一般不需要查询当日数据，订阅行情后系统会自动推送。实盘也无法读当日历史数据。

### Tick 数据

```csharp
// 获取某天全部Tick
IReadOnlyList<QuoteData> ticks = DataUtils.GetTicks(PreTradingDay, Instrument.FromCode("000300.SSE"));

// 期货Tick
var futTicks = DataUtils.GetTicks(PreTradingDay, Instrument.FromCode("IF2503"));
```

**存储路径格式**：`{basePath}/{market}/{yyyyMMdd}/tick_pb/{code}.pb.gz`
- 注意：Tick数据加载时会同时加载日线，用于填充涨跌停价、开盘价、昨收等字段

### K线（Candle）数据

```csharp
// 分钟线（一天）
var candles = DataUtils.GetCandles(
    Instrument.FromCode("000300.SSE"),
    CandleType.Minute,
    PreTradingDay,
    PreTradingDay);

// 多天范围
var candles = DataUtils.GetCandles(
    Instrument.FromCode("IF2503"),
    CandleType.Minute,
    startDate,
    endDate);

// K线类型
// CandleType.Minute  - 1分钟
// CandleType.Minute5 - 5分钟（如有）
// CandleType.Day     - 日线
```

**CandleData 字段**：
- `BeginTime` / `EndTime` - K线时间段
- `Open` / `High` / `Low` / `Close` - OHLC价格
- `Volume` - 成交量
- `Amount` - 成交额

### 日线（Daily）数据

```csharp
// 获取某个标的某日的日线记录
var daily = GetDailyData(PreTradingDay, Instrument.FromCode("000300.SSE"));
// 或通过 DataUtils 批量获取

// DailyRecord 字段：
// .Candle.Open/High/Low/Close/Volume
// .UpperLimit / .LowerLimit - 涨跌停价
// .PreClose - 前收盘价
// .PreSettlement - 前结算价（期货）
```

---

## 二、主力合约数据

IRS 提供了 `DataUtils.GetMainContracts` 方法，直接获取某天主力合约：

主力合约是通过成交金额排序取最大的合约。次主力是指交割日在主力合约之后的下一个成交金额最大的合约。

```csharp
// 获取某天某品种的主力合约代码
var mains = DataUtils.GetMainContracts(PreTradingDay, "IF");
```

**聚源数据库扩展查询（通过 FreeSql）**：

```csharp
// Fut_ContractMapping 表：主力合约每天的映射关系
// InfoContractCode  主力(连续)合约代码，如 "IF9999"
// MapContractCode   对应当天实际合约代码，如 "IF2503"
// TradingDay        交易日期
// ContractType = 1  代表主力合约

var mapping = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.FutContractMapping>()
    .Where(o => o.InfoContractCode == "IF9999" && o.TradingDay == PreTradingDay)
    .First();
var mainCode = mapping?.MapContractCode; // "IF2503"

// 获取合约基础信息（交割日期、合约乘数等）
// Fut_ContractMain 表：
var contractInfo = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.FutContractMain>()
    .Where(o => o.ContractCode == "IF2503")
    .First();
// contractInfo.DeliveryDate       交割日期
// contractInfo.LastTradingDate    最后交易日
// contractInfo.ContractState == 1 上市中
```

---

## 三、交易日历

IRS 内置多套交易日历，通过 `[UseCalendar<T>]` 特性指定：

| 类型                       | 描述                             | 数据来源                       |
| -------------------------- | -------------------------------- | ------------------------------ |
| `ChinaCalendar`            | A股/国内期货（**默认**）         | 147/factor/ChinaHolidays.csv   |
| `HKCalendar`               | 港股通                           | 聚源 `QT_SHSZHSCTradingDay` 表 |
| `USCalendar`               | 美国市场（NYMEX/COMEX/NASDAQ等） | 147/factor/USHolidays.csv      |
| `BVMFCalendar`             | 巴西BVMF                         | 147/factor/BVMFHolidays.csv    |
| `EveryDayCalendar`         | 每天都是交易日（比特币等）       | —                              |
| `IntersectCalendar<T1,T2>` | 两个日历的交集                   | —                              |
| `MergedCalendar<T1,T2>`    | 两个日历的并集                   | —                              |

```csharp
// 使用港股通日历
[UseCalendar<HKCalendar>]
public class HkStrategy : CommonStrategy { }

// 判断是否为交易日
bool isTrading = IsTradingDay(someDate);                    // 按策略日历
bool isTrading = ChinaCalendar.Instance.IsTradingDay(date); // 指定日历
bool isTrading = Instrument.FromCode("000001.SZSE").Calendar.IsTradingDay(date);

// 获取某时段内所有交易日
DateTime[] days = CommonStrategy.GetTradingDays(startDate, endDate);
DateTime[] days = ChinaCalendar.Instance.GetTradingDays(startDate, endDate);
```

**聚源扩展（查交易日细节）**：

```csharp
// QT_TradingDayNew 表：详细交易日标记
// SecuMarket: 83-上交所, 90-深交所, 72-港股联交所
// IfTradingDay: 1-是, 2-否
// IfWeekEnd / IfMonthEnd / IfQuarterEnd / IfYearEnd

var tradingDayInfo = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.QTTradingDayNew>()
    .Where(o => o.TradingDate >= startDate
             && o.TradingDate <= endDate
             && o.SecuMarket == 83         // 上交所
             && o.IfTradingDay == 1)        // 是交易日
    .OrderBy(o => o.TradingDate)
    .ToList();
```

---

## 四、汇率数据

### IRS 内置（跨币种结算时自动使用）

```csharp
// 设置临时固定汇率（回测时常用）
CurrencyRateManager.Default.SetTempFixedRate("HKD", 0.92);     
```

## 五、分红送股数据

### IRS 内置接口

```csharp
// 获取某标的的分红序列（处理除权用）
var dividends = GetStockDividend(Instrument.FromCode("000300.SSE"));
// 数据来源：\\192.168.1.147\sgd-data\data\factor\bonus.csv

// 在 AfterSettlement 中获取当日实际分红
public override void AfterSettlement(StrategyDailyInfo dailyInfo)
{
    var info = dailyInfo.AccountDailyInfos[MainAccountId];
    foreach (var (code, cashDiv) in info.StockCashDividend)
        LogInfo($"{code} 现金分红: {cashDiv}元");
    foreach (var (code, stockDiv) in info.StockDividend)
        LogInfo($"{code} 配股: {stockDiv}股");
    foreach (var (code, stockExt) in info.StockExtension)
        LogInfo($"{code} 转增: {stockExt}股");
}
// 注意：所有Tick/Candle/日线数据均为未除权数据，需自行处理
// ETF分红合并时，送股字段的值为负数（与股票相反）
```

## 六、ETF申赎数据

### IRS 内置接口

```csharp
// 获取ETF成分清单（含现金替代标志、数量等）
var components = DataUtils.GetEtfComponentInfos(
    Instrument.FromCode("588030"), PreTradingDay);
// 注意：深市ETF清单中 "159900" 并非真正成分股

// 获取ETF申赎信息（最小申赎单位、现金差额等）
var purRedInfo = DataUtils.GetEtfPurRedInfo(
    Instrument.FromCode("588030"), PreTradingDay);

// 申购
this.EtfPur(Instrument.Stock("588030"), 300000); // 申购30万份

// 赎回
this.EtfRed(Instrument.Stock("588030"), 300000);

// 持仓中可用于赎回的份额（扣除当日申购到账的）
var pos = GetPositions(MainAccountId, "588030");
var redeemable = pos.TotalLong - pos.EtfPuredOrStockRedeemed;
```

### 聚源数据库扩展查询

**MF_ETFPRComponents（ETF成分清单）**：
- `InnerCode` 基金内部编码
- `TradingDay` 交易日期
- `SecuCode` 成分股代码
- `StockAmount` 股票数量
- `CashSubstituteSign` 现金替代标志：1-允许, 2-必须, 3-禁止, 4-退补
- `CashSubstituteProportion` 现金替代比例
- `ApplyCashPremiumRate` 申购溢价比例
- `RedeemCashDiscountRate` 赎回折价比例
- `FixedSubstituteSum` 固定替代金额

```csharp
var etfComponents = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.MFETFPRComponents>()
    .InnerJoin<IRS.Common.DataBase.JYDB.SecuMain>((c, s) => c.InnerCode == s.InnerCode)
    .Where((c, s) => s.SecuCode == "588030" && c.TradingDay == PreTradingDay)
    .ToList();
```

**MF_ETFPRList（ETF申赎信息）**：
- 包含最小申赎单位、现金差额、申购上限等

---

## 七、停牌数据

```csharp
// IRS 内置接口（数据来源：聚源 LC_SuspendResumption 表）
if (Instrument.FromCode("600036").IsSuspend(PreTradingDay))
    LogInfo("停牌中");

// 聚源直接查询 LC_SuspendResumption：
// InnerCode - 与 SecuMain.InnerCode 关联
// InfoPublDate - 信息发布日期（停复牌公告日）
// 来源市场：18-北交所, 83-上交所, 90-深交所
```

---

## 八、股票日线（聚源 QT_DailyQuote）

当需要额外的市场行情信息（如成交笔数、换手率等）时，可通过聚源查询：

```csharp
// QT_DailyQuote 字段：
// InnerCode     与 SecuMain.InnerCode 关联
// TradingDay    交易日
// PrevClosePrice  昨收盘（元）
// OpenPrice / HighPrice / LowPrice / ClosePrice
// TurnoverVolume  成交量（股）
// TurnoverValue   成交金额（元）
// TurnoverDeals   成交笔数（笔）

var dailyQuotes = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.QTDailyQuote>()
    .InnerJoin<IRS.Common.DataBase.JYDB.SecuMain>((q, s) => q.InnerCode == s.InnerCode)
    .Where((q, s) => s.SecuCode == "600000"
                  && q.TradingDay >= startDate
                  && q.TradingDay <= endDate)
    .OrderBy((q, s) => q.TradingDay)
    .ToList<IRS.Common.DataBase.JYDB.QTDailyQuote>();
```

> **注意**：IRS 的 `DataUtils.GetCandles(..., CandleType.Day, ...)` 更高效，聚源 QT_DailyQuote 适合查额外字段。

---

## 九、期货日线（聚源 Fut_DailyQuote）

```csharp
// Fut_DailyQuote 包含期货特有字段：
// ContractInnerCode  合约内部编码（关联 Fut_ContractMain）
// SettlementPrice    结算价
// OpenInterest       持仓量
// TurnoverVolume / TurnoverValue
// ...
// 适合查合约持仓量、结算价等期货特有信息

var futDailyList = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.FutDailyQuote>()
    .InnerJoin<IRS.Common.DataBase.JYDB.FutContractMain>((d, c) => d.ContractInnerCode == c.ContractInnerCode)
    .Where((d, c) => c.ContractCode == "IF2503"
                  && d.TradingDay >= startDate)
    .OrderBy((d, c) => d.TradingDay)
    .ToList<IRS.Common.DataBase.JYDB.FutDailyQuote>();
```

---

## 十、SecuMain（证券主表）

聚源大多数表通过 `InnerCode` 关联此表获取证券代码：

```csharp
// SecuMain 关键字段：
// InnerCode     证券内部编码（聚源主键）
// SecuCode      交易代码（如 "600000"）
// SecuAbbr      证券简称
// SecuMarket    市场（83-上交所, 90-深交所, 18-北交所）
// SecuCategory  证券类别（1-A股, 8-ETF等）
// ListedDate / DelistedDate  上市/退市日期

var secuInfo = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.SecuMain>()
    .Where(o => o.SecuCode == "000300" && o.SecuMarket == 83)
    .First();
var innerCode = secuInfo?.InnerCode;
```

---

## 十一、聚源数据字典说明

聚源数据库（JYDB）在 `192.168.1.129` 上的 SqlServer，对应表已通过 ORM 映射为 C# 类，通过 `IRS.Common.DataBase.SqlHelper.JYDB` 访问（FreeSql）。

**常用表速查**：

| 表名                     | 说明             | 关键字段                                         |
| ------------------------ | ---------------- | ------------------------------------------------ |
| `SecuMain`               | 股票证券主表     | SecuCode, InnerCode, SecuMarket                  |
| `Fut_ContractMain`       | 期货合约基础信息 | ContractCode, DeliveryDate, ContractState        |
| `Fut_ContractMapping`    | 主力合约每日映射 | InfoContractCode, MapContractCode, TradingDay    |
| `Fut_DailyQuote`         | 期货日线行情     | ContractInnerCode, SettlementPrice, OpenInterest |
| `QT_DailyQuote`          | A股日线行情      | InnerCode, TurnoverDeals, ClosePrice             |
| `QT_TradingDayNew`       | 交易日历         | TradingDate, IfTradingDay, SecuMarket            |
| `QT_SHSZHSCTradingDay`   | 港股通交易日历   | 用于 HKCalendar                                  |
| `LC_Dividend`            | 股票分红方案     | InnerCode, EndDate, EventProcedure               |
| `LC_SuspendResumption`   | 停复牌           | InnerCode, InfoPublDate                          |
| `MF_ETFPRComponents`     | ETF申赎成分清单  | InnerCode, TradingDay, CashSubstituteSign        |
| `MF_ETFPRList`           | ETF申赎信息      | 最小申赎单位、现金差额                           |
| `ED_RMBBaseEXchangeRate` | 人民币官方汇率   | EndDate, ForeCurrency, MidExRate                 |
| `FX_OfficialFX`          | 官方外汇牌价     | 含港元/外币双向汇率                              |
| `HK_Dividend`            | 港股分红         | —                                                |

**在线数据字典**：https://dd.gildata.com/（用户名：szsgdsjk01，密码：gildata@123）

---

## 十二、关于逐笔数据

聚源数据库（JYDB）本身**不包含 Level2 逐笔成交/逐笔委托数据**，该类数据属于实时行情范畴。IRS 中 Tick 数据（QuoteData）对应的是 Level1 快照行情（每3秒），来源于 147 基础数据服务器。如需真正的 Level2 逐笔数据，需要接入专门的 Level2 行情源（非标准功能）。
