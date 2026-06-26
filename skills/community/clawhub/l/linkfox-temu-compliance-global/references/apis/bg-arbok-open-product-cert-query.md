# 商品资质查询 — `bg.arbok.open.product.cert.query`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_arbok_product_cert_query.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=5ec78e3b36c34fcba743a75523349fb5 |
| **网关** | `POST /temu/proxy`，`type`=`bg.arbok.open.product.cert.query`，业务载荷放在 Body 的 `params` |

**Description:** Query product certification / qualification information.

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── certTypeList (INTEGER[])
    └── language (STRING)
    └── productId (LONG **必填**)
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| certTypeList | INTEGER[] | 否 | certTypeList |
| language | STRING | 否 | language |
| productId | LONG | **是** | productId |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "productId": 1,
    "certTypeList": [
      1,
      1
    ],
    "language": "test"
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
    ├── productCertList[] (OBJECT[])
    ├── productCertList[].auditStatus (INTEGER)
    ├── productCertList[].certName (STRING)
    ├── productCertList[].certType (INTEGER)
    ├── productCertList[].rejectReason (STRING)
    ├── productCertList[].updateReason (STRING)
    ├── productCertList[].updateStatus (INTEGER)
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
| productCertList[] | OBJECT[] | Partner Response Example |
| productCertList[].auditStatus | INTEGER | Partner Response Example |
| productCertList[].certName | STRING | Partner Response Example |
| productCertList[].certType | INTEGER | Partner Response Example |
| productCertList[].rejectReason | STRING | Partner Response Example |
| productCertList[].updateReason | STRING | Partner Response Example |
| productCertList[].updateStatus | INTEGER | Partner Response Example |
| result | OBJECT | result |
| success | BOOLEAN | success |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_arbok_product_cert_query.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "productId": 1,     "certTypeList": [       1,       1     ],     "language": "test"   } }'
```
