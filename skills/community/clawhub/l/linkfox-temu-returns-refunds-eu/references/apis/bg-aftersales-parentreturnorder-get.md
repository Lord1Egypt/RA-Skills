# 父退货物流信息 — `bg.aftersales.parentreturnorder.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_returns_refunds_aftersales_parentreturnorder_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.aftersales.parentreturnorder.get`，业务载荷放在 Body 的 `params` |

**Description:** Query parent return order logistics information.

> **`parentAfterSalesSn`** 必填；**`afterSalesSn`** 选填，用于限定子售后单。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── parentAfterSalesSn (STRING, 必填)
    └── afterSalesSn (STRING, 否)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentAfterSalesSn | STRING | **是** | parent after-sales order number. |
| afterSalesSn | STRING | 否 | after-sales order number. |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentAfterSalesSn": "PAS-001",
    "afterSalesSn": "AS-001"
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
    └── logisticsInfoList[]
        ├── carrierName (STRING)
        ├── returnWarehouseRegion1Name (STRING)
        ├── returnWarehouseType (INTEGER)
        └── trackingNumber (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果对象（见下表） |

### `logisticsInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| carrierName | STRING | Carrier name（承运商名称） |
| returnWarehouseRegion1Name | STRING | Return warehouse primary region name（退货仓一级区域名称） |
| returnWarehouseType | INTEGER | Return warehouse type（退货仓类型） |
| trackingNumber | STRING | Tracking number（物流跟踪号） |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 130010001 | The parameter is illegal. Please check if the input parameter meets the regulations. | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/eu_returns_refunds_aftersales_parentreturnorder_get.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {"parentAfterSalesSn": "PAS-001", "afterSalesSn": "AS-001"}}'
```

**典型流程：** 退货寄出后查询 **`logisticsInfoList`** 跟踪号与退货仓信息。
