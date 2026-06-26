# 合规编辑 — `bg.compliance.edit`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_edit.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=a8829c8ede574d9a97cd3cea7c019bc4 |
| **网关** | `POST /temu/proxy`，`type`=`bg.compliance.edit`，业务载荷放在 Body 的 `params` |

**Description:** Edit product compliance information (governance attributes, GPSR, certificates, etc.).

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── editReqList (OBJECT[] **必填**)
    └── editReqList[].complianceType (INTEGER)
    └── editReqList[].inputText (OBJECT)
    └── editReqList[].inputText.$key (STRING)
    └── editReqList[].inputText.$value (OBJECT)
    └── editReqList[].inputText.$value.lang (OBJECT)
    └── editReqList[].inputText.$value.lang.$key (STRING)
    └── editReqList[].inputText.$value.lang.$value (STRING)
    └── editReqList[].inputText.$value.multiLineInputs (OBJECT[])
    └── editReqList[].inputText.$value.multiLineInputs[].lang (OBJECT)
    └── editReqList[].inputText.$value.multiLineInputs[].lang.$key (STRING)
    └── editReqList[].inputText.$value.multiLineInputs[].lang.$value (STRING)
    └── editReqList[].inputText.$value.multiLineInputs[].name (STRING)
    └── editReqList[].inputText.$value.name (STRING)
    └── editReqList[].properties (OBJECT)
    └── editReqList[].properties.$key (STRING)
    └── editReqList[].properties.$value (INTEGER[])
    └── editReqList[].repList (OBJECT[])
    └── editReqList[].repList[].repId (INTEGER)
    └── productId (LONG **必填**)
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| editReqList | OBJECT[] | **是** | edit single compliance req list |
| editReqList[].complianceType | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText | OBJECT | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$key | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value | OBJECT | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.lang | OBJECT | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.lang.$key | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.lang.$value | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.multiLineInputs | OBJECT[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.multiLineInputs[].lang | OBJECT | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.multiLineInputs[].lang.$key | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.multiLineInputs[].lang.$value | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.multiLineInputs[].name | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].inputText.$value.name | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].properties | OBJECT | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].properties.$key | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].properties.$value | INTEGER[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].repList | OBJECT[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| editReqList[].repList[].repId | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| productId | LONG | **是** | product id |

#### `editReqList[].inputText`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| $key | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| $value | OBJECT | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `editReqList[].inputText.$value`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| lang | OBJECT | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| multiLineInputs | OBJECT[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| name | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `editReqList[].inputText.$value.lang`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| $key | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| $value | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `editReqList[].inputText.$value.multiLineInputs[]`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| lang | OBJECT | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| name | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `editReqList[].inputText.$value.multiLineInputs[].lang`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| $key | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| $value | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

#### `editReqList[].properties`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| $key | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| $value | INTEGER[] | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "productId": 1,
    "editReqList": [
      {
        "inputText": {
          "$key": "test",
          "$value": {
            "name": "test",
            "lang": {
              "$key": "test",
              "$value": "test"
            },
            "multiLineInputs": [
              {
                "name": "test",
                "lang": {
                  "$key": "test",
                  "$value": "test"
                }
              }
            ]
          }
        },
        "repList": [
          {
            "repId": 1
          }
        ],
        "properties": {
          "$key": "test",
          "$value": [
            1,
            1
          ]
        },
        "complianceType": 1
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
| errorCode | INTEGER | errorCode |
| errorMsg | STRING | errorMsg |
| result | OBJECT | result |

### `result` 及下级（全部展开）

| 参数 | 类型 | 说明 |
|------|------|------|
| errorCode | INTEGER | errorCode |
| errorMsg | STRING | errorMsg |
| result | OBJECT | result |
| success | BOOLEAN | success |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_edit.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "productId": 1,     "editReqList": [       {         "inputText": {           "$key": "test",           "$value": {             "name": "test",             "lang": {               "$key": "test",               "$value": "test"             },             "multiLineInputs": [               {                 "name": "test",                 "lang": {                   "$key": "test",                   "$value": "test"                 }               }             ]           }         },         "repList": [           {             "repId": 1           }         ],         "properties": {           "$key": "test",           "$value": [             1,             1           ]         },         "complianceType": 1       }     ]   } }'
```
