# 订单核验信息上传 — `temu.local.order.verification.upload`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_order_verification_upload.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.local.order.verification.upload`，业务载荷放在 Body 的 `params` |

**Description:** The interface supports uploading serial numbers (SN) / International Mobile Equipment Identity (IMEI) of high-value goods, or authentication information for second-hand goods（支持上传高价值商品的序列号 SN / IMEI，或二手商品的鉴真/认证信息）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> 入参为**子订单号** `orderSn`（可从 `bg.order.detail.v2.get` 等接口的 `orderList[].orderSn` 取得）。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── orderList[] (OBJECT[], 选填)
        ├── orderSn
        ├── verificationInfo[]
        │   ├── serialNumber
        │   └── imeiNumberList[]
        └── secondHandVerificationInfo[]
            └── secondHandProofCertificateCode
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderList | OBJECT[] | 否 | order unique info list（订单唯一标识/核验信息列表）；按子订单维度批量上传 |

### `orderList[]` 元素

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderSn | STRING | 否 | order sn（子订单号） |
| verificationInfo | OBJECT[] | 否 | electronic ams open unique info list（高价值/电子产品唯一标识列表，如 SN、IMEI） |
| secondHandVerificationInfo | OBJECT[] | 否 | second hand ams open verification info（二手商品鉴真/认证信息列表） |

### `verificationInfo[]` 元素

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| serialNumber | STRING | 否 | serial number（序列号 SN） |
| imeiNumberList | STRING[] | 否 | imei number list（IMEI 号码列表） |

> 高价值商品场景：按实际商品要求填写 `serialNumber` 和/或 `imeiNumberList`；同一 `orderSn` 可包含多条 `verificationInfo`（例如多件商品各一条 SN）。

### `secondHandVerificationInfo[]` 元素

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| secondHandProofCertificateCode | STRING | 否 | second hand proof certificate code（二手商品鉴真/证明证书编码） |

> 二手商品场景：填写 `secondHandProofCertificateCode`；与高价值 `verificationInfo` 按订单实际类型择一或组合使用（以 Partner 与订单标签为准）。

### 网关 `params` 写法

**高价值商品（SN + IMEI）：**

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "orderList": [
      {
        "orderSn": "SO-123456789",
        "verificationInfo": [
          {
            "serialNumber": "SN-001234567890",
            "imeiNumberList": ["352099001761481", "352099001761482"]
          }
        ]
      }
    ]
  }
}
```

**二手商品（鉴真编码）：**

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "orderList": [
      {
        "orderSn": "SO-987654321",
        "secondHandVerificationInfo": [
          {
            "secondHandProofCertificateCode": "CERT-CODE-EXAMPLE"
          }
        ]
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
└── result (OBJECT)
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | 业务结果对象；官方出参表未展开子字段，上传成功时通常以 `success=true` 为准，具体以 Temu 实际返回为准 |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| _(无子字段)_ | — | Partner 文档未列出 `result` 内嵌套属性；若响应体含其它字段，以实际 JSON 为准 |

---

## 示例

```bash
python scripts/global_order_verification_upload.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "orderList": [
      {
        "orderSn": "SO-123456789",
        "verificationInfo": [
          {
            "serialNumber": "SN-001234567890",
            "imeiNumberList": ["352099001761481"]
          }
        ]
      }
    ]
  }
}'
```

典型流程：订单详情确认需上传 SN/IMEI 或二手鉴真 → 本接口上传 → 再执行发货相关接口。订单若带 `REQUIRES_AUTHENTICATION_REPORT_SUBMISSION` 等履约提示，以 `bg.order.list.v2.get` / `bg.order.detail.v2.get` 返回的 `fulfillmentWarning` 为准。
