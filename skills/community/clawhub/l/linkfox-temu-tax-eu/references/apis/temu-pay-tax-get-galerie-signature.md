# 获取 Galerie 签名 — `temu.pay.tax.get.galerie.signature`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_tax_get_galerie_signature.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896&sub_menu_code=d6147c0484a341c49790b6dfed7da275 |
| **网关** | `POST /temu/proxy`，`type`=`temu.pay.tax.get.galerie.signature`，业务载荷放在 Body 的 `params` |

**Description:** Get Galerie upload signature for tax-related file operations.

> **网关鉴权字段**由本 skill 处理；业务参数见下方 **`request`**。默认 **`site=eu`**、**`tokenPurpose=product-inventory`**。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT)
```

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
    ├── signature (STRING)
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
| signature | STRING | signature（STRING） |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_tax_get_galerie_signature.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "product-inventory",
  "site": "eu",
  "request": {}
}'
```
