# 退货地址查询 — `temu.aftersales.returnaddress.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_returns_refunds_aftersales_returnaddress_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.aftersales.returnaddress.get`，业务载荷放在 Body 的 `params` |

**Description:** Query return shipping address for after-sales.

> 仅 **`parentAfterSalesSn`** 必填。
> 错误码 **18002xxxx** 表示国家未开通、未签 DPA、全托管/仅退款/已上传面单等场景不支持查地址（见 Error Code 表）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── parentAfterSalesSn (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentAfterSalesSn | STRING | **是** | parentAfterSalesSn |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentAfterSalesSn": "PAS-001"
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success / errorCode / errorMsg
└── result
    ├── receiptAdditionalName, receiptName
    ├── regionName1 … regionName4
    ├── mail, mobile, backupMobile
    ├── addressLine1 … addressLine3, addressLineAll
    └── postCode
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
| receiptAdditionalName | STRING | Additional recipient name（收件人附加名） |
| receiptName | STRING | Recipient name（收件人姓名） |
| regionName1 | STRING | Region level 1 name（一级地区名） |
| regionName2 | STRING | Region level 2 name |
| regionName3 | STRING | Region level 3 name |
| regionName4 | STRING | Region level 4 name |
| mail | STRING | Email |
| mobile | STRING | Mobile phone |
| backupMobile | STRING | Backup mobile |
| addressLine1 | STRING | Address line 1 |
| addressLine2 | STRING | Address line 2 |
| addressLine3 | STRING | Address line 3 |
| addressLineAll | STRING | Full address line（完整地址拼接） |
| postCode | STRING | Postal code |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 180020001 | This country has not yet opened address query capabilities | 见 Partner 文档；修正入参或售后状态后重试 |
| 180020008 | Please sign on DPA agreement first | 见 Partner 文档；修正入参或售后状态后重试 |
| 180021001 | full managed, unSupport query address | 见 Partner 文档；修正入参或售后状态后重试 |
| 180021002 | only refund type, unSupport query address | 见 Partner 文档；修正入参或售后状态后重试 |
| 180021003 | uploaded label, unSupport query address | 见 Partner 文档；修正入参或售后状态后重试 |
| 180021004 | no need upload label, unSupport query address | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_returns_refunds_aftersales_returnaddress_get.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {"parentAfterSalesSn": "PAS-001"}}'
```

**典型流程：** 买家需自行寄回时先查 **`result`** 退货地址再发货或上传面单。
