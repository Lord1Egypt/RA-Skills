# 哈啰顺风车 MCP API

## 服务端点

| 环境 | 地址 |
|------|------|
| 生产 | `https://hellohitchapi.hellobike.com/ai-openplatform/mcp` |
| 测试 | `https://uat-hellohitchapi.hellobike.com/ai-openplatform/mcp` |

## 鉴权

HTTP Header 中携带 API Key：
```
Authorization: {your-api-key}
```

## 响应结构

所有工具遵循 MCP 规范返回：
```json
{
  "content": [{ "type": "text", "text": "{\"key\": \"value\"}" }],
  "isError": true
}
```
`content[0].text` 为 JSON 字符串，解析后为业务数据。`isError` 仅在异常时出现。

---

## 地图工具

### maps_textsearch

按关键词搜索地点/POI。所有需要经纬度的操作必须先通过此工具获取坐标。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 地点关键词，如"杭州东站" |
| city_code | string | 是 | 城市区号，如上海 021、杭州 0571 |
| lat | string | 否 | 当前位置纬度，传入后优先返回附近结果 |
| lon | string | 否 | 当前位置经度，与 lat 配套 |
| pageSize | integer | 否 | 返回条数，默认 10，上限 20 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 地点名称 |
| address | string | 详细地址 |
| cityCode | string | 城市区号 |
| cityName | string | 城市名称 |
| adCode | string | 区县编码 |
| lat | string | 纬度 |
| lon | string | 经度 |

---

## 顺风车工具

### hitch_estimate_price

获取运力列表和预估价格。返回的 `priceTraceId` 是创建订单的必要凭证。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| start_name | string | 是 | 起点名称 |
| start_lat | string | 是 | 起点纬度 |
| start_lon | string | 是 | 起点经度 |
| end_name | string | 是 | 终点名称 |
| end_lat | string | 是 | 终点纬度 |
| end_lon | string | 是 | 终点经度 |
| start_city_code | string | 是 | 起点城市区号 |
| end_city_code | string | 否 | 终点城市区号（跨城时建议传入） |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| distanceKm | string | 起终点直线距离（公里） |
| priceTraceId | string | 询价追踪 ID，下单时必传 |
| capacities[].skuCode | string | 运力编码，下单时放入 selectedCapacities |
| capacities[].displayName | string | 运力名称，如"顺风车拼座" |
| capacities[].estimatedPriceYuan | string | 预估价格（元） |
| capacities[].paymentMode | string | 支付方式，如"后付""预付" |

---

### hitch_create_order

创建顺风车订单。**需用户确认** — 调用前必须完成询价。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| selectedCapacities | array | 是 | 用户选择的 skuCode 数组 |
| priceTraceId | string | 是 | 询价返回的追踪 ID |
| start_name | string | 是 | 起点名称 |
| start_address | string | 是 | 起点详细地址 |
| start_lat | string | 是 | 起点纬度 |
| start_lon | string | 是 | 起点经度 |
| start_city_name | string | 是 | 起点城市名称 |
| start_city_code | string | 是 | 起点城市区号 |
| start_ad_code | string | 是 | 起点区县编码 |
| end_name | string | 是 | 终点名称 |
| end_address | string | 是 | 终点详细地址 |
| end_lat | string | 是 | 终点纬度 |
| end_lon | string | 是 | 终点经度 |
| end_city_name | string | 是 | 终点城市名称 |
| end_city_code | string | 是 | 终点城市区号 |
| end_ad_code | string | 是 | 终点区县编码 |
| idempotencyKey | string | 是 | 幂等键 |
| planDepartureTime | string | 否 | 出发时间（毫秒时间戳），默认即时，最大当前+10天 |
| waitMinutes | integer | 否 | 愿等时长（分钟），默认 10，上限 180 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| paymentModeCode | string | 支付方式编码，如 POSTPAY |
| paymentMode | string | 支付方式，如"后付" |
| needAppPayment | boolean | 是否需要跳转 App 完成支付 |
| nextAction | string | 建议下一步操作标识 |
| nextActionDesc | string | 下一步操作描述 |

---

### hitch_query_order

查询订单详情或进行中订单列表。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderGuid | string | 否 | 指定订单号；不传则返回所有进行中订单 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| statusCode | string | 状态编码 |
| status | string | 状态描述 |
| startAddress | string | 起点地址 |
| endAddress | string | 终点地址 |
| priceText | string | 价格描述 |
| actionHint | string | 当前状态的操作提示 |
| driverInfo | object | 车主信息，仅在车主已接单后返回 |
| driverInfo.name | string | 车主姓名 |
| driverInfo.phone | string | 车主电话 |
| driverInfo.carModel | string | 车型（如 "大众帕萨特"） |
| driverInfo.plateNumber | string | 车牌号 |
| driverInfo.etaMinutes | integer | 预计到达上车点的分钟数 |
| cancelReason | string | 取消原因（仅已取消状态返回） |
| tripDurationMinutes | integer | 行程时长（仅已完成状态返回） |
| actualPrice | string | 实际费用（仅已完成状态返回） |

---

### hitch_cancel_order

取消订单。**需用户确认** — 调用前必须获得用户二次确认。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderGuid | string | 是 | 订单号 |
| idempotencyKey | string | 是 | 幂等键 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| statusCode | string | 取消后状态编码 |
| status | string | 取消后状态描述 |
| cancelStatusBeforeCode | string | 取消前状态编码 |

