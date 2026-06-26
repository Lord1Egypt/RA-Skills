# 可合并发货订单组列表 — `bg.order.combinedshipment.list.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_order_combinedshipment_list_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.order.combinedshipment.list.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.order.combinedshipment.list.get` interface is designed for merchants to retrieve **combined shipping groups**, including lists of parent orders that can be combined for shipping（供商家查询**可合并发货**的订单组，每组包含可合并发货的父订单列表）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`（官方无额外筛选字段，可传空对象）。建议使用 **`tokenPurpose=order-shipping`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── （无子字段；可传 {} 或不传 request）
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| _(无)_ | — | — | 官方入参表仅声明 `request` 对象，**无其它业务筛选字段**；调用时通常传空对象 `{}` 或省略 `request` |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {}
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping"
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    └── combinedShippingGroups[] (OBJECT[])
        └── combinedShippingGroup[] (OBJECT[])
            ├── parentOrderSn
            ├── parentOrderStatus
            ├── parentOrderTime
            ├── mallId
            └── semiUniqueId
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | 可合并发货组列表等业务结果 |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| combinedShippingGroups | OBJECT[] | Combined shipping groups（可合并发货组列表）；每组内包含可合并发货的父订单列表 |

### `combinedShippingGroups[]` 元素

| 参数 | 类型 | 说明 |
|------|------|------|
| combinedShippingGroup | OBJECT[] | A list of parent orders that can be combined for shipping（本组内可合并发货的父订单列表） |

### `combinedShippingGroup[]` 元素

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderSn | STRING | parent order number（父订单号） |
| parentOrderStatus | INTEGER | Status of the parent order（父订单状态），见下表 |
| parentOrderTime | INTEGER | Time when the parent order was placed（父订单下单时间，秒级时间戳） |
| mallId | LONG | mallId（店铺/商城 ID） |
| semiUniqueId | STRING | Unique identifier for semi-managed stores（半托管店铺唯一标识） |

#### `parentOrderStatus`（出参）

| 值 | 说明 |
|----|------|
| `1` | PENDING（待处理） |
| `2` | UN_SHIPPING（待发货） |
| `3` | CANCELED（已取消） |
| `4` | SHIPPED（已发货） |
| `41` | PARTIALLY_SHIPPED（部分发货，仅 local mall） |
| `5` | DELIVERED / RECEIPTED（已签收） |
| `51` | PARTIALLY_DELIVERED（部分签收，仅 local mall） |

> 与 `bg.order.list.v2.get` 出参中 `parentOrderMap.parentOrderStatus` 含义一致；具体以 Partner 文档为准。

---

## 示例

```bash
python scripts/global_order_combinedshipment_list_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {}
}'
```

典型流程：本接口拉**可合并发货**父单组 → 对组内 `parentOrderSn` 调用 `bg.order.shippinginfo.v2.get` / `bg.order.decryptshippinginfo.get` 取地址 → 后续合并发货/面单接口（待接入）。
