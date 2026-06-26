# 售后签名获取 — `temu.aftersales.signature.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_returns_refunds_aftersales_signature_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.aftersales.signature.get`，业务载荷放在 Body 的 `params` |

**Description:** Get after-sales API signature.

> Partner Request 表仅含空 **`request`** 对象，无业务字段；**Request Example** 亦仅网关公共参数。
> 若上传面单等接口要求签名，先调本接口取 **`result.signature`**。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {}
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result
    └── signature (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果对象（见下表） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| signature | STRING | Signature string for subsequent after-sales calls（后续售后接口使用的签名字符串） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 130010001 | The parameter is illegal. Please check if the input parameter meets the regulations. | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_returns_refunds_aftersales_signature_get.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {}}'
```

**典型流程：** 与 [temu-aftersales-upload-returnlabel](./temu-aftersales-upload-returnlabel.md) 等配合使用。
