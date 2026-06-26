# 促销活动查询 — `bg.promotion.activity.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_promotion_activity_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.promotion.activity.query`，业务载荷放在 Body 的 `params` |

**Description:** Query promotion activities.

> 入参 **`activityType`** 为必填；分页使用 **`pageNumber`** / **`pageSize`**（与部分订单接口的 `pageNo` 不同）。
> 可用 **`activityStartTime`/`activityEndTime`**、**`activityStatus`**、**`activityIdList`**、**`onlyQueryJoinedActivity`** 筛选。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pageNumber (INTEGER, 必填)
    ├── activityEndTime (LONG, 否)
    ├── activityIdList (LONG[], 否)
    ├── activityStatus (INTEGER, 否)
    ├── pageSize (INTEGER, 必填)
    ├── activityStartTime (LONG, 否)
    ├── activityType (INTEGER, 必填)
    └── onlyQueryJoinedActivity (BOOLEAN, 否)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNumber | INTEGER | **是** | page number for pagination, default is 1. |
| activityEndTime | LONG | 否 | end time for querying activity, in seconds. |
| activityIdList | LONG[] | 否 | unique identifier for the activity |
| activityStatus | INTEGER | 否 | the status of activity 1 - Not started 2 - Ongoing 3 - Ended |
| pageSize | INTEGER | **是** | Page size for pagination, default is 10, max is 100. |
| activityStartTime | LONG | 否 | start time for querying activity, in seconds. |
| activityType | INTEGER | **是** | the type of activity 2 - lightning deals 13 - advanced big sale 27 - Clearance deals 100 - official big sale |
| onlyQueryJoinedActivity | BOOLEAN | 否 | whether to query only joined activities. TRUE / FALSE |

#### `activityType`（必填）

| 值 | 说明 |
|----|------|
| `2` | lightning deals |
| `13` | advanced big sale |
| `27` | Clearance deals |
| `100` | official big sale |

#### `activityStatus`（入参筛选）

| 值 | 说明 |
|----|------|
| `1` | Not started |
| `2` | Ongoing |
| `3` | Ended |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "pageNumber": 1,
    "pageSize": 20,
    "activityType": 2,
    "activityStatus": 2,
    "onlyQueryJoinedActivity": false
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result
    ├── total (LONG)
    └── activityList[]
        ├── activityId (LONG)
        ├── activityName (STRING)
        ├── activityType (INTEGER)
        ├── activityStatus (INTEGER)
        ├── activityStartTime (LONG)
        ├── activityEndTime (LONG)
        └── isJoinedActivity (BOOLEAN)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT 或 OBJECT[] | 业务结果（见下表；**goods.operation.query** 的 `result` 为数组） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| total | LONG | Total number of matching activities（匹配活动总数） |
| activityList | OBJECT[] | Activity list（活动列表） |

#### `activityList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| activityId | LONG | unique identifier for the activity（活动 ID） |
| activityName | STRING | Activity name（活动名称） |
| activityType | INTEGER | the type of activity（活动类型），见入参 `activityType` 枚举 |
| activityStatus | INTEGER | the status of activity（活动状态）：`1` Not started；`2` Ongoing；`3` Ended |
| activityStartTime | LONG | Activity start time in seconds（活动开始时间，秒级时间戳） |
| activityEndTime | LONG | Activity end time in seconds（活动结束时间，秒级时间戳） |
| isJoinedActivity | BOOLEAN | Whether the seller has joined the activity（卖家是否已报名该活动） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 220010001 | parameter is illegal | 见 Partner 文档；修正入参或活动状态后重试 |
| 220010002 | system error, please try again later | 见 Partner 文档；修正入参或活动状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_promotion_activity_query.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"pageNumber": 1, "pageSize": 20, "activityType": 2, "activityStatus": 2, "onlyQueryJoinedActivity": false}}'
```

**典型流程：** 促销流程入口：按 **`activityType`** 与时间窗查询 **`activityList`** → 用 **`activityId`** 查候选/已报名商品。
