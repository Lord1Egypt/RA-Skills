# 发票信息查询 — `temu.pay.tax.invoice.info.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_tax_invoice_info_query.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=5f5d1168742b4991a86684cbd0c21489 |
| **网关** | `POST /temu/proxy`，`type`=`temu.pay.tax.invoice.info.query`，业务载荷放在 Body 的 `params` |

**Description:** Query tax invoice summary list by parent order numbers.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=product-inventory`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── parentOrderSnList (STRING[] **必填**)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSnList | STRING[] | **是** | Parent order number list, max 20 per request. |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {}
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
    ├── taxInvoiceInfoList[] (OBJECT[])
    ├── taxInvoiceInfoList[].invoiceTime (INTEGER)
    ├── taxInvoiceInfoList[].invoiceNumber (STRING)
    ├── taxInvoiceInfoList[].parentOrderSn (STRING)
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
| taxInvoiceInfoList[] | OBJECT[] | taxInvoiceInfoList（OBJECT[]） |
| taxInvoiceInfoList[].invoiceTime | INTEGER | invoiceTime（INTEGER） |
| taxInvoiceInfoList[].invoiceNumber | STRING | invoiceNumber（STRING） |
| taxInvoiceInfoList[].parentOrderSn | STRING | parentOrderSn（STRING） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP |
|-----------|----------|----------|
| 200020001 | Non-compliant query, please use the information correctly. | — |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_tax_invoice_info_query.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {}
}'
```
