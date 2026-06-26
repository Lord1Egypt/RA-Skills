# 合规标签查询 — `bg.goods.compliancelabel.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_goods_compliancelabel_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=c49495eb93904c93b750e9798c95e7db |
| **网关** | `POST /temu/proxy`，`type`=`bg.goods.compliancelabel.get`，业务载荷放在 Body 的 `params` |

**Description:** Query compliance labels for goods.

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── page (INTEGER)
    └── pageSize (INTEGER)
    └── productIds (LONG[])
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | INTEGER | 否 | Page Number |
| pageSize | INTEGER | 否 | Page Size |
| productIds | LONG[] | 否 | spu ids |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "productIds": [
      1,
      1
    ],
    "pageSize": 1,
    "page": 1
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
    ├── pageResult (OBJECT)
    ├── pageResult.data[] (OBJECT[])
    ├── pageResult.data[].productId (INTEGER)
    ├── pageResult.data[].skuComplianceLabels[] (OBJECT[])
    ├── pageResult.data[].skuComplianceLabels[].complianceLabelPics[] (STRING[])
    ├── pageResult.data[].skuComplianceLabels[].complianceLabelStatus (INTEGER)
    ├── pageResult.data[].skuComplianceLabels[].productSkuId (INTEGER)
    ├── pageResult.totalCount (INTEGER)
```

> Partner **Response** 表仅含顶层字段；`result` 下全部子字段按 **Response 表层级** 与 **Response Example** 合并展开。

### Partner Response 表（HTML 导出可见行）

| 参数 | 类型 | 说明 |
|------|------|------|
| result | OBJECT | — |
| success | BOOLEAN | success |
| errorCode | INTEGER | error Code |
| errorMsg | STRING | error Msg |

### `result` 及下级（全部展开）

| 参数 | 类型 | 说明 |
|------|------|------|
| errorCode | INTEGER | error Code |
| errorMsg | STRING | error Msg |
| pageResult | OBJECT | Partner Response Example |
| pageResult.data[] | OBJECT[] | Partner Response Example |
| pageResult.data[].productId | INTEGER | Partner Response Example |
| pageResult.data[].skuComplianceLabels[] | OBJECT[] | Partner Response Example |
| pageResult.data[].skuComplianceLabels[].complianceLabelPics[] | STRING[] | Partner Response Example |
| pageResult.data[].skuComplianceLabels[].complianceLabelStatus | INTEGER | Partner Response Example |
| pageResult.data[].skuComplianceLabels[].productSkuId | INTEGER | Partner Response Example |
| pageResult.totalCount | INTEGER | Partner Response Example |
| result | OBJECT | — |
| success | BOOLEAN | success |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_goods_compliancelabel_get.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "productIds": [       1,       1     ],     "pageSize": 1,     "page": 1   } }'
```
