# 退货面单准备信息 — `temu.aftersales.returnlabel.prepare.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_returns_refunds_aftersales_returnlabel_prepare_get.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=d3d2812d87034d35adb016972349fcb0&sub_menu_code=f6d52305e84d4945b2b1c8d3218bbe20 |
| **网关** | `POST /temu/proxy`，`type`=`temu.aftersales.returnlabel.prepare.get`，业务载荷放在 Body 的 `params` |

**Description:** Get return label preparation information (pick-up times and warehouses).

> **`parentAfterSalesSn`** 与 **`parentOrderSn`** 均为必填。
> 上传面单前通常先调本接口获取 **`availableReturnWarehouseList`** 与上门揽收时间窗。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，**`managementType=semi-managed`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── parentAfterSalesSn (STRING, 必填)
    └── parentOrderSn (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentAfterSalesSn | STRING | **是** | Parent after-sales order number. |
| parentOrderSn | STRING | **是** | Parent order number. |

> 官方 Request 表将顶层 **`request`** 标为选填（False）；标 **必填** 的字段须在 **`params.request`** 中提供。Partner **Request Example** CURL 将业务字段写在 JSON 顶层；经 LinkFox 网关时建议放在 **`params.request`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-001",
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
    ├── userPickUpTimezone (STRING)
    ├── userSelectedPickUpTimeList[] → startTimestamp, endTimestamp
    ├── availableReturnWarehouseList[] → warehouseId, warehouseName
    └── merchantLatestPickUpTime (LONG)
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
| userPickUpTimezone | STRING | User pick-up timezone（用户上门揽收时区） |
| userSelectedPickUpTimeList | OBJECT[] | User-selected pick-up time intervals（可选揽收时间段） |
| availableReturnWarehouseList | OBJECT[] | Available return warehouses（可选退货仓列表） |
| merchantLatestPickUpTime | LONG | Merchant latest pick-up time（商家最晚揽收时间，毫秒时间戳） |

#### `userSelectedPickUpTimeList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| startTimestamp | LONG | Interval start（毫秒） |
| endTimestamp | LONG | Interval end（毫秒） |

#### `availableReturnWarehouseList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| warehouseId | STRING | Warehouse ID |
| warehouseName | STRING | Warehouse name |

---

## Error Code（Partner 表）

| errorCode | errorMsg | Error SOP / 处理建议 |
|-----------|----------|----------------------|
| 130010001 | The parameter is illegal. Please check if the input parameter meets the regulations. | 见 Partner 文档；修正入参或售后状态后重试 |
| 130010005 | operate forbid | 见 Partner 文档；修正入参或售后状态后重试 |

---

## 脚本

```bash
export LINKFOXAGENT_API_KEY="<key>"
python scripts/us_returns_refunds_aftersales_returnlabel_prepare_get.py '{"accessToken": "TOKEN", "tokenPurpose": "order-shipping", "request": {"parentOrderSn": "PO-001", "parentAfterSalesSn": "PAS-001"}}'
```

**典型流程：** → [temu-aftersales-carrier-get](./temu-aftersales-carrier-get.md) 取承运商 → [temu-aftersales-upload-returnlabel](./temu-aftersales-upload-returnlabel.md) 上传面单。
