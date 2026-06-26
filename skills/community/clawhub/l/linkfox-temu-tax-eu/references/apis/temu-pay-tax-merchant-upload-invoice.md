# 商家上传发票 — `temu.pay.tax.merchant.upload.invoice`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_tax_merchant_upload_invoice.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=98fcf420ee5c4f0d8c8f708adfd89160 |
| **网关** | `POST /temu/proxy`，`type`=`temu.pay.tax.merchant.upload.invoice`，业务载荷放在 Body 的 `params` |

**Description:** Merchant upload invoice or credit note file for an order.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=product-inventory`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── parentOrderSn (STRING **必填**)
    └── invoiceDirection (INTEGER **必填**)
    └── invoiceName (STRING **必填**)
    └── recipientType (INTEGER **必填**)
    └── fileUrl (STRING **必填**)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | parent order sn |
| invoiceDirection | INTEGER | **是** | invoice direction. 1-invoice, 2-credit-note |
| invoiceName | STRING | **是** | invoice name |
| recipientType | INTEGER | **是** | recipient type. 1-consumer, 2-platform |
| fileUrl | STRING | **是** | invoice file url |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {
    "parentOrderSn": "PO-123456789",
    "invoiceDirection": 1,
    "invoiceName": "invoice-001.pdf",
    "recipientType": 1,
    "fileUrl": "https://..."
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 嵌套子行在导出 HTML 中多为折叠状态；下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT)
    ├── success (BOOLEAN)
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Business result |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | Upload result inside `result`（上传是否成功；与响应顶层 `success` 不同，顶层表示 API 调用是否成功） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP |
|-----------|----------|----------|
| 200030003 | ParentOrderSn Invalid | — |
| 200030002 | Invalid Invoice Content | — |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_tax_merchant_upload_invoice.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {
    "parentOrderSn": "PO-123456789",
    "invoiceDirection": 1,
    "invoiceName": "invoice-001.pdf",
    "recipientType": 1,
    "fileUrl": "https://..."
  }
}'
```
