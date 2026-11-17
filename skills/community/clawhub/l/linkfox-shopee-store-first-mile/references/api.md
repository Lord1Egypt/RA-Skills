# linkfox-shopee-store-first-mile — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **FirstMile 模块**全部 16 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.first_mile.get_unbind_order_list](https://open.shopee.com/documents/v2/v2.first_mile.get_unbind_order_list?module=96&type=1)

## 通用约定

- **path**：须 `api/v2/first_mile/...`
- **标识**：通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.first_mile.{api}?module=96&type=1`

---

## FirstMile 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | bind_courier_delivery_first_mile_tracking_number | POST | `api/v2/first_mile/bind_courier_delivery_first_mile_tracking_number` | `bind_courier_delivery_first_mile_tracking_number.py` | [apis/bind-courier-delivery-first-mile-tracking-number.md](./apis/bind-courier-delivery-first-mile-tracking-number.md) |
| 2 | bind_first_mile_tracking_number | POST | `api/v2/first_mile/bind_first_mile_tracking_number` | `bind_first_mile_tracking_number.py` | [apis/bind-first-mile-tracking-number.md](./apis/bind-first-mile-tracking-number.md) |
| 3 | generate_and_bind_first_mile_tracking_number | POST | `api/v2/first_mile/generate_and_bind_first_mile_tracking_number` | `generate_and_bind_first_mile_tracking_number.py` | [apis/generate-and-bind-first-mile-tracking-number.md](./apis/generate-and-bind-first-mile-tracking-number.md) |
| 4 | generate_first_mile_tracking_number | POST | `api/v2/first_mile/generate_first_mile_tracking_number` | `generate_first_mile_tracking_number.py` | [apis/generate-first-mile-tracking-number.md](./apis/generate-first-mile-tracking-number.md) |
| 5 | get_channel_list | GET | `api/v2/first_mile/get_channel_list` | `get_channel_list.py` | [apis/get-channel-list.md](./apis/get-channel-list.md) |
| 6 | get_courier_delivery_channel_list | GET | `api/v2/first_mile/get_courier_delivery_channel_list` | `get_courier_delivery_channel_list.py` | [apis/get-courier-delivery-channel-list.md](./apis/get-courier-delivery-channel-list.md) |
| 7 | get_courier_delivery_detail | GET | `api/v2/first_mile/get_courier_delivery_detail` | `get_courier_delivery_detail.py` | [apis/get-courier-delivery-detail.md](./apis/get-courier-delivery-detail.md) |
| 8 | get_courier_delivery_tracking_number_list | GET | `api/v2/first_mile/get_courier_delivery_tracking_number_list` | `get_courier_delivery_tracking_number_list.py` | [apis/get-courier-delivery-tracking-number-list.md](./apis/get-courier-delivery-tracking-number-list.md) |
| 9 | get_courier_delivery_waybill | GET | `api/v2/first_mile/get_courier_delivery_waybill` | `get_courier_delivery_waybill.py` | [apis/get-courier-delivery-waybill.md](./apis/get-courier-delivery-waybill.md) |
| 10 | get_detail | GET | `api/v2/first_mile/get_detail` | `get_detail.py` | [apis/get-detail.md](./apis/get-detail.md) |
| 11 | get_tracking_number_list | GET | `api/v2/first_mile/get_tracking_number_list` | `get_tracking_number_list.py` | [apis/get-tracking-number-list.md](./apis/get-tracking-number-list.md) |
| 12 | get_transit_warehouse_list | GET | `api/v2/first_mile/get_transit_warehouse_list` | `get_transit_warehouse_list.py` | [apis/get-transit-warehouse-list.md](./apis/get-transit-warehouse-list.md) |
| 13 | get_unbind_order_list | GET | `api/v2/first_mile/get_unbind_order_list` | `get_unbind_order_list.py` | [apis/get-unbind-order-list.md](./apis/get-unbind-order-list.md) |
| 14 | get_waybill | GET | `api/v2/first_mile/get_waybill` | `get_waybill.py` | [apis/get-waybill.md](./apis/get-waybill.md) |
| 15 | unbind_first_mile_tracking_number | POST | `api/v2/first_mile/unbind_first_mile_tracking_number` | `unbind_first_mile_tracking_number.py` | [apis/unbind-first-mile-tracking-number.md](./apis/unbind-first-mile-tracking-number.md) |
| 16 | unbind_first_mile_tracking_number_all | POST | `api/v2/first_mile/unbind_first_mile_tracking_number_all` | `unbind_first_mile_tracking_number_all.py` | [apis/unbind-first-mile-tracking-number-all.md](./apis/unbind-first-mile-tracking-number-all.md) |
通用入口：`first_mile_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