---

### hitch_invite_driver_list

查询附近顺路车主。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderGuid | string | 是 | 订单号 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| hasNext | boolean | 是否有更多车主 |
| drivers[].driverGuid | string | 司机行程订单号（邀请时传入 driverOrderGuid） |
| drivers[].driverId | integer | 司机用户 ID |
| drivers[].name | string | 司机姓名 |
| drivers[].rating | string | 评分 |
| drivers[].vehicleModelName | string | 车型 |
| drivers[].hitchPercent | string | 顺路度 |
| driverCount | integer | 车主总数 |

---

### hitch_invite_driver

邀请指定车主接单。**需用户确认** — 需用户选择后调用。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderGuid | string | 是 | 乘客订单号 |
| driverOrderGuid | string | 是 | 司机行程订单号（来自 invite_driver_list 的 driverGuid） |
| driverId | integer | 是 | 司机用户 ID |
| hitchPercent | string | 是 | 顺路度，如 "0.85" |
| idempotencyKey | string | 是 | 幂等键，建议 orderGuid + driverId 拼接 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| driverOrderGuid | string | 司机行程订单号 |
| success | boolean | 是否成功 |
| message | string | 结果描述 |

---

### hitch_get_driver_location

查询已接单司机的实时位置。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderGuid | string | 是 | 订单号 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| driverLat | string | 司机纬度 |
| driverLon | string | 司机经度 |
| etaMinute | integer | 预计到达分钟数 |
| etaDesc | string | 到达时间描述 |

---

### hitch_pax_confirm_get_on_car

乘客确认已上车。**不可撤销**。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderGuid | string | 是 | 订单号 |
| idempotencyKey | string | 是 | 幂等键，建议直接用 orderGuid |
| lat | string | 否 | 乘客当前纬度 |
| lon | string | 否 | 乘客当前经度 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| success | boolean | 是否成功 |
| message | string | 结果描述 |

---

### hitch_pax_confirm_reach_destination

乘客确认到达目的地。**不可撤销**。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderGuid | string | 是 | 订单号 |
| idempotencyKey | string | 是 | 幂等键，建议直接用 orderGuid |
| lat | string | 否 | 乘客当前纬度 |
| lon | string | 否 | 乘客当前经度 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| success | boolean | 是否成功 |
| message | string | 结果描述 |

---

### hitch_generate_app_link

生成打开哈啰 App 发单页面的 Deep Link。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| start_name | string | 是 | 起点名称 |
| start_lat | string | 是 | 起点纬度 |
| start_lon | string | 是 | 起点经度 |
| start_city_code | string | 是 | 起点城市区号 |
| start_ad_code | string | 是 | 起点区县编码 |
| end_name | string | 是 | 终点名称 |
| end_lat | string | 是 | 终点纬度 |
| end_lon | string | 是 | 终点经度 |
| end_city_code | string | 是 | 终点城市区号 |
| end_ad_code | string | 是 | 终点区县编码 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| title | string | 跳转文案标题 |
| deepLink | string | Deep Link 地址 |
| description | string | 使用说明 |

---

### hitch_generate_wechat_link

生成微信小程序跳转链接。根据订单当前状态自动选择页面：接单前跳等待页，接单后跳履约页。

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| orderGuid | string | 是 | 订单号 |

**响应字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| orderGuid | string | 订单号 |
| statusCode | string | 订单状态编码 |
| link | string | 小程序跳转链接 |
| description | string | 跳转说明 |

---

## 调用示例

搜索地点 — `maps_textsearch`：
```json
{ "keyword": "杭州东站", "city_code": "0571" }
```

询价 — `hitch_estimate_price`：
```json
{ "start_name": "西溪湿地", "start_lat": "30.271", "start_lon": "120.062", "end_name": "杭州东站", "end_lat": "30.290", "end_lon": "120.220", "start_city_code": "0571" }
```

查询可邀请车主 — `hitch_invite_driver_list`：
```json
{ "orderGuid": "ORDER_GUID" }
```

---

## 错误码

| 错误码 | 含义 | 处理方式 |
|--------|------|----------|
| HITCH_PARAM_INVALID | 请求参数不合法 | 检查必填项是否遗漏，坐标是否为字符串 |
| HITCH_AUTH_INVALID | API Key 无效或过期 | 引导用户重新获取并配置 |
| HITCH_ESTIMATE_EXPIRED | 询价凭证已过期 | 重新调用 hitch_estimate_price |
| HITCH_ORDER_NOT_FOUND | 订单不存在 | 核实订单号 |
| HITCH_ORDER_NOT_CANCELABLE | 当前状态不允许取消 | 车主已接单或行程已开始 |
| HITCH_IDEMPOTENCY_CONFLICT | 幂等键冲突 | 同一个 key 不能用于不同业务参数 |
| HITCH_RATE_LIMITED | 触发限流 | 等待数秒后重试 |
| HITCH_INTERNAL_ERROR | 服务端异常 | 稍后重试，持续出现请联系 aiopen@hellobike.com |

## 常见问题

**预估价和实际费用有差距？**
预估价基于当前路况和距离估算，最终以行程结算金额为准。

**能查历史订单吗？**
MCP 接口仅支持查询通过该渠道创建的未完成订单。已完成订单请在哈啰 App 中查看。

**覆盖哪些城市？**
哈啰顺风车运营的所有大陆城市均可使用。
