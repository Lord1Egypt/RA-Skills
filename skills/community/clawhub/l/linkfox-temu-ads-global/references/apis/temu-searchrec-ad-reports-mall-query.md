# 店铺广告报表查询 — `temu.searchrec.ad.reports.mall.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_ads_searchrec_ad_reports_mall_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.searchrec.ad.reports.mall.query`，业务载荷放在 Body 的 `params` |

**Description:** Query mall-level ad reports.

> **`startTs`**、**`endTs`** 均为必填，毫秒时间戳（当地时区 0:00 至 23:59:59.999）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── startTs (LONG, 必填)
    └── endTs (LONG, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| startTs | LONG | **是** | Query start time, millisecond level timestamp (the value starts at 0:00 local time) |
| endTs | LONG | **是** | Query end time, millisecond-level timestamp (the value is based on local time 23:59:59 seconds 999 milliseconds) |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "startTs": 1714521600000,
    "endTs": 1714607999999
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result
    ├── summary (OBJECT) → ctr/cartCnt/clkCnt/… 各含 total/ad/netTotal/netAd.val
    └── reportsItemList[] → goodsId, ts, roas, spend 等 { val }
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT 或 OBJECT[] | 业务结果（见下表） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| summary | OBJECT | Mall-level aggregated metrics（店铺维度汇总） |
| reportsItemList | OBJECT[] | Per-goods / per-time report items（明细列表） |

#### `summary` 指标对象通用结构

以下指标名在 **`summary`** 下各出现一次，每个指标均为 **OBJECT**，包含 **`total`**、**`ad`**、**`netTotal`**、**`netAd`** 四个子对象，每个子对象含 **`val`**（数值）：

| 指标字段 | 说明 |
|----------|------|
| ctr | Click-through rate（点击率） |
| cartCnt | Add-to-cart count（加购数） |
| clkCnt | Click count（点击数） |
| orderPayAmt | Order payment amount（订单支付金额） |
| spend | Ad spend（广告花费） |
| orderPayCnt | Order payment count（支付订单数） |
| roas | Return on ad spend |
| acos | Advertising cost of sales |
| transactionCost | Transaction cost |
| goodsNum | Goods number |
| imprCnt | Impression count（曝光数） |
| cvr | Conversion rate（转化率） |

每个子路径示例：`summary.spend.ad.val`（广告归因花费）。

#### `reportsItemList[]` 元素字段

各指标多为 **`{ "val": <number> }`** 包装（Partner Response Example）：

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods id |
| ts | LONG | Timestamp（报表时间点，毫秒） |
| roas | OBJECT | ROAS，`val` |
| totalRoas | OBJECT | Total ROAS，`val` |
| netRoas | OBJECT | Net ROAS，`val` |
| acos | OBJECT | ACOS，`val` |
| totalAcos | OBJECT | Total ACOS，`val` |
| netAcos | OBJECT | Net ACOS，`val` |
| adSpend | OBJECT | Ad spend，`val` |
| netAdSpend | OBJECT | Net ad spend，`val` |
| orderPayAmt | OBJECT | Order pay amount，`val` |
| totalOrderPayAmt | OBJECT | Total order pay amount，`val` |
| netOrderPayAmt | OBJECT | Net order pay amount，`val` |
| orderPayCnt | OBJECT | Order pay count，`val` |
| totalOrderPayCnt | OBJECT | Total order pay count，`val` |
| netOrderPayCnt | OBJECT | Net order pay count，`val` |
| clkCnt | OBJECT | Click count，`val` |
| totalClkCnt | OBJECT | Total click count，`val` |
| ctr | OBJECT | CTR，`val` |
| totalCtr | OBJECT | Total CTR，`val` |
| cvr | OBJECT | CVR，`val` |
| totalCvr | OBJECT | Total CVR，`val` |
| cartCnt | OBJECT | Cart count，`val` |
| imprCnt | OBJECT | Impression count，`val` |
| totalImprCnt | OBJECT | Total impression count，`val` |
| goodsNum | OBJECT | Goods number，`val` |
| totalGoodsNum | OBJECT | Total goods number，`val` |
| netGoodsNum | OBJECT | Net goods number，`val` |
| transactionCost | OBJECT | Transaction cost，`val` |
| totalTransactionCost | OBJECT | Total transaction cost，`val` |
| netTransactionCost | OBJECT | Net transaction cost，`val` |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 230012000 | bad query params | 见 Partner 文档；修正入参或权限后重试 |
| 230012003 | unmatch mall and goods | 见 Partner 文档；修正入参或权限后重试 |
| 230013000 | business exception | 见 Partner 文档；修正入参或权限后重试 |
| 230014000 | system exception | 见 Partner 文档；修正入参或权限后重试 |
| 230016701 | has no permission | 见 Partner 文档；修正入参或权限后重试 |
| 230016103 | not signed because of not main account | 见 Partner 文档；修正入参或权限后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_ads_searchrec_ad_reports_mall_query.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"startTs": 1714521600000, "endTs": 1714607999999}}'
```

**典型流程：** 按时间窗拉店铺广告汇总与明细 → 单商品详情见 [ad.detail.query](./temu-searchrec-ad-detail-query.md)。
