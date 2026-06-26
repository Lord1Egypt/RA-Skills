# 确认子包裹发货 — `bg.logistics.shipment.sub.confirm`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_self_fulfilled_logistics_shipment_sub_confirm.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipment.sub.confirm`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipment.sub.confirm` interface should only be used in scenarios where the smallest sku needs to be shipped as split packages, and can append the sub-parcel information to the main parcel（仅在最小 SKU 需拆分为多个包裹发货时使用；向主包裹追加子包裹信息）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> - `mainPackageSn` 来自 **`bg.logistics.shipment.get`**（待接入时可先用 `temu_eu_proxy.py`）  
> - `selfShippingWarehouseId` 来自 **`linkfox-temu-fulfillment-eu`** 的 **`bg.logistics.warehouse.list.get`**（`warehouseId`）  
> - `carrierId` 可与 [bg-logistics-companies-get.md](./bg-logistics-companies-get.md) 返回的物流商 ID 对应

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── mainPackageSn (STRING, 是)
    └── sendSubRequestList[] (OBJECT[], 否)
        ├── carrierId (LONG, 是)
        ├── trackingNumber (STRING, 是)
        └── selfShippingWarehouseId (STRING, 是)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mainPackageSn | STRING | **是** | Package number that you already shipped（已发货的主包裹号）。可从 **`bg.logistics.shipment.get`** 获取 |
| sendSubRequestList | OBJECT[] | 否 | Send Sub Package Info（子包裹发货信息列表） |

### `sendSubRequestList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| carrierId | LONG | **是** | Carrier ID（承运商 ID） |
| trackingNumber | STRING | **是** | Tracking Number（物流跟踪号） |
| selfShippingWarehouseId | STRING | **是** | The shipment warehouse ID（发货仓库 ID），可从 **`linkfox-temu-fulfillment-eu`** 的 **`bg.logistics.warehouse.list.get`** 返回的 **`warehouseId`** 获取 |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "mainPackageSn": "PKG-MAIN-123456789",
    "sendSubRequestList": [
      {
        "carrierId": 123456789,
        "trackingNumber": "1Z999AA10123456784",
        "selfShippingWarehouseId": "WH-001"
      }
    ]
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
└── result (BOOLEAN)
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | BOOLEAN | 业务结果（Partner 文档类型为 BOOLEAN；具体语义以 Temu 返回为准） |

---

## 示例

```bash
python scripts/eu_self_fulfilled_logistics_shipment_sub_confirm.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "mainPackageSn": "PKG-MAIN-123456789",
    "sendSubRequestList": [
      {
        "carrierId": 123456789,
        "trackingNumber": "1Z999AA10123456784",
        "selfShippingWarehouseId": "WH-001"
      }
    ]
  }
}'
```

典型流程：主包裹已发货并取得 `mainPackageSn`（`bg.logistics.shipment.get`）→ 同一最小 SKU 需拆分子包裹时 → 本接口追加 `sendSubRequestList` 子包裹物流信息。
