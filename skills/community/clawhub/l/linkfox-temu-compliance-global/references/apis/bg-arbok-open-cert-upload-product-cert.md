# 上传商品资质 — `bg.arbok.open.cert.uploadProductCert`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_arbok_cert_upload_product_cert.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=56de04bcafae45509b21edeab57c9fdb |
| **网关** | `POST /temu/proxy`，`type`=`bg.arbok.open.cert.uploadProductCert`，业务载荷放在 Body 的 `params` |

**Description:** Upload product certification / qualification documents.

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── productCatCertReqList (OBJECT[])
    └── productCatCertReqList[].authCode (STRING)
    └── productCatCertReqList[].authCodes (OBJECT[])
    └── productCatCertReqList[].authCodes[].authCode (STRING)
    └── productCatCertReqList[].authCodes[].effectiveTime (INTEGER)
    └── productCatCertReqList[].authCodes[].expireTime (INTEGER)
    └── productCatCertReqList[].authCodes[].fileName (STRING)
    └── productCatCertReqList[].authCodes[].fileUrl (STRING)
    └── productCatCertReqList[].authCodes[].showCustomer (BOOLEAN)
    └── productCatCertReqList[].certType (INTEGER)
    └── productCatCertReqList[].inspectReportFiles (OBJECT[])
    └── productCatCertReqList[].inspectReportFiles[].authCode (STRING)
    └── productCatCertReqList[].inspectReportFiles[].effectiveTime (INTEGER)
    └── productCatCertReqList[].inspectReportFiles[].expireTime (INTEGER)
    └── productCatCertReqList[].inspectReportFiles[].fileName (STRING)
    └── productCatCertReqList[].inspectReportFiles[].fileUrl (STRING)
    └── productCatCertReqList[].inspectReportFiles[].showCustomer (BOOLEAN)
    └── productCatCertReqList[].productCertFiles (OBJECT[])
    └── productCatCertReqList[].productCertFiles[].authCode (STRING)
    └── productCatCertReqList[].productCertFiles[].effectiveTime (INTEGER)
    └── productCatCertReqList[].productCertFiles[].expireTime (INTEGER)
    └── productCatCertReqList[].productCertFiles[].fileName (STRING)
    └── productCatCertReqList[].productCertFiles[].fileUrl (STRING)
    └── productCatCertReqList[].productCertFiles[].showCustomer (BOOLEAN)
    └── productCatCertReqList[].supplementaryMaterials (OBJECT[])
    └── productCatCertReqList[].supplementaryMaterials[].authCode (STRING)
    └── productCatCertReqList[].supplementaryMaterials[].effectiveTime (INTEGER)
    └── productCatCertReqList[].supplementaryMaterials[].expireTime (INTEGER)
    └── productCatCertReqList[].supplementaryMaterials[].fileName (STRING)
    └── productCatCertReqList[].supplementaryMaterials[].fileUrl (STRING)
    └── productCatCertReqList[].supplementaryMaterials[].showCustomer (BOOLEAN)
    └── productId (LONG **必填**)
    └── realPictures (OBJECT[])
    └── realPictures[].imageUrl (STRING)
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productCatCertReqList | OBJECT[] | 否 | productCatCertReqList |
| productCatCertReqList[].authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].authCodes | OBJECT[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].authCodes[].authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].authCodes[].effectiveTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].authCodes[].expireTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].authCodes[].fileName | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].authCodes[].fileUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].authCodes[].showCustomer | BOOLEAN | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].certType | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].inspectReportFiles | OBJECT[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].inspectReportFiles[].authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].inspectReportFiles[].effectiveTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].inspectReportFiles[].expireTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].inspectReportFiles[].fileName | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].inspectReportFiles[].fileUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].inspectReportFiles[].showCustomer | BOOLEAN | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].productCertFiles | OBJECT[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].productCertFiles[].authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].productCertFiles[].effectiveTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].productCertFiles[].expireTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].productCertFiles[].fileName | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].productCertFiles[].fileUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].productCertFiles[].showCustomer | BOOLEAN | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].supplementaryMaterials | OBJECT[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].supplementaryMaterials[].authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].supplementaryMaterials[].effectiveTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].supplementaryMaterials[].expireTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].supplementaryMaterials[].fileName | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].supplementaryMaterials[].fileUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productCatCertReqList[].supplementaryMaterials[].showCustomer | BOOLEAN | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productId | LONG | **是** | productId |
| realPictures | OBJECT[] | 否 | realPictures |
| realPictures[].imageUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `productCatCertReqList[].authCodes[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| effectiveTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| expireTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| fileName | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| fileUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| showCustomer | BOOLEAN | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `productCatCertReqList[].inspectReportFiles[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| effectiveTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| expireTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| fileName | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| fileUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| showCustomer | BOOLEAN | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `productCatCertReqList[].productCertFiles[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| effectiveTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| expireTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| fileName | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| fileUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| showCustomer | BOOLEAN | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `productCatCertReqList[].supplementaryMaterials[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| authCode | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| effectiveTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| expireTime | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| fileName | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| fileUrl | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| showCustomer | BOOLEAN | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "productId": 1,
    "productCatCertReqList": [
      {
        "authCodes": [
          {
            "fileName": "test",
            "fileUrl": "test",
            "showCustomer": true,
            "expireTime": 1,
            "authCode": "test",
            "effectiveTime": 1
          }
        ],
        "productCertFiles": [
          {
            "fileName": "test",
            "fileUrl": "test",
            "showCustomer": true,
            "expireTime": 1,
            "authCode": "test",
            "effectiveTime": 1
          }
        ],
        "supplementaryMaterials": [
          {
            "fileName": "test",
            "fileUrl": "test",
            "showCustomer": true,
            "expireTime": 1,
            "authCode": "test",
            "effectiveTime": 1
          }
        ],
        "certType": 1,
        "inspectReportFiles": [
          {
            "fileName": "test",
            "fileUrl": "test",
            "showCustomer": true,
            "expireTime": 1,
            "authCode": "test",
            "effectiveTime": 1
          }
        ],
        "authCode": "test"
      }
    ],
    "realPictures": [
      {
        "imageUrl": "test"
      }
    ]
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

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_arbok_cert_upload_product_cert.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "productId": 1,     "productCatCertReqList": [       {         "authCodes": [           {             "fileName": "test",             "fileUrl": "test",             "showCustomer": true,             "expireTime": 1,             "authCode": "test",             "effectiveTime": 1           }         ],         "productCertFiles": [           {             "fileName": "test",             "fileUrl": "test",             "showCustomer": true,             "expireTime": 1,             "authCode": "test",             "effectiveTime": 1           }         ],         "supplementaryMaterials": [           {             "fileName": "test",             "fileUrl": "test",             "showCustomer": true,             "expireTime": 1,             "authCode": "test",             "effectiveTime": 1           }         ],         "certType": 1,         "inspectReportFiles": [           {             "fileName": "test",             "fileUrl": "test",             "showCustomer": true,             "expireTime": 1,             "authCode": "test",             "effectiveTime": 1           }         ],         "authCode": "test"       }     ],     "realPictures": [       {         "imageUrl": "test"       }     ]   } }'
```
