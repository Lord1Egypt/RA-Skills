---
name: valuescan-skill-beta
description: ValueScan 加密货币主力资金流分析工具。支持资金异动监控、主力动向追踪、鲸鱼地址分析、板块轮动、机会/风险代币识别、大户成本分析。
version: 1.0.7
user-invocable: true
category: Data Analysis
license: MIT
homepage: https://beta.valuescan.io
dependencies:
  - node: 16.x
tags:
  - cryptocurrency
  - data analysis
  - blockchain
  - finance
documentation: |
  该 Skill 用于对加密货币市场进行分析，帮助用户识别资金流向、主力动向等信息。
support_email: support@openclaw.com
website: https://beta.valuescan.io
credentials:
  api_key:
    description: 用于认证的 API 密钥
    required: true
  secret_key:
    description: 用于认证的 Secret 密钥
    required: true
---

# ValueScan API

加密货币主力资金流动向分析 API，追踪大户资金动向，让数据成为你的交易副驾驶。

## 使用场景示例

| 场景           | 通过 Skill 实现                                              |
| -------------- | ------------------------------------------------------------ |
| **行情信号**   | 用户问：“最近有哪些币出现主力异动？” →  调用 `资金异动列表` 返回结果。<br>用户问：“BTC主力资金异动信号有哪些？”→ Skill 调用 `资金异动消息` 返回结果。 |
| **行情信号**   | 用户问：“最近有哪些币可能上涨” →  调用 `资金异动列表`和  `机会代币列表`返回结果并说明场景     <br/>用户问：“BTC机会信号有哪些？”→ Skill 调用 `机会代币消息` 返回结果。 |
| **链上监控**   | 用户设置：“当 ETH 出现超过 1000 ETH 的大额转账时通知我。” →  调用 `大额交易` 实现实时监控。 |
| **投资决策**   | 用户问：“BTC 现在的压力位和支撑位在哪？” →  调用 `压力支撑位` 提供数据。 |
| **资金面分析** | 用户问：“过去一周，AI 板块的资金流向如何？” →  调用 `板块资金列表` 获取板块轮动数据。 |
| **地址分析**   | 用户提供地址：“帮我分析这个地址的持仓成本变化。” →  调用 `持仓趋势` 返回建仓成本曲线。 |

## 接口列表

### 基础数据

| 接口         | 用途                                              |
| ------------ | ------------------------------------------------- |
| 代币列表     | 搜索代币，获取对应的 `vsTokenId` 等基础标识信息。 |
| 代币基本信息 | 获取代币的实时价格、市值、`coinKey` 等详细信息。  |
| K线数据      | 支持多时间窗口的 K 线数据查询，用于技术分析。     |

### AI智选

AI综合多维度数据，追踪当前行情下的具有上涨机会或有下跌风险的代币，并实时追踪主力行为，提供实时追踪信号，辅助市场判断。

| 接口         | 用途                                                   |
| ------------ | ------------------------------------------------------ |
| 机会代币列表     | 追踪当前行情下具有上涨潜力的代币                       |
| 机会代币消息     | 上涨潜力币的主力动向实时信号（如吸筹、突破、出逃等）。 |
| 风险代币列表     | 当前行情下具有下跌风险趋势的代币                       |
| 风险代币消息     | 下跌风险币的主力动向实时信号（如派发、破位、反弹等）。 |
| 资金异动列表     | 上涨或震荡行情中资金活跃且具有短期套利潜力的代币       |
| 资金异动消息     | 短线/趋势异动的实时信号（如主力入场、抛压等）。        |

### 交易所主力资金监控

监控中心化交易所（现货/合约）的资金流数据，追踪主力动向。

| 接口           | 用途                                            |
| -------------- | ----------------------------------------------- |
| 实时资金积累       | 当日资金变化监控，反映主力实时流入/流出。       |
| 资金快照           | 最近100天的资金积累趋势，用于中长期资金面分析。 |
| 资金市值比         | 资金流入强度判断，辅助识别资金与市值匹配度。    |
| 板块资金列表       | 板块轮动资金监控，快速定位热点赛道。            |
| 板块代币资金       | 板块内龙头代币的实时资金积累数据。              |

### 链上主力资金监控

交易所的充/提资金监控，以及链上大户持仓成本变化监控，辅助主力行为追踪

| 接口     | 用途                                          |
| -------- | --------------------------------------------- |
| 代币流向     | 链上与交易所之间的资金交互监控（交易所的充提数据） |
| 主力成本变化趋势 | 大户平均持仓成本分析，识别主力建仓/出货位置。 |

### 市场指标

valuescan特色指标数据，对关键位置具有重要参考价值

