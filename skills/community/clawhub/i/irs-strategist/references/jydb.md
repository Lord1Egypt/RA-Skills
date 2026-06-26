# 聚源数据字典（JYDB）索引

> 数据库：SqlServer `192.168.1.129`，库名 `JYDB`
> 连接串：`Server=192.168.1.129;Database=JYDB;User Id=Traders;Password=abcd4321;Encrypt=false;TrustServerCertificate=True`
> ORM 访问：`IRS.Common.DataBase.SqlHelper.JYDB`（FreeSql）
> 在线数据字典：https://dd.gildata.com/（用户名：szsgdsjk01，密码：gildata@123）

> **说明**：本索引列出聚源数据库全部 610 张表。**字段详情请查阅同目录下的 `tableInfo/{TableName}.json`**。

---

## 使用指南

### 1. JSON 文件结构

每个 `tableInfo/{TableName}.json` 文件包含该表所有字段的定义，格式如下：

```json
[
    {
        "columnOrderId": 1,
        "columnName": "InnerCode",
        "columnChiName": "证券内部编码",
        "columnType": "int",
        "isNullable": 0,
        "isEffective": true,
        "remark": "与SecuMain.InnerCode关联",
        "valueRate": "100.0"
    }
]
```

**关键字段说明**：

| JSON 字段 | 含义 | 示例 |
|-----------|------|------|
| `columnName` | 数据库列名，即 SQL / ORM 中使用的字段名 | `InnerCode`, `TradingDay` |
| `columnChiName` | 中文描述 | 证券内部编码, 交易日 |
| `columnType` | SQL 数据类型 | `int`, `varchar(30)`, `decimal(10,4)`, `datetime` |
| `isNullable` | 是否允许为空 | `0`=不允许, `1`=允许 |
| `isEffective` | 是否为有效字段 | `true` |
| `remark` | 补充说明（部分字段有） | 关联关系、计算方式等 |

### 2. 表名 → C# 类名映射

IRS 已将聚源数据库的表映射为 C# 实体类，命名规则：**去掉下划线，保留大小写**，命名空间为 `IRS.Common.DataBase.JYDB`。

| 聚源表名 | C# 实体类 |
|----------|-----------|
| `SecuMain` | `IRS.Common.DataBase.JYDB.SecuMain` |
| `QT_DailyQuote` | `IRS.Common.DataBase.JYDB.QTDailyQuote` |
| `QT_TradingDayNew` | `IRS.Common.DataBase.JYDB.QTTradingDayNew` |
| `LC_Dividend` | `IRS.Common.DataBase.JYDB.LCDividend` |
| `Fut_ContractMain` | `IRS.Common.DataBase.JYDB.FutContractMain` |
| `MF_ETFPRComponents` | `IRS.Common.DataBase.JYDB.MFETFPRComponents` |

> **注意**：不是所有 610 张表都已映射为 C# 实体类。已映射的表通常在 `data.md` 中有使用示例。未映射的表可以用原生 SQL 查询。

### 3. 用 FreeSql ORM 查询（推荐）

已映射的表通过 `SqlHelper.JYDB` (FreeSql) 访问，支持 Lambda 表达式：

```csharp
// 示例1：查证券信息
// 从 tableInfo/SecuMain.json 可知字段：InnerCode, SecuCode, SecuAbbr, SecuMarket...
var stock = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.SecuMain>()
    .Where(o => o.SecuCode == "600000" && o.SecuMarket == 83)
    .First();
// stock.SecuCode   -> "600000"
// stock.SecuAbbr   -> "浦发银行"
// stock.InnerCode  -> 1 (用于关联其他表)

// 示例2：连表查日线行情
// QT_DailyQuote.json 字段：InnerCode, TradingDay, ClosePrice, TurnoverVolume...
var quotes = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.QTDailyQuote>()
    .InnerJoin<IRS.Common.DataBase.JYDB.SecuMain>((q, s) => q.InnerCode == s.InnerCode)
    .Where((q, s) => s.SecuCode == "600000" && q.TradingDay >= startDate)
    .OrderBy((q, s) => q.TradingDay)
    .ToList();

// 示例3：查某ETF成分股
// MF_ETFPRComponents.json 字段：InnerCode, TradingDay, SecuCode, StockAmount...
var components = IRS.Common.DataBase.SqlHelper.JYDB
    .Select<IRS.Common.DataBase.JYDB.MFETFPRComponents>()
    .InnerJoin<IRS.Common.DataBase.JYDB.SecuMain>((c, s) => c.InnerCode == s.InnerCode)
    .Where((c, s) => s.SecuCode == "588030" && c.TradingDay == PreTradingDay)
    .ToList();
```

### 4. 用原生 SQL 查询（未映射的表）

未映射为 C# 实体类的表，可以直接写 SQL。先查 JSON 确认字段名和类型，再写查询：

```csharp
// 示例：查指数成份股权重（LC_IndexComponentsWeight 表）
// 先看 tableInfo/LC_IndexComponentsWeight.json 确认字段：
//   IndexCode, InnerCode, Weight, TradingDay...

// 原生 SQL 查询
var weights = IRS.Common.DataBase.SqlHelper.JYDB
    .Ado.SqlQuery<dynamic>(
        @"SELECT a.SecuCode, b.SecuAbbr, w.Weight, w.TradingDay
          FROM LC_IndexComponentsWeight w
          INNER JOIN SecuMain a ON w.InnerCode = a.InnerCode
          INNER JOIN SecuMain b ON w.IndexCode = b.InnerCode
          WHERE b.SecuCode = '000300' AND w.TradingDay = @day
          ORDER BY w.Weight DESC",
        new { day = PreTradingDay });
```

### 5. 典型工作流

```
需求：查某数据
  │
  ├─ 1. 在下方索引中搜索关键词（表名/中文名/说明）
  │     或直接浏览对应分类
  │
  ├─ 2. 点击"查看"链接打开 tableInfo/{TableName}.json
  │     确认需要哪些字段、字段类型、关联关系（remark）
  │
  ├─ 3. 检查是否已有 C# 实体类（参考 data.md 中的映射）
  │     ├─ 有 → 用 FreeSql ORM (SqlHelper.JYDB.Select<T>)
  │     └─ 无 → 用原生 SQL (SqlHelper.JYDB.Ado.SqlQuery)
  │
  └─ 4. 关联 SecuMain 时注意：
        InnerCode 是聚源主键，大多数表通过它关联
        SecuCode 是交易代码（如 "600000"）
        SecuMarket 区分市场（83=上交所, 90=深交所, 18=北交所）
```

### 6. 通用关联字段

| 字段 | 说明 | 用法 |
|------|------|------|
| `InnerCode` | 证券内部编码（聚源主键） | 大多数表通过此字段关联 `SecuMain` |
| `CompanyCode` | 公司代码 | 上市公司相关表 |
| `TradingDay` / `TradingDate` | 交易日期 | 行情/日级别数据 |
| `ID` | 自增主键 | 部分表用此做主键 |
| `InfoPublDate` | 信息发布日期 | 公告/财报发布日期 |
| `EndDate` | 截止日期 | 财报/分红所属会计年度 |

---

## SecuMain - 证券主表

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `SecuMain` | 证券主表 | 本表收录单个证券品种（股票、基金、债券）的代码、简称、上市交易所等基础信息。 | [查看](tableInfo/SecuMain.json) |

