# 取消订单售后列表查询 — `bg.aftersales.cancel.list.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_cancel_aftersales_cancel_list_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation（`menu_code` / `sub_menu_code` 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`bg.aftersales.cancel.list.get`，业务载荷放在 Body 的 `params` |

**Description:** Query cancel order after-sales information（查询取消订单售后信息）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── pageSize (INTEGER, 否)
    ├── pageNo (INTEGER, 否)
    ├── parentOrderSnList[] (STRING[], 否)
    ├── parentAfterSalesSnList[] (STRING[], 否)
    └── afterSalesStatusGroup (INTEGER, 否)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageSize | INTEGER | 否 | Page size for pagination，**默认 10**，**最大 200** |
| pageNo | INTEGER | 否 | Page number for pagination，**默认 1** |
| parentOrderSnList | STRING[] | 否 | Parent order number list；留空则不限制父订单号范围；**单次查询最多 200 条** |
| parentAfterSalesSnList | STRING[] | 否 | Parent after-sales order number list；留空则不限制父售后单号范围；**单次查询最多 200 条** |
| afterSalesStatusGroup | INTEGER | 否 | The cancel order after-sales status group（取消订单售后状态组），见下表 |

#### `afterSalesStatusGroup`（入参筛选）

| 值 | 说明 |
|----|------|
| `8` | Cancel order pending（取消订单待处理） |
| `9` | Cancel order approved（取消订单已同意） |
| `10` | Cancel order rejected（取消订单已拒绝） |
| `11` | Cancel order revoked（取消订单已撤销） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNo": 1,
    "pageSize": 20,
    "afterSalesStatusGroup": 8,
    "parentOrderSnList": ["PO-123456789"]
  }
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
    ├── total
    ├── pageNumber
    └── data[]
        ├── parentAfterSalesSn
        ├── parentAfterSalesStatus
        └── afterSalesInfoList[]
            ├── afterSalesSn
            ├── parentOrderSn
            ├── orderSn
            ├── productSkuId
            ├── applyGoodsNumber
            ├── goodsId
            ├── productList[]
            │   ├── productSkuId
            │   └── extCode
            └── createAtMillis
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Specific information |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| total | LONG | Total number of matching records（匹配记录总数） |
| pageNumber | INTEGER | Current page number of the result（当前结果页码） |
| data | OBJECT[] | The record data returned from this query（本次查询返回的记录） |

> 入参分页字段为 **`pageNo`**，出参当前页为 **`pageNumber`**，勿混用。

### `data[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentAfterSalesSn | STRING | Parent after-sales order number for the canceled order（取消订单的父售后单号） |
| parentAfterSalesStatus | INTEGER | Current parent after-sales status（当前父售后状态），见下表 |
| afterSalesInfoList | OBJECT[] | Cancel order after-sales information list（取消订单售后信息列表） |

#### `parentAfterSalesStatus`（出参）

| 值 | 说明 |
|----|------|
| `1` | Buyer has applied for a refund, pending processing（买家已申请退款，待处理） |
| `4` | Refund has been initiated, being processed by the system（退款已发起，系统处理中） |
| `5` | Refund has been issued（退款已发放） |
| `6` | Buyer has cancelled the after-sales request（买家已撤销售后申请） |
| `7` | After-sales request has been rejected（售后申请已被拒绝） |
| `9` | Refund initiated, being processed by the system（退款已发起，系统处理中） |

### `afterSalesInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| afterSalesSn | STRING | After-sales order number（售后单号） |
| parentOrderSn | STRING | Parent order number（父订单号） |
| orderSn | STRING | Order number（子订单号） |
| productSkuId | LONG | Product SKU ID |
| applyGoodsNumber | LONG | Quantity requested for cancellation（申请取消数量） |
| goodsId | LONG | Goods ID |
| productList | OBJECT[] | Product information list（产品信息列表） |
| createAtMillis | LONG | After-sales order creation time, unit in milliseconds（售后单创建时间，毫秒） |

### `productList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| productSkuId | LONG | Product SKU ID |
| extCode | STRING | Product external code（商品外部编码） |

---

## 示例

```bash
python scripts/global_cancel_aftersales_cancel_list_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pageNo": 1,
    "pageSize": 20,
    "afterSalesStatusGroup": 8
  }
}'
```

可与 `linkfox-temu-order-global` 的 `bg.order.list.v2.get` / `bg.order.detail.v2.get` 配合：先查订单 `pending_buyer_cancellation` 标签，再按 `parentOrderSnList` 拉取消售后明细。
