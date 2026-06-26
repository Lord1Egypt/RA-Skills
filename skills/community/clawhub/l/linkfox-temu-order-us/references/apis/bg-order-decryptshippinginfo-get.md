# 订单收货地址解密查询 — `bg.order.decryptshippinginfo.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_order_decryptshippinginfo_get.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`bg.order.decryptshippinginfo.get`，业务载荷放在 Body 的 `params` |

**Description:** The `bg.order.decryptshippinginfo.get` interface is designed to retrieve **sensitive shipping address information** for a specific order（获取指定订单的**敏感**收货地址信息，通常为解密后的明文姓名、电话、地址等）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> **隐私提示**：返回含收件人姓名、电话、详细地址等 PII，请按合规要求存储与展示，勿写入日志或公开渠道。

与 `bg.order.shippinginfo.v2.get` 的区别：本接口用于获取**解密/敏感**收货信息；若仅需常规收货地址（含 `warning` 限制提示），见 [bg-order-shippinginfo-v2-get.md](./bg-order-shippinginfo-v2-get.md)。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── parentOrderSn (STRING, 否)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | 否 | parentOrderSn（父订单号）；查询指定订单敏感收货地址时**应传入** |

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
    └── addressExtra
        ├── firstName
        ├── lastName
        ├── additionalFirstName
        └── additionalLastName
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | 解密后的敏感收货地址等业务结果 |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| receiptName | STRING | Name（收件人姓名） |
| receiptAdditionalName | STRING | Additional Name（附加姓名） |
| mobile | STRING | Phone Number（手机号） |
| backupMobile | STRING | Alternate Phone（备用电话） |
| mail | STRING | Virtual Email（虚拟邮箱） |
| regionName1 | STRING | regionName1（一级行政区名称） |
| regionName2 | STRING | regionName2（二级行政区名称） |
| regionName3 | STRING | regionName3（三级行政区名称） |
| regionName4 | STRING | regionName4（四级行政区名称） |
| addressLine1 | STRING | addressLine1（地址行 1） |
| addressLine2 | STRING | addressLine2（地址行 2） |
| addressLine3 | STRING | addressLine3（地址行 3） |
| postCode | STRING | postCode（邮编） |
| addressLineAll | STRING | addressLineAll（完整地址行，通常为 addressLine1 + Line2 + Line3 拼接） |
| addressExtra | OBJECT | addressExtra（姓名拆分等扩展信息） |

### `addressExtra`

| 参数 | 类型 | 说明 |
|------|------|------|
| firstName | STRING | firstName（名） |
| lastName | STRING | lastName（姓） |
| additionalFirstName | STRING | additionalFirstName（附加名） |
| additionalLastName | STRING | additionalLastName（附加姓） |

---

## 示例

```bash
python scripts/us_order_decryptshippinginfo_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789"
  }
}'
```

典型流程：`bg.order.list.v2.get` / `bg.order.detail.v2.get` 取得 `parentOrderSn` → 本接口拉**解密**收货地址 → 打单发货（`bg.order.shippinginfo.v2.get` 可用于带 `warning` 的常规地址查询）。
