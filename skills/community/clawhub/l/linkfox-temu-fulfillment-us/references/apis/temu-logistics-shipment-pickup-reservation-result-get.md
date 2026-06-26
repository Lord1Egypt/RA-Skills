# 查询上门揽收预约结果 — `temu.logistics.shipment.pickup.reservation.result.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_buy_shipping_logistics_shipment_pickup_reservation_result_get.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=cf516cfc49364acba34be29c2600ec20&sub_menu_code=5cfaf127fdea4d419c6c9aa9c1b2536a |
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.shipment.pickup.reservation.result.get`，业务载荷放在 Body 的 `params` |

**Description:** The `temu.logistics.shipment.pickup.reservation.result.get` API retrieves reservation details for the current package. When multiple packages correspond to one `reservationSn`, the response returns all packages under that reservation.

（查询**上门揽收预约**的异步处理结果。传入 **`packageSnList`** 后，返回各包裹对应的 **`reservationSn`**、**`reservationStatus`** 及该预约下包含的全部 **`packageSnList`**；多个包裹合并为同一预约时，响应会返回该 **`reservationSn`** 下的全部包裹。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。  
> **前置依赖：** 须先调用 [**`temu.logistics.shipment.pickup.reservation.create`**](./temu-logistics-shipment-pickup-reservation-create.md) 提交预约；本接口用于异步查询预约是否成功及 **`reservationSn`**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── packageSnList[] (STRING[], 必填，最多 50)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| packageSnList | STRING[] | **是** | packageSn list, maximum 50（需要查询预约结果的**包裹号列表**，**单次最多 50 个**；通常传入 [**pickup.reservation.create**](./temu-logistics-shipment-pickup-reservation-create.md) 时使用的 **`packageSnList`**） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`packageSnList`** 为必填（True）。Partner **Request Example** CURL 将 **`packageSnList`** 写在顶层，经 LinkFox 网关时建议放在 **`params.request.packageSnList`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSnList": ["PKG-001", "PKG-002"]
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；**`result`** 在导出 HTML 中为折叠状态，下列子层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    └── reservationResultList[] (OBJECT[])
        ├── reservationSn
        ├── packageSnList[] (STRING[])
        └── reservationStatus
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
| reservationResultList | OBJECT[] | Reservation result list（按请求 **`packageSnList`** 返回的预约结果列表；同一 **`reservationSn`** 下可能包含多个包裹） |

#### `reservationResultList[]` 元素字段

> Partner **Response** 表中 **`result`** 子行在导出 HTML 中为折叠状态；下列字段与类型来自 **Response Example**，说明结合接口 Description 整理。若 Partner 在线文档 **Expand** 后对 **`reservationStatus`** 有枚举说明，以在线表为准。

| 参数 | 类型 | 说明 |
|------|------|------|
| reservationSn | STRING | Reservation serial number（预约单号/预约序列号；[**pickup.reservation.create**](./temu-logistics-shipment-pickup-reservation-create.md) 合并预约后生成的唯一标识） |
| packageSnList | STRING[] | Package SN list under this reservation（该 **`reservationSn`** 下包含的全部包裹号；当多个包裹对应同一预约时，此处返回该预约下的**所有**包裹，而不仅是请求中的单个 **`packageSn`**） |
| reservationStatus | INTEGER | Reservation status（预约状态；Response Example 为 **`1`**；具体枚举含义以 Partner 在线 Response 表为准，可轮询本接口直至预约处理完成） |

> 调用成功时先判断 **`success === true`**，再遍历 **`result.reservationResultList`**，按 **`packageSn`** 匹配条目，查看 **`reservationStatus`** 与 **`reservationSn`**。若多个包裹共享同一 **`reservationSn`**，**`packageSnList`** 会列出该预约下的全部包裹。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 120011002 | Invalid request parameters. | 检查 **`packageSnList`** 非空且格式正确 |

---

## 典型用法

```text
1. bg.logistics.shipment.create                         → 购标，获得 packageSn
2. bg.logistics.shippingservices.get                    → 可选揽收时段
3. temu.logistics.shipment.pickup.reservation.create    → 提交上门揽收预约
4. temu.logistics.shipment.pickup.reservation.result.get → 本接口：查询 reservationSn / reservationStatus
5. （可选）temu.logistics.shipment.pickup.reservation.cancel → 取消预约（见 [文档](./temu-logistics-shipment-pickup-reservation-cancel.md)）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_buy_shipping_logistics_shipment_pickup_reservation_result_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "packageSnList": ["PKG-001", "PKG-002"]
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.shipment.pickup.reservation.result.get",
  "params": {
    "request": {
      "packageSnList": ["PKG-001"]
    }
  }
}'
```
