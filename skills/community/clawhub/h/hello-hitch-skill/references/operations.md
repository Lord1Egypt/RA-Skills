# 顺风车操作手册

各场景的具体调用方式和执行细节。调用任何工具前，先核对 [api.md](./api.md) 中的参数定义。

## 通用约定

- 优先级：用户当前输入 > 默认值
- 所有字符串参数必须用引号包裹
- 起点缺失时直接询问用户，不要从历史对话推测
- 用户拒绝提供位置时回复：无法在缺少位置信息的情况下继续操作

---

## 搜索地点

通过关键词定位地理位置，提取坐标和行政区划信息供后续使用。

调用 `maps_textsearch`：
```json
{
  "keyword": "杭州东站",
  "city_code": "0571"
}
```

从返回中保存六要素：`lat`、`lon`、`cityCode`、`adCode`、`address`、`cityName`。

**地址补全策略**：
- 起终点都有 → 直接询价
- "上班了"/"回家" → 直接询问用户具体地址
- "回家"但没说从哪出发 → 先问当前位置
- 用户说"不对"或更正了地址 → 用更正后的内容重新搜索，已有的询价结果作废

---

## 询价比价

获取可选运力和预估价格。返回的 `priceTraceId` 是下单的必要凭证。

调用 `hitch_estimate_price`：
```json
{
  "start_name": "西溪湿地",
  "start_lat": "30.271",
  "start_lon": "120.062",
  "end_name": "杭州东站",
  "end_lat": "30.290",
  "end_lon": "120.220",
  "start_city_code": "0571"
}
```

拿到运力列表后向用户展示选项：
```
从 [起点] 到 [终点]，约 XX 公里，以下运力可选：
1. 拼座 — 约 XX 元
2. 独享 — 约 XX 元
3. 特惠独享 — 约 XX 元
请回复编号选择（可多选如"1 3"，或回复"全选"）
```

重新询价后旧的 `priceTraceId` 自动作废，只能使用最新的。

---

## 创建订单

传入完整起终点六要素 + 询价凭证 + 用户选择的运力。

调用 `hitch_create_order`：
```json
{
  "selectedCapacities": ["sku_code_1", "sku_code_2"],
  "priceTraceId": "TRACE_ID",
  "start_name": "西溪湿地",
  "start_address": "杭州市西湖区天目山路518号",
  "start_lat": "30.271",
  "start_lon": "120.062",
  "start_city_name": "杭州",
  "start_city_code": "0571",
  "start_ad_code": "330106",
  "end_name": "杭州东站",
  "end_address": "杭州市江干区全福桥路2号",
  "end_lat": "30.290",
  "end_lon": "120.220",
  "end_city_name": "杭州",
  "end_city_code": "0571",
  "end_ad_code": "330104",
  "idempotencyKey": "unique-key-here",
  "waitMinutes": 10
}
```

下单成功后展示：
```
✅ 顺风车订单已发出！

📋 订单号: [orderGuid]
📍 [起点] → [终点]
🎫 运力: [拼座/独享]
💰 预估: 约 XX 元
⏳ 等待时长: XX 分钟

正在为您匹配顺路车主...
💡 随时问我「订单怎么样了」查看最新状态
💡 也可以说「帮我看看有没有司机」主动邀请车主
```

---

## 邀请车主

### 查看顺路车主

调用 `hitch_invite_driver_list`：
```json
{
  "orderGuid": "ORDER_GUID"
}
```

展示格式：
```
找到 N 位顺路车主：
1. 张师傅 ⭐4.9 | 白色本田雅阁 | 顺路 85%
2. 李师傅 ⭐4.7 | 黑色大众帕萨特 | 顺路 72%
要邀请哪位？（回复编号或姓名）
```

### 发出邀请

调用 `hitch_invite_driver`：
```json
{
  "orderGuid": "ORDER_GUID",
  "driverOrderGuid": "DRIVER_GUID",
  "driverId": 12345,
  "hitchPercent": "0.85",
  "idempotencyKey": "ORDER_GUID-12345"
}
```

---

## 查询订单

调用 `hitch_query_order`：
```json
{
  "orderGuid": "ORDER_GUID"
}
```

不传 `orderGuid` 时返回当前进行中的订单列表。

响应中会携带 `statusCode`、`status`、`actionHint` 等字段，如果车主已接单还会包含 `driverInfo` 对象（姓名、车型、车牌、预计到达分钟数）。各状态下必须展示的信息和引导策略详见 `SKILL.md` 的「场景三：订单管理」。

---

## 行程中操作

### 确认上车

调用 `hitch_pax_confirm_get_on_car`：
```json
{
  "orderGuid": "ORDER_GUID",
  "idempotencyKey": "ORDER_GUID"
}
```

### 确认到达

调用 `hitch_pax_confirm_reach_destination`：
```json
{
  "orderGuid": "ORDER_GUID",
  "idempotencyKey": "ORDER_GUID"
}
```

---

## 取消订单

**必须先向用户二次确认后再执行。**

调用 `hitch_cancel_order`：
```json
{
  "orderGuid": "ORDER_GUID",
  "idempotencyKey": "unique-key"
}
```

---

## 查询司机位置

调用 `hitch_get_driver_location`：
```json
{
  "orderGuid": "ORDER_GUID"
}
```

---

## 生成跳转链接

### App 深链

调用 `hitch_generate_app_link`：
```json
{
  "start_name": "西溪湿地",
  "start_lat": "30.271",
  "start_lon": "120.062",
  "start_city_code": "0571",
  "start_ad_code": "330106",
  "end_name": "杭州东站",
  "end_lat": "30.290",
  "end_lon": "120.220",
  "end_city_code": "0571",
  "end_ad_code": "330104"
}
```

### 微信小程序链接

调用 `hitch_generate_wechat_link`：
```json
{
  "orderGuid": "ORDER_GUID"
}
```

---

## 预约出行

**方式一**：通过 `planDepartureTime` 参数（毫秒时间戳），最大当前时间 +10 天。

**方式二**：cron 定时触发。模板见 SKILL.md「定时任务模板」章节。
