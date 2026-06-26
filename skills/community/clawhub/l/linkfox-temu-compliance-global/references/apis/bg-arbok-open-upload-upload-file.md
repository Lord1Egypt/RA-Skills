# 合规文件上传 — `bg.arbok.open.upload.uploadFile`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_arbok_upload_upload_file.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=01b8792d2e4a40f7b3b14f4a1f2711b6 |
| **网关** | `POST /temu/proxy`，`type`=`bg.arbok.open.upload.uploadFile`，业务载荷放在 Body 的 `params` |

**Description:** Upload compliance-related files (base64) via Arbok open API.

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── base64File (STRING **必填**)
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| base64File | STRING | **是** | base64File |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "base64File": "test"
  }
}
```

> Partner **Request Example** 为 CURL，业务字段可能在顶层；经 LinkFox 网关请放在 **`params.request`**（或脚本接受的顶层 `request`）。

---

## Response（Partner Response 表 + 全量展开）

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT)
    ├── url (STRING)
```

> Partner **Response** 表仅含顶层字段；`result` 下全部子字段按 **Response 表层级** 与 **Response Example** 合并展开。

### Partner Response 表（HTML 导出可见行）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | result |

### `result` 及下级（全部展开）

| 参数 | 类型 | 说明 |
|------|------|------|
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | result |
| success | BOOLEAN | success |
| url | STRING | Partner Response Example |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_arbok_upload_upload_file.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "base64File": "test"   } }'
```
