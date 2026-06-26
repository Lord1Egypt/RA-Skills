# 实拍图上传（Flash） — `bg.flash.open.upload.real.image`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_compliance_flash_upload_real_image.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=fb16b05f7a904765aac4af3a24b87d4a&sub_menu_code=ef77dada37ac49569f6e7c787dd696d9 |
| **网关** | `POST /temu/proxy`，`type`=`bg.flash.open.upload.real.image`，业务载荷放在 Body 的 `params` |

**Description:** Upload real product images for compliance verification (Flash open API).

> 默认 **`site=global`**、**`tokenPurpose=product-inventory`**。入参来自 Partner **Request** 表；出参来自 **Response** 表 + **Response Example** 展开。

---

## Request 结构（Partner Request 表）

```text
params
└── request (OBJECT)
    └── clientId (STRING)
    └── image (STRING)
```

### `request` 内字段（Partner Request 表 + 未展开子级自 Request Example 补充）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| clientId | STRING | 否 | Kaiping clientId |
| image | STRING | 否 | Supported formats include: jpg/jpeg, png and other image formats. Note that the input image must be transcoded into base64 encoding. |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "site": "global",
  "tokenPurpose": "product-inventory",
  "request": {
    "image": "test",
    "clientId": "test"
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
| result | OBJECT | Return to detailed information |
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |

### `result` 及下级（全部展开）

| 参数 | 类型 | 说明 |
|------|------|------|
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Return to detailed information |
| success | BOOLEAN | success |
| url | STRING | Partner Response Example |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_compliance_flash_upload_real_image.py '{   "accessToken": "TOKEN",   "site": "global",   "tokenPurpose": "product-inventory",   "request": {     "image": "test",     "clientId": "test"   } }'
```
