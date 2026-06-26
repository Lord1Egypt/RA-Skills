# 活动商品报名 — `bg.promotion.activity.goods.enroll`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_promotion_activity_goods_enroll.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.promotion.activity.goods.enroll`，业务载荷放在 Body 的 `params` |

**Description:** Enroll goods into a promotion activity.

> **`activityId`**、**`enrollGoods`** 必填。
> **`enrollGoods`** 子字段在 Partner Request 表中为折叠行，按 **Request Example** 展开。
> 返回 **`draftId`**，可用 [goods.operation.query](./bg-promotion-activity-goods-operation-query.md) 轮询 **`operationStatus`**。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── activityId (LONG, 必填)
    └── enrollGoods (OBJECT, 必填)
        ├── goodsId (LONG, 必填)
        ├── activityQuantity (LONG, 必填)
        ├── traceCode (STRING, 否)
        └── enrollSkuList[] (OBJECT[], 必填)
            ├── skuId (LONG)
            └── activitySupplierPrice (LONG)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| activityId | LONG | **是** | unique identifier for the activity |
| enrollGoods | OBJECT | **是** | goods information required for activity registration |

#### `enrollGoods`（OBJECT，必填）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| goodsId | LONG | 是 | goods id |
| activityQuantity | LONG/INTEGER | 是 | Activity quantity for enrollment（报名活动数量） |
| traceCode | STRING | 否 | Idempotent key（幂等键，单次操作长度不超过 32 字符，Partner Request Example） |
| enrollSkuList | OBJECT[] | 是 | SKU list to enroll |

#### `enrollGoods.enrollSkuList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| skuId | LONG | sku id |
| activitySupplierPrice | LONG | Activity supplier price for this SKU（该 SKU 活动供货价） |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "activityId": 123456,
    "enrollGoods": {
      "goodsId": 100001,
      "activityQuantity": 50,
      "traceCode": "enroll-001",
      "enrollSkuList": [
        {
          "skuId": 200001,
          "activitySupplierPrice": 1999
        }
      ]
    }
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
    ├── draftId (LONG)
    ├── operationStatus (INTEGER)
    ├── failReason (STRING)
    └── goodsId (LONG)
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
| draftId | LONG | goods registration activity draft id（报名草稿 ID；前置流程成功时生成，用于 [goods.operation.query](./bg-promotion-activity-goods-operation-query.md)） |
| operationStatus | INTEGER | Operation status（操作状态码；异步处理时请轮询 operation.query） |
| failReason | STRING | Failure reason when operation failed（失败原因） |
| goodsId | LONG | goods id |

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
python scripts/global_promotion_activity_goods_enroll.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"activityId": 123456, "enrollGoods": {"goodsId": 100001, "activityQuantity": 50, "traceCode": "enroll-001", "enrollSkuList": [{"skuId": 200001, "activitySupplierPrice": 1999}]}}}'
```

**典型流程：** 报名 → 保存 **`draftId`** → **goods.operation.query** 确认结果。
