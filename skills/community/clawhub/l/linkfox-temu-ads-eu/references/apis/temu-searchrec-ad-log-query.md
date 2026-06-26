# 广告操作日志查询 — `temu.searchrec.ad.log.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_ads_searchrec_ad_log_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.searchrec.ad.log.query`，业务载荷放在 Body 的 `params` |

**Description:** Query ad operation logs for a goods.

> **`goodsId`**、**`startTime`**、**`endTime`** 均为必填（毫秒时间戳，规则同报表查询）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── goodsId (LONG, 必填)
    ├── startTime (LONG, 必填)
    └── endTime (LONG, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | **是** | Goods id |
| startTime | LONG | **是** | Query start time, millisecond level timestamp (the value starts at 0:00 local time) |
| endTime | LONG | **是** | Query end time, millisecond-level timestamp (the value is based on local time 23:59:59 seconds 999 milliseconds) |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "goodsId": 100001,
    "startTime": 1714521600000,
    "endTime": 1714607999999
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result[]
    ├── eventType (STRING)
    ├── updateSellerName (STRING)
    ├── changeInfo (STRING)
    └── updatedAt (STRING)
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT 或 OBJECT[] | 业务结果（见下表） |

### `result`（OBJECT[]）

Partner Response Example 中 **`result`** 直接为数组。

| 参数 | 类型 | 说明 |
|------|------|------|
| eventType | STRING | Event type（操作事件类型） |
| updateSellerName | STRING | Seller name who made the change |
| changeInfo | STRING | Change information（变更内容描述） |
| updatedAt | STRING | Update time（更新时间，Example 为字符串） |

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
python scripts/eu_ads_searchrec_ad_log_query.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"goodsId": 100001, "startTime": 1714521600000, "endTime": 1714607999999}}'
```

**典型流程：** 排查某 **`goodsId`** 广告变更历史。
