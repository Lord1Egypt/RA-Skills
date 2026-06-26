# 取消上门揽收预约 — `temu.logistics.shipment.pickup.reservation.cancel`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_buy_shipping_logistics_shipment_pickup_reservation_cancel.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.shipment.pickup.reservation.cancel`，业务载荷放在 Body 的 `params` |

**Description:** The `temu.logistics.shipment.pickup.reservation.cancel` API enables sellers to cancel reservationSn.

（卖家按 **`reservationSn`** **取消上门揽收预约**；适用于已通过预约且当前状态允许取消的场景。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：**  
> - **`reservationSn`** 来自 [**`temu.logistics.shipment.pickup.reservation.create`**](./temu-logistics-shipment-pickup-reservation-create.md) 同步返回的 **`pickupReservationList`**，或经 [**`temu.logistics.shipment.pickup.reservation.result.get`**](./temu-logistics-shipment-pickup-reservation-result-get.md) 查询得到的 **`reservationSn`**。  
> - 仅**预约成功**的状态允许取消（错误码 **120019022**）；部分渠道不允许卖家取消（**120019010**）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── reservationSn (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reservationSn | STRING | **是** | reservation Sn（上门揽收预约单号；与 [**pickup.reservation.create**](./temu-logistics-shipment-pickup-reservation-create.md) / [**pickup.reservation.result.get**](./temu-logistics-shipment-pickup-reservation-result-get.md) 返回的 **`reservationSn`** 一致） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`reservationSn`** 为必填（True）。Partner **Request Example** CURL 将 **`reservationSn`** 写在顶层；经 LinkFox 网关时建议放在 **`params.request.reservationSn`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "reservationSn": "RSV-20260101001"
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表仅包含顶层 **`response`** 下的 **`success`**、**`errorCode`**、**`errorMsg`**，**无 `result` 业务对象**（与 **Response Example** 一致）。

```text
response（或解析后的根对象）
├── success
├── errorCode
└── errorMsg
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |

> 调用成功时判断 **`success === true`** 即可；取消结果无额外 **`result`** 载荷。建议取消后再次调用 [**`temu.logistics.shipment.pickup.reservation.result.get`**](./temu-logistics-shipment-pickup-reservation-result-get.md) 确认 **`reservationStatus`** 已变更。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120011002 | Invalid request parameters. | 检查 **`reservationSn`** 格式与非空 |
| 120019007 | The reservationSn is invalid. | 核对 **`reservationSn`** 是否存在、站点是否正确 |
| 120019010 | The channel don't allow seller cancel the pickup reservation. | 当前物流渠道不允许卖家取消预约 |
| 120019022 | Current reservation status don't allow you to cancel the reservation, only successful reservation can be cancelled. | 仅**预约成功**状态可取消；先查 [**pickup.reservation.result.get**](./temu-logistics-shipment-pickup-reservation-result-get.md) |

<details>
<summary>完整错误码列表（4 条，Partner 原文）</summary>

| 错误码 | 错误信息 |
|--------|----------|
| 120011002 | Invalid request parameters. |
| 120019007 | The reservationSn is invalid. |
| 120019010 | The channel don't allow seller cancel the pickup reservation. |
| 120019022 | Current reservation status don't allow you to cancel the reservation, only successful reservation can be cancelled. |

</details>

---

## 典型用法

```text
1. bg.logistics.shipment.create                              → 购标
2. temu.logistics.shipment.pickup.reservation.create         → 提交上门揽收预约
3. temu.logistics.shipment.pickup.reservation.result.get     → 确认 reservationSn、reservationStatus 为成功
4. temu.logistics.shipment.pickup.reservation.cancel（本接口） → 取消预约
5. temu.logistics.shipment.pickup.reservation.result.get     → 复核预约状态
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/eu_buy_shipping_logistics_shipment_pickup_reservation_cancel.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "reservationSn": "RSV-20260101001"
  }
}'
```

```bash
python scripts/temu_eu_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.shipment.pickup.reservation.cancel",
  "params": {
    "request": {
      "reservationSn": "RSV-20260101001"
    }
  }
}'
```
