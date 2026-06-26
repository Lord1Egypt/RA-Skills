# 预约上门揽收 — `temu.logistics.shipment.pickup.reservation.create`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_buy_shipping_logistics_shipment_pickup_reservation_create.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=cf516cfc49364acba34be29c2600ec20&sub_menu_code=aff85d40b1364572a8383bcf5171f75b |
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.shipment.pickup.reservation.create`，业务载荷放在 Body 的 `params` |

**Description:** The `temu.logistics.shipment.pickup.reservation.create` API enables sellers to schedule package pickups. When multiple packages meet the criteria for consolidated pickup appointments, they will be merged into a single reservation (`reservationSn`). Note: Reservation results must be retrieved via `temu.logistics.shipment.pickup.reservation.result.get`.

（卖家为已购标包裹**预约上门揽收**；符合合并条件的多个包裹将合并为同一预约（**`reservationSn`**）。**预约结果须异步查询** [**`temu.logistics.shipment.pickup.reservation.result.get`**](./temu-logistics-shipment-pickup-reservation-result-get.md)。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：**  
> - **`packageSnList`** 来自 [**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md)（购标成功）。  
> - **`pickupStartTime`** / **`pickupEndTime`** 宜来自 [**`bg.logistics.shippingservices.get`**](./bg-logistics-shippingservices-get.md) 返回的 **`availablePickupTimeSlotList`**（错误码 **120019025**）。  
> - 单次请求的 **`packageSnList`** 须来自**同一渠道、同一仓库**（**120019002**），且**最多 50** 个包裹（**120019030**）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── pickupStartTime (LONG, 必填)
    ├── pickupEndTime (LONG, 必填)
    └── packageSnList[] (STRING[], 必填，最多 50)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pickupStartTime | LONG | **是** | The start time for scheduling pickup, with a timestamp of seconds（预约上门揽收**开始时间**，**Unix 秒级时间戳**） |
| pickupEndTime | LONG | **是** | The end time for scheduling pickup, with a timestamp of seconds（预约上门揽收**结束时间**，**Unix 秒级时间戳**；须晚于 **`pickupStartTime`**） |
| packageSnList | STRING[] | **是** | packageSn list, maximum 50（需要预约揽收的**包裹号列表**，**单次最多 50 个**；须为同一物流渠道、同一仓库下的包裹） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但上述三个字段均为必填。Partner **Request Example** CURL 将字段写在顶层，经 LinkFox 网关时建议放在 **`params.request`** 下。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pickupStartTime": 1717200000,
    "pickupEndTime": 1717203600,
    "packageSnList": ["PKG-001", "PKG-002"]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；**`result`** 在导出 HTML 中为折叠状态。下列层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    └── pickupReservationList[] (OBJECT[])
        ├── pickupWarehouseId
        ├── packageSnList[] (STRING[])
        ├── pickupStartTime
        └── pickupEndTime
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | result（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| pickupReservationList | OBJECT[] | Pickup reservation list（本次提交的揽收预约分组列表；符合合并条件的包裹可能合并为一组，对应一个 **`reservationSn`**，详见 Partner 说明与 **`temu.logistics.shipment.pickup.reservation.result.get`**） |

#### `pickupReservationList[]` 元素字段

> 下列字段来自 **Response Example**；若在线 Response 表有 **`reservationSn`** 等补充字段，以 Partner 在线文档为准。

| 参数 | 类型 | 说明 |
|------|------|------|
| pickupWarehouseId | STRING | Pickup warehouse ID（揽收仓库 ID） |
| packageSnList | STRING[] | Package SN list（本预约分组内包含的包裹号列表） |
| pickupStartTime | LONG | Scheduled pickup start time（本组预约的揽收开始时间，Unix 秒级时间戳） |
| pickupEndTime | LONG | Scheduled pickup end time（本组预约的揽收结束时间，Unix 秒级时间戳） |

> 接口 Description 说明：多包裹满足合并条件时将合并为单一预约（**`reservationSn`**）。同步响应中的 **`pickupReservationList`** 反映分组与时段；**最终预约是否成功、`reservationSn`、失败原因等须调用 **`temu.logistics.shipment.pickup.reservation.result.get`** 查询（Partner 明确要求）。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文摘要） | 处理建议 |
|--------|----------------------|----------|
| 120019030 | The number of packages must be less than {*} | **`packageSnList`** 不超过 **50** 个 |
| 120019009 | Invalid pickup reservation time. See pickupRules for valid options. | 按 **`pickupRules`** / 查价返回时段重选 |
| 120019025 | pickupStartTime or pickupEndTime invalid; get valid time slot from bg.logistics.shippingservices.get | 使用 [**shippingservices.get**](./bg-logistics-shippingservices-get.md) 的 **`availablePickupTimeSlotList`** |
| 120019002 | PackageSn doesn't match; same channel and same warehouse | 同一请求内包裹须同渠道、同仓 |
| 120019005 | PackageSn in packageSnList is invalid | 核对 **`packageSn`** 是否有效、已购标 |
| 120019006 | Pickup reservation of this package is ongoing | 勿重复预约 |
| 120019023 | Duplicated packageSn in one api call | 去重 **`packageSnList`** |
| 120019001 | Haven't support pickup reservation of this channel through open api yet | 该渠道暂不支持 OpenAPI 预约揽收 |
| 120011002 | Invalid request parameters. | 检查必填字段与时间戳 |

---

## 典型用法

```text
1. bg.logistics.shipment.create              → 购标 packageSn
2. bg.logistics.shippingservices.get       → availablePickupTimeSlotList（pickupStartTime / pickupEndTime）
3. temu.logistics.shipment.pickup.reservation.create（本接口） → 提交预约
4. temu.logistics.shipment.pickup.reservation.result.get → 查询 reservationSn 与预约结果
5. （可选）temu.logistics.shipment.pickup.reservation.cancel → 取消预约（见 [文档](./temu-logistics-shipment-pickup-reservation-cancel.md)）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_buy_shipping_logistics_shipment_pickup_reservation_create.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "pickupStartTime": 1717200000,
    "pickupEndTime": 1717203600,
    "packageSnList": ["PKG-001", "PKG-002"]
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.shipment.pickup.reservation.create",
  "params": {
    "request": {
      "pickupStartTime": 1717200000,
      "pickupEndTime": 1717203600,
      "packageSnList": ["PKG-001"]
    }
  }
}'
```
