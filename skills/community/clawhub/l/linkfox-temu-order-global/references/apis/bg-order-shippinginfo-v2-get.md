# 订单收货地址查询 V2 — `bg.order.shippinginfo.v2.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_order_shippinginfo_v2_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.order.shippinginfo.v2.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.order.shippinginfo.v2.get` interface is designed to retrieve shipping address information for a specific order. This functionality is crucial for merchants and logistics providers to ensure that orders are shipped to the correct location.

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── parentOrderSn (STRING, 否)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | 否 | parentOrderSn（父订单号）；查询指定订单收货地址时**应传入** |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789"
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
    ├── receiptName
    ├── receiptAdditionalName
    ├── mobile
    ├── backupMobile
    ├── mail
    ├── regionName1
    ├── regionName2
    ├── regionName3
    ├── regionName4
    ├── addressLine1
    ├── addressLine2
    ├── addressLine3
    ├── postCode
    ├── addressLineAll
    ├── addressExtra
    │   ├── firstName
    │   ├── lastName
    │   ├── additionalFirstName
    │   └── additionalLastName
    └── warning
        ├── isRestriction
        └── reason
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | 收货地址等业务结果 |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| receiptName | STRING | Name（收件人姓名） |
| receiptAdditionalName | STRING | Additional Name（附加姓名） |
| mobile | STRING | Phone Number（手机号） |
| backupMobile | STRING | Alternate Phone（备用电话） |
| mail | STRING | Virtual Email（虚拟邮箱） |
| regionName1 | STRING | First-Level Administrative Division Name（一级行政区名称） |
| regionName2 | STRING | Secondary Administrative Division Name（二级行政区名称） |
| regionName3 | STRING | Third-Level Administrative Division Name（三级行政区名称） |
| regionName4 | STRING | Fourth-Level Administrative Division Name（四级行政区名称） |
| addressLine1 | STRING | Address Line 1（地址行 1） |
| addressLine2 | STRING | Address Line 2（地址行 2） |
| addressLine3 | STRING | Address Line 3（地址行 3） |
| postCode | STRING | Postal Code（邮编） |
| addressLineAll | STRING | Address Line 1 + Line 2 + Line 3（拼接完整地址行） |
| addressExtra | OBJECT | addressExtra（姓名拆分等扩展信息） |
| warning | OBJECT | warning information（地址/履约限制提示） |

### `addressExtra`

| 参数 | 类型 | 说明 |
|------|------|------|
| firstName | STRING | First Name |
| lastName | STRING | Last Name |
| additionalFirstName | STRING | Additional First Name |
| additionalLastName | STRING | Additional Last Name |

### `warning`

| 参数 | 类型 | 说明 |
|------|------|------|
| isRestriction | BOOLEAN | isRestriction（是否存在地址返回限制） |
| reason | INTEGER | When there is an address return restriction, it indicates the restriction scenario |

#### `warning.reason` 枚举

| 值 | 说明 |
|----|------|
| `1` | COD |
| `2` | Restricting self shipment（限制自发货） |
| `3` | Promise only buy shipping（仅承诺购买平台物流） |

---

## 示例

```bash
python scripts/global_order_shippinginfo_v2_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}'
```

发货前典型流程：`bg.order.list.v2.get` / `bg.order.detail.v2.get` 取得 `parentOrderSn` → 本接口拉收货地址 → 后续发货/面单接口（待接入）。
