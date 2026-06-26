# 发票 PDF 下载 — `temu.pay.tax.invoice.pdf.download`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_tax_invoice_pdf_download.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=2b8a5a8a75604779b2e0017ee79b462a |
| **网关** | `POST /temu/proxy`，`type`=`temu.pay.tax.invoice.pdf.download`，业务载荷放在 Body 的 `params` |

**Description:** Get signed URL to download invoice PDF.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=product-inventory`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── parentOrderSn (STRING **必填**)
    └── invoiceNumber (STRING **必填**)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | Parent order number |
| invoiceNumber | STRING | **是** | Invoice number |

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
    ├── signUrl (STRING)
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
| signUrl | STRING | signUrl（STRING） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP |
|-----------|----------|----------|
| 200020001 | Non-compliant query, please use the information correctly. | — |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_tax_invoice_pdf_download.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {}
}'
```
