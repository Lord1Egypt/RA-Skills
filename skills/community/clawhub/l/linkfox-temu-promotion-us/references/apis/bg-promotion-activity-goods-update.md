# 活动商品更新 — `bg.promotion.activity.goods.update`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_promotion_activity_goods_update.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=873ac072a78249c893e5f8d0e656a11f&sub_menu_code=29959238217c41f38f5904e32bf1d14f |
| **网关** | `POST /temu/proxy`，`type`=`bg.promotion.activity.goods.update`，业务载荷放在 Body 的 `params` |

**Description:** Update enrolled promotion activity goods.

> **`activityId`**、**`goodsId`**、**`operateType`** 必填。
> **`operateType`** 决定必填子参数（见下表）；**`updateSkuList`/`addSkuList`** 按 Request Example 展开。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=product-inventory`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── traceCode (STRING, 否)
    ├── activityId (LONG, 必填)
    ├── activityQuantity (LONG, 否)
    ├── goodsId (LONG, 必填)
    ├── operateType (INTEGER, 必填)
    ├── updateSkuList[] (OBJECT[], 否)
    │   ├── skuId (LONG)
    │   └── activitySupplierPrice (LONG)
    └── addSkuList[] (OBJECT[], 否)
        ├── skuId (LONG)
        └── activitySupplierPrice (LONG)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| traceCode | STRING | 否 | Optional. The traceCode is an Idempotent Key for single operations. Its length cannot exceed 32 characters. |
| activityId | LONG | **是** | unique identifier for the activity |
| activityQuantity | LONG | 否 | activity quantity, the quantity you set for participating activities. This is independent of product quantity. The updated activity quantity must be more than the original one. |
| goodsId | LONG | **是** | goods id |
| operateType | INTEGER | **是** | the type of operation. It determines which parameters are required. For example, if the operation type is 20, then the "activityQuantity" parameter must not be null, while all other parameters should be null. If the operation type is 30, then all other parameters must be null. 10 - update activity supplier price 20 - update activity quantity 30 - deactivate activity goods 40 - add activity sku |
| updateSkuList | OBJECT[] | 否 | sku information required for updating activity sku information |
| addSkuList | OBJECT[] | 否 | sku information required for adding activity sku information |

#### `operateType`（必填）

| 值 | 说明 | 必填参数 |
|----|------|----------|
| `10` | update activity supplier price | `updateSkuList`（其他参数应为 null） |
| `20` | update activity quantity | `activityQuantity`（须大于原活动数量；其他参数应为 null） |
| `30` | deactivate activity goods | 其他参数应为 null |
| `40` | add activity sku | `addSkuList` |

#### `updateSkuList[]` / `addSkuList[]`（Request Example 展开）

| 参数 | 类型 | 说明 |
|------|------|------|
| skuId | LONG | sku id |
| activitySupplierPrice | LONG | Activity supplier price |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "request": {
    "activityId": 123456,
    "goodsId": 100001,
    "operateType": 10,
    "traceCode": "update-001",
    "updateSkuList": [
      {
        "skuId": 200001,
        "activitySupplierPrice": 1899
      }
    ]
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
| draftId | LONG | Draft id for async operation |
| operationStatus | INTEGER | Operation status |
| failReason | STRING | Failure reason |
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
python scripts/us_promotion_activity_goods_update.py '{"accessToken": "TOKEN", "tokenPurpose": "product-inventory", "request": {"activityId": 123456, "goodsId": 100001, "operateType": 10, "traceCode": "update-001", "updateSkuList": [{"skuId": 200001, "activitySupplierPrice": 1899}]}}'
```

**典型流程：** 按 **`operateType`** 更新价/量/下架/加 SKU → 用 **goods.operation.query** 查 **`draftId`** 结果。
