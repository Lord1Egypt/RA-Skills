# 更新物流跟踪号 / 发货方式 — `bg.logistics.shipment.shippingtype.update`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_self_fulfilled_logistics_shipment_shippingtype_update.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.shipment.shippingtype.update`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.logistics.shipment.shippingtype.update` interface is used by sellers to update logistics tracking numbers, supporting the following scenarios（卖家更新物流跟踪号，支持以下场景）：

1. **Non-integrated logistics updating logistics tracking numbers** — 非集成物流更新物流跟踪号  
2. **Temu-integrated logistics has been changed to non-integrated logistics** — Temu 集成物流已改为非集成物流

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> - `packageSn` 通常来自 **`bg.logistics.shipment.v2.get`** 或 **`bg.logistics.shipment.get`**  
> - `shipCompanyId` 与 [bg-logistics-companies-get.md](./bg-logistics-companies-get.md) 返回的 **`logisticsServiceProviderId`** 相同  
> - `selfShippingWarehouseId` 来自 **`linkfox-temu-fulfillment-global`** 的 **`bg.logistics.warehouse.list.get`**

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── editPackageRequestList[] (OBJECT[], 否)
        ├── packageSn (STRING, 是)
        ├── trackingNumber (STRING, 是)
        ├── shipCompanyId (LONG, 是)
        └── selfShippingWarehouseId (STRING, 是)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| editPackageRequestList | OBJECT[] | 否 | edit package request list（编辑包裹请求列表） |

### `editPackageRequestList[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSn | STRING | **是** | package number（包裹号） |
| trackingNumber | STRING | **是** | tracking number（物流跟踪号） |
| shipCompanyId | LONG | **是** | It's the same ID with the **`logisticsServiceProviderId`** you got from **`bg.logistics.companies.get`**（与 `bg.logistics.companies.get` 返回的 `logisticsServiceProviderId` 相同） |
| selfShippingWarehouseId | STRING | **是** | The shipment warehouse ID（发货仓库 ID），可从 **`linkfox-temu-fulfillment-global`** 的 **`bg.logistics.warehouse.list.get`** 获取 |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "editPackageRequestList": [
      {
        "packageSn": "PKG-123456789",
        "trackingNumber": "1Z999AA10123456784",
        "shipCompanyId": 123456789,
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
python scripts/global_self_fulfilled_logistics_shipment_shippingtype_update.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "editPackageRequestList": [
      {
        "packageSn": "PKG-123456789",
        "trackingNumber": "1Z999AA10123456784",
        "shipCompanyId": 123456789,
        "selfShippingWarehouseId": "WH-001"
      }
    ]
  }
}'
```

典型流程：已发货包裹需更正跟踪号，或 Temu 集成物流改为非集成物流 → `bg.logistics.companies.get` 取 `shipCompanyId` → 本接口批量更新 `editPackageRequestList` → 可用 `bg.logistics.shipment.v2.get` 核对。