# 承运商列表 — `temu.aftersales.carrier.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_returns_refunds_aftersales_carrier_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.aftersales.carrier.get`，业务载荷放在 Body 的 `params` |

**Description:** Query carriers for return label by return warehouse region.

> **`returnWarehouseRegionId1`** 必填（商家退货仓一级区域 ID）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── returnWarehouseRegionId1 (LONG, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| returnWarehouseRegionId1 | LONG | **是** | Merchant return warehouse primary region id. |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "returnWarehouseRegionId1": 1
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
    └── carrierDTOList[]
        ├── carrierId (LONG)
        └── carrierName (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果对象（见下表） |

### `carrierDTOList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| carrierId | LONG | Carrier ID |
| carrierName | STRING | Carrier name |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 130010001 | The parameter is illegal. Please check if the input parameter meets the regulations. | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_returns_refunds_aftersales_carrier_get.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {"returnWarehouseRegionId1": 1}}'
```

**典型流程：** 上传面单前按退货仓区域查询 **`carrierId`**。