### 头程绑定

| API | 要点 |
|-----|------|
| `get_unbind_order_list` | 未绑定头程运单的订单 — [apis/get-unbind-order-list.md](./apis/get-unbind-order-list.md) |
| `generate_first_mile_tracking_number` | 生成头程运单号 — [apis/generate-first-mile-tracking-number.md](./apis/generate-first-mile-tracking-number.md) |
| `bind_first_mile_tracking_number` | 绑定订单到头程运单 — [apis/bind-first-mile-tracking-number.md](./apis/bind-first-mile-tracking-number.md) |
| `generate_and_bind_first_mile_tracking_number` | 一步生成并绑定 — [apis/generate-and-bind-first-mile-tracking-number.md](./apis/generate-and-bind-first-mile-tracking-number.md) |
| `unbind_first_mile_tracking_number` | 解绑 — [apis/unbind-first-mile-tracking-number.md](./apis/unbind-first-mile-tracking-number.md) |
| `get_tracking_number_list` | 头程运单号列表 — [apis/get-tracking-number-list.md](./apis/get-tracking-number-list.md) |
| `get_waybill` | 头程面单 — [apis/get-waybill.md](./apis/get-waybill.md) |

### 渠道与仓库

| API | 要点 |
|-----|------|
| `get_channel_list` | 头程渠道 — [apis/get-channel-list.md](./apis/get-channel-list.md) |
| `get_transit_warehouse_list` | 中转仓列表 — [apis/get-transit-warehouse-list.md](./apis/get-transit-warehouse-list.md) |
| `get_courier_delivery_channel_list` | 快递配送渠道 — [apis/get-courier-delivery-channel-list.md](./apis/get-courier-delivery-channel-list.md) |

### 快递配送头程

| API | 要点 |
|-----|------|
| `bind_courier_delivery_first_mile_tracking_number` | 绑定快递头程运单 — [apis/bind-courier-delivery-first-mile-tracking-number.md](./apis/bind-courier-delivery-first-mile-tracking-number.md) |
| `get_courier_delivery_detail` | 快递头程详情 — [apis/get-courier-delivery-detail.md](./apis/get-courier-delivery-detail.md) |
| `get_courier_delivery_waybill` | 快递头程面单 — [apis/get-courier-delivery-waybill.md](./apis/get-courier-delivery-waybill.md) |
| `get_courier_delivery_tracking_number_list` | 快递头程运单列表 — [apis/get-courier-delivery-tracking-number-list.md](./apis/get-courier-delivery-tracking-number-list.md) |

---

## curl 示例

```bash
curl -X POST ${LINKFOX_TOOL_GATEWAY}/shopee/developerProxy \
  -H "Authorization: $LINKFOX_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/first_mile/get_unbind_order_list",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890"
  }'
```

> 认证：从 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 任一环境变量读取（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）。请求地址使用 `${LINKFOX_TOOL_GATEWAY}`（回退到 `SHOPEE_API_BASE_URL`，再回退到 `https://tool-gateway.linkfox.com`）。

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-first-mile","sentiment":"POSITIVE",
       "category":"OTHER","content":"头程订单查询正常"}'
```
