# 商家税务报表下载 — `temu.pay.tax.merchant.report.download`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_tax_merchant_report_download.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=cc87994f2ac24fc88795f2a3a8844683 |
| **网关** | `POST /temu/proxy`，`type`=`temu.pay.tax.merchant.report.download`，业务载荷放在 Body 的 `params` |

**Description:** Download merchant tax report file by task/request.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=product-inventory`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── requestId (STRING)
    └── taskId (LONG)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| requestId | STRING | 否 | Request ID |
| taskId | LONG | 否 | Task ID |

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
    ├── fileUrl (STRING)
    ├── status (INTEGER)
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
| fileUrl | STRING | fileUrl（STRING） |
| status | INTEGER | status（INTEGER） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP |
|-----------|----------|----------|
| 200020004 | Reqeust parameter is invalid. | — |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_tax_merchant_report_download.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {}
}'
```