## Bond - 债券相关

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `Bond_ABSBasicInfo` | 券商专项资产收益计划表 | 1.收录由中国证监会监管的专项资产收益计划的基本资料。此表信息已经并入Bond_BasicInfoN债券要素新表，... | [查看](tableInfo/Bond_ABSBasicInfo.json) |
| `Bond_ABSFCashFlow` | 资产支持证券预测现金流 | 1.内容说明：（1）根据资产流入端现金流归集表和资产支持证券分配机制，建立偿付模型，有足够的要素来较为准确的预测未... | [查看](tableInfo/Bond_ABSFCashFlow.json) |
| `Bond_ABSRiskS` | 资产支持证券风险状态 | 1.记录ABS项目发行说明书和跟踪评级报告披露的每只债券的资产池分布情况，其中涵盖五级分类分布、贷款合同金额分布、... | [查看](tableInfo/Bond_ABSRiskS.json) |
| `Bond_ABSTermAnalyse` | 资产支持证券期限分析表 | 1.内容说明：资产证券支持证券的期限敏感性分析情况,包括早偿率、违约率的影响因素等影响ABS的加权平均期限及预计到... | [查看](tableInfo/Bond_ABSTermAnalyse.json) |
| `Bond_ABSTradingQuote` | 券商专项资产大宗交易行情 | 1.信息来源：上海交易所，深圳交易所。 2.收录券商专项资产收益计划（资产证券化产品）每天的大宗交易行情数据。 3... | [查看](tableInfo/Bond_ABSTradingQuote.json) |
| `Bond_ABSWaterfall` | 资产支持证券分配机制 | 1.内容说明：本表记录资产支持证券发行说明书公布的现金流分配机制，包括证券端在正常、违约、加速清偿等情景下的偿付顺... | [查看](tableInfo/Bond_ABSWaterfall.json) |
| `Bond_AccruedInterest` | 债券应计利息 | 1.记录各类债券在每个交易日的债券应计利息信息。 2.数据范围：1986-07-01 至今 | [查看](tableInfo/Bond_AccruedInterest.json) |
| `Bond_AnnClassifi` | 债券公告分类 | 该表记录每条公告的分类信息。 | [查看](tableInfo/Bond_AnnClassifi.json) |
| `Bond_AsPoCashInflow` | 资产池现金流归集表 | 1.本表记录资产支持证券发行说明书公布的资产池现金流归集信息，客户可用此现金流估算ABS未来还本信息，便于评估投资... | [查看](tableInfo/Bond_AsPoCashInflow.json) |
| `Bond_AsPoInfo` | 资产池总体信息 | 1.本表记录资产支持证券发行说明书和跟踪评级报告、受托报告等公布的资产池基本情况，包含资产池笔数特征、金额特征、利... | [查看](tableInfo/Bond_AsPoInfo.json) |
| `Bond_AsPoRatingInfo` | 资产池评级指标表 | 内容说明：评级报告披露的量化分析压力测试指标，包括首次发行的评级报告和跟踪评级报告； 数据范围：2018年1月1日... | [查看](tableInfo/Bond_AsPoRatingInfo.json) |
| `Bond_BADepositI` | 大额存单概况 | 1.记录大额存单的基本资料，包括基本要素信息、发行情况等。  2.数据范围：2015-08-13 至今 3.信息来... | [查看](tableInfo/Bond_BADepositI.json) |
| `Bond_BADepositT` | 大额存单条款 | 1.记录大额存单的行权条款信息，主要包括转让、提前赎回、提前支取、质押条款。 2.数据范围：2015-08-13 ... | [查看](tableInfo/Bond_BADepositT.json) |
| `Bond_BADiscountRate` | 银行承兑汇票贴现利率 | 1.银行承兑汇票(BAbankacceptance)贴现率，利率类型包括直贴利率，转帖利率等 2.数据范围：200... | [查看](tableInfo/Bond_BADiscountRate.json) |
| `Bond_BDCreditGrading` | 债项信用评级 | 1.涵盖券种：短期融资券、可转换债券、企业债券、金融债券、金融次级债、银行间和交易所资产支持证券、混合资本债券等。... | [查看](tableInfo/Bond_BDCreditGrading.json) |
| `Bond_BIIndustry` | 债券主体行业划分 | 1.本表记录债券主体，包括发行人、原始权益人等行业划分情况。 2.数据范围：2005-10-11 至今 3.信息来... | [查看](tableInfo/Bond_BIIndustry.json) |
| `Bond_BasicInfo` | 债券要素表 | 1.本表展现所有债券（除可转债、券商专项资产支持证券以外）的基本要素。 2.涵盖在交易所、银行间、柜台等所有市场上... | [查看](tableInfo/Bond_BasicInfo.json) |
| `Bond_BasicInfoN` | 债券要素新表 | 1.本表展现所有债券（除可转债）的基本要素信息； 2.涵盖在交易所、银行间、柜台等所有市场上交易的国债、金融债、企... | [查看](tableInfo/Bond_BasicInfoN.json) |
| `Bond_Bid` | 债券发行招标 | 1.收录以招标方式发行的债券的招标及发行情况。 2.数据范围：2001-02-27 至今 3.信息来源：中债登 | [查看](tableInfo/Bond_Bid.json) |
| `Bond_BidDoc` | 债券发行招标书 | 1.收录以招标方式发行的债券招标情况。 2.数据范围：1998-08-22 至今 3.信息来源：中债登、货币网 | [查看](tableInfo/Bond_BidDoc.json) |
| `Bond_BidDoc_Add` | 债券招标书_追加投标 | 1.收录以招标方式发行的债券追加招标情况。 2.数据范围：2008-01-08 至今 3.信息来源：中债登、货币网 | [查看](tableInfo/Bond_BidDoc_Add.json) |
| `Bond_BondIndexQuote` | 债券指数行情 | 1.收录了上证债券指数、中证债券指数、深证债券/国证债券指数等指数的行情数据。 2.历史数据：1996年7月至今 ... | [查看](tableInfo/Bond_BondIndexQuote.json) |
| `Bond_CBCurrencyPT` | 央行货币政策工具 | 1.记录中国人民银行披露的货币政策工具信息，主要记录中期借贷便利(MLF)、常备借贷便利(SLF)、抵押补充贷款(... | [查看](tableInfo/Bond_CBCurrencyPT.json) |
| `Bond_CBDerivNew` | 可转换债券衍生指标新表 | 1.收录可转换债券（包括可交换债券）衍生指标，包括纯债到期收益率，当期收益率，久期，凸性，转股价值，转股溢价率，纯... | [查看](tableInfo/Bond_CBDerivNew.json) |
| `Bond_CBNotesIssue` | 央行票据发行 | 1.收录中国人民银行公开市场业务操作中，历次央行票据发行情况。 2.数据范围：2002-06-25 至今 3.信息... | [查看](tableInfo/Bond_CBNotesIssue.json) |
| `Bond_CBOMOStatW` | 周央行公开市场操作统计 | 1.统计每周央行公开市场操作中，央行票据的发行及到期情况、正回购及到期情况、逆回购及到期情况等，并提供“周资金净投... | [查看](tableInfo/Bond_CBOMOStatW.json) |
| `Bond_CBRepo` | 央行回购操作 | 1.收录中国人民银行公开市场业务操作中，每笔正回购及逆回购的操作情况。 2.数据范围：2000-01-04 至今 ... | [查看](tableInfo/Bond_CBRepo.json) |
| `Bond_CBSpotTrading` | 央行现券买卖操作 | 1.收录中国人民银行在公开市场业务操作中，每笔现券买卖的操作情况。 2.数据范围：2000-01-04 至今 3.... | [查看](tableInfo/Bond_CBSpotTrading.json) |
| `Bond_CBYCurveInfo` | 收益率曲线信息表 | 1.本表记录中债登收益率曲线编码的基本信息，及收益率曲线变更时段状态。 2.数据范围：2006-02-05 至今 ... | [查看](tableInfo/Bond_CBYCurveInfo.json) |
| `Bond_COMCreditGrading` | 债券相关机构信用评级 | 1.涵盖机构：债券发行人、债券担保人及银行评级。 2.主要内容：各评级机构公布的债券相关机构的信用评级数据，包括国... | [查看](tableInfo/Bond_COMCreditGrading.json) |
| `Bond_CRAsCreditRM` | 信用评级机构信用等级含义 | 1.内容说明：本表记录各信用评级机构的信用等级含义，包括：评级类型、信用级别与投资等级等； 2.数据范围：现有国内... | [查看](tableInfo/Bond_CRAsCreditRM.json) |
| `Bond_CSIBondIndicesQuote` | 中证债券指数行情 | 1.收录了中证债券系列指数的每日指数值、成交量以及修正久期、凸性等；包含中证全债指数，以及4只分年期指数（中证3债... | [查看](tableInfo/Bond_CSIBondIndicesQuote.json) |
| `Bond_CSIComponent` | 中证债券指数成份 | 1.收录了中证指数有限公司发布的中证债券指数的成份债券构成情况，包含成份债券的所有历史入选日期、删除日期以及成份标... | [查看](tableInfo/Bond_CSIComponent.json) |
| `Bond_CallPutInfo` | 含权债回售赎回情况 | 1.收录非可转换债券含权债的含权行权情况，主要包含：发行人赎回权、利息递延权、上调票面利率选择权、持有人回售权、提... | [查看](tableInfo/Bond_CallPutInfo.json) |
| `Bond_CashFlow` | 债券现金流 | 1.记录全市场债券在每个付息兑付时的每百元利息、债权登记除权信息。 2.若违约、递延付息等日常公告明确说明下述情况... | [查看](tableInfo/Bond_CashFlow.json) |
| `Bond_ChangeMergeInfo` | 债券调换与合并 | 1.收录含有调换选择权、转换选择权以及合并权的债券的相关信息。 2.包括行权期间、行权操作日、最低操作金额、行权目... | [查看](tableInfo/Bond_ChangeMergeInfo.json) |
| `Bond_CirculationBBN` | 债券发行量_按券种(清算所) | 1.记录每月末各类债券的总体发行只数、发行量等信息。 2.该表中的数据为包含上海清算所登记托管的所有产品。 3.数... | [查看](tableInfo/Bond_CirculationBBN.json) |
| `Bond_Code` | 债券代码对照表 | 1.针对同一债券在不同市场的交易代码不统一的问题，设置了“统一内部编码”，与发行的债券对应，不随交易市场而改变。 ... | [查看](tableInfo/Bond_Code.json) |
| `Bond_CodeRelated` | 债券代码关联 | 1.收录同一债券对应同期债券关联代码等信息。 2.数据范围：1997年至今 3.信息来源：中债登、货币网、上交所、... | [查看](tableInfo/Bond_CodeRelated.json) |
| `Bond_ConBDBasicInfo` | 可转债基本信息 | 1.包含可转换债券的评级人、担保人、主承销商、债券要素、上市情况、以及发行公告中的转股和赎回信息等。 2.数据范围... | [查看](tableInfo/Bond_ConBDBasicInfo.json) |
| `Bond_ConBDCallInfo` | 可转债券赎回信息 | 1.收录可转债赎回信息，包括：赎回价，及触发条件等。 2.数据范围：1992-11-19 至今 3.信息来源：上交... | [查看](tableInfo/Bond_ConBDCallInfo.json) |
| `Bond_ConBDCallPutInfo` | 可转债赎回和回售 | 1.收录可转换债券回售或赎回的相关信息。 2.包括权利描述、执行原因、行权日期、回售/赎回价格、回售/赎回金额等信... | [查看](tableInfo/Bond_ConBDCallPutInfo.json) |
| `Bond_ConBDChangeInfo` | 可转债券修正信息 | 1.记录可转债券修正信息触发相关内容。 2.数据范围：2000-03-15 至今 3.信息来源：上交所、深交所、巨... | [查看](tableInfo/Bond_ConBDChangeInfo.json) |
| `Bond_ConBDConvertInfo` | 可转债转股及规模变动情况 | 1.记录可转换债券每次转股时的转股金额、转股数量、对应转股价、累计转股金额、剩余债券金额等信息，并展示因赎回、回售... | [查看](tableInfo/Bond_ConBDConvertInfo.json) |
| `Bond_ConBDConvertPrice` | 可转债转股价格变动 | 1.包含可转换债券转股价的历次变动情况。 2.数据范围：1992-11-01 至今 3.信息来源：上交所、深交所、... | [查看](tableInfo/Bond_ConBDConvertPrice.json) |
| `Bond_ConBDExchangeQuote` | 可转换债券行情 | 1.本表记录沪深交易所披露的可转债（含可交债）和三板市场披露的退债行情，其中：上交所提供的是上交所竞价平台的行情，... | [查看](tableInfo/Bond_ConBDExchangeQuote.json) |
| `Bond_ConBDHolder` | 可转债持有人持券情况 | 1.交易所市场可转换债券持有人的持券变动情况。 2.可通过可转债持有人的代码，得到持有人的其他信息。 3.数据范围... | [查看](tableInfo/Bond_ConBDHolder.json) |
| `Bond_ConBDIssue` | 可转债发行信息 | 1.包含可转换债券的发行要素、发债担保、承销情况、网下配售、网上发行、发行结果、上市情况、主要财务指标预测等信息。... | [查看](tableInfo/Bond_ConBDIssue.json) |
| `Bond_ConBDIssueAttach` | 可转债发行信息附表 | 1.包含可转换债券发行过程中，涉及收款账号、发行方式等信息。 2.数据范围：1991-08-11 至今 3.信息来... | [查看](tableInfo/Bond_ConBDIssueAttach.json) |
| `Bond_ConBDIssueProject` | 可转债发行预案 | 1.该表包含上市公司发行可转换债券的发行预案信息。 2.该表收录了所有可转换债券的发行预案信息，其中尚未实施的预案... | [查看](tableInfo/Bond_ConBDIssueProject.json) |
| `Bond_ConBDIssueTerm` | 可转债发行条款 | 1.包含可转换债券在招募说明书中列示的各类发行条款。 2.数据范围：1992-11-01 至今 3.信息来源：上交... | [查看](tableInfo/Bond_ConBDIssueTerm.json) |
| `Bond_ConBDPutInfo` | 可转债券回售信息 | 1.收录可转债回售信息，包括：回售价，及触发条件等。 2.数据范围：2002-12-13 至今 3.信息来源：上交... | [查看](tableInfo/Bond_ConBDPutInfo.json) |
| `Bond_ConceptNature` | 债券概念分类表 | 1.内容说明：本表记录债券概念分类、涵盖市场上热门分类，如绿色债、金融债、城投债、城投债各类细分。还涵盖发改委专项... | [查看](tableInfo/Bond_ConceptNature.json) |
| `Bond_DCMCardinalRate` | 债务融资工具发行指导利率 | 1.收录每周，非金融企业债务融资工具定价估值。 2.数据范围：2010-06-07- 至今 3.信息来源：中国银行... | [查看](tableInfo/Bond_DCMCardinalRate.json) |
| `Bond_DealerInfo` | 交易商信息表 | 1.介绍上交所固定收益平台交易商、上交所三方回购投资者适当性备案信息以及深圳证券交易所交易商。 2.数据范围：20... | [查看](tableInfo/Bond_DealerInfo.json) |
| `Bond_Default` | 债券违约信息 | 1.记录债券违约的相关信息。 2.数据范围：2014-03-28 至今 3.信息来源：中债登、货币网、上清所、上交... | [查看](tableInfo/Bond_Default.json) |
| `Bond_DepositBBN` | 债券托管量_按券种(清算所) | 1.反映上海清算所各类债券的托管情况。 2.该表中的数据为包含上海清算所登记托管的所有产品。 3.数据范围：201... | [查看](tableInfo/Bond_DepositBBN.json) |
| `Bond_Deriv` | 债券基础衍生指标 | 1.收录（除ABS、永续债）外所有类型债券基于债券行情（银行间市场、沪深交易所竞价系统、上交所固定收益平台、深交所... | [查看](tableInfo/Bond_Deriv.json) |
| `Bond_EmbeddedCashFlow` | 含权债券现金流表 | 1.内容说明：该表包含（除ABS、ABN外）所有含回售、赎回等权利的债券，在存续期内约定行权条件下的现金流数据。 ... | [查看](tableInfo/Bond_EmbeddedCashFlow.json) |
| `Bond_EmbeddedDeriv` | 含权债券衍生指标 | 1.收录（除ABS）外所有含回售、赎回等约定权利债券基于债券行情（银行间市场、沪深交易所竞价系统、上交所固定收益平... | [查看](tableInfo/Bond_EmbeddedDeriv.json) |
| `Bond_ExchangeQuote` | 交易所债券行情 | 1.内容说明：包含目前在交易所交易的债券（可转债、回购除外）的行情信息。 2.提供根据当天行情计算的净价、全价、均... | [查看](tableInfo/Bond_ExchangeQuote.json) |
| `Bond_ExchangeQuoteFI` | 交易所固收平台债券行情 | 1.内容说明：提供根据当天行情计算的净价、全价、均价、涨跌幅、振幅、换手率、到期收益率、麦氏久期、修正久期、凸度、... | [查看](tableInfo/Bond_ExchangeQuoteFI.json) |
| `Bond_FRNRefRate` | 浮息债基准利率表 | 1.记录所有浮动利率计息基准每日数据 2.数据范围：1987-01-02 至今 3.信息来源：人民银行、货币网等 | [查看](tableInfo/Bond_FRNRefRate.json) |
| `Bond_FloatCashFlow` | 债券现金流历次变动表 | 1.该表包含（除ABS、ABN外）所有债券存续期内，按时间序列历次发生变化时的现金流。包括但不限于：初始发行时理论... | [查看](tableInfo/Bond_FloatCashFlow.json) |
| `Bond_GradeCuListSt` | 评级客户名单统计 | 1.记录各大评级公司定期统计并发布债务融资时信用评级的企业名单。 2.数据范围：2006-01-06 至今 3.信... | [查看](tableInfo/Bond_GradeCuListSt.json) |
| `Bond_Guarantor` | 债券担保人 | 1.内容说明：收录债券担保机构的名称、性质、担保方式、担保期限、以及担保函内容等。 2.ABS内部增信由基础资产提... | [查看](tableInfo/Bond_Guarantor.json) |
| `Bond_Guarantor_Add` | 债券担保人_附表 | 1.内容说明：收录债券担保方式(ABS内部增信为常量值大于等于3000的部分)、担保物类型、担保物初始价值、担保物... | [查看](tableInfo/Bond_Guarantor_Add.json) |
| `Bond_HoldDepositBN` | 主要产品持有托管量_按投资者(清算所) | 1.反映上海清算所不同投资者投资各类债券明细情况。 2.该表中的数据为包含上海清算所登记托管的所有产品。 3.数据... | [查看](tableInfo/Bond_HoldDepositBN.json) |
| `Bond_HolderMeetingA` | 债券持有人大会附表 | 1.内容说明：本表记录债券持有人大会的召集人和详细的议案情况以及议案是否通过等信息。    本表通过内部代码和首次... | [查看](tableInfo/Bond_HolderMeetingA.json) |
| `Bond_HolderMeetingM` | 债券持有人大会主表 | 1.内容说明：本表记录债券持有人大会的通知，变更通知，决议等信息，包含召会议召开时间，地点，召开方式，决议时间等信... | [查看](tableInfo/Bond_HolderMeetingM.json) |
| `Bond_HonourBBn` | 债券兑付金额_按券种(清算所) | 1.记录每月末各类债券的提前兑付、到期兑付、利息支付等信息。 2.该表中的数据为包含上海清算所登记托管的所有产品。... | [查看](tableInfo/Bond_HonourBBn.json) |
| `Bond_IBMember` | 银行间市场交易会员 | 1.介绍参与银行间市场的交易会员信息，包含机构和基金。 2.数据范围：2015-04-02 至今 3.信息来源：中... | [查看](tableInfo/Bond_IBMember.json) |
| `Bond_IBORStat` | 银行间同业拆借统计 | 1.收录中国人民银行发布的CHIBOR月交易统计数据，以及香港金融管理局发布的HIBOR月统计数据。 2.数据范围... | [查看](tableInfo/Bond_IBORStat.json) |
| `Bond_IBSettMemberInfo` | 银行间结算成员情况 | 1.收录银行间市场的结算成员的基本信息。 2.银行间成员类型包括柜台交易市场成员、结算代理成员、一级交易商、双边报... | [查看](tableInfo/Bond_IBSettMemberInfo.json) |
| `Bond_IRS` | 人民币利率互换保证券 | 1.记录银行间市场中人民币利率互换保证券的基本资料，包括折扣率、到期日、集中度上线，上海清算所每月发布一次最新有效... | [查看](tableInfo/Bond_IRS.json) |
| `Bond_IncOrDecHold` | 债券增减持情况表 | 1.内容说明：本表收录控股股东及实控人增减持可转换债券的减持数量、减持比例等。 2.数据范围：2003-12-17... | [查看](tableInfo/Bond_IncOrDecHold.json) |
| `Bond_IndexBasicInfo` | 债券指数概况 | 1.收录了市场上主要债券指数的基本情况，包括指数类别、指数名称、成份证券类别、发布机构、发布日期、基期基点、成份证... | [查看](tableInfo/Bond_IndexBasicInfo.json) |
| `Bond_IndexComponent` | 债券指数成份 | 1.收录了市场上主要债券指数的成份债券构成情况，包含成份债券的所有历史入选日期、删除日期以及成份标志等信息。 2.... | [查看](tableInfo/Bond_IndexComponent.json) |
| `Bond_InstalRedempPrin` | 分期兑付本金表 | 1.内容说明：记录债券提前分期还本的类型及债券还本比例值，其中ABS因为不确定未来还本计划，所以生成比例和会存在不... | [查看](tableInfo/Bond_InstalRedempPrin.json) |
| `Bond_IntRedInfoN` | 债券付息兑付新表 | 1.涵盖全部债券，如ABS、ABN、可转债、私募债，全部付息兑付类型，如一次性还本、提前还本、分期还本等。 2.本... | [查看](tableInfo/Bond_IntRedInfoN.json) |
| `Bond_IntRedInfoPL` | 债券付息兑付(理论) | 1.内容说明：目前仅包含债券初始发行文件公布的未来付息和兑付情况（ABS和ABN除外） 2.数据范围：1987-0... | [查看](tableInfo/Bond_IntRedInfoPL.json) |
| `Bond_InterestRate` | 债券利率变动 | 1.记录固定利率债券、浮动利率债券每个利息支付期间的利率情况，包括分段计息的具体利率。 2.数据范围：1981-7... | [查看](tableInfo/Bond_InterestRate.json) |
| `Bond_Issue` | 债券发行与上市 | 1.记录债券（可转换债券、交易所ABS除外）在不同市场上的发行和上市信息。 2.同一债券若在多个市场上市，将对应多... | [查看](tableInfo/Bond_Issue.json) |
| `Bond_IssueNew` | 债券发行上市与增发 | 1.收录债券（可转换债券除外）首次发行、增发的基本信息、发行规模、认购单位和数量等信息。 2.数据范围：1981-... | [查看](tableInfo/Bond_IssueNew.json) |
| `Bond_IssueNewAttach` | 债券发行与增发附表 | 1.收录债券（可转换债券除外）发行过程涉及的细节信息。 2.数据范围：2019-12-05至今 3.信息来源：中债... | [查看](tableInfo/Bond_IssueNewAttach.json) |
| `Bond_IssueProject` | 债券发行预案 | 1.收录债券（不包括可转换债券）的发行预案信息。 2.对于上市公司的发行预案，该表仅收录股东大会尚未表决或未通过的... | [查看](tableInfo/Bond_IssueProject.json) |
| `Bond_IssueRegInfo` | 债券发行登记注册信息 | 1.记录债券发行时，在中国银行间交易商协会登记注册的相关信息同时还包含了同业存单的发行计划。 2.数据范围：200... | [查看](tableInfo/Bond_IssueRegInfo.json) |
| `Bond_IssueTerm` | 债券发行条款表 | 1.记录所有债券（除可转债）的发行条款信息，包含含权条款、利息条款、支付机制说明、提前还本条款。 2.数据范围：1... | [查看](tableInfo/Bond_IssueTerm.json) |
| `Bond_IssuerCreditLine` | 债券发行人授信情况 | 1.反映银行等机构给予债券发行人的授信额度情况。 2.包括授信额度、授信说明、使用情况等。 3.数据范围：2005... | [查看](tableInfo/Bond_IssuerCreditLine.json) |
| `Bond_LCBondsIssuePlan` | 上市公司债券发行计划 | 1.收录上市公司对公司债、企业债、短期融资券、金融债券等各类债券的计划发行规模、计划发行年限、发行进程等。 2.数... | [查看](tableInfo/Bond_LCBondsIssuePlan.json) |
| `Bond_MoneyMktCode` | 货币市场代码表 | 1.内容说明：本表记录银行间和交易所货币市场证券编码和基本信息 2.数据范围：1995年至今 3.信息来源：上交所... | [查看](tableInfo/Bond_MoneyMktCode.json) |
| `Bond_Nature` | 债券多维度分类表 | 1.内容说明：记录债券各个官方分类，包含交易所分类，中债分类，外汇交易所中新分类，清算所分类，交易商协会分类，聚源... | [查看](tableInfo/Bond_Nature.json) |
| `Bond_NotTextAnnounce` | 债券公告非文本 | 1.记录债券的发行公告、募集说明书、上市公告书等公告原文，公司发行可转换债券的可转换债券募集说明书、可转换债券上市... | [查看](tableInfo/Bond_NotTextAnnounce.json) |
| `Bond_NotTextAttach` | 债券公告非文本附表 | 1.内容说明：本表为Bond_NotTextAnnounce的附表，用于存放Bond_NotTextAnnounc... | [查看](tableInfo/Bond_NotTextAttach.json) |
| `Bond_NoteInfo` | 票据基本信息表 | 内容说明：记录票据的票面金额、出票日期、出票人等基本信息 数据范围：2019年开始 信息来源：目前维护标准化票据的... | [查看](tableInfo/Bond_NoteInfo.json) |
| `Bond_NoteInfoA` | 票据基本信息附表 | 内容说明：票据基本信息附表，记录票据其他的基本信息，如持票人、是否已贴现、贴现人等数据 数据范围：2019年开始 ... | [查看](tableInfo/Bond_NoteInfoA.json) |
| `Bond_OTCQuote` | 柜台报价情况 | 1.信息来源：中央国债登记结算有限责任公司。 2.收录柜台交易市场上，每个承办银行在每个交易日对柜台交易债券的报价... | [查看](tableInfo/Bond_OTCQuote.json) |
| `Bond_OTCTransaction` | 柜台交易情况 | 1.信息来源：中央国债登记结算有限责任公司。 2.收录柜台交易市场上，每个承办银行在每个交易日的债券买入金额、卖出... | [查看](tableInfo/Bond_OTCTransaction.json) |
| `Bond_OtherIBOR` | 主要拆借市场加权利率 | 1.收录SHIBOR、LIBOR、HIBOR、SIBOR、EURIBOR、TIBOR、SOFR等主要拆借市场的日拆... | [查看](tableInfo/Bond_OtherIBOR.json) |
| `Bond_PreIsuue` | 债券预发行 | 1.内容说明：本表记录债券预发行相关信息，主要包括国债 2.数据范围：2013-10-8至今 3.信息来源：上交所 | [查看](tableInfo/Bond_PreIsuue.json) |
| `Bond_PreIsuueQuote` | 债券预发行行情 | 1.内容说明：本表记录国债预发行行情信息 2.数据范围：2013-10-10至今 3.信息来源：上交所 | [查看](tableInfo/Bond_PreIsuueQuote.json) |
| `Bond_RFundsUseAttach` | 债券募集资金用途附表 | 1.发行债券所得募集资金用途的分类情况。 2.数据范围：1992-11-01至今 3.信息来源：募集说明书以及募集... | [查看](tableInfo/Bond_RFundsUseAttach.json) |
| `Bond_RMBInterestRate` | 人民币利率表 | 1.反映历年来各项人民币利率的变动情况。 2.包含活期存款利率、定期存款利率、长期贷款利率、短期贷款利率、个人住房... | [查看](tableInfo/Bond_RMBInterestRate.json) |
| `Bond_RaiseFundsUse` | 债券募集资金用途 | 1.发行债券所得募集资金的项目投资情况以及改投状况。 2.数据范围：1992-11-01至今 3.信息来源：募集说... | [查看](tableInfo/Bond_RaiseFundsUse.json) |
| `Bond_RegInfo` | 债券注册信息 | 1.收录债券的注册进度信息，主要包含券种有小公募、私募、交易所ABS、企业债、交易商协会注册的品种。 2.数据范围... | [查看](tableInfo/Bond_RegInfo.json) |
| `Bond_RegInfoAttach` | 债券注册信息附表 | 1.本表为债券注册信息(Bond_RegInfo)的附表，通过RID进行关联使用，包含发行人代码、涉及债券、承销商... | [查看](tableInfo/Bond_RegInfoAttach.json) |
| `Bond_RelatedInstitutions` | 债券机构基本信息 | 1.收录债券各类相关机构的基本信息。 2.机构包括承销商、保荐人、国际协调人、发行人法律顾问、承销商法律顾问、会计... | [查看](tableInfo/Bond_RelatedInstitutions.json) |
| `Bond_RepoConversionStd` | 债券回购折算比率表 | 1.信息来源：中国证券登记结算公司。 2.收录中国证券登记结算公司根据《标准券折算率管理办法》，每周计算（或修正）... | [查看](tableInfo/Bond_RepoConversionStd.json) |
| `Bond_RepoDiscRate` | 债券回购折扣率表 | 1.收录各类回购质押券、所属篮子、折扣率等数据 2.数据范围：2018-5-23 至今 3.信息来源：上交所，深交... | [查看](tableInfo/Bond_RepoDiscRate.json) |
| `Bond_SAPYieldCurve` | 全球债券收益率曲线 | 1. 收录全球债券收益率曲线的点信息。 2.本表包括多种预测步长的曲线数据。 3.数据范围：1974-09-24 ... | [查看](tableInfo/Bond_SAPYieldCurve.json) |
| `Bond_SBFC_CF` | 标准债券远期转换因子 | 1.该表记录标准债券远期转换因子 2.数据范围：2015-04-06 至今 3.信息来源：货币网 | [查看](tableInfo/Bond_SBFC_CF.json) |
| `Bond_SBFC_Info` | 标准债券远期合约基本信息 | 1.记录标准债券远期合约的基本信息。 2.数据范围：2015-04-06 至今 3.信息来源：货币网 | [查看](tableInfo/Bond_SBFC_Info.json) |
| `Bond_SCHIndexCMPT` | 上清所指数样本券及构成 | 1.收录了上清所发布的银行间信用债综合指数(SCH00100)、银行间高等级信用债指数(SCH00200)、银行间... | [查看](tableInfo/Bond_SCHIndexCMPT.json) |
| `Bond_SCHIndexQuote` | 上清所指数行情 | 1.收录了上清所发布的银行间信用债综合指数(SCH00100)、银行间高等级信用债指数(SCH00200)、银行间... | [查看](tableInfo/Bond_SCHIndexQuote.json) |
| `Bond_SHCHValuation` | 上清所债券估值 | 1.信息来源：银行间市场清算所股份有限公司。 2.收录清算所官方公布的估值数据，包含银行间和交易所债券。 3.包含... | [查看](tableInfo/Bond_SHCHValuation.json) |
| `Bond_SHCHYieldCurve` | 上清所债券收益率曲线 | 1.记录上海清算所发布的收益率曲线信息。 2.数据范围：2011-06-30 至今 3.信息来源：上清所 | [查看](tableInfo/Bond_SHCHYieldCurve.json) |
| `Bond_Size` | 债券规模 | 1.记录全市场债券的规模构成及规模变动情况，包括债券行权、转股、提前还本等。 2.数据范围：1981-6-30 至... | [查看](tableInfo/Bond_Size.json) |
| `Bond_SpecialNotice` | 债券特别提示 | 1.收录所有债券的各类提示信息，如赎回登记日、转股价调整日等，包括当日提示和未来提示 2.数据范围：1993-06... | [查看](tableInfo/Bond_SpecialNotice.json) |
| `Bond_SystemConst` | 债券项目编码表 | 本表目前主要用于对债券分类的编码和资产支持证券资产池的总体信息和分布提供标准化的常量编码信息。 | [查看](tableInfo/Bond_SystemConst.json) |
| `Bond_TextAnnounce` | 债券公告文本表 | 1.记录债券的发行公告、募集说明书、上市公告书等公告原文，公司发行可转换债券的可转换债券募集说明书、可转换债券上市... | [查看](tableInfo/Bond_TextAnnounce.json) |
| `Bond_TradeTChange` | 债券交易方式变动 | 1.记录不同的债券类型在相关市场的交易方式及变动情况。 2.数据范围：1990-12-19 至今 3.信息来源：上... | [查看](tableInfo/Bond_TradeTChange.json) |
| `Bond_UnderWriter` | 债券发行承销 | 1.收录各类债券的承销商、分销商的名称及机构编号等。 2.涵盖券种：可转换债券、企业债、金融债、资产支持证券等。 ... | [查看](tableInfo/Bond_UnderWriter.json) |

## CS - 市场统计/异动

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `CS_ForeignHoldingSt` | 外资持股统计 | 内容说明：境外投资者持股统计，包含持股总数、持股比例，境外投资者指QFII/RQFII/深股通/全球存托凭证跨境转... | [查看](tableInfo/CS_ForeignHoldingSt.json) |
| `CS_IntensityTrendADJ` | 境内股票强弱与趋向技术指标(后复权) | 内容说明：收录境内股票上市之日起基于日、周、月、季、半年、年K线后复权行情衍生计算的趋向、强弱等大类技术指标 数据... | [查看](tableInfo/CS_IntensityTrendADJ.json) |
| `CS_StockFluctuAttach` | 境内股票交易公开营业部信息 | 内容说明：记录沪深京交易所披露的股票在交易异常波动期间证券公司交易席位的公开买卖信息 数据范围：1997-02至今... | [查看](tableInfo/CS_StockFluctuAttach.json) |
| `CS_StockFluctuation` | 境内股票交易公开信息表 | 内容说明：记录沪深京交易所披露的股票在异常波动期间的公开交易信息，包括异常交易日期、涨跌幅、涨跌幅偏离值、振幅、换... | [查看](tableInfo/CS_StockFluctuation.json) |
| `CS_StockPatterns` | 股票技术形态表 | 内容说明：收录股票从最近一个交易日往前追溯一段时期的行情表现和技术形态表现，包括近1周、近1月、近3月、近半年、近... | [查看](tableInfo/CS_StockPatterns.json) |
| `CS_SupplyChainRela` | 上市公司供应链关系表 | 1.内容说明：收录公司的供应商、客户、潜在供应商、潜在客户等供应链关系信息。 2.数据范围：境内上市公司 3.信息... | [查看](tableInfo/CS_SupplyChainRela.json) |

## CT - 行业/概念/分类

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `CT_Industry` | 行业表 | 本表收录行业名称、代码、板块等基本信息。 | [查看](tableInfo/CT_Industry.json) |
| `CT_IndustryType` | 行业类别表 | 本表收录不同行业分类标准下，各行业的行业代码、行业名称、行业级别等。 | [查看](tableInfo/CT_IndustryType.json) |
| `CT_Keywords` | 系统关键词表 | 本表收录证券新闻等中用到的关键词 | [查看](tableInfo/CT_Keywords.json) |
| `CT_Personal` | 人员表 | 1、表说明：本表收录与证券市场相关人员的基本信息，目前维护上海证券交易所、深圳证券交易所、北京证券交易所公布的发行... | [查看](tableInfo/CT_Personal.json) |
| `CT_Product` | 产品表 | 本表收录各种产品名称、代码、分类以及所属行业的情况。 | [查看](tableInfo/CT_Product.json) |
| `CT_SystemConst` | 系统常量表 | 本表收录数据库中各种常量值的具体分类和常量名称描述。 | [查看](tableInfo/CT_SystemConst.json) |

## DZ - 公告/资讯

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `DZ_CodeRelationship` | 公司代码关联表 | 收录国内上市公司对应的港股等关联代码的信息。包括：所属市场、 关联代码内部编码、关联代码公司代码等内容。 | [查看](tableInfo/DZ_CodeRelationship.json) |
| `DZ_DailyQuote` | 日行情表 | 1.内容说明：收录股票、债券（不包含银行间交易的债券）、基金、指数每个交易日收盘行情数据，包括昨收盘、今开盘、最高... | [查看](tableInfo/DZ_DailyQuote.json) |
| `DZ_NotTextAnnouncement` | 公司公告原文非文本 | 1.内容说明：公司首次发行股票的招股说明书、招股意向书、上市公告书，公司增发新股招股说明书、增发新股招股意向书、增... | [查看](tableInfo/DZ_NotTextAnnouncement.json) |

## ED - 经济数据/宏观

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `ED_BOCExchangeQuoteRT` | 中国银行外汇实时牌价 | 1.收录中国银行发布的外汇实时价格，包括现汇买入价、现钞买入价、现汇卖出价、现钞卖出价、基准价、中行折算价 2.数... | [查看](tableInfo/ED_BOCExchangeQuoteRT.json) |
| `ED_BOCForexQuote` | 中国银行外汇牌价 | 1.收录中国银行公布的当天首笔外汇价格，包括现汇买入价、现钞买入价、卖出价、基准价等 2.数据范围：1994年8月... | [查看](tableInfo/ED_BOCForexQuote.json) |
| `ED_ExchangeRateRMBtoUSD` | 各种货币对美元折算率 | 1.收录国际主要货币和美元的汇率，包括港元、人民币、欧元、英镑、日元等100多个币种与美元的汇率 2.数据范围：2... | [查看](tableInfo/ED_ExchangeRateRMBtoUSD.json) |
| `ED_LawsAndStatutes` | 法律法规 | 1.收录国家行政机关披露的政策法律法规或公告、通知类信息。 2.数据范围：2002-至今 | [查看](tableInfo/ED_LawsAndStatutes.json) |
| `ED_RMBBaseEXchangeRate` | 人民币基准汇价 | 1.内容说明：收录人民币对其他主要币种的基准汇价，包含中国外汇交易中心披露的人民币对100单位外币的中间价的期初期... | [查看](tableInfo/ED_RMBBaseEXchangeRate.json) |

## FM - 货币/利率

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `FM_FundCMPFSize` | 基金业协会公募基金规模 | 1.本表记录基金管理公司管理公募基金的基金数量、基金份额和基金净值等统计情况。 2.数据范围：2013.1-至今 ... | [查看](tableInfo/FM_FundCMPFSize.json) |
| `FM_FundCMSRank` | 基金公司管理规模排名 | 1.收录每季度末，不同细分项下基金公司的管理规模排名情况（从2015年第四季度末开始只披露部分排名）。 2.数据范... | [查看](tableInfo/FM_FundCMSRank.json) |
| `FM_FundCSMSSize` | 基金管理公司及其子公司专户业务规模 | 1.本表记录基金管理公司及其子公司专户业务的相关产品数量和资产规模等统计情况。 2.数据范围：2014.12-至今... | [查看](tableInfo/FM_FundCSMSSize.json) |
| `FM_PrRegSta` | 私募登记备案统计 | 1.收录在基金业协会已登记的私募基金管理人家数、基金数量、认缴规模和实缴规模等统计情况。 2.数据范围：2014.... | [查看](tableInfo/FM_PrRegSta.json) |
| `FM_StockTransactionFees` | 证券市场交易费率 | 1.信息来源：中国证监会、上海交易所、深圳交易所2.收录在深沪两市交易的A股、B股、基金、债券、债券回购、权证等品... | [查看](tableInfo/FM_StockTransactionFees.json) |
| `FM_TVOfAreaByBCNSH` | 交易额统计_地区_营业部所在地_沪市 | 1.以营业部所在地为统计口径，按地区营业部数量排名，收录每个月末上海交易所在各地区的证券交易金额情况。 2.数据范... | [查看](tableInfo/FM_TVOfAreaByBCNSH.json) |
| `FM_TVOfAreaByMNSH` | 交易额统计_地区_会员所在地_沪市 | 1.以会员所在地为统计口径，按地区会员数量排名，收录每个月末上海交易所在各地区的证券交易金额情况。 2.数据范围：... | [查看](tableInfo/FM_TVOfAreaByMNSH.json) |
| `FM_TVOfAreaSZ` | 交易额统计_地区_深市 | 1.收录每个月末深圳交易所在各地的证券交易情况，按地区交易总额排名。 2.数据范围：2002.12-至今 3.信息... | [查看](tableInfo/FM_TVOfAreaSZ.json) |
| `FM_TVOfBShareSH` | 交易额统计_B股券商_沪市 | 1.收录每个月末，各B股券商在上海交易所的证券交易情况，按B股交易总额排名。 2.数据范围：2002-至今 3.信... | [查看](tableInfo/FM_TVOfBShareSH.json) |
| `FM_TVOfBSpecialSeatSZ` | 交易额统计_B股特别席位和特许经纪_深市 | 1.收录每个月末，B股特别席位和特许经纪席位在深圳交易所的证券交易情况，按席位交易总额排名。 2.数据范围：200... | [查看](tableInfo/FM_TVOfBSpecialSeatSZ.json) |
| `FM_TVOfBusinessOffice` | 交易额统计_营业部_深沪 | 1.反映每年末各营业部的证券交易金额情况，按营业部的交易总额排名。 2.数据范围：1999.12-至今 3.信息来... | [查看](tableInfo/FM_TVOfBusinessOffice.json) |
| `FM_TVOfFundCorpSZ` | 交易额统计_基金管理公司_深市 | 1.反映每个月末，各基金公司在深圳交易所的证券交易情况，按基金公司交易总额排名。 2.数据范围：2004.1-20... | [查看](tableInfo/FM_TVOfFundCorpSZ.json) |
| `FM_TVOfMembers` | 交易额统计_会员_深沪 | 1.反映每个月末或年末，交易所会员的证券交易金额情况，按会员交易总额排名。 2.数据范围：1999.1-至今 3.... | [查看](tableInfo/FM_TVOfMembers.json) |

## FX - 外汇相关

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `FX_OfficialFX` | 各国官方汇率 | 1.收录香港金管局披露的官方外汇汇率数据、国际货币基金组织IMF和中国外汇交易中心CFETS公布的SDR（特别提款... | [查看](tableInfo/FX_OfficialFX.json) |

## Fut - 期货相关

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `Fut_CGBDeriv` | 国债期货衍生指标 | 1.内容说明：本表收录国债期货衍生指标，包括发票价格、基差、交割利息、IRR、CTD券等。 2.数据范围：2013... | [查看](tableInfo/Fut_CGBDeriv.json) |
| `Fut_ContractMain` | 期货合约 | 1.内容说明：本表收录国内外商品期货、货币期货、利率期货、股指期货和虚拟货币期货5大合约类型期货合约的基本信息，包... | [查看](tableInfo/Fut_ContractMain.json) |
| `Fut_ContractMapping` | 主力(连续)合约与月合约对应关系 | 1.内容说明：本表收录每个交易日各大交易所各品种主力(连续)合约与月合约的对应关系。 2.数据范围：1992年至今... | [查看](tableInfo/Fut_ContractMapping.json) |
| `Fut_ConversionFactors` | 期货交割转换因子 | 1.内容说明：本表收录国债期货交易的转换因子。可查询该期货的合约信息和转换债券的相关信息。包括票面利率(%)、转换... | [查看](tableInfo/Fut_ConversionFactors.json) |
| `Fut_DailyQuote` | 商品期货每日行情 | 1.内容说明：本表收录国内外各大交易所上市的商品期货以及国外交易所上市的金融期货的日收盘行情，包括高开低收、成交量... | [查看](tableInfo/Fut_DailyQuote.json) |
| `Fut_FutureIndicators` | 期货合约指标变动 | 1.内容说明：本表收录商品期货和金融期货合约中涉及的各类指标的历史变动数据，包括：最低交易保证金比率、合约乘数、最... | [查看](tableInfo/Fut_FutureIndicators.json) |
| `Fut_FuturesContract` | 期货品种 | 1.内容说明：本表收录国内外商品期货、货币期货、利率期货、股指期货和虚拟货币期货5大合约类型期货标准合约的基本信息... | [查看](tableInfo/Fut_FuturesContract.json) |
| `Fut_MemberInfo` | 期货会员资格 | 1.内容说明：本表收录中国金融期货交易所公布的会员资格变动情况。包括会员号、会员类型、会员标志、入选日期、取消日期... | [查看](tableInfo/Fut_MemberInfo.json) |
| `Fut_MemberRankByContract` | 期货会员交易排名_按交易合约 | 1.内容说明：本表收录国内期货交易所会员以交易合约为维度，日度的按照成交量统计、持买单量统计和持卖单量统计三种统计... | [查看](tableInfo/Fut_MemberRankByContract.json) |
| `Fut_Parameters` | 期货业务参数表 | 1.内容说明：本表收录上海期货交易所、上海国际能源交易中心、大连商品期货交易所、郑州商品期货交易所、中国金融期货交... | [查看](tableInfo/Fut_Parameters.json) |
| `Fut_QJIndexCW` | 千际商品指数成份及权重 | 1.收录了千际投资发布的全商品系列指数的成份构成涵盖的品种，以及该品种在对应指数中的权重配置数据等信息。 2.历史... | [查看](tableInfo/Fut_QJIndexCW.json) |
| `Fut_Statute` | 期货法规及提示 | 1.内容说明：本表收录历年出台的期货或股指期货的法律法规条例原文。包括法规类别为期货条例、合约挂牌、合约交割、最后... | [查看](tableInfo/Fut_Statute.json) |
| `Fut_TradeStat` | 期货交易统计 | 1.内容说明：本表收录上海期货交易所、大连商品交易所、郑州商品交易所、中国金融期货交易所在每个月末的期货成交量、成... | [查看](tableInfo/Fut_TradeStat.json) |
| `Fut_TradeStatByContract` | 期货交易统计_按交易合约 | 1.内容说明：本表收录国内各大交易所按交易合约统计的信息。包括期货成交量、成交额、持仓量等数据，数据统计期间为月和... | [查看](tableInfo/Fut_TradeStatByContract.json) |
| `Fut_TradingHours` | 国内期货交易时间表 | 1.内容说明：本表收录国内以日度和合约为维度的连续交易和非连续交易品种的各个交易时段的交易时间。 2.数据范围：1... | [查看](tableInfo/Fut_TradingHours.json) |
| `Fut_TradingQuote` | 金融期货每日行情 | 1.内容说明：本表收录股指期货、国债期货的日行情数据。包括高开低收、涨跌幅、持仓量、成交量、成交额、持仓量变化和基... | [查看](tableInfo/Fut_TradingQuote.json) |
| `Fut_WRStatByOption` | 期货仓单统计_按品种 | 1.内容说明：本表收录上海期货交易所、上海国际能源交易中心、大连商品交易所、郑州商品交易所公布的以品种为维度的日度... | [查看](tableInfo/Fut_WRStatByOption.json) |

## HK - 港股相关

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `HK_Dividend` | 港股分红 | 1.记录港股分红方案、数据以及日期安排等信息，包含主要字段有：股息期间、财政年度、是否分红、每股股息、送红股比例、... | [查看](tableInfo/HK_Dividend.json) |
| `HK_IndexCPsWeight` | 港股指数成份股权重 | 1.收录了在港股市场上发布的主要指数成份证券的权重信息，通过与港股证券主表进行关联，可以获取指数以及成份股的基本信... | [查看](tableInfo/HK_IndexCPsWeight.json) |
| `HK_IndexComponent` | 港股指数成份 | 1.收录了在港股市场上发布的主要指数的成份构成情况，包括成份证券的所有历史入选日期、删除日期以及成份标志等信息。 ... | [查看](tableInfo/HK_IndexComponent.json) |
| `HK_SecuCodeTable` | 港股证券交易代码表 | 1.内容说明：新建港股证券交易代码表，记录当前时点处于正常上市状态的港交所可交易券种的常用信息。 2.数据范围：无... | [查看](tableInfo/HK_SecuCodeTable.json) |
| `HK_SecuMain` | 港股证券主表 | 本表收录港股单个证券品种的简称、上市交易所等基础信息。 | [查看](tableInfo/HK_SecuMain.json) |
| `HK_ShareStru` | 港股股本结构 | 1.介绍港股的具体股本结构信息，包括股票面值、普通股、优先股、股本变动原因等内容。记录有港股股本历次变动的信息，和... | [查看](tableInfo/HK_ShareStru.json) |

## Index - 指数相关

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `Index_AnnClassifi` | 指数公告分类 | 1.根据聚源制定的最新公告分类标准，收录了指数类公告的具体分类信息，包括一级分类，二级分类，三级分类三个层级，可根... | [查看](tableInfo/Index_AnnClassifi.json) |
| `Index_DerivPercentile` | 指数衍生指标分位数 | 1.内容说明：本表记录A股、港股主要指数衍生指标的百分位，包括滚动市盈率、市净率等指标每天所处的历史分位情况；以及... | [查看](tableInfo/Index_DerivPercentile.json) |
| `Index_FinIndicator` | 指数财务指标 | 1.内容说明：本表记录主要A股、港股指数的财务分析衍生指标，包括净资产收益率、总资产净利率、销售净利率等指标。本表... | [查看](tableInfo/Index_FinIndicator.json) |
| `Index_NotTextAnnounce` | 指数公告非文本 | 1.收录了指数发布机构发布的指数编制和发布、指数编制方案、指数成份股调整、指数发布状态调整等公告的原文。 2.历史... | [查看](tableInfo/Index_NotTextAnnounce.json) |
| `Index_QuoteTecIndex` | 指数技术指标 | 1.内容说明：本表记录境内指数的技术指标，包括收盘价均线、EMA、MACD指数平滑异动平均、BBI多空指数、DMA... | [查看](tableInfo/Index_QuoteTecIndex.json) |
| `Index_ReleaseChanInfo` | 主要发布渠道指数信息 | 1.收录市场上主要指数发布渠道发布的指数的信息，包括证券代码、证券简称、发布状态等。 2.数据源：中证指数有限公司... | [查看](tableInfo/Index_ReleaseChanInfo.json) |
| `Index_TextAnnounce` | 指数公告文本 | 1.收录了指数发布机构发布的指数编制和发布、指数编制方案、指数成份股调整、指数发布状态调整等公告的文本。 2.数据... | [查看](tableInfo/Index_TextAnnounce.json) |

## JYDB - 系统表/元数据

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `JYDB_DeleteRec` | JYDB_删除表 | 本表记录各表删除记录的ID值 本表保留最近一个月数据记录 | [查看](tableInfo/JYDB_DeleteRec.json) |

## LC - 上市公司/股票相关

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `LC_7PercentChange` | 交易所日公开信息 | 1.收录交易所公布的，触发日涨跌幅偏离值达到7％、日价格振幅达到15%、日换手率达到20％、连续三个交易日内收盘价... | [查看](tableInfo/LC_7PercentChange.json) |
| `LC_AICRelAttach` | 一致行动人关系附表 | 1.内容说明: 收录根据上市公司在招投说明书、定期报告及临时公告中披露的一致行动人的每个人单独的详细信息。 2.数... | [查看](tableInfo/LC_AICRelAttach.json) |
| `LC_AICRelationship` | 一致行动人关系 | 1.内容说明: 收录根据上市公司在招投说明书、定期报告及临时公告中披露的一致行动人信息。 2.数据范围：2019年... | [查看](tableInfo/LC_AICRelationship.json) |
| `LC_AShareCDRTransRatio` | CDR与基础证券转换 | 1.内容说明：本表记录A股市场上市的中国存托凭证与其基础证券的转换比例、存托凭证份数、面值等信息。 2.数据范围：... | [查看](tableInfo/LC_AShareCDRTransRatio.json) |
| `LC_AShareIPO` | A股发行与上市 | 1.该表包括A股首次发行上市的明细情况。 2.中文名称带*的，表示该字段表述的信息当前已不再披露。 3.2016年... | [查看](tableInfo/LC_AShareIPO.json) |
| `LC_AShareIPO_Fee` | A股IPO费用关联表 | 1.收录IPO的发行费用以及募资类型，包括费用总额、承销费用、注册会计师费用、资产评估费用、土地评估费用、律师费用... | [查看](tableInfo/LC_AShareIPO_Fee.json) |
| `LC_ASharePlacement` | A股配股 | 1.收录A股历次配股预案及实施进展明细，包括预案有效期、配股价格区间、配股说明书、募集资金和配股交款日等内容。 2... | [查看](tableInfo/LC_ASharePlacement.json) |
| `LC_AShareSeasonedNewIssue` | A股增发 | 1.收录A股增发A股、B股增发A股、H股增发A股等的明细情况，包括历次增发预案、进程日期、预案有效期、发行属性、发... | [查看](tableInfo/LC_AShareSeasonedNewIssue.json) |
| `LC_ActualController` | 公司实际控制人 | 1.收录根据上市公司在招投说明书、定期报告、及临时公告中披露的实际控制人结构图判断的上市公司实际控制人信息。 2.... | [查看](tableInfo/LC_ActualController.json) |
| `LC_AddressChange` | 公司地址变更明细 | 1.收录上市公司公告中披露的公司地址变更等重大事项描述说明。 2.数据范围：2005-至今 3.信息来源：上市公司公告 | [查看](tableInfo/LC_AddressChange.json) |
| `LC_AnalyseReport` | 公司研究报告 | 1.收录各调研机构对上市公司的分析研究报告。 2.数据范围：2001-至今 | [查看](tableInfo/LC_AnalyseReport.json) |
| `LC_AnnClassifi` | 股票公告分类 | 1.根据聚源制定的最新公告分类标准，收录股票类公告的具体分类信息，包括一级分类，二级分类，三级分类三个层级，可根据... | [查看](tableInfo/LC_AnnClassifi.json) |
| `LC_AnnounceStru` | 公告分类指引表 | 收录聚源最新制定的公告分类标准。三级公告类别隶属于二级公告类别，二级公告类别隶属于一级公告类别，一级分类主要分为股... | [查看](tableInfo/LC_AnnounceStru.json) |
| `LC_Announcement` | 公司公告原文 | 1.公司首次发行股票的招股说明书、招股意向书、上市公告书，公司增发新股招股说明书、增发新股招股意向书、增发新股上市... | [查看](tableInfo/LC_Announcement.json) |
| `LC_AnnouncementInfo` | 公司公告(不含原文) | 1.公司首次发行股票的招股说明书、招股意向书、上市公告书，公司增发新股招股说明书、增发新股招股意向书、增发新股上市... | [查看](tableInfo/LC_AnnouncementInfo.json) |
| `LC_AppoitmentSecu` | 约定购回式证券交易 | 1.记录投资者以融资为目的的交易行为，符合条件的客户以约定价格向其指定交易的证券公司卖出标的证券（即\初始交易\"... | [查看](tableInfo/LC_AppoitmentSecu.json) |
| `LC_AreaCode` | 国家城市代码表 | 内容说明：本表收录国家及地区的数据，及中国省级，市级，区县及城镇级的行政区域相关的数据。 数据来源：ISO组织及国... | [查看](tableInfo/LC_AreaCode.json) |
| `LC_AreaRelatingInfo` | 国家城市相关信息 | 内容说明：本表以国家城市代码表(LC_AreaCode)中，各个国家、城市、地区为中心，记录该国家、城市、地区的一... | [查看](tableInfo/LC_AreaRelatingInfo.json) |
| `LC_AshareIPOBid` | A股询价明细 | 1.收录新上市A股询价、网下配售明细，包括投资者名称、配售对象名称、申报价格、拟申购股数、总实际申购股数和总获配售... | [查看](tableInfo/LC_AshareIPOBid.json) |
| `LC_AshareIssueCostPlaned` | A股拟发行费用 | 1.收录即将上市的A股的招股意向书中的拟发行费用，包括费用总额、承销费用、承销费用比例、保荐费用、注册会计师费用等... | [查看](tableInfo/LC_AshareIssueCostPlaned.json) |
| `LC_AshareSNIBid` | A股增发询价明细 | 1.股票增发是指上市公司通过指定投资者（如大股东或机构投资者）或全部投资者额外发行股份募集资金的融资方式。该表收录... | [查看](tableInfo/LC_AshareSNIBid.json) |
| `LC_AssetTCLD` | 公司资产托管承包租赁及赠与明细 | 1.公司资产托管承包租赁及赠与等重大事项，包括事件主体/交易对象名称、企业编号、与上市公司关联关系，涉及金额等指标... | [查看](tableInfo/LC_AssetTCLD.json) |
| `LC_AuditOpinion` | 公司历年审计意见 | 1.收录中介机构对公司季度、半年度、年度经营情况的评价，区分审计单位、审计意见类型，本表涵盖了公司招股以来的历次纪... | [查看](tableInfo/LC_AuditOpinion.json) |
| `LC_BShareIPO` | B股首次发行与上市 | 1.收录B股首次发行上市的明细情况，包括发行概况、配售日期、承配缴款日、承销日期、发行结果等内容。 2.数据范围：... | [查看](tableInfo/LC_BShareIPO.json) |
| `LC_BSharePlacement` | B股配股 | 1.B股历次配股预案及实施进展明细，包括预案、预案有效期、配股价格区间、决案、配股权证交易起始日等内容。 2.数据... | [查看](tableInfo/LC_BSharePlacement.json) |
| `LC_BShareSeasonedNewIssue` | B股增发 | 1.收录A股增发B股、B股增发B股、A股增发H股等的明细情况，包括历次增发预案及实施进展。 2.数据范围：1995... | [查看](tableInfo/LC_BShareSeasonedNewIssue.json) |
| `LC_BalanceSheetAll` | 资产负债表_新会计准则 | 1.反映企业依据2007年新会计准则在年报、中报、季报中披露的资产负债表数据；并依据新旧会计准则的科目对应关系，收... | [查看](tableInfo/LC_BalanceSheetAll.json) |
| `LC_BalanceSheetPSCN` | 资产负债表附注_中国会计准则 | 1.内容说明 1.1描述新会计准则下，上市公司、发债人资产负债表附注的明细情况。 1.2对于公告原文披露的项目名称... | [查看](tableInfo/LC_BalanceSheetPSCN.json) |
| `LC_BankIncomeExpense` | 银行收入支出类细分指标 | 1.本表记录银行利息收入及支出，手续费及佣金收入及支出，业务以及管理费等细分项。 2.数据范围：2011-12-3... | [查看](tableInfo/LC_BankIncomeExpense.json) |
| `LC_BankIndiConst` | 银行财务附注常量表 | 本表记录银行收入支出类细分指标LC_BankIncomeExpense、银行贷款类细分指标LC_BankLoan、... | [查看](tableInfo/LC_BankIndiConst.json) |
| `LC_BankLoan` | 银行贷款类细分指标 | 1.本表记录银行各类贷款余额，包括按产品分、按行业分、按地区、按期限分等细项。 2.数据范围：2011-12-31... | [查看](tableInfo/LC_BankLoan.json) |
| `LC_BlockTrading` | 大宗交易成交明细 | 1.内容说明：本表收录大宗交易每日成交信息，包括成交价，成交量，成交金额，以及买入营业部和卖出营业部等信息； 2.... | [查看](tableInfo/LC_BlockTrading.json) |
| `LC_BlockTradingIntent` | 大宗交易意向申报 | 1.收录交易所公布的大宗交易意向申报数据，包括买卖方向、价格、数量等。 2.数据范围：2005-06-27至今 3... | [查看](tableInfo/LC_BlockTradingIntent.json) |
| `LC_Business` | 公司经营范围与行业变更 | 1.收录上市公司、发债公司的经营范围（包括主营和兼营）以及涉足行业情况。 2.信息来源：公开转让说明书、董事会决议... | [查看](tableInfo/LC_Business.json) |
| `LC_Buyback` | 股份回购 | 1.介绍上市公司(包含科创板)发生股份回购的相关方案信息，包括股份类别、首次信息发布日期、回购协议签署日、股份被回... | [查看](tableInfo/LC_Buyback.json) |
| `LC_BuybackAttach` | 股份回购关联表 | 1.补充上市公司(包含科创板)发生股份回购的相关信息，包括本次回购数量、累计回购数量、本次回购资金和累计回购数量等... | [查看](tableInfo/LC_BuybackAttach.json) |
| `LC_COConcept` | 概念所属公司表 | 记录A股上市公司所属概念信息。 | [查看](tableInfo/LC_COConcept.json) |
| `LC_CSIIndusPE` | 行业市盈率_中证发布 | 1.收录中证指数有限公司披露的沪深A股、证监会行业、中证行业以及板块的静态市盈率、动态市盈率、市净率和股息率数据。... | [查看](tableInfo/LC_CSIIndusPE.json) |
| `LC_CSIIndustry` | 公司行业分类_中证发布 | 1.收录了证券的中证行业分类及证监会行业分类（中证披露）等，中证行业分类涵盖四级分类，证监会行业分类涵盖二级分类。... | [查看](tableInfo/LC_CSIIndustry.json) |
| `LC_CapitalInvest` | 资金投向说明 | 1.公司自有资金、通过发行新股、增发新股、配股等方式所得募集资金的项目投资情况以及运用进展和改投状况。 2.数据范... | [查看](tableInfo/LC_CapitalInvest.json) |
| `LC_CashFlowStatementAll` | 现金流量表_新会计准则 | 1.反映企业依据2007年新会计准则在年报、中报、季报中披露的现金流量表数据；并依据新旧会计准则的科目对应关系，收... | [查看](tableInfo/LC_CashFlowStatementAll.json) |
| `LC_Certification` | 企业认定情况 | 收录企业各种资质认证情况，包括企业认定单位、企业认定类型、企业认定时间和认定取消时间等内容。 | [查看](tableInfo/LC_Certification.json) |
| `LC_CodeChange` | 证券代码变更对照 | 收录证券代码的历次变更情况，包括证券市场、代码定义、启用日期和停用日期等内容。 | [查看](tableInfo/LC_CodeChange.json) |
| `LC_CodeRelationship` | 公司代码关联表 | 收录国内上市公司对应的港股等关联代码的信息。包括：所属市场、 关联代码内部编码、关联代码公司代码等内容。 | [查看](tableInfo/LC_CodeRelationship.json) |
| `LC_ConceptList` | 概念板块常量表 | 记录A股市场中热点概念的相关信息 | [查看](tableInfo/LC_ConceptList.json) |
| `LC_ConsultingPlatform` | 上市公司咨询互动平台 | 1.主要记录上市公司的投资者与上市公司董秘互动问答、传闻求证等内容,包括咨询日期,问题情况,问题回复,回复日期等内... | [查看](tableInfo/LC_ConsultingPlatform.json) |
| `LC_CorrIndexIndustry` | 指数与行业对应 | 1.收录了行业指数与所属行业的对应关系，包括行业分类标准，行业分类信息；通过与系统常量表等相关联，能获取具体的行业... | [查看](tableInfo/LC_CorrIndexIndustry.json) |
| `LC_Credit` | 公司借贷明细 | 1.收录上市公司公告中披露的公司借贷等重大事项描述，包括时间内容、时间主体、交易对象名称、借贷金额、还款金额、借贷... | [查看](tableInfo/LC_Credit.json) |
| `LC_DIndicesForValuation` | 公司估值分析日指标_新会计准则 | 1.收录市盈率、市净率、市销率等估值指标。 2.数据范围：1990-12-19至今 | [查看](tableInfo/LC_DIndicesForValuation.json) |
| `LC_Deregulation` | 重大事项违规处罚 | 1、记录企业违规受处罚的明细数据，包括违规企业、违规原因、涉及关联企业、处罚金额、处分措施等指标。 2、数据范围：... | [查看](tableInfo/LC_Deregulation.json) |
| `LC_Dividend` | 公司分红 | 1.该表包括上市公司历次分红预案及实施进展，以及下年分配次数、方式等，以分红事件为维度，一次分红做一条记录。 2.... | [查看](tableInfo/LC_Dividend.json) |
| `LC_DividendProgress` | 公司分红进度 | 1.收录上市公司分红的详细信息，以事件进程为维度，一次分红根据不同的进程，分多条记录展示，主要进程包括：意向、预案... | [查看](tableInfo/LC_DividendProgress.json) |
| `LC_ESOP` | 员工持股计划 | 1.主要记录员工持股计划当期的情况：包括相关日期、事件进程、事件说明、资金来源、资金总额、股票来源、股票规模、实施... | [查看](tableInfo/LC_ESOP.json) |
| `LC_ESOPConduct` | 员工持股计划实施情况 | 1.主要记录员工持股计划当期实施情况：包括相关日期、实施股份、实施价格等指标。 2.数据范围：2014.6-至今 ... | [查看](tableInfo/LC_ESOPConduct.json) |
| `LC_ESOPHolder` | 员工持股计划持有人 | 1.主要记录实施员工持股计划的上市公司在员工持股计划公告中公布的持有人及持有比例。 2.数据范围：2014.6-至... | [查看](tableInfo/LC_ESOPHolder.json) |
| `LC_ESOPSummary` | 员工持股计划概况 | 1.本表主要记录员工持股计划总体情况：包括相关日期、事件进程、事件说明、资金来源、资金总额、股票来源、股票规模等一... | [查看](tableInfo/LC_ESOPSummary.json) |
| `LC_EmbeddedValue` | 保险公司内含价值 | 1.反映保险公司披露的内含价值表数据 2.收录保险公司在报告期末未调整和调整的合并报表 3.由于披露精度的问题，数... | [查看](tableInfo/LC_EmbeddedValue.json) |
| `LC_EmbeddedValueChange` | 保险公司内含价值变动 | 1.反映保险公司在年报中披露的内含价值变动数据。 2.仅收录保险公司在报告期末未调整的合并报表。 3.该表中各科目... | [查看](tableInfo/LC_EmbeddedValueChange.json) |
| `LC_EmbeddedValueIndex` | 保险公司内含价值分析指标 | 1.根据报告期公布的数据进行内含价值的分析与预测，以反映保险公司内含价值相关指标的纵比分析、同比分析。 2.仅收录... | [查看](tableInfo/LC_EmbeddedValueIndex.json) |
| `LC_EnterpriseLogo` | 企业标志 | 收录企业的logo、更新日期、图片链接、图片格式等信息。 | [查看](tableInfo/LC_EnterpriseLogo.json) |
| `LC_EntrustInv` | 重大事项委托理财 | 1.公司委托贷款等重大事项，包括事件主体/交易对象名称、企业编号、与上市公司关联关系、涉及金额、委托期限、委托起始... | [查看](tableInfo/LC_EntrustInv.json) |
| `LC_EquityChangesStatement` | 所有者权益变动表_新会计准则 | 1.反映企业依据2007年新会计准则在在年报、中报、季报中披露的权益变动表。 2.收录同一公司在报告期末的四种财务... | [查看](tableInfo/LC_EquityChangesStatement.json) |
| `LC_ExecutivesHoldings` | 公司报告期管理层持股 | 1.公司董事会、监事会、高管人员在报告期的持股状况及其获取的年度报酬情况等。 2.数据范围：1989-12-31至... | [查看](tableInfo/LC_ExecutivesHoldings.json) |
| `LC_ExgIndustry` | 公司行业划分表 | 收录上市公司在证监会行业划分、中信行业划分、GICS行业划分、申万行业划分、中信建投、中银(BOCI)行业分类、中... | [查看](tableInfo/LC_ExgIndustry.json) |
| `LC_FLAgency` | 公司聘请财务及法律中介机构 | 1.收录了上市公司自公开发行以来所有聘请的财务、法律中介机构及变更情况。 2.信息来源：招股说明书、董事会公告、临... | [查看](tableInfo/LC_FLAgency.json) |
| `LC_FSDerivedData` | 公司衍生报表数据_新会计准则(新) | 1.由公司披露的主要会计科目（合并报表）衍生出来的数据，单位均为人民币元，起始年度为1989年。 2.若三大财务报... | [查看](tableInfo/LC_FSDerivedData.json) |
| `LC_FSPerformedLetters` | 业绩快报(全) | 1.内容说明： 1）收录公司在业绩快报中披露的主要财务数据和指标，包括本期数据、去年同期或本期期初数据以及同比或与... | [查看](tableInfo/LC_FSPerformedLetters.json) |
| `LC_FSpecialIndicators` | 金融类特有指标(新) | 1.反映银行、证券公司、保险公司等特有的指标数据，包括指标名称、金额、比率等内容。 2.数据范围：1998-12-... | [查看](tableInfo/LC_FSpecialIndicators.json) |
| `LC_FinanceIndex` | 金融类公司财务指标 | 1.收录金融公司的一般性财务指标。 2.数据范围：2001-06-30至今 3.信息来源：招股意向书、定期报告等 | [查看](tableInfo/LC_FinanceIndex.json) |
| `LC_FixedAssetsDepreciation` | 资产负债表附注_固定资产及折旧明细 | 1.描述新会计准则下，上市公司固定资产及折旧的明细情况，包括固定资产的原值、累计折旧、减值准备、账面价值、净值等各... | [查看](tableInfo/LC_FixedAssetsDepreciation.json) |
| `LC_FreeFloat` | 自由流通股本 | 1.内容说明：本表记录境内A股市场(包含科创板)每只股票对应某一股本变动日期实际可在二级市场上交易的流通股数量。 ... | [查看](tableInfo/LC_FreeFloat.json) |
| `LC_GreatEvents` | 公司大事记 | 1.该表依据上市公司公告采编而成，主要涵盖公告中提及的上市公司重大事件。 2.数据来源：上海证券交易所、深圳证券交... | [查看](tableInfo/LC_GreatEvents.json) |
| `LC_IPODeclaration` | A股发行申报企业信息 | 1.收录了中国证监会公布的首次公开发行股票申报企业基本信息，包括申报企业名称、所属板块、证监会所属行业代码以及涉及... | [查看](tableInfo/LC_IPODeclaration.json) |
| `LC_IPONews` | 新股IPO资讯 | 1.新股发行介绍和定价的相关信息 2.数据范围：2002-至今 | [查看](tableInfo/LC_IPONews.json) |
| `LC_IPOQuoteDetails` | A股IPO投资者报价情况 | 1.内容说明：收录A股新上市公司首次发行股票公告中披露的投资者报价信息 3.信息来源：上市公司首次发行股票公告 | [查看](tableInfo/LC_IPOQuoteDetails.json) |
| `LC_InactStockHoldSt` | 股东持有非自由流通股本明细 | 1.内容说明：本表记录境内A股市场每只股票符合非自由流通扣除条件的股东持股明细及变动情况 2.数据范围：2018年... | [查看](tableInfo/LC_InactStockHoldSt.json) |
| `LC_IncentivePlanChange` | 激励计划要素变动 | 1.收录上市公司激励计划实施前的要素变动信息，包括公司派现、送股等引致的激励数量变化。 2.数据范围：2005-至... | [查看](tableInfo/LC_IncentivePlanChange.json) |
| `LC_IncentivePlanImplement` | 激励计划实施 | 1.收录上市公司激励计划的实施结果信息，包括实施日期、激励权益数量、兑换比例、激励股票数量、激励价格、激励金额等指... | [查看](tableInfo/LC_IncentivePlanImplement.json) |
| `LC_IncentivePlans` | 激励计划 | 1.收录公告中披露的公司实行股权激励计划方案的要素信息，包括股东大会公告日期、授予日、事件进程、方案说明、激励模式... | [查看](tableInfo/LC_IncentivePlans.json) |
| `LC_IncomeStatementAll` | 利润分配表_新会计准则 | 1.反映企业依据2007年新会计准则在在年报、中报、季报中披露的利润表数据；并依据新旧会计准则的科目对应关系，收录... | [查看](tableInfo/LC_IncomeStatementAll.json) |
| `LC_IncomeStatementPSCN` | 利润分配表附注_中国会计准则 | 1.内容说明： 1.1描述新会计准则下，上市公司、发债人利润分配表附注的明细情况。 1.2对于公告原文披露的项目名... | [查看](tableInfo/LC_IncomeStatementPSCN.json) |
| `LC_IndexBasicInfo` | 指数基本情况 | 1.内容说明：收录了市场上主要指数的基本情况，包括指数类别、成份证券类别、发布机构、发布日期、基期基点、指数发布的... | [查看](tableInfo/LC_IndexBasicInfo.json) |
| `LC_IndexComponent` | 指数成份 | 1.收录了市场上主要指数的成份证券构成情况，包括成份证券的市场代码、入选日期、删除日期以及成份标志等信息。 2.该... | [查看](tableInfo/LC_IndexComponent.json) |
| `LC_IndexComponentsWeight` | 指数成份股权重 | 1.收录了市场上主要指数成份证券的权重信息，包括中证指数有限公司每月发布的“沪深300”指数的权重数据等。中证基金... | [查看](tableInfo/LC_IndexComponentsWeight.json) |
| `LC_IndexDerivative` | 指数估值指标 | 1.内容说明：本表记录A股、港股主要股票指数的衍生指标，包括指数总市值、静态市盈率、动态市盈率、市净率、股息率等指... | [查看](tableInfo/LC_IndexDerivative.json) |
| `LC_IndexNews` | 指数动态信息 | 1.内容说明：收录了指数发布机构发布的指数动态，包含指数停用、指数代码/简称变更以及成份券的定期/临时调整预告等。... | [查看](tableInfo/LC_IndexNews.json) |
| `LC_IndexPrepComponent` | 指数备选成份 | 1.主要收录了上交所上海证券交易所和中证指数公司发布的部分指数的备选成份证券名单信息，包括生效日期、备选顺序。 2... | [查看](tableInfo/LC_IndexPrepComponent.json) |
| `LC_IndexRelationship` | 指数代码关联 | 1.收录了同一指数在不同的证券发布市场上的代码之间的关联信息。 2.数据源：深圳证券交易所、上海证券交易所等 | [查看](tableInfo/LC_IndexRelationship.json) |
| `LC_IndustryValuation` | 行业估值指标 | 内容说明：本表记录不同行业标准下的的衍生指标，包括行业静态市盈率、滚动市盈率、市净率、股息率等指标。 数据范围：2... | [查看](tableInfo/LC_IndustryValuation.json) |
| `LC_IntAssetsDetail` | 公司研发投入与产出 | 1.内容说明：收录上市公司研发投入相关数据，主要包括研发费用投入总额、占比，研发人员构成、占比等信息。 2.数据范... | [查看](tableInfo/LC_IntAssetsDetail.json) |
| `LC_IntangibleAsset` | 主营业务与产品_工业产权等无形资产 | 1.工业产权等无形资产类别、名称、所有权归属、取得或使用方式，项目具体说明。 2.数据范围：2000-12-22至... | [查看](tableInfo/LC_IntangibleAsset.json) |
| `LC_IntangibleAssetNew` | 资产负债表附注_无形资产 | 1.描述新会计准则下，上市公司无形资产的明细情况。 2.对于公告原文披露的项目名称，收录在“科目名称（ItemNa... | [查看](tableInfo/LC_IntangibleAssetNew.json) |
| `LC_InterimBulletin` | 公司临时公告 | 1.公司历年披露的除发行上市公告书、定期报告等以外的其他各类公告，其他机构如交易所、证监会、拍卖行等发布的相关公告... | [查看](tableInfo/LC_InterimBulletin.json) |
| `LC_InvestorDetail` | 投资者关系活动调研明细 | 1、收录参与上市公司调研活动的调研机构明细数据，包括调研单位、调研人员等指标。 2、数据范围：2016-至今 3、... | [查看](tableInfo/LC_InvestorDetail.json) |
| `LC_InvestorRa` | 投资者关系活动 | 1.收录各调研机构对上市公司调研的详情，包括调研日期、参与单位、调研人员、调研主要内容等信息。 2.数据范围：20... | [查看](tableInfo/LC_InvestorRa.json) |
| `LC_IssuanceExamination` | 发行审核表 | 1.收录股票发行审核委员会历年来对各拟发行人的审核情况，包括审核会议召开日期、参会委员、是否通过等信息。 2.数据... | [查看](tableInfo/LC_IssuanceExamination.json) |
| `LC_IssueAndListAgent` | 发行与上市中介机构 | 1.收录A股上市公司历次发行与上市聘请的所有中介机构包括主承销商、分销商、上市推荐人、国际协调人、会计师事务所、律... | [查看](tableInfo/LC_IssueAndListAgent.json) |
| `LC_KeywordInfo` | 股票行情统计资讯 | 1.收录股票行情类资讯，包括机构推荐个股、机构多空意见对比、沪市振幅/换手率/成交量排名等。 2.数据范围：200... | [查看](tableInfo/LC_KeywordInfo.json) |
| `LC_LargeSHSubscription` | 配股大股东认配状况 | 1.收录配股实施过程中大股东的认配状况，如全额实物认配、部分现金认配等内容。 2.数据范围：1993-03-29至今 | [查看](tableInfo/LC_LargeSHSubscription.json) |
| `LC_LeaderIntroduce` | 公司领导人介绍 | 1.收录A\B股上市公司在任和历任的领导人的简历介绍，包括姓名、职位、职称、性别、出生年月、学历背景、上任离任日期... | [查看](tableInfo/LC_LeaderIntroduce.json) |
| `LC_LeaderPosition` | 公司领导人任职情况 | 本表收录了上市公司董事会、监事会、经营层中主要领导人的历史任职变动情况，包括出生年月、职位名称、任职起始日和截止日... | [查看](tableInfo/LC_LeaderPosition.json) |
| `LC_LeaderRelate` | 公司领导人亲属信息 | 1.内容说明：收录了上市公司董事会、监事会、经营层中主要领导人及核心技术人员的亲属，包括配偶、子女、兄弟姐妹等所在... | [查看](tableInfo/LC_LeaderRelate.json) |
| `LC_LeaderStockAlter` | 公司领导人持股变动 | 收录深沪交易所披露的上市公司领导人及其亲属买卖所在公司股份的情况。 | [查看](tableInfo/LC_LeaderStockAlter.json) |
| `LC_LegalDistribution` | 法人配售与战略投资者 | 1.收录公司首次发行、增发新股、发行可转债过程中采用网下配售方式过程中，获得配售的企业、基金明细。 2.数据范围：... | [查看](tableInfo/LC_LegalDistribution.json) |
| `LC_ListStatus` | 上市状态更改 | 收录各证券上市状态变更的情况，包括证券市场、变更日期、变更类型、变更说明等内容。 | [查看](tableInfo/LC_ListStatus.json) |
| `LC_MSecuFinance` | 证券公司月度主要财务指标 | 1.收记录上市券商及其子公司每月的主要财务信息。 2.数据范围：2009-12-31至今 3.信息来源：财务信息公告 | [查看](tableInfo/LC_MSecuFinance.json) |
| `LC_MainDataNew` | 公司报告期主要会计数据_新会计准则 | 1.展示上市公司、发债主体，定期报告维度下的主要指标。 2.该表收录报告期（一季度、半年度、三季度、年度）合并未调... | [查看](tableInfo/LC_MainDataNew.json) |
| `LC_MainIndexChange` | 公司主要财务指标变动原因 | 1.内容说明：记录上市公司定期报告主要财务数据、财务指标发生重大变动的情况及原因  2.数据范围：2018-09-... | [查看](tableInfo/LC_MainIndexChange.json) |
| `LC_MainIndexNew` | 公司主要财务分析指标_新会计准则 | 1.根据报告期公布的财务科目数据衍生而来的每股指标，以及反映公司盈利、偿债、成长、营运、分红、现金流、资本结构等能... | [查看](tableInfo/LC_MainIndexNew.json) |
| `LC_MainOperIncome` | 公司主营业务构成 | 1收录公司主营业务的收入来源、成本构成；主营业务收入、成本和利润与上年同期的对比较。 2.数据范围：1998-12... | [查看](tableInfo/LC_MainOperIncome.json) |
| `LC_MainQuarterData` | 公司季度主要会计数据及财务指标_新会计准则 | 1.反映上市公司的主要指标。 2.该表反映报告期为第三季度当季（7月-9月）财务数据。 3.该表中各财务科目的单位... | [查看](tableInfo/LC_MainQuarterData.json) |
| `LC_MainSHListNew` | 股东名单(新) | 1.收录公司主要股东构成及持股数量比例、持股性质等明细资料，包括发行前和上市后的历次变动记录。 2.数据范围：19... | [查看](tableInfo/LC_MainSHListNew.json) |
| `LC_MajorContract` | 公司重大经营合同明细 | 1.本表存放公司重大经营合同的事项，包括事件主体/交易对象名称、企业编号、与上市公司关联关系、合同标的、合同获得方... | [查看](tableInfo/LC_MajorContract.json) |
| `LC_MajorEventStat` | 重大事项综合统计 | 1.年报、半年报中公布的募集资金使用、重大担保、关联债权债务、委托理财、关联交易总额、关联销售和采购等的综合统计。... | [查看](tableInfo/LC_MajorEventStat.json) |
| `LC_MajorPunishALL` | 重大事项处罚全表 | 1、本表记录机构违规处罚的内容信息,通过【非文本记录ID】字段关联公告表LC_NotTextAnnouncemen... | [查看](tableInfo/LC_MajorPunishALL.json) |
| `LC_Merger` | 重大事项吸收合并 | 1.收录上市公司公告中披露的公司吸收合并其他公司的事项，包括吸收合并日期进程、被合并公司代码及名称、主营、吸收合并... | [查看](tableInfo/LC_Merger.json) |
| `LC_Mshareholder` | 大股东介绍 | 1.收录上市公司及发债企业大股东的基本资料，包括直接持股和间接持股，以及持股比例、背景介绍等内容。 2.数据范围：... | [查看](tableInfo/LC_Mshareholder.json) |
| `LC_NameChange` | 公司名称更改状况 | 收录公司名称历次变更情况，包括：中英文名称、中英文缩写名称、更改日期等内容。 | [查看](tableInfo/LC_NameChange.json) |
| `LC_NationalStockHoldSt` | A股国家队持股统计 | 1.内容说明：本表记录股市国家队成员持有A股的相关信息，包含：持有A股总数，占总股本比例，持有A股数量增减，持有A... | [查看](tableInfo/LC_NationalStockHoldSt.json) |
| `LC_NewestFinaIndex` | 公司最新财务指标 | 1.内容说明：展示上市公司最新财务指标，这些指标的主要特点是已经发生了变化，但尚未在报表中反映出来； 2.覆盖企业... | [查看](tableInfo/LC_NewestFinaIndex.json) |
| `LC_NewestShareStru` | 最新公司股本结构 | 1.收录上市公司最新股本机构数据,包括未流通股份、流通股份、有限售流通股份明细、总股本等内容。 2.数据范围：保留... | [查看](tableInfo/LC_NewestShareStru.json) |
| `LC_News` | 公司动态新闻 | 1.收录各主流媒体发布的公司新闻报道，包括互动关系平台上的互动新闻。 2.数据范围：2001-至今 | [查看](tableInfo/LC_News.json) |
| `LC_NewsAbstract` | 公司动态摘要 | 1.该表主要覆盖各主流媒体发布的上市公司相关新闻资讯。 2.数据范围：2001-至今 | [查看](tableInfo/LC_NewsAbstract.json) |
| `LC_NonRecurringEvent` | 公司非经常性损益 | 1.收录定期报告中的非经常性损益数据，包括项目名称、项目类别、金额、计价货币等内容。 2.数据范围：2003-12... | [查看](tableInfo/LC_NonRecurringEvent.json) |
| `LC_NotTextAnnouncement` | 公司公告原文非文本 | 1.公司首次发行股票的招股说明书、招股意向书、上市公告书，公司增发新股招股说明书、增发新股招股意向书、增发新股上市... | [查看](tableInfo/LC_NotTextAnnouncement.json) |
| `LC_NotTextAttach` | 公司公告原文非文本附表 | 1.内容说明：本表为LC_NotTextAnnouncement的附表，用于存放LC_NotTextAnnounc... | [查看](tableInfo/LC_NotTextAttach.json) |
| `LC_OperatingStatus` | 公司经营情况述评 | 1.收录公司管理层对季度、半年度、年度经营情况的自我评价，以及其后期发展计划和预测，本表涵盖了公司招股以来的历次纪... | [查看](tableInfo/LC_OperatingStatus.json) |
| `LC_OtherAssets` | 资产负债表附注_其他资产 | 1.描述新会计准则下，上市公司在资产负债表附注中公布的投资性房产、生产性生物资产、油气资产等资产的明细情况。 2.... | [查看](tableInfo/LC_OtherAssets.json) |
| `LC_PerformanceForecast` | 业绩预告 | 1.收录上市公司对未来报告期本公司业绩的预计情况，包括业绩预计类型、预计内容、具体预计值等。 2.数据范围：199... | [查看](tableInfo/LC_PerformanceForecast.json) |
| `LC_PromiseImplement` | 股东承诺实施 | 1.收录自股权分置开始，股东对于承诺实施日期、承诺实施截止日期、承诺实施价格、承诺事项说明等具体承诺详情。 2.数... | [查看](tableInfo/LC_PromiseImplement.json) |
| `LC_PurchaseAndSale` | 公司采销明细 | 1.收录上市公司定期报告中披露的向前5名供应商的采购情况及向前5名客户的销售情况等。 2.数据范围：2000年-至... | [查看](tableInfo/LC_PurchaseAndSale.json) |
| `LC_QCashFlowStatementNew` | 单季现金流量表_新会计准则 | 1.本表收录自公布季报以来公司的单季现金流量表情况，数据单位均为人民币元。 2.科目的计算方法：第一季度数据=直接... | [查看](tableInfo/LC_QCashFlowStatementNew.json) |
| `LC_QFinancialIndexNew` | 公司单季财务指标_新会计准则 | 1.本表收录自公布季报以来上市企业(含科创板)、发债企业的单季主要财务指标信息，计算基础数据为“单季利润表_新会计... | [查看](tableInfo/LC_QFinancialIndexNew.json) |
| `LC_QIncomeStatementNew` | 单季利润表_新会计准则 | 1.本表收录自公布季报以来公司的单季利润表情况，数据单位均为人民币元。 2.科目的计算方法：第一季度数据=直接取公... | [查看](tableInfo/LC_QIncomeStatementNew.json) |
| `LC_RCalendar` | 股东大会日期 | 1.收录上市公司历史股权分置事件日期及召开股东大会网络、互联网、交易系统投票日期进程，以竖表形式展示。 2.数据范... | [查看](tableInfo/LC_RCalendar.json) |
| `LC_RConsideration` | 股权分置对价方案 | 1.收录股权分置改革方案具体内容，包括公司派现、送转股、非流通股东现金对价、股份对价支付、非流通股缩情况、改革方案... | [查看](tableInfo/LC_RConsideration.json) |
| `LC_Regroup` | 公司资产重组明细 | 1.公司资产重组，如资产出售与转让、资产置换、债权债务重组等重大事项描述说明。 2.数据范围：2001-至今 3.... | [查看](tableInfo/LC_Regroup.json) |
| `LC_RelatedSH` | 企业之间参股情况 | 1.收录上市公司与其股东之间的关联关系，权益形成方式，关联股东持股情况等。 2.数据范围：2004-12-31至今... | [查看](tableInfo/LC_RelatedSH.json) |
| `LC_RelatedTrade` | 公司关联交易明细 | 1.收录上市公司中披露的与关联企业之间的各类关联交易，包括购买商品、接受劳务、销售商品、应收帐款、支付费用、支付利... | [查看](tableInfo/LC_RelatedTrade.json) |
| `LC_Relationship` | 公司关联关系明细 | 1.收录上市公司、债券发行人定期报告中披露的控股参股企业数据，包括关联企业名称、关联关系，关联企业注册资本、权益比... | [查看](tableInfo/LC_Relationship.json) |
| `LC_ReserveReportDate` | 财务报告预约披露日 | 1.收录上市公司（剔除科创板）定期报告预约披露日信息，包括公告类别、预约披露起始与截止日和实际披露日期等内容。 2... | [查看](tableInfo/LC_ReserveReportDate.json) |
| `LC_RestrictedToFloats` | 限售股票解禁明细 | 1.收录上市公司股东历次限售股票解禁明细，包括流通起始日、股东名称、股东持股总数、新增可售A股、新增可售B股、股本... | [查看](tableInfo/LC_RestrictedToFloats.json) |
| `LC_RewardStat` | 公司管理层报酬统计 | 1.按报告期统计管理层的报酬情况，包括报酬总额、前三名董事报酬、前三名高管报酬、报酬区间统计分析等。 2.数据范围... | [查看](tableInfo/LC_RewardStat.json) |
| `LC_SHNumber` | 股东户数 | 1.反映公司全体股东、A股股东、B股东、H股东、CDR股东的持股情况及其历史变动情况等。 2.指标计算公式：   ... | [查看](tableInfo/LC_SHNumber.json) |
| `LC_SHPromise` | 股东承诺 | 1.收录股权分置改革中非流通股东承诺事项，包括对价支付、持股变动、限售解禁期限、上市价格、增持计划等类别指标。 2... | [查看](tableInfo/LC_SHPromise.json) |
| `LC_SHSCActiveShares` | 沪港通成交活跃股 | 1.内容说明：收录沪港通交易每日/月前十大成交活跃股票信息。 2.数据范围：2014年11月起-至今 3.信息来源... | [查看](tableInfo/LC_SHSCActiveShares.json) |
| `LC_SHSCComponent` | 沪港通成分股 | 1.收录沪港通业务中，‘沪股通’和‘港股通（沪）’各自的成分构成情况。 2.历史数据：2014年11月起-至今 3... | [查看](tableInfo/LC_SHSCComponent.json) |
| `LC_SHSCEliStocks` | 沪港通合资格股份 | 1.收录沪港通业务中，各类交易（可买入及卖出、只可卖出、可进行保证金交易、可进行担保卖空）的合资格股票的最新清单以... | [查看](tableInfo/LC_SHSCEliStocks.json) |
| `LC_SHSCForex` | 沪港通汇率信息 | 1.收录沪港通交易的参考汇率及结算汇率。汇率为直接报价。 2.历史数据：2014年11月起-至今 3.数据来源：聚... | [查看](tableInfo/LC_SHSCForex.json) |
| `LC_SHSCQuotaInfo` | 沪港通额度信息 | 1.收录沪港通业务中，沪股通和港沪股通交易的每日额度及总额度信息。 2.历史数据：2014年11月起-至今 3.数... | [查看](tableInfo/LC_SHSCQuotaInfo.json) |
| `LC_SHSCTradeStat` | 沪港通交易统计 | 1.收录沪港通业务中，沪股通和港沪股通交易的日、周、月、年四个维度下成交量、成交额的统计信息。 2.历史数据：20... | [查看](tableInfo/LC_SHSCTradeStat.json) |
| `LC_SHSZHSCHoldings` | 沪(深)港通持股统计 | 1.记录港交所中央結算系統参与者在每日日终的合计持股数量，持股占比。 2.历史数据：港交所2017年3月起-至今，... | [查看](tableInfo/LC_SHSZHSCHoldings.json) |
| `LC_SMAttendInfo` | 股东大会出席信息 | 1.收录股东大会召开时间，地点，类别；投票方式；见证律师事务所及经办律师；全体股东出席情况；非流通股东出席情况；流... | [查看](tableInfo/LC_SMAttendInfo.json) |
| `LC_SMTVoting` | 股权分置股东大会流通表决 | 1.收录股权分置改革进程中，流通股东分类表决情况，主要有股东名称、持股数量、议案情况、表决意见等指标。 2.数据范... | [查看](tableInfo/LC_SMTVoting.json) |
| `LC_SMVoting` | 股东大会表决 | 1.收录股东大会议案、普通股全部股东表决情况、普通股中小股东表决情况、优先股股东表决情况、非流通股东表决情况、流通... | [查看](tableInfo/LC_SMVoting.json) |
| `LC_SSIIndusPE` | 行业市盈率_深证发布 | 1.收录证监会行业分类和国证行业分类下各板块的静态市盈率、滚动市盈率数据。 2.数据范围：2016.01-至今 3... | [查看](tableInfo/LC_SSIIndusPE.json) |
| `LC_STIBAICRelAttach` | 科创板一致行动人关系附表 | 1.内容说明: 收录根据科创板上市公司在招投说明书、定期报告及临时公告中披露的一致行动人的每个人单独的详细信息。 ... | [查看](tableInfo/LC_STIBAICRelAttach.json) |
| `LC_STIBAICRelationship` | 科创板一致行动人关系 | 1.内容说明: 收录根据科创板上市公司在招投说明书、定期报告及临时公告中披露的一致行动人信息。 2.数据范围：20... | [查看](tableInfo/LC_STIBAICRelationship.json) |
| `LC_STIBAbVolatiAtta` | 科创板严重异常波动信息附表 | 1.内容说明：收录交易所公布的科创板严重异常波动信息以及成交明细等；本表是附表展示成交明细信息，主表为科创板交易所... | [查看](tableInfo/LC_STIBAbVolatiAtta.json) |
| `LC_STIBAdjustingFactor` | 科创板复权因子 | 1.内容说明：收录科创板股票因为分红、送转股、配股等发生除权除息，计算出比例复权因子，可用于推算股票前复权或后复权... | [查看](tableInfo/LC_STIBAdjustingFactor.json) |
| `LC_STIBAfterDailyQuote` | 科创板盘后日行情 | 1.内容说明：收录科创板每个交易日盘后以固定价格交易的行情数据，包括收盘价、买入申报数量、卖出申报数量、成交量、成... | [查看](tableInfo/LC_STIBAfterDailyQuote.json) |
| `LC_STIBAuditOpinion` | 科创板历年审计意见 | 1.内容说明:收录科创板披露的中介机构对公司季度、半年度、年度经营情况的评价，区分审计单位、审计意见类型等相关信息... | [查看](tableInfo/LC_STIBAuditOpinion.json) |
| `LC_STIBAuditRegister` | 科创板IPO审核注册 | 1.内容说明：收录科创板上市委对科创板发行人的审核注册情况，包括审核会议召开日期、参会委员、是否通过等信息。 2.... | [查看](tableInfo/LC_STIBAuditRegister.json) |
| `LC_STIBBalanceSheet` | 科创板资产负债表 | 1.内容说明： 1.1依据新会计准则在年报、中报、季报中披露的资产负债表数据。 1.2该表收录科创板的公司。 1.... | [查看](tableInfo/LC_STIBBalanceSheet.json) |
| `LC_STIBBalanceSheetPS` | 科创板资产负债表附注 | 1.内容说明：收录新会计准则下，科创板披露公司涉及资产负债表附注的明细情况。 2.数据范围：科创板上市至今 3.信... | [查看](tableInfo/LC_STIBBalanceSheetPS.json) |
| `LC_STIBBlockTrading` | 科创板大宗交易成交明细 | 1.内容说明：本表收录科创板大宗交易每日成交信息，包括成交价，成交量，成交金额，以及买入营业部和卖出营业部等信息。... | [查看](tableInfo/LC_STIBBlockTrading.json) |
| `LC_STIBBrandLogo` | 科创板公司产品品牌 | 1.内容说明：记录科创板公司产品品牌logo，记录商标的整体情况，包括注册、续用、LOGO图片、专用权期限等 2.... | [查看](tableInfo/LC_STIBBrandLogo.json) |
| `LC_STIBBusiness` | 科创板公司经营范围 | 1.内容说明：科创板公司的经营范围（包括主营和兼营）、主要产品业务情况。 2.数据范围：2019年至今 3.信息来... | [查看](tableInfo/LC_STIBBusiness.json) |
| `LC_STIBCDRHolder` | 科创板CDR持有人 | 1.内容说明：收录科创板公司发行存托凭证前十大持有人名单。 2.数据范围：2019至今 3.信息来源：上市公告书、... | [查看](tableInfo/LC_STIBCDRHolder.json) |
| `LC_STIBCDRTransRatio` | 科创板CDR与基础证券转换 | 1.内容说明：本表记录科创板上市的中国存托凭证与其基础证券的转换比例、存托凭证份数、面值等信息。 2.数据范围：科... | [查看](tableInfo/LC_STIBCDRTransRatio.json) |
| `LC_STIBCSRights` | 科创板公司普通股股权结构 | 1、内容说明：收录科创板上市公司各类普通股的投票权、转换权的分类及描述 2、数据范围：科创板上市至今 3、信息来源... | [查看](tableInfo/LC_STIBCSRights.json) |
| `LC_STIBCapFlowSta` | 科创板交易资金流向统计 | 1.内容说明：本表记录科创板股票交易资金流向统计数据，包含每日净流入金额，净流入量总计；主力净流入金额、净流入率（... | [查看](tableInfo/LC_STIBCapFlowSta.json) |
| `LC_STIBCapFlowType` | 科创板交易资金分类流向 | 1.内容说明：展示每个交易日科创板股票在不同单笔成交金额区间的累计主买、主卖金额及成交量情况。 本表仅包括二级市场... | [查看](tableInfo/LC_STIBCapFlowType.json) |
| `LC_STIBCapitalInvest` | 科创板资金投向说明 | 1.内容说明：科创板公司自有资金、通过发行新股、增发新股、配股等方式所得募集资金的项目投资情况以及运用进展和改投状... | [查看](tableInfo/LC_STIBCapitalInvest.json) |
| `LC_STIBCashFlowState` | 科创板现金流量表 | 1.内容说明： 1.1依据新会计准则在年报、中报、季报中披露的现金流量表数据。 1.2该表收录科创板的公司。 1.... | [查看](tableInfo/LC_STIBCashFlowState.json) |
| `LC_STIBCodeChange` | 科创板证券代码变更 | 1.内容说明：收录科创板证券代码的历次变更情况，包括启用日期和停用日期等内容 2.数据范围：科创板上市至今 3.信... | [查看](tableInfo/LC_STIBCodeChange.json) |
| `LC_STIBCodeRel` | 科创板公司代码关联 | 本表记录国内科创板上市公司对应的三板等关联代码的信息。包括： 关联代码内部编码、关联代码公司代码等内容。 | [查看](tableInfo/LC_STIBCodeRel.json) |
| `LC_STIBCompetitor` | 科创板公司竞争关系 | 1.内容说明：记录公司的竞争企业列表，可通过行业、产品、品牌等确定竞争企业； 2.数据范围：2016年至今； 3.... | [查看](tableInfo/LC_STIBCompetitor.json) |
| `LC_STIBConPlatform` | 科创板咨询互动平台 | 1.内容说明：主要记录科创板上市公司的投资者与上市公司董秘互动问答、传闻求证等内容,包括咨询日期,问题情况,问题回... | [查看](tableInfo/LC_STIBConPlatform.json) |
| `LC_STIBCoreTechnology` | 科创板公司核心技术 | 1.内容说明：收录科创板上市公司核心技术信息，包括技术名称、类别、技术来源、保护措施、技术所处阶段、技术水平等。 ... | [查看](tableInfo/LC_STIBCoreTechnology.json) |
| `LC_STIBDIndiForValue` | 科创板估值分析日指标 | 1.内容说明：收录市盈率、市净率、市销率等估值指标。 2.数据范围：科创板上市至今 3.信息来源：科创板公司公告 | [查看](tableInfo/LC_STIBDIndiForValue.json) |
| `LC_STIBDailyQuote` | 科创板日行情 | 1.内容说明：收录科创板每个交易日收盘行情数据，包括昨收盘、今开盘、最高价、最低价、收盘价、成交量、成交金额、成交... | [查看](tableInfo/LC_STIBDailyQuote.json) |
| `LC_STIBDerivedData` | 科创板衍生报表数据 | 1.内容说明：由上市公司的主要会计科目（合并报表）衍生出来的数据，若三大财务报表中任意报表在某报告期的数据经历调整... | [查看](tableInfo/LC_STIBDerivedData.json) |
| `LC_STIBDividend` | 科创板分红 | 1.内容说明：收录科创板A股发行人分红的详细信息，以事件进程为维度，一次分红根据不同的进程，分多条记录展示，主要进... | [查看](tableInfo/LC_STIBDividend.json) |
| `LC_STIBEnterpriseLogo` | 科创板企业LOGO | 1.内容说明：收录科创板企业的logo、更新日期、图片链接、图片格式等信息。 2.数据范围：2019年至今 3.信... | [查看](tableInfo/LC_STIBEnterpriseLogo.json) |
| `LC_STIBEquityChaState` | 科创板所有者权益变动表 | 1.内容说明： 1.1反映科创板发行公司根据新会计准则在年报、中报等披露的权益变动表。 1.2收录同一公司在报告期... | [查看](tableInfo/LC_STIBEquityChaState.json) |
| `LC_STIBExeHoldReward` | 科创板报告期高管及核心技术人员持股薪酬 | 1.内容说明：记录科创板公司董事会、监事会、高管人员及核心技术人员在报告期的持股状况及其获取的年度报酬情况等。 2... | [查看](tableInfo/LC_STIBExeHoldReward.json) |
| `LC_STIBExgIndustry` | 科创板公司行业划分 | 收录科创板上市公司在证监会行业划分、中信行业划分、GICS行业划分、申万行业划分、中信建投、中银(BOCI)行业分... | [查看](tableInfo/LC_STIBExgIndustry.json) |
| `LC_STIBFinancingAgent` | 科创板融资中介机构 | 1.内容说明：收录科创板历次发行与上市聘请的所有中介结构包括主承销商、分销商、会计师事务所、律师事务所、收款银行等... | [查看](tableInfo/LC_STIBFinancingAgent.json) |
| `LC_STIBFixedIntAssets` | 科创板固定及无形等资产明细 | 1.内容说明：描述新会计准则下，科创板发行公司披露的固定资产、无形资产、投资性房地产、油气资产、生产性生物资产的明... | [查看](tableInfo/LC_STIBFixedIntAssets.json) |
| `LC_STIBFloatingDetail` | 科创板股东限售解禁明细 | 1.内容说明：收录科创板上市公司股东历次限售股票解禁明细，包括解禁日期、解禁原因类别、股东名称、股东初始限售总数、... | [查看](tableInfo/LC_STIBFloatingDetail.json) |
| `LC_STIBFloatingStat` | 科创板公司限售解禁汇总 | 1.内容说明：收录科创板上市公司因IPO、增发等原因所限售的股票的具体解禁时间，以上市公司为维度，不区分具体股东，... | [查看](tableInfo/LC_STIBFloatingStat.json) |
| `LC_STIBGuideIndustry` | 科创板公司推荐指引行业分类 | 内容说明：根据“上海证券交易所科创板企业上市推荐指引”结合“战略性新兴产业分类（2018）”，对拟上市的科创板公司... | [查看](tableInfo/LC_STIBGuideIndustry.json) |
| `LC_STIBIPOBid` | 科创板IPO询价明细 | 1.内容说明：收录A股科创板新上市询价、网下配售明细，包括投资者名称、配售对象名称、申报价格、拟申购股数、总实际申... | [查看](tableInfo/LC_STIBIPOBid.json) |
| `LC_STIBIPODeclare` | 科创板IPO申报状态 | 1.内容说明：收录了上海证券交易所公布的首次公开发行科创板A股申报企业基本信息，包括申报企业名称、所属板块、证监会... | [查看](tableInfo/LC_STIBIPODeclare.json) |
| `LC_STIBIPOFee` | 科创板IPO发行费用 | 1、内容说明：收录即将上市的A股的招股意向书中的拟发行费用以及IPO上市各募资类型的实际的发行费用，包括费用总额、... | [查看](tableInfo/LC_STIBIPOFee.json) |
| `LC_STIBIPOIssue` | 科创板IPO发行上市 | 1.内容说明：该表包括A股科创板首次发行上市的明细情况。 2.数据范围：2019年-至今 3.信息来源：招股意向书... | [查看](tableInfo/LC_STIBIPOIssue.json) |
| `LC_STIBIPOQuoteDetails` | 科创板IPO投资者报价情况 | 1.内容说明：收录科创板新上市公司首次发行股票公告中披露的投资者报价信息 2.数据范围：科创板上市至今 3.信息来... | [查看](tableInfo/LC_STIBIPOQuoteDetails.json) |
| `LC_STIBIncomeState` | 科创板利润分配表 | 1.内容说明： 1.1依据新会计准则在年报、中报、季报中披露的利润分配表数据。 1.2该表收录科创板的公司。 1.... | [查看](tableInfo/LC_STIBIncomeState.json) |
| `LC_STIBIncomeStatePS` | 科创板利润分配表附注 | 1.内容说明：依据中国会计准则，收录科创板披露公司的利润分配表附注的明细情况。 2.数据范围：科创板上市至今 3.... | [查看](tableInfo/LC_STIBIncomeStatePS.json) |
| `LC_STIBInvestorDetail` | 科创板投资者关系活动调研明细 | 1、内容说明：收录参与科创板上市公司调研活动的调研机构明细数据，包括调研单位、调研人员等指标。 2、数据范围：证券... | [查看](tableInfo/LC_STIBInvestorDetail.json) |
| `LC_STIBInvestorRa` | 科创板投资者关系活动 | 1.内容说明：收录各调研机构对科创板上市公司调研的详情，包括调研日期、参与单位、调研人员、调研主要内容等信息。 2... | [查看](tableInfo/LC_STIBInvestorRa.json) |
| `LC_STIBLawAuditAgent` | 科创板法律与审计中介机构 | 1.内容说明：收录了科创板上市公司自公开发行以来所有聘请的法律、审计中介机构及变更情况。 2.数据范围：科创板上市... | [查看](tableInfo/LC_STIBLawAuditAgent.json) |
| `LC_STIBLeadStockAlter` | 科创板高管及相关人员股份变动 | 1.内容说明：收录深沪交易所披露的科创板上市公司领导人及其亲属买卖所在公司股份的情况。 2.数据范围：2019年至... | [查看](tableInfo/LC_STIBLeadStockAlter.json) |
| `LC_STIBLeaderIntroduce` | 科创板高管及核心技术人员背景 | 1.内容说明：收录科创板上市公司在任和历任的领导人及核心技术人员背景的简历介绍，包括姓名、职位、职称、性别、出生年... | [查看](tableInfo/LC_STIBLeaderIntroduce.json) |
| `LC_STIBLeaderPosition` | 科创板高管及核心技术人员任职 | 1.内容说明：收录了科创板上市公司董事会、监事会、经营层中主要领导人及核心技术人员的历史任职变动情况，包括职位名称... | [查看](tableInfo/LC_STIBLeaderPosition.json) |
| `LC_STIBLeaderRelate` | 科创板高管及核心技术人员亲属信息 | 1.内容说明：收录了科创板上市公司董事会、监事会、经营层中主要领导人及核心技术人员的亲属，包括配偶、子女、兄弟姐妹... | [查看](tableInfo/LC_STIBLeaderRelate.json) |
| `LC_STIBLegalDistri` | 科创板法人配售与战略投资者 | 收录科创板公司首次发行、增发新股、发行可转债过程中采用网下配售方式过程中，获得配售的企业、基金明细。 | [查看](tableInfo/LC_STIBLegalDistri.json) |
| `LC_STIBListStatus` | 科创板上市状态更改 | 收录各科创板证券上市状态变更的情况，包括变更日期、变更类型、变更说明等内容。 | [查看](tableInfo/LC_STIBListStatus.json) |
| `LC_STIBMainData` | 科创板报告期主要会计数据 | 1.内容说明： 1.1展示发行科创板公司，定期报告维度下的主要指标。 1.2该表收录报告期（一季度、半年度、三季度... | [查看](tableInfo/LC_STIBMainData.json) |
| `LC_STIBMainIndex` | 科创板主要财务分析指标 | 1.内容说明： 1.1 由上市公司的主要会计科目（合并报表）衍生出来的数据，若三大财务报表中任意报表在某报告期的数... | [查看](tableInfo/LC_STIBMainIndex.json) |
| `LC_STIBMainOperIncome` | 科创板主营业务构成 | 1.内容说明：收录科创板公司主营业务的收入来源、成本构成；主营业务收入、成本和利润与上年同期的比较。 2.数据范围... | [查看](tableInfo/LC_STIBMainOperIncome.json) |
| `LC_STIBMainSHList` | 科创板股东名单 | 1.内容说明：收录科创板A股发行人的主要股东构成及持股数量比例、持股性质等明细资料，包括发行前和上市后的历次变动记... | [查看](tableInfo/LC_STIBMainSHList.json) |
| `LC_STIBMajorContract` | 科创板公司重大事项购销合同 | 1.内容说明：收录科创板上市公司重大采购、销售合同的事项，包括事件主体/交易对象名称、与上市公司关联关系、合同标的... | [查看](tableInfo/LC_STIBMajorContract.json) |
| `LC_STIBMajorContractA` | 科创板公司重大事项购销合同附表 | 1.内容说明：收录科创板上市公司重大采购、销售合同中涉及到多个交易主体中每一个具体的交易主体的基本信息。 2.数据... | [查看](tableInfo/LC_STIBMajorContractA.json) |
| `LC_STIBMshSubscription` | 科创板配股大股东认配状况 | 1、内容说明：收录科创板配股实施过程中大股东的认配状况，如全额实物认配、部分现金认配等内容。 2、数据范围：201... | [查看](tableInfo/LC_STIBMshSubscription.json) |
| `LC_STIBNameChange` | 科创板公司名称更改 | 1.内容说明：收录科创板公司上市后的名称历次变更情况，包括：中英文名称、中英文缩写名称、更改日期等内容。 2.数据... | [查看](tableInfo/LC_STIBNameChange.json) |
| `LC_STIBNewIssue` | 科创板增发 | 1、内容说明：收录科创板增发A股的明细情况，包括历次增发预案、进程日期、预案有效期、发行属性、发行价区间、发行量区... | [查看](tableInfo/LC_STIBNewIssue.json) |
| `LC_STIBNewIssueFee` | 科创板增发发行费用 | 1、内容说明：收录科创板A股的增发上市各募资类型的实际的发行费用，包括承销费用、注册会计师费用、资产评估费用、土地... | [查看](tableInfo/LC_STIBNewIssueFee.json) |
| `LC_STIBNewestFinIndex` | 科创板最新财务指标 | 1.内容说明：收录科创板公司最新的一些财务指标，这些指标的主要特点是已经发生了变化，但尚未在报表中反映出来； 2.... | [查看](tableInfo/LC_STIBNewestFinIndex.json) |
| `LC_STIBNonRecurrEvent` | 科创板非经常性损益 | 1.内容说明：收录科创板发行公司披露的非经常性损益数据，包括项目名称、金额等内容。 2.数据范围：科创板上市至今 ... | [查看](tableInfo/LC_STIBNonRecurrEvent.json) |
| `LC_STIBNotTextAnnounce` | 科创板公司公告原文主表 | 1.内容说明：记录科创板公司公告的信息，如公告类别、公告链接、公告标题等。 2.数据范围：证券上市-至今。 3.信... | [查看](tableInfo/LC_STIBNotTextAnnounce.json) |
| `LC_STIBNotTextAttach` | 科创板公司公告原文非文本附表 | 本表为LC_STIBNotTextAnnounce的附表，用于存放LC_STIBNotTextAnnounce表对... | [查看](tableInfo/LC_STIBNotTextAttach.json) |
| `LC_STIBOpTradInfo` | 科创板交易所日公开信息 | 1.内容说明：收录交易所公布的，触发日收盘价涨跌幅达到15％、日振幅达到30%、日换手率达到30％ 等各类披露条件... | [查看](tableInfo/LC_STIBOpTradInfo.json) |
| `LC_STIBOpTradInfoAtta` | 科创板交易所日公开信息附表 | 1.内容说明：收录交易所公布的，触发日收盘价涨跌幅达到15％、日振幅达到30%、日换手率达到30％ 等各类披露条件... | [查看](tableInfo/LC_STIBOpTradInfoAtta.json) |
| `LC_STIBPerformForecast` | 科创板业绩预告 | 1.内容说明：收录科创板公司对未来报告期本公司业绩的预计情况，包括业绩预计类型、预计内容、具体预计值等。 2.数据... | [查看](tableInfo/LC_STIBPerformForecast.json) |
| `LC_STIBPerformLetters` | 科创板业绩快报 | 1.内容说明： 1）收录公司在业绩快报中披露的主要财务数据和指标，包括本期数据、去年同期或本期期初数据以及同比或与... | [查看](tableInfo/LC_STIBPerformLetters.json) |
| `LC_STIBPerformance` | 科创板行情表现 | 1.内容说明：展示科创板股票从最近一个交易日往前追溯一段时期的行情表现信息，包括近1周、1周以来、近1月、1月以来... | [查看](tableInfo/LC_STIBPerformance.json) |
| `LC_STIBPerformanceData` | 科创板日行情表现 | 1.内容说明：收录科创板股票行情表现相关的一些特色指标数据，如连涨天数、是否破发、是否破净、是否创历史新高或新低等... | [查看](tableInfo/LC_STIBPerformanceData.json) |
| `LC_STIBPlacementFee` | 科创板配股发行费用 | 1、内容说明：收录科创板A股的配股上市实际的发行费用，包括费用总额、承销费用、注册会计师费用、资产评估费用、土地评... | [查看](tableInfo/LC_STIBPlacementFee.json) |
| `LC_STIBPriceLimit` | 科创板股票涨跌停价 | 1.内容说明：存储股票每天的涨停价和跌停价，盘前提供。 2.数据范围：科创板上市-至今。 3.信息来源：上交所每日... | [查看](tableInfo/LC_STIBPriceLimit.json) |
| `LC_STIBProductsMain` | 科创板产品主表 | 1.内容说明：本表记录产品的基本信息，包括产品名称、编码； 2.信息来源：招股说明书，定期报告等。 | [查看](tableInfo/LC_STIBProductsMain.json) |
| `LC_STIBReserveRepD` | 科创板财务报告预约披露日 | 1.收录科创板上市公司定期报告预约披露日信息，包括公告类别、预约披露起始与截止日和实际披露日期等内容。 2.数据范... | [查看](tableInfo/LC_STIBReserveRepD.json) |
| `LC_STIBRewardStat` | 科创板报告期高管薪酬汇总 | 1.内容说明：记录按报告期统计管理层的报酬情况。 2.数据范围：2019年-至今。 3.信息来源：招股说明书、定期报告等 | [查看](tableInfo/LC_STIBRewardStat.json) |
| `LC_STIBSHNumber` | 科创板股东户数 | 1.内容说明：本表记录科创板上市公司全体股东、A股股东、H股东的持股情况及其历史变动情况等。 2.指标计算公式： ... | [查看](tableInfo/LC_STIBSHNumber.json) |
| `LC_STIBSecuChange` | 科创板证券简称更改 | 1.内容说明：收录了科创板公司的证券简称，历次变更情况及被特别处理(或撤销)的相关信息，包括：简称更改日期、证券简... | [查看](tableInfo/LC_STIBSecuChange.json) |
| `LC_STIBSharePlacement` | 科创板配股 | 1.内容说明：收录A股科创板历次配股预案及实施进展明细，包括预案有效期、配股价格区间、配股说明书、募集资金和配股交... | [查看](tableInfo/LC_STIBSharePlacement.json) |
| `LC_STIBShareRights` | 科创板股权层级 | 1.内容说明：本表以公司纬度收录适用科创板上市公司的股本构成情况。 2.数据范围：科创板上市至今 3.信息来源：上... | [查看](tableInfo/LC_STIBShareRights.json) |
| `LC_STIBShareStru` | 科创板公司股本结构 | 1.内容说明：收录科创板上市公司股本结构历史变动情况。其中：标注“披露”的字段为公司公告原始披露，标注“计算”的字... | [查看](tableInfo/LC_STIBShareStru.json) |
| `LC_STIBSpecialNotice` | 科创板特别提示 | 1. 收录公司发行上市、分红配股、公告停牌、临时停牌、召开股东大会、报告预约披露等方面的当日提示、未来提示信息。 ... | [查看](tableInfo/LC_STIBSpecialNotice.json) |
| `LC_STIBStaff` | 科创板公司职工构成 | 1.内容说明：从技术职称、专业、文化程度、年龄等几个方面介绍科创板公司职工构成情况。 2.数据范围：2019年-至... | [查看](tableInfo/LC_STIBStaff.json) |
| `LC_STIBStockArchives` | 科创板公司概况 | 1.内容说明：收录科创板公司的基本情况，包括：联系方式、注册信息、背景资料等内容。 2.数据范围：2019年至今 ... | [查看](tableInfo/LC_STIBStockArchives.json) |
| `LC_STIBSuppCustAttach` | 科创板公司供应商与客户附表 | 1.内容说明：收录企业供应商与客户明细表中供应商、客户的具体清单，以及交易金额、占比等信息。 2.数据范围：201... | [查看](tableInfo/LC_STIBSuppCustAttach.json) |
| `LC_STIBSuppCustDetail` | 科创板公司供应商与客户 | 1.内容说明：收录科创板公司主要供应商、客户清单，以及交易标的、交易金额等信息。 2.数据范围：2016年至今 3... | [查看](tableInfo/LC_STIBSuppCustDetail.json) |
| `LC_STIBSuspendResume` | 科创板停复牌 | 1.内容说明：收录上海交易所披露科创板停牌复牌信息及科创板上市公司临时公告信息，如停牌日期、停牌时间、停牌事项说明... | [查看](tableInfo/LC_STIBSuspendResume.json) |
| `LC_STIBTextAnnounce` | 科创板公司公告原文附表(文本表) | 1.内容说明：记录科创板公司公告的文本类信息。 2.数据范围：证券上市-至今。 3.信息来源：上海证券交易所，巨潮... | [查看](tableInfo/LC_STIBTextAnnounce.json) |
| `LC_SecuChange` | 证券简称更名 | 收录了证券简称的历次变更情况，包括：股东大会决议公告日期、是否否决、简称更改日期、证券简称、简称变更原因等内容。 | [查看](tableInfo/LC_SecuChange.json) |
| `LC_SecuHolder` | 证券持有人 | 1.收录持有数量达到或超过可流通数量5%的权证持有人信息(当前已不再更新)、基金的关联方持有人信息等。 2.数据范... | [查看](tableInfo/LC_SecuHolder.json) |
| `LC_SecurityOperatingPR` | 证券公司经营业绩排名表 | 1.内容说明： 1.1该表记录的是证券公司会员经审计经营数据及业务情况进行了统计排名。指标分为企业规模与经营绩效、... | [查看](tableInfo/LC_SecurityOperatingPR.json) |
| `LC_ShareFP` | 股东股权冻结和质押 | 1.收录股东股权被冻结和质押及进展情况，包括被冻结质押股东、被接受股权质押方、涉及股数以及冻结质押期限起始和截止日... | [查看](tableInfo/LC_ShareFP.json) |
| `LC_ShareFPSta` | 股东股权冻结和质押统计 | 1.收录股东股权的质押冻结统计数据，包括股东股权累计冻结质押股数、累计占冻结质押方持股数比例和累计占总股本比例等情... | [查看](tableInfo/LC_ShareFPSta.json) |
| `LC_ShareMergerReform` | 股权分置 | 1.收录上市公司股权分置改革中日期进程以及方案实施前后股本结构对比，包括事件进程、方案类型、保荐机构、董事会决议公... | [查看](tableInfo/LC_ShareMergerReform.json) |
| `LC_ShareStru` | 公司股本结构变动 | 1.收录上市公司股本结构历史变动情况。其中：标注“披露”的字段为公司公告原始披露，标注“计算”的字段为聚源依据股权... | [查看](tableInfo/LC_ShareStru.json) |
| `LC_ShareTransfer` | 股东股权变动 | 1.收录公司股东股权转让、二级市场买卖、股权拍卖、大宗交易、股东重组等引起股东股权变动方面的明细资料，并包含与股权... | [查看](tableInfo/LC_ShareTransfer.json) |
| `LC_ShareTrustee` | 股东股权托管 | 1.收录公司股东股权委托第三方经营方面的明细资料。包括股权授权方、股权授权方所持股数、接受股权授权方、托管涉及股数... | [查看](tableInfo/LC_ShareTrustee.json) |
| `LC_SharesFloatingSchedule` | 限售股票解禁时间表 | 1.收录上市公司因为股权分置改革、定向增发、公开增发等原因所限售的股票的具体解禁时间，以上市公司为维度，不区分具体... | [查看](tableInfo/LC_SharesFloatingSchedule.json) |
| `LC_SpecialNotice` | 特别提示 | 1. 收录公司发行上市、分红配股、公告停牌、临时停牌、召开股东大会、报告预约披露等方面的当日提示、未来提示信息。 ... | [查看](tableInfo/LC_SpecialNotice.json) |
| `LC_SpecialTrade` | 证券特别处理 | 收录证券（含股票，债券）被特别处理(或撤销)的相关信息,包括ST、PT、*ST、撤销ST、撤销PT、撤销*ST等。 | [查看](tableInfo/LC_SpecialTrade.json) |
| `LC_Staff` | 公司职工构成 | 1.从技术职称、专业、文化程度、年龄等几个方面介绍公司职工构成情况。 2.数据范围：1999-12-31至今 3.... | [查看](tableInfo/LC_Staff.json) |
| `LC_StockArchives` | 公司概况 | 收录上市公司的基本情况，包括：联系方式、注册信息、中介机构、行业和产品、公司证券品种及背景资料等内容。 | [查看](tableInfo/LC_StockArchives.json) |
| `LC_StockHoldingSt` | 股东持股统计 | 1.收录报告期末，各类机构投资者对每只股票的持仓情况，以及前十大（无限售条件）股东合计持股情况等。 2.机构持股统... | [查看](tableInfo/LC_StockHoldingSt.json) |
| `LC_StockRecommend` | 个股资讯 | 1.收录各机构对上市公司股票历年推荐报告。 2.数据范围：2001-至今 | [查看](tableInfo/LC_StockRecommend.json) |
| `LC_StockStyle` | 股票风格属性 | 内容说明：本表收录股票风格属性（如价值型、成长型和平衡型）及规模属性的数据。 数据范围：2017-01-01至今 ... | [查看](tableInfo/LC_StockStyle.json) |
| `LC_Subsidy` | 公司非常补贴明细 | 1.收录上市公司公告中披露的非常补贴等重大事项描述说明。 2.数据范围：2001年-至今 3.信息来源：上市公司公告 | [查看](tableInfo/LC_Subsidy.json) |
| `LC_SuitArbitration` | 公司诉讼仲裁明细 | 1.公司诉讼仲裁等重大事项，包括事件主体/交易对象名称、企业编号、与上市公司关联关系、诉讼仲裁金额、原告及与上市公... | [查看](tableInfo/LC_SuitArbitration.json) |
| `LC_SuppCustAttach` | 公司供应商与客户附表 | 1.内容说明：收录企业供应商与客户明细表中供应商、客户的具体清单，以及交易金额、占比等信息。 2.数据范围：201... | [查看](tableInfo/LC_SuppCustAttach.json) |
| `LC_SuppCustDetail` | 公司供应商与客户 | 1.内容说明：收录A股上市公司的主要供应商、客户清单，以及交易标的、交易金额等信息。 2.数据范围：2015年至今... | [查看](tableInfo/LC_SuppCustDetail.json) |
| `LC_SuspendResumption` | 停牌复牌表 | 1.收录上市公司/基金/债券停牌复牌信息，如停牌日期、停牌时间、停牌原因、停牌事项说明、停牌期限、复牌日期、复牌时... | [查看](tableInfo/LC_SuspendResumption.json) |
| `LC_TaxChange` | 公司税负变动明细 | 1.公司税负变动等重大事项，包括事件主体/交易对象名称、企业编号、与上市公司关联关系、税负类别、税负变动对象名称、... | [查看](tableInfo/LC_TaxChange.json) |
| `LC_TenderOffer` | 重大事项要约收购 | 1.本表存放公司要约收购其它公司的事项说明，包括信息发布时间、时间内容、交易双方名称、企业编号、与上市公司关联关系... | [查看](tableInfo/LC_TenderOffer.json) |
| `LC_TextAnnounce` | 股票公告文本表 | 1.公司首次发行股票的招股说明书、招股意向书、上市公告书等公告原文，公司A股增发A股、B股增发A股、H股增发A股、... | [查看](tableInfo/LC_TextAnnounce.json) |
| `LC_TrustInvestSITN` | 上市公司投资理财明细 | 1.董事会同意公司拟使用闲置自有资金或闲置募集资金通过商业银行理财、信托理财及其他理财工具进行运作和管理。该表收录... | [查看](tableInfo/LC_TrustInvestSITN.json) |
| `LC_ViolBulletin` | 违规公告关联表 | 1.该表记录与违规事件关联的对应公告的信息，包括公告日期、公告类型、公告标题、行政文号、涉及事件编号等指标，通过R... | [查看](tableInfo/LC_ViolBulletin.json) |
| `LC_ViolProcess` | 违规事件进程 | 1.该表记录每个违规事件下的每一步事件进程，包括事件进程、事件进程日期等指标。 2.数据范围：2014年-至今 3... | [查看](tableInfo/LC_ViolProcess.json) |
| `LC_ViolatiEvent` | 违规事件表 | 1.该表以事件为维度，记录单条违规事件最新公告日期、首次信息发布日期、最新事件进程、事项内容、涉及公司、涉及证券等... | [查看](tableInfo/LC_ViolatiEvent.json) |
| `LC_ViolatiParty` | 违规当事人处罚 | 1.该表以事件+当事人+处罚为维度，记录单个事件下单个当事人的每一个处罚，包括当事人及其性质、当事人编码、开始日期... | [查看](tableInfo/LC_ViolatiParty.json) |
| `LC_Warrant` | 公司担保明细 | 1.收录上市公司公告中披露的担保等重大事项，包括时间内容、最新进展、事件主体/交易对象名称、企业编号、与上市公司关... | [查看](tableInfo/LC_Warrant.json) |
| `LC_ZHSCActiveShares` | 深港通成交活跃股 | 1.内容说明：收录深港通交易每日/月前十大成交活跃股票信息。 2.数据范围：2016年12月起-至今 3.信息来源... | [查看](tableInfo/LC_ZHSCActiveShares.json) |
| `LC_ZHSCComponent` | 深港通成分股 | 1.收录深港通业务中，“深股通”和“港股通（深）”各自的成分构成情况。 2.历史数据：2016年12月起-至今 3... | [查看](tableInfo/LC_ZHSCComponent.json) |
| `LC_ZHSCEliStocks` | 深港通合资格股份 | 1.收录深港通业务中，各类交易（可买入及卖出、只可卖出、可进行保证金交易、可进行担保卖空）的合资格股票的最新清单以... | [查看](tableInfo/LC_ZHSCEliStocks.json) |
| `LC_ZHSCForex` | 深港通汇率信息 | 1.收录深港通交易的参考汇率及结算汇率（汇率为直接报价）。 2.历史数据：2016年12月起-至今 3.数据来源：... | [查看](tableInfo/LC_ZHSCForex.json) |
| `LC_ZHSCQuotaInfo` | 深港通额度信息 | 1.收录深港通业务中，深股通和港深股通交易的每日额度及总额度信息。 2.历史数据：2016年12月起-至今 3.数... | [查看](tableInfo/LC_ZHSCQuotaInfo.json) |
| `LC_ZHSCTradeStat` | 深港通交易统计 | 1.收录深港通业务中，深股通和港深股通交易的日、周、月、年四个维度下成交量、成交额的统计信息。 2.数据范围：20... | [查看](tableInfo/LC_ZHSCTradeStat.json) |

## MF - 基金相关

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `MF_AdjustingFactor` | 公募基金净值比例复权因子 | 1.本表记录根据各基金因为分红等原因来计算出的基金净值增长率比例复权因子及基金收益率比例复权因子。 2.历史数据：... | [查看](tableInfo/MF_AdjustingFactor.json) |
| `MF_AssetAllocation` | 公募基金资产配置 | 1.本表记录基金资产的大类配置情况，包括股票、债券、银行存款和清算备付金、其他资产、买入返售证券、卖出回购证券、国... | [查看](tableInfo/MF_AssetAllocation.json) |
| `MF_AssetAllocationAll` | 公募基金资产配置总表 | 1.内容说明：公募基金资产配置合表，较之MF_AssetAllocationNew，包含了公募基金子份额数据，以及... | [查看](tableInfo/MF_AssetAllocationAll.json) |
| `MF_AssetAllocationNew` | 公募基金资产配置(新) | 1.本表记录基金资产的大类配置情况，包括股票、债券、银行存款和清算备付金、其他资产、买入返售证券、卖出回购证券、国... | [查看](tableInfo/MF_AssetAllocationNew.json) |
| `MF_BondCreditGrading` | 公募基金债券投资信用评级 | 1.本表记录基金年报、半年报公布债券投资信用评级信息，包括债券投资信用等级等数据。 2.历史数据：2013年6月起... | [查看](tableInfo/MF_BondCreditGrading.json) |
| `MF_BondPortifolioDetail` | 公募基金债券组合明细 | 1.本表记录基金债券组合中重仓的债券及处于转股期的可转换债券明细，包括债券代码、持有数量、持有市值、市值占净资产的... | [查看](tableInfo/MF_BondPortifolioDetail.json) |
| `MF_BondPortifolioStru` | 公募基金债券组合结构 | 1.本表记录基金债券组合结构信息，包括国债、金融债、企业债、可转债、央行票据等各类券种占债券总体的比重。 2.历史... | [查看](tableInfo/MF_BondPortifolioStru.json) |
| `MF_ChargeRateNew` | 公募基金费率(新) | 1.本表记录基金的相关费率数据及执行情况，包括认购费、申购费、赎回费、管理费、托管费等详细费用。 2.历史数据：1... | [查看](tableInfo/MF_ChargeRateNew.json) |
| `MF_CodeAndChange` | 公募基金代码及变更情况 | 1.本表记录了聚源根据公开披露数据整理的公募基金各类代码数据以及代码的变更情况。代码类别包括交易代码、基金主代码、... | [查看](tableInfo/MF_CodeAndChange.json) |
| `MF_CodeRelationshipNew` | 公募基金代码关联(新) | 1.本表收录了聚源整理的分级基金的关联代码、复制型基金的关联代码、封转开基金代码对应关系、基金与其收益线对应关系等... | [查看](tableInfo/MF_CodeRelationshipNew.json) |
| `MF_ETFPRComponents` | 公募基金ETF申购赎回成份股信息 | 1.本表收录ETF基金每个交易日公布的申购赎回成份股信息，包括成分股的名称、代码、现金替代标志等数据。 2.历史数... | [查看](tableInfo/MF_ETFPRComponents.json) |
| `MF_ETFPRList` | 公募基金ETF申购赎回清单信息 | 1.本表收录ETF基金每个交易日公布的ETF申购赎回清单，包括是否允许赎回、是否允许申购，及单个账户申购、赎回上限... | [查看](tableInfo/MF_ETFPRList.json) |
| `MF_ExchangFundHolderInfo` | 公募基金场内外持有人结构信息 | 1.本表记录LOF、ETF等上市基金披露的基金场内外持有人户数、持有人结构信息。 2.历史数据：2004年12月起... | [查看](tableInfo/MF_ExchangFundHolderInfo.json) |
| `MF_FundArchives` | 公募基金概况 | 1.本表记录了基金基本情况，包括基金规模、成立日期、投资类型、管理人、托管人、存续期、历史简介等。 2.历史数据：... | [查看](tableInfo/MF_FundArchives.json) |
| `MF_FundArchivesAttach` | 公募基金概况附表 | 1.本表主要记录了证监会基金分类、银河证券基金分类、基金运作方式、封闭期、货币基金收益分配方式等数据内容。 2.历... | [查看](tableInfo/MF_FundArchivesAttach.json) |
| `MF_FundArchivesText` | 公募基金文本类基本信息 | 1.本表记录基金文本类的基本信息，如基金风险揭示，基金特有风险等 2.历史数据：1998年12月起-至今。 3.信... | [查看](tableInfo/MF_FundArchivesText.json) |
| `MF_FundBondPortTerm` | 公募基金投资剩余期限分布 | 1.本表记录定期报告披露基金投资组合的剩余期限分布。如各类期限的资产占总资产的比例、各类期限的负债占总资产的比例。... | [查看](tableInfo/MF_FundBondPortTerm.json) |
| `MF_FundFuturesDetail` | 公募基金期货投资明细 | 1. 本表记录基金季度报告公布的基金投资期货明细，包括期货合约内部编码、持仓量、合约市值、持仓性质等信息。 2. ... | [查看](tableInfo/MF_FundFuturesDetail.json) |
| `MF_FundHolderMeeting` | 公募基金持有人大会 | 1.本表记录公募基金持有人大会基本情况介绍，包括召开方式、召开地点、大会议题、决议结果等等。  2.历史数据：19... | [查看](tableInfo/MF_FundHolderMeeting.json) |
| `MF_FundHolderMeetingA` | 公募基金持有人大会附表 | 1.内容说明：本表记录公募基金持有人大会议案中的议题情况，包括议题类型以及通过与否等。 2.数据范围：1998年3... | [查看](tableInfo/MF_FundHolderMeetingA.json) |
| `MF_FundNetValueRe` | 公募基金复权净值 | 1.本表记录开放式基金每日单位基金净值、封闭式每周单位基金净值，以及基金复权单位净值和净值日增长率。 【复权因子：... | [查看](tableInfo/MF_FundNetValueRe.json) |
| `MF_FundNetValueReTrans` | 公募基金复权净值(转型) | 1.本表记录开放式基金每日单位基金净值、封闭式每周单位基金净值，以及基金复权单位净值和净值日增长率。 【转型处理：... | [查看](tableInfo/MF_FundNetValueReTrans.json) |
| `MF_FundPortifolioDetail` | 公募基金投资基金明细 | 1.本表记录公募基金投资基金的明细。 2.历史数据：2009年12月起-至今。 3.数据来源：基金公司披露的定期报... | [查看](tableInfo/MF_FundPortifolioDetail.json) |
| `MF_FundProdName` | 公募基金产品名称 | 1.本表记录基金的交易所披露简称、集中申购简称、ETF申购赎回简称等基金相关的名称类信息。 2.历史数据：1998... | [查看](tableInfo/MF_FundProdName.json) |
| `MF_FundRiskLevel` | 公募基金风险等级表 | 1.内容说明：本表记录基金公司披露的全市场基金的风险等级的数据。应监管需要，本数据可服务于各类公募基金销售场景。 ... | [查看](tableInfo/MF_FundRiskLevel.json) |
| `MF_FundType` | 公募基金分类表 | 1.本表记录各类型的基金分类标准体系，及发布分类体系的机构。 2.历史数据：2017年6月起-至今。 3.信息来源... | [查看](tableInfo/MF_FundType.json) |
| `MF_FutFairValue` | 公募基金期货投资价值变动 | 1. 本表记录基金定期报告公布的基金投资股指期货、国债期货的公允价值变动、本期收益、本期公允价值变动等情况。 2.... | [查看](tableInfo/MF_FutFairValue.json) |
| `MF_HolderInfo` | 公募基金持有人结构信息 | 1.本表记录基金份额持有人户数、持有人结构，包括机构、个人持有份额的详细数据、占比等。前十大持有的持有份额合计、占... | [查看](tableInfo/MF_HolderInfo.json) |
| `MF_IndustryPortAll` | 公募基金股票投资组合行业分类总表 | 1.本表记录公募基金、QDII基金行业投资分布信息，包括行业的名称、代码、行业市值、该行业市值占基金净资产的比例等... | [查看](tableInfo/MF_IndustryPortAll.json) |
| `MF_InherentFundInvest` | 公募基金管理人固有资金投资 | 1.本表记录基金管理公司持有的旗下基金的份额变动信息，变动方式包括：认购、申购、赎回、红利再投资、其他等。 2.历... | [查看](tableInfo/MF_InherentFundInvest.json) |
| `MF_InvestAdvisorOutline` | 公募基金管理人概况 | 1.本表记录了基金管理人的基本情况介绍，包括成立日期、注册资本、法人代表、联系方式、背景简介等。 2.历史数据：1... | [查看](tableInfo/MF_InvestAdvisorOutline.json) |
| `MF_InvestIndustry` | 公募基金行业投资 | 1.本表记录基金行业投资分布信息，包括行业的名称、代码、行业市值、该行业市值占基金净资产的比例等。 2.历史数据：... | [查看](tableInfo/MF_InvestIndustry.json) |
| `MF_InvestTargetCriterion` | 公募基金投资目标比例 | 1.本表记录基金投资的资产类别及规定比例、基金参照的业绩比较基准(InvestTarget=90)、指数及指增基金... | [查看](tableInfo/MF_InvestTargetCriterion.json) |
| `MF_JYFundType` | 公募基金聚源分类 | 1.内容说明：本表记录聚源基金分类数据 2.数据范围：1998年3月起-至今 3.信息来源：基金公司官网披露的产品... | [查看](tableInfo/MF_JYFundType.json) |
| `MF_KeyStockPortfolio` | 公募基金重仓股票组合 | 1.本表记录基金季报公布重仓股票组合信息，主要包括前十大持有股票的股票代码、数量、市值、占净资产的比例等数据。 2... | [查看](tableInfo/MF_KeyStockPortfolio.json) |
| `MF_ListStatus` | 公募基金上市状态更改 | 1.本表记录各公募基金上市状态更改的情况，包括上市、清算、终止上市、基金合同失效等。 2.历史数据：1998年3月... | [查看](tableInfo/MF_ListStatus.json) |
| `MF_MFNetValue` | 公募基金净值_货币型基金 | 1.本表记录货币基金、短期理财型债券基金每天的净值及万份收益、7日年化收益等数据。交易日的数据处理与MF_NetV... | [查看](tableInfo/MF_MFNetValue.json) |
| `MF_MoneySpecialIndex` | 公募基金货币型基金专项指标 | 1.本表记录包括货币基金的季报数据，年报数据及半年报数据的债券回购融资情况，平均剩余期限入资产净值的偏离值。 2.... | [查看](tableInfo/MF_MoneySpecialIndex.json) |
| `MF_NetValue` | 公募基金净值 | 1.本表记录公募基金单位基金净值、单位累计净值、净资产值以及货币基金万份收益、七日折算年收益率。 2.历史数据：1... | [查看](tableInfo/MF_NetValue.json) |
| `MF_NetValueCashe` | 公募基金净值_含清算后净值 | 1.本表记录开放式基金每日单位基金净值，包括封闭式基金每周单位基金净值、开放式基金每日净值以及货币基金万份收益。 ... | [查看](tableInfo/MF_NetValueCashe.json) |
| `MF_NetValueReTransTwo` | 公募基金复权净值二(转型) | 1.本表记录开放式基金每日单位基金净值、封闭式每周单位基金净值，以及基金复权单位净值和净值日增长率。 【转型处理：... | [查看](tableInfo/MF_NetValueReTransTwo.json) |
| `MF_NetValueTrans` | 公募基金净值(转型) | 1.内容说明：本表记录开放式基金每日单位基金净值，包括封闭式基金每周单位基金净值、开放式基金每日净值以及货币基金万... | [查看](tableInfo/MF_NetValueTrans.json) |
| `MF_NetValueYieldTrans` | 公募基金收益率走势(转型) | 1.本表记录基金的最新趋势表现，包括一个月、三个月、半年、一年、二年、三年、五年、成立以来的回报走势。可用于基金走... | [查看](tableInfo/MF_NetValueYieldTrans.json) |
| `MF_NetValueYieldTrend` | 公募基金收益率走势 | 1.本表记录基金的最新趋势表现，包括一个月、三个月、半年、一年、二年、三年、五年成立以来的回报。可用于基金走势的展... | [查看](tableInfo/MF_NetValueYieldTrend.json) |
| `MF_PortfolioDetailsAll` | 公募基金投资组合明细总表 | 公募基金投资组合明细大合表，包含股票、债券、基金、期货等全部投资对象,同时也囊括进QDII数据 | [查看](tableInfo/MF_PortfolioDetailsAll.json) |
| `MF_PortfolioPublished` | 公募基金投资组合披露状况表 | 1.内容说明：本表记录季报基金投资组合相关披露与不披露的数据及对应数据代码。 2.数据范围：1998年6月起-至今... | [查看](tableInfo/MF_PortfolioPublished.json) |
| `MF_PriceLimit` | 上市基金涨跌停价表 | 1.内容说明：记录存储上市基金每天的涨停价和跌停价，盘前提供。 2.数据范围：2020年9月起-至今。 3.信息来... | [查看](tableInfo/MF_PriceLimit.json) |
| `MF_REITsBalanceST` | REITs项目公司资产负债表 | 1.内容说明：收录项目公司年报、中报、季报、招募说明书中披露的资产负债表数据。 2.数据范围：2021-至今 3.... | [查看](tableInfo/MF_REITsBalanceST.json) |
| `MF_REITsCashFlowST` | REITs项目公司现金流量表 | 1.内容说明：收录项目公司年报、中报、季报、招募说明书中披露的现金流量表数据。 2.数据范围：2021-至今 3.... | [查看](tableInfo/MF_REITsCashFlowST.json) |
| `MF_REITsDeclare` | 基础设施基金(REITs)申报状态与信息 | 1.内容说明：收录基础设施基金(REITs)上市前的申报进度与相关信息。 2.数据范围：2021年4月起-至今 。... | [查看](tableInfo/MF_REITsDeclare.json) |
| `MF_REITsIncomeST` | REITs项目公司利润分配表 | 1.内容说明：收录项目公司年报、中报、季报、招募说明书中披露的利润表数据。 2.数据范围：2021-至今 3.信息... | [查看](tableInfo/MF_REITsIncomeST.json) |
| `MF_REITsProjects` | 基础设施基金(REITs)-项目公司信息 | 1.内容说明：收录基础设施公募REITs与项目公司间的交易架构信息，包括资产支持证券、新设SPV等。 2.数据范围... | [查看](tableInfo/MF_REITsProjects.json) |
| `MF_REITsProjectsAttach` | 基础设施基金(REITs)-项目公司信息附表 | 1.内容说明：本表用于记录基础设施公募REITs的招募说明书中，涉及项目公司原始权益人、运营管理机构等相关信息。 ... | [查看](tableInfo/MF_REITsProjectsAttach.json) |
| `MF_REITsQuoteDetails` | 基础设施基金(REITs)投资者报价情况 | 1.内容说明：收录基础设施公募REITs首次发行、基金扩募等询价过程中的投资者报价信息。 2.数据范围：2021年... | [查看](tableInfo/MF_REITsQuoteDetails.json) |
| `MF_REITsRestricted` | 基础设施基金(REITs)限售 | 1.内容说明：收录基础设施证券投资基金限售方式，限售的企业、限售股份明细. 2.数据范围：2021年至今 3.信息... | [查看](tableInfo/MF_REITsRestricted.json) |
| `MF_RestrictedSecu` | 公募基金所持流通受限制证券 | 1.本表记录中报、年报中公布由于配售等原因暂时不能上市的证券明细，及暂时不能上市的原因、复牌的日期等信息。 2.历... | [查看](tableInfo/MF_RestrictedSecu.json) |
| `MF_SHInfluence` | 公募基金单一持有人份额信息 | 1.本表记录定报披露的单一持有人持有份额超过20%信息,包含报告期、持有人性质、持有份额、持有比例,以及在报告期中... | [查看](tableInfo/MF_SHInfluence.json) |
| `MF_SecuAdjustedPrice` | 公募基金持仓证券调价表 | 1.内容说明：本表记录基金公司披露的对于旗下基金持有证券的调整估值价格信息。 2.数据范围：2004年3月起-至今... | [查看](tableInfo/MF_SecuAdjustedPrice.json) |
| `MF_SharesChange` | 公募基金份额变动 | 1.本表记录基金份额变动情况，包括期初份额，本期申购或赎回，期末份额等数据，份额变化的绝对值、变化率等数据。 2.... | [查看](tableInfo/MF_SharesChange.json) |
| `MF_StockChangeAll` | 公募基金股票投资组合变动总表 | 1.内容说明：公募基金股票投资组合变动总表,包含一般基金和QDII基金 2.信息来源：基金公司披露的定期报告 3.... | [查看](tableInfo/MF_StockChangeAll.json) |
| `MF_StockPortfolioChange` | 公募基金股票组合重大变动 | 1.本表记录中报、年报中公布报告期内股票投资组合的重大变动，比如买入了哪些股票、市值有多少、占净资产的比例等。 2... | [查看](tableInfo/MF_StockPortfolioChange.json) |
| `MF_StockPortfolioDetail` | 公募基金股票组合明细 | 1.本表记录基金年报、半年报公布股票组合明细信息，包括股票的名称、代码、持有数量、持有市值、市值占基金净资产的比例... | [查看](tableInfo/MF_StockPortfolioDetail.json) |
| `MF_TopTenHolder` | 公募基金前10名持有人持股信息 | 1.本表记录基金前10名持有人持有基金份额情况，包括持有人名称、持有的份额、持有的比例、持有的性质等。 2.历史数... | [查看](tableInfo/MF_TopTenHolder.json) |
| `MF_TransSetFunds` | 证券市场交易结算金 | 1.证券市场交易结算资金余额及变动情况，包括结算金期末余额、期末日平均数、银证转账增加额、银证转账减少额、银证转账... | [查看](tableInfo/MF_TransSetFunds.json) |
| `MF_UmbrellaFunds` | 公募基金伞形系列关系 | 1.本表记录了基金之间的伞形关系，包括招商安泰系列、国泰金龙系列、鹏华普天系列、银河银联系列等。 2.历史数据：1... | [查看](tableInfo/MF_UmbrellaFunds.json) |
| `MF_WarrantDetails` | 公募基金权证投资明细 | 1.本表记录基金定期报告中披露的报告期权证投资情况。包括持有权证的代码、数量、市值、市值占净资产比例等数据。 2.... | [查看](tableInfo/MF_WarrantDetails.json) |

## MT - 融资融券

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `MT_DailyConvensionRate` | 可充抵保证金证券日折算率 | 1.收录国内证券交易所及券商每日可充抵保证金证券的券种及折算率等数据 2.历史数据：2010年3月起-至今。 3.... | [查看](tableInfo/MT_DailyConvensionRate.json) |
| `MT_DailyMargin` | 标的证券日保证金比例 | 1.收录国内证券交易所及各券商每日可融资（融券）的标的证券券种及保证金比例。 2.历史数据：2010年2月起-至今... | [查看](tableInfo/MT_DailyMargin.json) |
| `MT_MarginMkt` | 融资融券市场统计 | 记录融资融券日频和月频的余额情况、交易情况、公司开展业务情况和担保品的市场统计情况。 1.收录融资融券市场担保品日... | [查看](tableInfo/MT_MarginMkt.json) |
| `MT_MarginSecu` | 融资融券担保券统计 | 1.记录国内证券交易所及主要券商披露的融资融券担保券日度数据信息。 2.历史数据：2015年4月起-至今。 3.数... | [查看](tableInfo/MT_MarginSecu.json) |
| `MT_MemTradeMonStat` | 会员融资融券交易月度统计 | 1.收录国内证券交易所下会员的月度融资融券交易统计情况。 2.历史数据：2010年3月起-至今。 3.数据来源：聚... | [查看](tableInfo/MT_MemTradeMonStat.json) |
| `MT_NTargetSecurities` | 融资融券最新标的证券 | 1.收录国内证券交易所及券商每日可融资（融券）的最新标的证券清单。 2.历史数据：2015年3月起-至今。 3.数... | [查看](tableInfo/MT_NTargetSecurities.json) |
| `MT_NewDailyMargin` | 标的证券最新日保证金比例 | 1.收录国内证券交易所及及券商每日最新可融资（融券）的标的证券券种及保证金比例。 2.历史数据：2015年11月起... | [查看](tableInfo/MT_NewDailyMargin.json) |
| `MT_OperationIndicators` | 融资融券业务参数 | 1.收录国内证券交易所及各券商披露的融资融券业务的常用参数以及各参数的历次变动情况。 2.历史数据：2010年4月... | [查看](tableInfo/MT_OperationIndicators.json) |
| `MT_TargetSecurities` | 融资融券标的证券 | 1.收录国内交易所公布的融资融券标的清单，包括融资买入标的和融券卖出标的；同时还收录了有披露起证券历次入选和剔除融... | [查看](tableInfo/MT_TargetSecurities.json) |
| `MT_TradingDetail` | 融资融券交易明细 | 1.内容说明：收录国内证券交易所披露的收录融资融券日交易明细数据 2.数据范围：2010年3月起-至今。 3.信息... | [查看](tableInfo/MT_TradingDetail.json) |
| `MT_TradingStat` | 融资融券交易总量 | 1.收录国内证券交易所披露的融资融券日交易汇总数据 2.历史数据：2010年3月起-至今。 3.数据来源：聚源按照... | [查看](tableInfo/MT_TradingStat.json) |

## NI - 新闻资讯

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `NI_FinancialCalendar` | 财经日历 | 1.主要录入未来30天内将进行的行业会议、高峰论坛等事件预告，并给出受此影响的相关概念板块及其个股。    2.数... | [查看](tableInfo/NI_FinancialCalendar.json) |
| `NI_InfoMine` | 信息地雷 | 1.记录各个证券的分时地雷和K线地雷；实时地雷仅保留最近的数据，删除T-2个交易日之前的历史数据。 2.数据范围：... | [查看](tableInfo/NI_InfoMine.json) |
| `NI_NewsConst` | 资讯常量表 | 本表主要用于对新闻资讯数据的分类，提供标准化的常量信息。 | [查看](tableInfo/NI_NewsConst.json) |
| `NI_ShortNews` | 短新闻资讯 | 1.针对证券和市场的动态信息，提供停复牌、增发、配股、新股上市、融资融券、财务、行情、财务、高管持股变动等多维度短... | [查看](tableInfo/NI_ShortNews.json) |
| `NI_TagTree` | 标签树表 | 1.记录标签信息，包括标签的层级关系，有效性等属性。 2.数据范围：2014 | [查看](tableInfo/NI_TagTree.json) |

## Opt - 期权相关

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `Opt_Adjustment` | 期权合约调整 | 1.内容说明：本表收录上海证券交易所和深圳证券交易所期权合约的历次调整信息，包括原交易代码、原行权价、调整日期、新... | [查看](tableInfo/Opt_Adjustment.json) |
| `Opt_ContractNotice` | 期权合约日历 | 1.内容说明：本表收录国内交易所上市的股票期权和商品期权合约的挂牌、最后交易日、行权交收等信息提示。其中主要涵盖“... | [查看](tableInfo/Opt_ContractNotice.json) |
| `Opt_DailyGreeks` | 期权每日风险指标 | 1.内容说明：本表收录上海证券交易所、深圳证券交易所发布的期权合约盘后每日风险指标信息：包括Delta、Theta... | [查看](tableInfo/Opt_DailyGreeks.json) |
| `Opt_DailyPreOpen` | 期权每日盘前静态数据 | 1.内容说明：本表收录上海证券交易所和深圳证券交易所交易日期当日可交易的期权合约信息。主要包是50ETF和300沪... | [查看](tableInfo/Opt_DailyPreOpen.json) |
| `Opt_DailyQuote` | 期权每日行情 | 1.内容说明：本表收录上海证券交易所、深圳证券交易所个股期权 及 国内商品交易所下的期货期权（如大连商品交易所下豆... | [查看](tableInfo/Opt_DailyQuote.json) |
| `Opt_DailyTradeStat` | 期权每日交易统计 | 1.内容说明：本表收录上海证券交易所和深圳证券交易所期权合约的盘后每日交易统计信息。包括按成交量统计和持仓量统计2... | [查看](tableInfo/Opt_DailyTradeStat.json) |
| `Opt_OptionContract` | 期权合约 | 1.内容说明：本表收录上海证券交易所、深圳证券交易所、大连商品交易所、郑州商品交易所和上海期货交易所等场所的期权品... | [查看](tableInfo/Opt_OptionContract.json) |
| `Opt_SettlementStat` | 期权行权交收 | 1.内容说明：本表收录上海证券交易所和深圳证券交易所期权行权交收信息， 包括标的名称、行权日期、合约种类、行权张数... | [查看](tableInfo/Opt_SettlementStat.json) |
| `Opt_ULAComponent` | 期权标的成份 | 1.内容说明：本表收录上海证券交易所和深圳证券交易所期权标的类别为ETF基金和股票的证券调入调出信息，包括标的类别... | [查看](tableInfo/Opt_ULAComponent.json) |
| `Opt_ULAContract` | 期权品种 | 1.内容说明：本表收录国内交易所发布的期权品种合约的基本信息。具体包含上海证券交易所发布的股票期权、深交所发布的沪... | [查看](tableInfo/Opt_ULAContract.json) |

## QT - 行情/交易数据

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `QT_AdjustingFactor` | 复权因子表 | 1.收录股票、基金等因为分红配股发生除权除息行为，衍生计算出的精确复权因子、精确复权常数、比例复权因子等指标，其中... | [查看](tableInfo/QT_AdjustingFactor.json) |
| `QT_CSIIndexQuote` | 中证指数行情 | 1.收录了所有中证指数有限公司发布及转发的股票指数、债券指数、可转债指数、基金指数、期货指数、组合资产指数、其他指... | [查看](tableInfo/QT_CSIIndexQuote.json) |
| `QT_CommIndexQuote` | 商品指数行情 | 1.内容说明：本表记录国内主流商品指数发布方发布的商品指数每日的行情数据，包括高、开、低、收、结算价等信息。 2.... | [查看](tableInfo/QT_CommIndexQuote.json) |
| `QT_ConceptQuote` | 概念行情 | 1.收录了概念每日的行情数据，包括了常用指数的高、开、低、收等信息； 2.历史数据：2016年2月29日至今； 3... | [查看](tableInfo/QT_ConceptQuote.json) |
| `QT_DailyQuote` | 日行情表 | 1.收录股票、债券（不包含银行间交易的债券）、基金、指数每个交易日收盘行情数据，包括昨收盘、今开盘、最高价、最低价... | [查看](tableInfo/QT_DailyQuote.json) |
| `QT_FundsPerformance` | 上市基金最新行情 | 1.本表记录展示在交易所交易的封闭式基金、LOF等，从最近一个交易日往前追溯一段时期的行情表现信息，包括当日、近1... | [查看](tableInfo/QT_FundsPerformance.json) |
| `QT_FundsPerformanceHis` | 上市基金历史行情 | 1.展示在交易所交易的封闭式基金、LOF等，历史行情表现信息，包括当日、近1周、近1月、近1年的表现情况。 2.本... | [查看](tableInfo/QT_FundsPerformanceHis.json) |
| `QT_GoldTradeMarket` | 上海黄金交易所交易行情 | 1.收录上海黄金交易所下黄金、白银、铂等金属标准化交易的每日盘后行情，包括开盘价、收盘价、最高价、最低价、成交量、... | [查看](tableInfo/QT_GoldTradeMarket.json) |
| `QT_HKDailyQuote` | 港股行情库表 | 1.香港联合交易所交易日行情报价盘后数据。包含主要字段有：最高价、最低价、开盘价、昨收盘价、收盘价、涨跌幅、交易单... | [查看](tableInfo/QT_HKDailyQuote.json) |
| `QT_HKDailyQuoteIndex` | 港股行情指标表 | 1.记录随港股行情变动的重要指标，包含的字段有：最小变动价格、港股股数、非港股股数、市盈率、动态市盈率、滚动市盈率... | [查看](tableInfo/QT_HKDailyQuoteIndex.json) |
| `QT_IndexPerformance` | 指数行情表现 | 1.内容说明：收录指数从最近一个交易日往前追溯一段时期的行情表现信息，包括近1周、1周以来、近1月、1月以来、近3... | [查看](tableInfo/QT_IndexPerformance.json) |
| `QT_IndexQuote` | 指数行情 | 1.收录了指数每日的行情数据，包括了国内指数发布机构发布的常用指数的高、开、低、收等信息； 2.使用说明：交易所指... | [查看](tableInfo/QT_IndexQuote.json) |
| `QT_InterestRateIndex` | 利率指数行情 | 1.收录了以1000点为基数，按照人民币利率，计算活期存款、三个月定存、半年定存、一年定存、二年定存、三年定存、五... | [查看](tableInfo/QT_InterestRateIndex.json) |
| `QT_MonthData` | 股票月度行情数据 | 1.收录证券每月最后一个日期的收盘价及相关股本财务指标，如流通股本、总股本、市盈率TTM，市净率等。 2.数据范围... | [查看](tableInfo/QT_MonthData.json) |
| `QT_NewestPerformance` | 股票最新行情表现 | 1. 收录股票最新交易日的行情表现信息，包括本周以来、近1周，本月以来、近1月，近3月，近半年，本年以来、近1年，... | [查看](tableInfo/QT_NewestPerformance.json) |
| `QT_OSIndexQuote` | 境外指数行情(含香港) | 1.主要收录了境外指数发布方(如标普、MSCI等)发布/提供的指数行情；以及在港交所、台交所、纽交所、新加坡交易所... | [查看](tableInfo/QT_OSIndexQuote.json) |
| `QT_Performance` | 股票行情表现 | 1.收录股票从最近一个交易日往前追溯一段时期的行情表现信息，包括近1周、1周以来、近1月、1月以来、近3月、近半年... | [查看](tableInfo/QT_Performance.json) |
| `QT_PerformanceData` | 股票日行情表现 | 1.收录A股行情表现相关的一些特色指标数据，如连涨天数、是否破发、是否破净、是否创历史新高或新低等指标，其中判断是... | [查看](tableInfo/QT_PerformanceData.json) |
| `QT_PriceLimit` | 股票涨跌停价 | 1.内容说明：存储股票每天的涨停价和跌停价，盘前提供。 2.数据范围：2020年9月-至今。 3.信息来源：上交所... | [查看](tableInfo/QT_PriceLimit.json) |
| `QT_SHSZHSCTradingDay` | 沪(深)港通交易日 | 1.反映沪港通和深港通交易日的基本属性和补充属性。 2.历史数据：沪股通2014年11月17日起，深股通2016年... | [查看](tableInfo/QT_SHSZHSCTradingDay.json) |
| `QT_StockAdjustFactor` | 股票复权因子 | 1.收录A股因发生除权除息行为，基于行情计算出的比例复权因子指标，可用于推算股票前复权或后复权价格，该算法适合进行... | [查看](tableInfo/QT_StockAdjustFactor.json) |
| `QT_StockPerformance` | 股票行情表现(新) | 1.内容说明： 收录股票从最近一个交易日往前追溯一段时期的行情表现信息，包括近1周、1周以来、近1月、1月以来、近... | [查看](tableInfo/QT_StockPerformance.json) |
| `QT_TradingCapitalFlow` | 股票交易资金流向 | 1.展示每个交易日在深沪交易所交易的股票，在不同单笔成交金额区间的累计主买、主卖金额及成交量情况。 流入量（金额）... | [查看](tableInfo/QT_TradingCapitalFlow.json) |
| `QT_TradingDayNew` | 交易日表(新) | 本表收录各个市场的交易日信息，包括每个日期是否是交易日，是否周、月、季、年最后一个交易日 | [查看](tableInfo/QT_TradingDayNew.json) |

## RF - 回购/融资

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `RF_ConvRateBy` | 可充抵保证金证券折算率 | 1.收录中证金公司每日披露的转融通可充抵保证金证券的折算率数据。 2.历史数据：2012年8月起-至今 3.数据来... | [查看](tableInfo/RF_ConvRateBy.json) |
| `RF_FTradingSum` | 转融资交易汇总 | 1.收录中证金公司每日披露的沪深市场上转融资交易汇总。信息包含转融资的起初余额、偿还金额和期末金额，从转融资期限看... | [查看](tableInfo/RF_FTradingSum.json) |
| `RF_Participant` | 转融通参与人名单 | 1.收录中证金公司披露的转融通参与人名单，包括出借人—代理证券公司和借入人—转融资借入人和转融券借入的当前清单以及... | [查看](tableInfo/RF_Participant.json) |
| `RF_STradingDetail` | 转融券交易明细 | 1.收录中证金公司披露的转融券（含3天、7天、14天、28天、182天五种）交易明细数据。 2.历史数据：2012... | [查看](tableInfo/RF_STradingDetail.json) |
| `RF_STradingSum` | 转融券交易汇总 | 1.记录中证金公司每日披露的转融券交易汇总，包括期初、期末的余量、余额及转融券融出数量等。 2.历史数据：2012... | [查看](tableInfo/RF_STradingSum.json) |
| `RF_TargetSecurities` | 转融通标的证券 | 1.收录中证金公司披露的转融通标的证券的当前清单，以及历次入选和剔除转融通标的变化情况。 2.历史数据：2012年... | [查看](tableInfo/RF_TargetSecurities.json) |
| `RF_TermFeeRate` | 转融通期限费率 | 1.收录中证金公司每日披露的转融通（转融资和转融券）的转融入和转融出年利率。 2.历史数据：2012年8月起-至今... | [查看](tableInfo/RF_TermFeeRate.json) |

## SIF - 结构性产品/衍生品

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `SIF_FinancefutureQuote` | 期货行情及统计 | 1.内容说明：本表收录海内外市场广泛关注的商品期货及金融期货的日收盘类行情及月度、年末的统计数据。其中：日行情类，... | [查看](tableInfo/SIF_FinancefutureQuote.json) |

## SM - 市场宏观指标

| 表名 | 中文名称 | 说明 | 字段详情 |
| --- | --- | --- | --- |
| `SM_ABSMRegSta` | 资产证券化管理人已备案产品统计 | 1.收录资产证券化管理人已备案产品规模和产品数量情况。 2.数据范围：2016.6-2017.3 3.信息来源：中... | [查看](tableInfo/SM_ABSMRegSta.json) |
| `SM_CSCRMember` | 证监会机构委员情况 | 1.收录各届次证监会发审委委员、证监会并购重组委委员及交易所涉及上市委员会委员等 2.数据范围：2003.12-至... | [查看](tableInfo/SM_CSCRMember.json) |
| `SM_EmployeeSta` | 证券市场从业人员统计 | 1.本表收录各个证券金融机构的从业人员分布情况，包括从业人员数量、证券经纪人数量、保荐代表人数量、投资主办人数量等... | [查看](tableInfo/SM_EmployeeSta.json) |
| `SM_Investor` | 证券市场投资者统计 | 1.本表记录中国结算公司定期披露的证券市场上投资者的主要数据，包括新增投资者、期末投资者、期末持仓投资者、期末参与... | [查看](tableInfo/SM_Investor.json) |
| `SM_MainIndicator` | 证券市场指标概览 | 1.本表记录中国结算公司定期披露的证券市场主要指标数据。中国结算登记所披露数据随着时间推移而内容有所变化。2015... | [查看](tableInfo/SM_MainIndicator.json) |
| `SM_PledRepMPR` | 股票质押回购市场质押率 | 1.本表记录沪深两市股票质押回购每周的平均质押率，包括无限售条件股份质押率、有限售条件股份质押率。 2.数据范围：... | [查看](tableInfo/SM_PledRepMPR.json) |
| `SM_PledRepPD` | 股票质押回购质押明细 | 1.本表记录的证券范围包括Ａ股股票，不含基金、债券；质押数量包括场内质押和场外质押，深市不包括场内股票质押式回购交... | [查看](tableInfo/SM_PledRepPD.json) |
| `SM_PledRepTSta` | 股票质押回购交易状态 | 1.本表记录暂停或恢复股票用于质押式回购交易的情况。 2.数据范围：2015.4-至今 3.信息来源：深交所。 | [查看](tableInfo/SM_PledRepTSta.json) |
| `SM_PledRepTraTD` | 股票质押回购交易明细 | 1.本表记录股票质押回购个股交易状态和交易数量等。 2.数据范围：2014.3-至今 3.信息来源：上交所、深交所 | [查看](tableInfo/SM_PledRepTraTD.json) |
| `SM_PledRepTraTV` | 股票质押回购交易总量 | 1.本表记录沪深两市股票质押回购总体交易情况，包括初始交易金额、购回交易金额等指标。 2.数据范围：2014.3-... | [查看](tableInfo/SM_PledRepTraTV.json) |
| `SM_PromRepTraTV` | 股票约定购回式证券交易总量 | 1.本表记录约定购回式证券交易总体情况。 2.数据范围：2014.3-至今 3.信息来源：上交所、深交所 | [查看](tableInfo/SM_PromRepTraTV.json) |
| `SM_SecuAccount` | 证券市场账户 | 1.收录国内证券市场基本帐户、开户代理机构情况数据，包括累计开户、新增开户、累计销户、新增销户等大类指标。 2.数... | [查看](tableInfo/SM_SecuAccount.json) |
| `SM_SecuCAMSRank` | 证券公司资产管理规模排名 | 1.收录每季度末，不同细分项下证券公司的资产管理规模排名情况（从2015年第四季度末开始只披露前20名） 2.数据... | [查看](tableInfo/SM_SecuCAMSRank.json) |
| `SM_SecuCAMSize` | 证券公司资产管理业务规模 | 1.本表记录证券公司资产管理业务的相关产品数量和资产规模等统计情况，包括产品数量、资产规模等大类指标。 2.数据范... | [查看](tableInfo/SM_SecuCAMSize.json) |
| `SM_SecuTrading` | 证券市场交易 | 1.收录国内证券市场交易情况数据，包括交易对象、市盈率/换手率、交易同比等大类指标 2.数据范围：1997-至今 ... | [查看](tableInfo/SM_SecuTrading.json) |

