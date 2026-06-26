# 活动候选商品查询 — `bg.promotion.activity.candidate.goods.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_promotion_activity_candidate_goods_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.promotion.activity.candidate.goods.query`，业务载荷放在 Body 的 `params` |

**Description:** Query candidate goods for a promotion activity.

> **`activityId`**、**`pageNumber`**、**`pageSize`** 均为必填。
> 返回 **`isAllowedEnroll`** 与推荐活动价/数量，用于报名前选品。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── activityId (LONG, 必填)
    ├── pageNumber (INTEGER, 必填)
    └── pageSize (INTEGER, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| activityId | LONG | **是** | unique identifier for the activity |
| pageNumber | INTEGER | **是** | page number for pagination, default is 1. |
| pageSize | INTEGER | **是** | Page size for pagination, default is 10, max is 100. |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "activityId": 123456,
    "pageNumber": 1,
    "pageSize": 20
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
    ├── activityInfo (OBJECT)
    │   └── activityId, activityName, activityType, activityStatus, …
    └── goodsList[]
        ├── goodsId (LONG)
        ├── isAllowedEnroll (BOOLEAN)
        ├── recommendActivityQuantity (INTEGER)
        └── skuList[]
            ├── skuId (LONG)
            └── recommendActivitySupplierPrice (LONG)
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
| total | LONG | Total records（总记录数） |
| activityInfo | OBJECT | Activity information（当前活动信息） |
| goodsList | OBJECT[] | Candidate goods list（候选商品列表） |

#### `activityInfo`

| 参数 | 类型 | 说明 |
|------|------|------|
| activityId | LONG | unique identifier for the activity |
| activityName | STRING | Activity name |
| activityType | INTEGER | Activity type |
| activityStatus | INTEGER | Activity status（`1` Not started；`2` Ongoing；`3` Ended） |
| activityStartTime | LONG | Start time in seconds |
| activityEndTime | LONG | End time in seconds |
| isJoinedActivity | BOOLEAN | Whether joined |

#### `goodsList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| goodsId | LONG | goods id |
| isAllowedEnroll | BOOLEAN | Whether the goods is allowed to enroll（是否允许报名） |
| recommendActivityQuantity | INTEGER | Recommended activity quantity（推荐活动数量） |
| skuList | OBJECT[] | SKU list with recommended prices |

#### `goodsList[].skuList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| skuId | LONG | sku id |
| recommendActivitySupplierPrice | LONG | Recommended activity supplier price（推荐活动供货价） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 220010001 | parameter is illegal | 见 Partner 文档；修正入参或活动状态后重试 |
| 220010002 | system error, please try again later | 见 Partner 文档；修正入参或活动状态后重试 |
| 220010003 | The activity has been cancelled, please select another activity to participate | 见 Partner 文档；修正入参或活动状态后重试 |
| 220010004 | The activity has ended, please select another activity to participate | 见 Partner 文档；修正入参或活动状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_promotion_activity_candidate_goods_query.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"activityId": 123456, "pageNumber": 1, "pageSize": 20}}'
```

**典型流程：** 在 [activity.query](./bg-promotion-activity-query.md) 取得 **`activityId`** 后，查询可报名商品与推荐价。
