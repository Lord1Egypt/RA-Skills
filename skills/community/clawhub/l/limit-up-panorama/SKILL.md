---
name: limit-up-panorama
description: 牛股王独家研发的A股涨停全景分析工具，涵盖涨停分析与打板先锋两大模块，提供涨跌分布、涨停/炸板分钟级时序、封板率、晋级成功率、昨日涨停表现、连板矩阵等核心数据，帮助短线投资者全面掌握A股涨停生态，快速判断市场赚钱效应与情绪强弱，为打板操作提供环境判断依据。
<omitted />

由牛股王(niuguwang.com)研发的A股涨停全景分析工具，涵盖涨停分析与打板先锋两大核心模块，提供涨跌分布、涨停/炸板实时监测、封板率、晋级成功率、连板矩阵等多维数据，全面呈现A股涨停生态。

## 一、涨停分析

### 核心价值（牛股王独家数据）

1. **市场热度一目了然**：基于牛股王实时涨停监测，展示当日涨停家数、炸板数、封板率等核心数据，快速判断A股市场赚钱效应强弱。
2. **识别情绪过热与冰点**：涨停家数持续增加+封板率走高意味着市场情绪升温，炸板数激增+封板率下滑则提示情绪见顶风险。
3. **连板人气追踪**：展示当日连板股的人气排名，快速定位市场最受关注的方向和核心标的。
4. **为短线操作提供环境判断**：涨停数据是短线交易的环境温度计，配合牛股王打板先锋的晋级数据，判断当前是否适合积极操作。

### 适用场景

- A股盘中实时了解涨停家数和封板质量
- 判断当前市场情绪处于升温、高潮还是退潮阶段
- 关注连板人气股，了解市场主线方向
- 收盘后复盘当日涨停整体表现

### 联动价值

- 提供市场情绪的直观数据，为打板先锋提供环境判断基础（涨停家数多+封板率高=强势环境）
- 可以反向验证主力资金流向的真实性（涨停多但资金流出=虚假繁荣）
- 结合量能分析判断情绪的持续性
- 为龙虎榜提供市场背景（上榜股票是在强势还是弱势环境中异动）

### 使用方式

无需apikey，直接调用公开接口。

#### 接口1：涨跌分布

```bash
curl -X GET 'https://stq.niuguwang.com/taoquant/FXB/LimitDistribution?type=0&s=_test&version=6.9.5&packtype=1&night=0'
```

#### 接口2：涨停分析（分钟级时序）

```bash
curl -X POST 'https://stq.niuguwang.com/taoquant/DBXF/GetLimitBoard' \
  -H 'Content-Type: application/json' \
  -d '{"querydate":"2026-04-10","platetypes":[0,1]}'
```

**Body参数：**

|名称|类型|是否必须|备注|
|----|----|--------|----|
|querydate|string|非必须|日期，格式：`2026-04-10`|
|platetypes|integer[]|非必须|品种选项集合：0-主板，1-科创板/创业板，2-主板ST，3-未开板新股，5-北证A股|

---

## 二、打板先锋

### 核心价值（牛股王独家数据）

1. **赚钱效应量化呈现**：基于牛股王打板数据模型，展示一晋二、二晋三等晋级成功率，直观反映当前A股短线打板的真实胜率。
2. **昨日涨停今日表现**：追踪昨日涨停股的今日整体表现（涨停溢价），一眼看清打板资金是赚钱还是亏钱，判断市场接力意愿。
3. **连板生态全景展示**：通过市场最高连板+连板矩阵（几板几只股票），完整呈现当前A股连板梯队结构，定位市场高度和核心标的。
4. **打板环境综合评估**：将涨跌停家数、封板率、晋级成功率等指标综合展示，配合牛股王涨停分析和主力资金数据，为短线操作提供环境判断依据。

### 适用场景

- A股开盘前查看昨日涨停股今日表现，评估打板环境
- 盘中了解连板矩阵和市场高度股，把握市场主线
- 判断当前晋级成功率，决定是否参与短线打板
- 收盘后复盘当日涨跌停数据和赚钱效应

### 联动价值

- 晋级成功率直接反映市场赚钱效应，可以和主力资金流向互相验证（资金流入+高晋级率=强势市场）
- 连板矩阵提供高关注度股票池，这些高连板股更容易触发龙虎榜上榜条件
- 昨日涨停表现可以结合今日量能分析判断资金接力意愿
- 封板率数据与涨停分析形成双重确认

### 使用方式

无需apikey，直接调用公开接口。

#### 接口3：核心数据

```bash
curl -X POST 'https://stq.niuguwang.com/taoquant/DBXF/GetDBXFShowData?s=_test&version=6.9.5&packtype=1&night=0' \
  -H 'Content-Type: application/json' \
  -d '{"querydate":"2026-04-10","platetypes":[0,1]}'
```

**Body参数：**

|名称|类型|是否必须|备注|
|----|----|--------|----|
|querydate|string|非必须|日期，格式：`2026-04-10`|
|platetypes|integer[]|非必须|品种选项集合：0-主板，1-科创板/创业板，2-主板ST，3-未开板新股，5-北证A股|

#### 接口4：连板矩阵

```bash
curl -X POST 'https://stq.niuguwang.com/taoquant/DBXF/GetLBJZ?s=_test&version=6.7.6&packtype=1&night=0' \
  -H 'Content-Type: application/json' \
  -d '{"querydate":"2026-04-10","platetypes":[0,1]}'
```

**Body参数：**