| 接口         | 用途                                        |
| ------------ | ------------------------------------------- |
| 主力行为指标     | BTC/ETH 趋势判断，提供主力买卖行为信号。    |
| 压力支撑位     | 关键价格位置（支撑/压力）计算，辅助交易决策 |
| 社媒情绪        | 多空情绪分析，基于社交媒体热度与情绪指数。  |

### 链上大额交易

链上巨鲸交易监控，实时预警。

| 接口     | 用途                         |
| -------- | ---------------------------- |
| 大额交易     | 鲸鱼在多链上的转账交易监控。 |

### 链上持仓地址数据

| 接口           | 用途                                           |
| -------------- | ---------------------------------------------- |
| 持币地址           | 筹码集中度分析，查看地址数量与持仓分布。       |
| 余额趋势         | 指定地址的持仓变化历史。                       |
| 盈亏趋势         | 指定地址的投资绩效（盈利/亏损情况）。          |
| 持仓成本趋势 | 指定地址的建仓成本分析（均价变化）。           |
| 交易行为趋势 | 指定地址的交易活跃度（转账次数、频率）。       |

---

## 接口参考文件结构

`references/` 目录下的每个接口 JSON 文件均遵循统一结构，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 接口中文名称 |
| `endpoint` | string | HTTP方法 + API路径（如 `POST /trade/getCoinTrade`） |
| `description` | string | 接口功能描述 |
| `credits_cost` | integer | 调用该接口消耗的积分数量 |
| `needToken` | boolean | 是否需要认证（true/false） |
| `use_case` | string | 业务使用场景说明，包含接口适用场景和使用建议 |
| `notes` | string | 调用注意事项和重要提醒 |
| `update_frequency` | string | 数据更新频率（如 `实时更新`） |
| `typeNote` | string | 类型转换说明（如部分数值字段实际返回字符串） |
| `params` | object | 请求参数定义，key 为参数名，value 含 `type`、`req`、`desc` |
| `response` | object | 响应字段定义，含 `type`、`actualType`、`desc` |
| `field_meta` | object | 字段业务含义，含 `meaning`（业务定义）、`range`（取值范围）、`advice`（使用建议） |
| `enums` | object | 枚举值映射表，定义关键字段的可选值含义 |
| `example` | object | 请求/响应示例，含 `req`（请求体）和 `res`（响应体） |

### 字段类型说明

| type 值 | 说明 |
|---------|------|
| `long` / `integer` | 整数类型 |
| `number` | 数值类型（可能实际返回字符串） |
| `string` | 字符串类型 |
| `boolean` | 布尔类型 |
| `array` | 数组类型，含 `item` 定义元素结构 |

### 关键字段解析

#### 调用前必读字段

| 字段 | 说明 |
|------|------|
| `params` | 请求参数定义，`req: true` 表示必填参数，`req: false` 表示可选参数。调用接口前必须检查并填入所有必填参数。 |
| `notes` | 调用注意事项，包含接口使用限制、数据范围、业务约束等重要提示。必须阅读后再发起请求。 |
| `enums` | 枚举值映射表。某些字段（如 `tradeType`、`timeParticleEnum`）使用数字编码，需参照此表转换为实际含义，或从 `references/enums.json` 加载标准枚举定义。 |

#### 返回解读字段

| 字段 | 说明 |
|------|------|
| `response` | 响应字段定义，包含字段名、`type`（声明类型）、`actualType`（实际类型）、`desc`（字段含义）。用于解析返回数据的结构和含义。 |
| `field_meta` | 核心业务字段解读，提供字段的 `meaning`（业务定义）、`range`（取值范围）、`advice`（使用建议）。解读返回数据时优先参考此字段。 |
| `typeNote` | 类型转换说明。部分接口的数值字段声明为 `number` 但实际返回 `string`，使用前需注意类型转换。 |
| `example` | 请求/响应示例，包含 `req`（标准请求体格式）和 `res`（典型响应数据结构）。用于验证请求格式和理解返回数据。 |

---

## 快速开始

**Base URL**: `https://api-beta.valuescan.io/api/open/v1`

**认证**: HMAC-SHA256 签名

```

X-API-KEY: 你的API Key
X-TIMESTAMP: 13位毫秒时间戳
X-SIGN: HMAC-SHA256(secret=Secret Key, message=timestamp+body_json)

````

**API Key**: 访问 <https://beta.valuescan.io/dev-portal/home/> 注册：

```json
{ 
  "valuescanApiKey": "你的API Key", 
  "valuescanSecretKey": "你的Secret Key" 
}
````

**签名约束**: Raw Body 必须与请求体完全一致，禁止格式化 | 签名SDK: `sdk/README.md`

---

## 核心参数

