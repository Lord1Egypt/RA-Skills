# 在线发货物流类型 — `temu.logistics.shiplogisticstype.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_buy_shipping_logistics_shiplogisticstype_get.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=38e79b35d2cb463d85619c1c786dd303&sub_menu_code=81e2cc2b0d6f4443b29ea8d1596e0fca |
| **网关** | `POST /temu/proxy`，`type`=`temu.logistics.shiplogisticstype.get`，业务载荷放在 Body 的 `params` |

**Description:** Merchant can use this API to get all online-shipment logisticstype. After that, they can call `bg.logistics.shipment.create` to buy-shipping on Temu. Once you choose to buy-shipping with ship logistics type, Temu will automatically chose the most recommended channel id and buy-shipping for you.

（获取全部**在线发货**（online-shipment）可用的物流类型；选定类型后可调用 **`bg.logistics.shipment.create`** 在 Temu 平台购标；Temu 会按所选 **ship logistics type** 自动选择推荐 **channel id** 并完成购标。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**。

**Permission Package（Partner）：**

| Permission Package | App type |
|--------------------|----------|
| Semi Online Call Shipment Management | private, public |
| Local Order Fulfillment Management | private, public |

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── regionId (LONG, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| regionId | LONG | **是** | regionId（请求区域 ID）。错误码 **120011072** 提示：美国站请求区域为 **US**，其他非欧洲国家为 **global**；请与业务站点一致。美国站订单/物流类接口常用 **`regionId=211`**（USA），见 [regionId 编码说明](https://partner.temu.com/documentation?menu_code=38e79b35d2cb463d85619c1c786dd303&sub_menu_code=97bf9f5f4f454a589fb3192725bfeb7a) 与 `linkfox-temu-order-us`；Partner **Request Example**  CURL 示例为 `regionId: 1`，以实际调通值为准。 |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`request.regionId`** 为必填（True）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "regionId": 211
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；网关解析后通常直接见到 `success` / `errorCode` / `errorMsg` / `result`（与 **Response Example** 一致）。下列层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── regionId
    └── shipLogisticsTypeInfoDTOList[] (OBJECT[])
        ├── logisticsProviderLabelList[] (STRING[])
        ├── shipLogisticsType
        ├── shippingCompanyName
        └── shipCompanyId
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | result（业务结果对象） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| regionId | LONG | regionId（与请求区域对应的区域 ID；Response Example 中与入参呼应） |
| shipLogisticsTypeInfoDTOList | OBJECT[] | 在线发货物流类型列表（可选物流类型及承运商信息） |

#### `shipLogisticsTypeInfoDTOList[]` 元素字段

> 下列字段在 Partner **Response** 表中位于 **`result`** 子树（需在线文档点击 **Expand** 展开）；本 skill 按 **Response Example** 与购标流程语义补全说明。若在线 Response 表有更完整描述，以 Partner 为准。

| 参数 | 类型 | 说明 |
|------|------|------|
| shipLogisticsType | STRING | Ship logistics type（发货物流类型编码/标识；购标时在 **`bg.logistics.shipment.create`** 等接口中选择此类型，Temu 将自动匹配推荐 channel） |
| shippingCompanyName | STRING | Shipping company name（物流公司/承运商名称） |
| shipCompanyId | LONG | Ship company ID（物流公司 ID） |
| logisticsProviderLabelList | STRING[] | Logistics provider label list（物流服务商标签列表，用于展示或筛选） |

> 调用成功时先判断 **`success === true`**，再遍历 **`result.shipLogisticsTypeInfoDTOList`**，选定 **`shipLogisticsType`** 后调用 [**`bg.logistics.shipment.create`**](./bg-logistics-shipment-create.md) 完成购标。

---

## Error Code（Partner 摘录）

| Error Code | Error Message |
|------------|---------------|
| 120011001 | System abnormality, please check the data and try again |
| 120011002 | Invalid request parameters. |
| 120011072 | The request area is incorrect. Please check the request area and replace it with the correct request area. The request area for the United States is US, and the request area for other non-European countries is global. |

---

## 典型用法

```text
1. bg.logistics.warehouse.list.get          → 购标可用仓库
2. temu.logistics.shiplogisticstype.get     → 本接口：在线发货物流类型列表
3. [bg.logistics.shipment.create](./bg-logistics-shipment-create.md) → 购标
4. 打印面单 / 订单状态刷新                   → 其他 Buy-Shipping 接口（待接入）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_buy_shipping_logistics_shiplogisticstype_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "regionId": 211
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "temu.logistics.shiplogisticstype.get",
  "params": {
    "request": {
      "regionId": 211
    }
  }
}'
```
