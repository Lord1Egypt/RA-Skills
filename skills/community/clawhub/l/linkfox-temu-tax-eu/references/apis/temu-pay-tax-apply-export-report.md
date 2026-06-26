# 申请导出税务报表 — `temu.pay.tax.apply.export.report`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_tax_apply_export_report.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=6494bb7afd8048d380a13e92f6275d17 |
| **网关** | `POST /temu/proxy`，`type`=`temu.pay.tax.apply.export.report`，业务载荷放在 Body 的 `params` |

**Description:** Apply to export tax/sales report for a given month.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=product-inventory`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
    └── reportMonth (STRING **必填**)
    └── requestId (STRING **必填**)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reportMonth | STRING | **是** | Report Month, format YYYY-MM |
| requestId | STRING | **是** | Request Id |

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
    ├── taskId (INTEGER)
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
| taskId | INTEGER | taskId（INTEGER） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP |
|-----------|----------|----------|
| 200020005 | Region or site not support | — |
| 200020004 | Reqeust parameter is invalid. | — |
| 200020003 | Not supported to apply for sales report for the current month | — |
| 200020002 | Cannot apply for sales reports repeatedly | — |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_tax_apply_export_report.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {}
}'
```