| 参数                 | 说明                                       | 获取方式                                                                                                                                                    |
| ------------------ | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `vsTokenId`        | 代币唯一标识                                   | 1. 调用 `/vs-token/list` 接口（参数 `search` 传代币符号如 `BTC`）；2. 从返回数据的 `id` 字段获取；3. 示例：`{ "id": 1, "symbol": "BTC", "name": "Bitcoin" }` 中 `id=1` 即为 `vsTokenId` |
| `coinKey`          | 链上代币标识（格式： `{symbol}_{contractAddress}`） | 1. 先通过 `vsTokenId` 调用 `/vs-token/detail` 接口；2. 从返回的 `chainAddresses[].coinKey` 获取；3. 示例：`BTC` 返回 `"BTC_BTC"`，`ETH` 返回 `"ETH_0x..."`（原生代币无合约地址）          |
| `address`          | 链上钱包地址                                   | 1. 调用 `持币地址` 接口获取某代币的持币地址列表；2. 或由用户直接提供；3. 格式为区块链标准地址（如 `0x...` 开头的以太坊地址）                                                                               |
| `timeParticleEnum` | 时间粒度编码                                   | 按分析周期选择：`5`=5分钟, `15`=15分钟, `101`=1小时, `104`=4小时, `124`=24小时, `201`=1天, `207`=7天, `230`=30天                                                             |
| `tradeType`        | 交易类型                                     | `1`=现货市场, `2`=合约/永续市场                                                                                                                                   |

### 参数获取示例

```
# 场景：用户查询 BTC 的主力资金数据

Step 1: 调用代币列表接口
POST /vs-token/list
Body: { "search": "btc" }
响应: { "id": 1, "symbol": "BTC", "name": "Bitcoin" }
      → 获取 vsTokenId = 1

Step 2: 调用代币详情（可选，获取coinKey）
POST /vs-token/detail
Body: { "vsTokenId": 1 }
响应: chainAddresses[0].coinKey = "BTC_BTC"
      → 获取 coinKey = "BTC_BTC"（用于链上数据查询）

Step 3: 使用 vsTokenId 调用目标接口
POST /trade/getCoinTrade
Body: { "vsTokenId": 1, "tradeType": 1 }
```

---

## 目录结构

```
valuescan-skill-beta/
├── SKILL.md                          # 技能文档
├── _meta.json                        # 元信息
├── references/                       # 接口参考文件
│   ├── enums.json                    # 通用枚举定义
│   │
│   ├── base/                         # 基础数据
│   │   ├── token-list.json           # 代币列表
│   │   ├── token-detail.json         # 代币详情
│   │   └── kline.json                # K线数据
│   │
│   ├── ai/                           # AI智选
│   │   ├── chance-coin-list.json     # 机会代币列表
│   │   ├── chance-coin-messages.json # 机会代币消息
│   │   ├── risk-coin-list.json       # 风险代币列表
│   │   ├── risk-coin-messages.json   # 风险代币消息
│   │   ├── funds-coin-list.json      # 资金异动列表
│   │   └── funds-coin-messages.json  # 资金异动消息
│   │
│   ├── fund/                         # 主力资金
│   │   ├── realtime-fund.json        # 实时资金积累
│   │   ├── fund-snapshot.json        # 资金快照
│   │   ├── marketcap-ratio.json      # 资金市值比
│   │   ├── coin-flow.json            # 代币流向
│   │   └── cost.json                 # 主力成本
│   │
│   ├── category/                     # 板块资金
│   │   ├── category-list.json        # 板块资金列表
│   │   └── category-tokens.json      # 板块代币资金
│   │
│   ├── indicator/                    # 市场指标
│   │   ├── price-market.json         # 主力行为指标
│   │   ├── dense-area.json           # 压力支撑位
│   │   └── sentiment.json            # 社媒情绪
│   │
│   └── chain/                        # 链上数据
│       ├── large-trade.json          # 大额交易
│       ├── holders.json              # 持币地址
│       ├── balance-trend.json        # 余额趋势
│       ├── profit-loss-trend.json    # 盈亏趋势
│       ├── hold-trend.json           # 持仓趋势
│       └── trade-count-trend.json    # 交易数量趋势
│
└── script/
    └── sdk/                          # 签名SDK
        ├── README.md                 # SDK说明
        └── vs_api_sign.js            # JavaScript签名
```

---

## 运行环境说明

| 项目    | 说明                                       |
| ----- | ---------------------------------------- |
| SDK依赖 | Node.js: 内置crypto/fetch，无需额外依赖           |
| 运行时要求 | Node.js 16+                              |
| 本地资源  | references/ 目录下的 JSON 文件仅供接口定义参考，运行时无需加载 |
| 安装安全性 | 本 Skill 无外部下载行为，所有依赖均为标准库或常用包            |

---

## API 文档

详细 API 文档请参考：[https://beta-claw.valuescan.io/zh-CN/](https://beta-claw.valuescan.io/zh-CN/)

