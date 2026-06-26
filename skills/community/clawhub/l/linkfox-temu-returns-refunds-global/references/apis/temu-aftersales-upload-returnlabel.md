# 上传退货面单 — `temu.aftersales.upload.returnlabel`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_returns_refunds_aftersales_upload_returnlabel.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.aftersales.upload.returnlabel`，业务载荷放在 Body 的 `params` |

**Description:** Upload return shipping label.

> **`parentAfterSalesSn`**、**`parentOrderSn`** 必填。
> **`returnLabelDTOList[]`** 子字段在 Partner Request 表中为折叠行，按 **Request Example** 展开（见下表）。
> **`pickUpTimeScheduleMode`**：1 用户偏好时段；2 重新预约时段；3 最晚揽收时间点（与 **`startTimestamp`/`endTimestamp`/`latestTimestamp`** 配合）。
> 成功时 Response Example 无 **`result`** 业务字段，仅 **`success`** / **`errorCode`** / **`errorMsg`**。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── parentAfterSalesSn (STRING, 必填)
    ├── parentOrderSn (STRING, 必填)
    ├── returnLabelDTOList (OBJECT[], 否)
    ├── pickUpTimeScheduleMode (INTEGER, 否)
    ├── startTimestamp (LONG, 否)
    ├── endTimestamp (LONG, 否)
    └── latestTimestamp (LONG, 否)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentAfterSalesSn | STRING | **是** | Parent after-sales order number. |
| parentOrderSn | STRING | **是** | Parent order number. |
| returnLabelDTOList | OBJECT[] | 否 | Return label information. |
| pickUpTimeScheduleMode | INTEGER | 否 | Pick up time scheduling mode, required for pick up, enumerated as follows: 1: Select user's preferred time interval, 2: Re-schedule time interval, 3: Select latest pick up time point. |
| startTimestamp | LONG | 否 | Start timestamp, unit in milliseconds, required for pick up time schedule mode 1 and 2. |
| endTimestamp | LONG | 否 | End timestamp, unit in milliseconds, required for pick up time schedule mode 1 and 2. |
| latestTimestamp | LONG | 否 | Latest timestamp, unit in milliseconds, required for pick up time schedule mode 3. |

#### `returnLabelDTOList[]`（Partner Request 表为折叠行，按 Request Example 展开）

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mallWarehouseId | STRING | 否 | Merchant return warehouse ID（商家退货仓 ID，与 prepare 接口 **`warehouseId`** 对应） |
| returnLabelUrl | STRING | 否 | Return label file URL（退货面单文件 URL） |
| carrierId | LONG | 否 | Carrier ID（承运商 ID，见 [temu-aftersales-carrier-get](./temu-aftersales-carrier-get.md)） |
| trackingNumber | STRING | 否 | Tracking number（物流单号） |
| pickUpCertificateImageUrl | STRING | 否 | Pick-up certificate image URL（上门揽收凭证图片 URL） |

#### `pickUpTimeScheduleMode`

| 值 | 说明 |
|----|------|
| `1` | Select user's preferred time interval |
| `2` | Re-schedule time interval |
| `3` | Select latest pick-up time point |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-001",
    "parentAfterSalesSn": "PAS-001",
    "returnLabelDTOList": [
      {
        "mallWarehouseId": "WH-001",
        "returnLabelUrl": "https://example.com/label.pdf",
        "carrierId": 1,
        "trackingNumber": "1Z999",
        "pickUpCertificateImageUrl": "https://example.com/pickup.jpg"
      }
    ],
    "pickUpTimeScheduleMode": 1,
    "startTimestamp": 1714521600000,
    "endTimestamp": 1714525200000
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；嵌套子行在导出 HTML 中多为折叠状态，下列层级按 **Response 表 + Response Example** 全部展开。

```text
response
├── success (BOOLEAN)
├── errorCode (INTEGER)
└── errorMsg (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |

> 本接口成功时无 `result` 业务体；以 **`success === true`** 判断上传是否成功。

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 130010000 | system error | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010001 | The parameter is illegal. Please check if the input parameter meets the regulations. | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010004 | no afterSales found | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010005 | operate forbid | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010006 | return label invalid | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010007 | tracking number invalid | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/global_returns_refunds_aftersales_upload_returnlabel.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {"parentOrderSn": "PO-001", "parentAfterSalesSn": "PAS-001", "returnLabelDTOList": [{"mallWarehouseId": "WH-001", "returnLabelUrl": "https://example.com/label.pdf", "carrierId": 1, "trackingNumber": "1Z999", "pickUpCertificateImageUrl": "https://example.com/pickup.jpg"}], "pickUpTimeScheduleMode": 1, "startTimestamp": 1714521600000, "endTimestamp": 1714525200000}}'
```

**典型流程：** 在 [returnlabel.prepare.get](./temu-aftersales-returnlabel-prepare-get.md) 与 [carrier.get](./temu-aftersales-carrier-get.md) 之后提交面单与物流信息。
