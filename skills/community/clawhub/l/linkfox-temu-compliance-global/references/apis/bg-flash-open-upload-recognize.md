# 上传识别（Flash） — `bg.flash.open.upload.recognize`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_flash_upload_recognize.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=960adb7a9d1f47069cdc0a9abd686dc9 |
| **网关** | `POST /temu/proxy`，`type`=`bg.flash.open.upload.recognize`，业务载荷放在 Body 的 `params` |

**Description:** Upload and recognize compliance-related images (Flash open API).

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── clientId (STRING)
    └── skuId (LONG)
    └── skuSame (BOOLEAN)
    └── spuId (LONG)
    └── uploadImageList (OBJECT[])
    └── uploadImageList[].image (STRING)
    └── uploadImageList[].position (INTEGER)
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| clientId | STRING | 否 | Open platform gateway transparently transmits parameters, not user-provided parameters |
| skuId | LONG | 否 | skuId |
| skuSame | BOOLEAN | 否 | Is the sku consistent |
| spuId | LONG | 否 | spuId |
| uploadImageList | OBJECT[] | 否 | Merchant uploads picture list |
| uploadImageList[].image | STRING | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |
| uploadImageList[].position | INTEGER | — | Partner Request Example（CURL `-d` 展开；Request 表未列出子级时补充） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "clientId": "test",
    "uploadImageList": [
      {
        "image": "test",
        "position": 1
      }
    ],
    "skuSame": true,
    "spuId": 1,
    "skuId": 1
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
    ├── checkResult (BOOLEAN)
    ├── ruleCheckResult[] (OBJECT[])
    ├── ruleCheckResult[].ruleName (STRING)
    ├── ruleCheckResult[].ruleStatus (INTEGER)
```

> Partner **Response** 表仅含顶层字段；`result` 下全部子字段按 **Response 表层级** 与 **Response Example** 合并展开。

### Partner Response 表（HTML 导出可见行）

| 参数 | 类型 | 说明 |
|------|------|------|
| result | OBJECT | Return to detailed information |
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |

### `result` 及下级（全部展开）

| 参数 | 类型 | 说明 |
|------|------|------|
| checkResult | BOOLEAN | Partner Response Example |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Return to detailed information |
| ruleCheckResult[] | OBJECT[] | Partner Response Example |
| ruleCheckResult[].ruleName | STRING | Partner Response Example |
| ruleCheckResult[].ruleStatus | INTEGER | Partner Response Example |
| success | BOOLEAN | success |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_flash_upload_recognize.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "clientId": "test",     "uploadImageList": [       {         "image": "test",         "position": 1       }     ],     "skuSame": true,     "spuId": 1,     "skuId": 1   } }'
```