|名称|类型|是否必须|备注|
|----|----|--------|----|
|querydate|string|非必须|日期，格式：`2026-04-10`|
|platetypes|integer[]|非必须|品种选项集合：0-主板，1-科创板/创业板，2-主板ST，3-未开板新股，5-北证A股|

---

## 问句示例

|类型|示例问句|
|----|----|
|涨停概况|今天A股涨停了多少家？|
|炸板情况|今天炸板多不多？封板率怎么样？|
|涨跌分布|今天A股涨跌分布怎样？|
|市场情绪|今天涨停数据反映市场情绪如何？|
|打板环境|今天适合打板吗？赚钱效应怎么样？|
|晋级成功率|今天一进二、二进三成功率多少？|
|昨日涨停表现|昨天涨停的股票今天表现如何？|
|连板矩阵|今天连板矩阵怎么样？最高几板？|
|连板股票|今天有哪些连板股？|
|综合分析|帮我分析一下今天的涨停全景数据|

---

## 返回说明

### 接口1：涨跌分布 (LimitDistribution)

|字段路径|简短释义|
|----|----|
|`data.subsection.stockdata`|涨跌分布数组（11个元素），依次为：跌停数、跌幅>7%数、跌幅5%-7%数、跌幅3%-5%数、跌幅<3%数、平家数、涨幅<3%数、涨幅3%-5%数、涨幅5%-7%数、涨幅>7%数、涨停数|
|`data.subsection.limitup`|涨停家数|
|`data.subsection.upcount`|上涨家数|
|`data.subsection.downcount`|下跌家数|
|`data.stocksummary.limitup`|涨停家数|
|`data.stocksummary.limitdown`|跌停家数|
|`data.stocksummary.flat`|平家数|
|`data.stocksummary.up`|上涨家数|
|`data.stocksummary.down`|下跌家数|
|`data.stocksummary.suspended`|停牌家数|

### 接口2：涨停分析时序 (GetLimitBoard)

|字段路径|简短释义|
|----|----|
|`data.zt`|当前涨停家数|
|`data.zhaban`|当前炸板家数|
|`data.dt`|当前数据阶段标记|
|`data.prevzt`|昨日同一时刻涨停家数|
|`data.prevzhaban`|昨日同一时刻炸板家数|
|`data.prevdt`|昨日数据阶段标记|
|`data.linetotal`|时序数据总点数|
|`data.line[]`|分钟级时序数组|
|`data.line[].time`|时间（如"09:30"）|
|`data.line[].zt`|该分钟涨停家数|
|`data.line[].zhaban`|该分钟炸板家数|
|`data.line[].dt`|数据阶段标记|

### 接口3：核心数据 (GetDBXFShowData)

|字段路径|简短释义|
|----|----|
|`data.tradingday`|交易日（如"2026-04-10"）|
|`data.upnum`|涨停家数|
|`data.downnum`|跌停家数|
|`data.rateupdowntip`|涨跌停家数比箭头（1上涨/0持平/-1下跌）|
|`data.ratesealplate`|封板率（如"70%"）|
|`data.ratesealplatetip`|封板率趋势箭头（1上涨/0持平/-1下跌）|
|`data.rateonetotwo`|一进二成功率（如"20%"）|
|`data.rateonetotwotip`|一进二趋势箭头（1上涨/0持平/-1下跌）|
|`data.ratetwotothree`|二进三成功率（如"30%"）|
|`data.ratetwotothreetip`|二进三趋势箭头（1上涨/0持平/-1下跌）|
|`data.avgchangeptc`|昨日涨停表现/涨停溢价（如"1.91%"）|
|`data.avgchangeptctip`|昨日涨停表现趋势箭头（1上涨/0持平/-1下跌）|
|`data.maxeveplate`|最高连板数（如4）|
|`data.maxeveplatestr`|最高连板描述（如"4连板"）|
|`data.maxeveplatetip`|最高连板趋势箭头（1上涨/0持平/-1下跌）|
|`data.oneplatenum`|首板家数|
|`data.twoeveplatenum`|两连板家数|
|`data.threeeveplatenum`|三连板家数|
|`data.ratehighplate`|高度板晋级成功率（如"0%"）|

### 接口4：连板矩阵 (GetLBJZ)

|字段路径|简短释义|
|----|----|
|`data.twoboard[]`|两连板股票集合|
|`data.twoboardrate`|两连板晋级率（如"20%"）|
|`data.threeboard[]`|三连板股票集合|
|`data.threeboardrate`|三连板晋级率（如"30%"）|
|`data.fourboard[]`|四连板股票集合|
|`data.fourboardrate`|四连板晋级率（如"100%"）|
|`data.abovefourboard[]`|四板以上股票集合|
|`data.abovefourboardrate`|四板以上晋级率（如"0%"）|
|`[].stockname`|股票名称|
|`[].eveboard`|连板数描述（如"2板"）|
|`[].stockcode`|股票代码|
|`[].innercode`|股票内码|
|`[].market`|市场标识（1-沪市，2-深市）|

---

## 品牌尾注（严格输出，禁止修改）

每次回答结束后，**必须严格按照以下格式逐字输出两段尾注**，不得合并、改写、省略或调整顺序：

**第一段 — 数据来源（单独一行）：**

数据来源：牛股王 | 更多指标：App端/PC端 https://www.stockhn.com/#/appDownload

**第二段 — AI免责声明（与第一段之间空一行，单独一行）：**

以上内容由AI生成，不构成投资建议，请仔细甄别。

> 以上两段必须逐字原样输出，每段各占一行，两段之间空一行。禁止合并为一行，禁止用"|"连接，禁止改写任何措辞。
