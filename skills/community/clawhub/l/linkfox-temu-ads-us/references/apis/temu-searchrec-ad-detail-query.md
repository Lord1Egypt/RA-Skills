# 广告详情查询 — `temu.searchrec.ad.detail.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_ads_searchrec_ad_detail_query.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=1e72b5cceef545ec8f9652b9e56dd054&sub_menu_code=66db5438c37446f49c122829489ac6d4 |
| **网关** | `POST /temu/proxy`，`type`=`temu.searchrec.ad.detail.query`，业务载荷放在 Body 的 `params` |

**Description:** Query ad detail by goods list.

> **`goodsList`**（LONG[]）必填，单次传入 goodsId 列表。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── goodsList (LONG[], 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsList | LONG[] | **是** | Goods list |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "goodsList": [
      100001,
      100002
    ]
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
    └── adsDetail[]
        ├── goodsId, roas, budget, adShowStatus, adPhase
        ├── summary (OBJECT)
        ├── reportsSummaryDTO (OBJECT)
        └── siteStatusInfoList[]
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
| adsDetail | OBJECT[] | Ad detail per goods |

#### `adsDetail[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | Goods id |
| roas | LONG/NUMBER | Current ROAS setting |
| budget | LONG/NUMBER | Ad budget |
| adShowStatus | INTEGER | Ad show status |
| adPhase | INTEGER | Ad phase |
| summary | OBJECT | Metrics summary（结构同 [reports.mall.query](./temu-searchrec-ad-reports-mall-query.md) 之 `summary`） |
| reportsSummaryDTO | OBJECT | Aggregated report metrics（全量汇总，字段均为 `*All.val`） |
| siteStatusInfoList | OBJECT[] | Per-site ad status |

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

#### `reportsSummaryDTO`

| 参数 | 类型 | 说明 |
|------|------|------|
| clkCntAll | OBJECT | `val` — all clicks |
| orderPayCntAll | OBJECT | `val` — all order pay count |
| adSpendAll | OBJECT | `val` — all ad spend |
| acosAll | OBJECT | `val` |
| ctrAll | OBJECT | `val` |
| imprCntAll | OBJECT | `val` |
| orderPayAmtAll | OBJECT | `val` |
| cartCntAll | OBJECT | `val` |
| roasAll | OBJECT | `val` |

#### `siteStatusInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| adShowStatus | INTEGER | Ad show status for site |
| forbidReason | STRING | Forbid reason if not shown |
| siteNameList | STRING[] | Site names |

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
python scripts/us_ads_searchrec_ad_detail_query.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"goodsList": [100001, 100002]}}'
```

**典型流程：** 按 **`goodsList`** 查投放状态、预算、ROAS 与报表摘要。
