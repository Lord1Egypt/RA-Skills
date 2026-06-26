# 查询发货信息 V2 — `bg.logistics.shipment.v2.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_self_fulfilled_logistics_shipment_v2_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipment.v2.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipment.v2.get` interface is for sellers to verify shipped info after self-fulfillment（卖家自发货后，按订单查询并核对已提交的发货/物流信息）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> 通常在 **`bg.logistics.shipment.v2.confirm`** 确认发货之后调用，用于核对运单号、包裹号、承运商及子包裹信息；`parentOrderSn` / `orderSn` 来自 **`linkfox-temu-order-eu`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── parentOrderSn    ← 必填
    └── orderSn          ← 必填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent Order Number（父订单号） |
| orderSn | STRING | **是** | Order Number（子订单号 / 订单号） |

> 官方表将顶层 **`request`** 标为选填（False），但 **`parentOrderSn`**、**`orderSn`** 均为必填；实际调用时**应传入完整 `request` 对象**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-20260101001",
    "orderSn": "O-20260101001-1"
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
└── result (OBJECT)
    └── shipmentInfoDTO[]              ← shipment result（发货结果列表）
        ├── carrierId
        ├── carrierName
        ├── trackingNumber
        ├── skuId
        ├── quantity
        ├── packageSn
        ├── packageDeliveryType
        ├── trackingWarningLabel
        ├── cooperativeWarehouseDTO (OBJECT)   ← 合作仓履约时可能有值；卖家自发货时可能为空
        │   ├── warehouseProviderCode
        │   ├── warehouseProviderBrandName
        │   ├── warehouseCode
        │   └── warehouseName
        └── subPackageShipmentInfoList[]     ← subPackage Shipment result（子包裹发货结果）
            ├── carrierId
            ├── carrierName
            ├── packageSn
            ├── packageDeliveryType
            └── trackingNumber
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | result（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| shipmentInfoDTO | OBJECT[] | shipment result（发货结果列表；每个元素对应一条主包裹维度的发货信息，可含子包裹列表） |

#### `shipmentInfoDTO[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| carrierId | LONG | Carrier ID（承运商 ID），与 **`bg.logistics.companies.get`** 返回的 **`logisticsServiceProviderId`** 相同 |
| carrierName | STRING | Carrier name（承运商名称）；Partner 原文表述为与 `bg.logistics.companies.get` 中对应 ID 的名称一致（字段 **`logisticsServiceProviderName`**） |
| trackingNumber | STRING | Tracking Number（物流运单号）。**Y2 订单**：仅当 API 调用时间戳 **≥ `earliestTimeGetShippingDocument`** 时才会返回 `trackingNumber` |
| skuId | LONG | SKU ID |
| quantity | INTEGER | Quantity of the product（该包裹行对应的发货数量） |
| packageSn | STRING | Package number（包裹号） |
| packageDeliveryType | INTEGER | Package delivery type（包裹履约/发货渠道类型），见下表 |
| trackingWarningLabel | INTEGER | Tracking warning labels（轨迹预警标签），见下表 |
| cooperativeWarehouseDTO | OBJECT | 仅当该订单由**合作仓**履约时可能返回 DTO；**卖家自发货**时可能为空 |
| subPackageShipmentInfoList | OBJECT[] | subPackage Shipment result（子包裹发货结果列表；拆包/多包裹场景） |

##### `packageDeliveryType`（主包裹与子包裹共用）

| 值 | 说明 |
|----|------|
| `1` | Seller fulfills this order by **non-integrated** channel（卖家通过**非 Temu 集成**渠道履约） |
| `2` | Seller fulfills this order by **Temu-integrated** channel（卖家通过 **Temu 集成**渠道履约） |
| `3` | Cooperative warehouse fulfills this order by **non-integrated** channel（合作仓通过**非集成**渠道履约） |
| `4` | Cooperative warehouse fulfills this order by **Temu-integrated** channel（合作仓通过 **Temu 集成**渠道履约） |

##### `trackingWarningLabel`

| 值 | 说明 |
|----|------|
| `0` | No issues（无异常） |
| `1` | No tracking information（无轨迹信息） |
| `2` | Potentially incorrect（轨迹可能不正确） |
| `3` | The receiving address is inconsistent（收货地址不一致） |
| `4` | Over time collection（揽收超时） |

##### `cooperativeWarehouseDTO` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| warehouseProviderCode | STRING | Warehouse Provider Code（仓配服务商编码） |
| warehouseProviderBrandName | STRING | Warehouse Provider Brand Name（仓配服务商品牌名） |
| warehouseCode | STRING | warehouse Code（仓库编码） |
| warehouseName | STRING | Warehouse Name（仓库名称） |

> 卖家自发货（Self-Fulfilled）场景下，该对象常为 **空或不返回**；合作仓履约订单才需关注。

##### `subPackageShipmentInfoList[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| carrierId | LONG | Carrier ID，与 **`bg.logistics.companies.get`** 的 **`logisticsServiceProviderId`** 相同 |
| carrierName | STRING | Carrier name，与 `bg.logistics.companies.get` 中对应承运商名称一致 |
| packageSn | STRING | Package number（子包裹号） |
| packageDeliveryType | INTEGER | Package delivery type，枚举同主包裹 **`packageDeliveryType`** |
| trackingNumber | STRING | Tracking Number（子包裹运单号） |

> 调用成功时先判断 **`response.success === true`**，再解析 **`result.shipmentInfoDTO`**。若需核对平台侧订单状态，可配合 **`linkfox-temu-order-eu`** 的 `bg.order.detail.v2.get`。

---

## 典型用法

```text
1. bg.logistics.shipment.v2.confirm   → 确认发货
2. bg.logistics.shipment.v2.get       → 按 parentOrderSn + orderSn 核对运单、包裹号、预警标签
3. （拆包场景）subPackageShipmentInfoList → 获取各子包裹 packageSn / trackingNumber，供 sub.confirm 等后续操作
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_self_fulfilled_logistics_shipment_v2_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-20260101001",
    "orderSn": "O-20260101001-1"
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.shipment.v2.get",
  "params": {
    "request": {
      "parentOrderSn": "PO-20260101001",
      "orderSn": "O-20260101001-1"
    }
  }
}'
```
