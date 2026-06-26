# 待上传资质项查询 — `bg.arbok.open.cert.queryNeedUploadItems`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_arbok_cert_query_need_upload_items.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=84d3118d3a604947abf35144606cdea2 |
| **网关** | `POST /temu/proxy`，`type`=`bg.arbok.open.cert.queryNeedUploadItems`，业务载荷放在 Body 的 `params` |

**Description:** Query certification items that need to be uploaded for a product.

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── certType (INTEGER **必填**)
    └── productId (LONG **必填**)
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| certType | INTEGER | **是** | certType |
| productId | LONG | **是** | productId |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "certType": 1,
    "productId": 1
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
    ├── certNeedUploadItems[] (OBJECT[])
    ├── certNeedUploadItems[].aliasName (STRING)
    ├── certNeedUploadItems[].contentType (INTEGER)
    ├── certNeedUploadItems[].expireDays (INTEGER)
    ├── certNeedUploadItems[].expireNoticeDays (INTEGER)
    ├── certNeedUploadItems[].expireTime (INTEGER)
    ├── certNeedUploadItems[].expireType (INTEGER)
    ├── certNeedUploadItems[].hasExpireTime (BOOLEAN)
    ├── certNeedUploadItems[].needShowCustomer (BOOLEAN)
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
| certNeedUploadItems[] | OBJECT[] | Partner Response Example |
| certNeedUploadItems[].aliasName | STRING | Partner Response Example |
| certNeedUploadItems[].contentType | INTEGER | Partner Response Example |
| certNeedUploadItems[].expireDays | INTEGER | Partner Response Example |
| certNeedUploadItems[].expireNoticeDays | INTEGER | Partner Response Example |
| certNeedUploadItems[].expireTime | INTEGER | Partner Response Example |
| certNeedUploadItems[].expireType | INTEGER | Partner Response Example |
| certNeedUploadItems[].hasExpireTime | BOOLEAN | Partner Response Example |
| certNeedUploadItems[].needShowCustomer | BOOLEAN | Partner Response Example |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | result |
| success | BOOLEAN | success |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_arbok_cert_query_need_upload_items.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "certType": 1,     "productId": 1   } }'
```
