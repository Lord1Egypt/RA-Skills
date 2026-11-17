# linkfox-shopee-store-logistics — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Logistics 模块**全部 46 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.logistics.get_shipping_parameter](https://open.shopee.com/documents/v2/v2.logistics.get_shipping_parameter?module=95&type=1)

## 通用约定

- **Base URL**：`https://tool-gateway.linkfox.com`
- **Method**：POST（网关），上游 Method 见各接口
- **Auth**：Header `Authorization: <api_key>`（`LINKFOXAGENT_API_KEY`）（如未配置 按 SKILL.md 的 **## 解决认证和算力问题** 处理）
- **流程**：`POST /shopee/storeTokens` → `POST /shopee/developerProxy`
- **path**：须 `api/v2/logistics/...`
- **标识**：店铺级物流 API，通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.logistics.{api}?module=95&type=1`
- **复杂 POST**（如 `ship_order`）：推荐传完整 `body` 对象

---

## Logistics 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | batch_ship_order | POST | `api/v2/logistics/batch_ship_order` | `batch_ship_order.py` | [apis/batch-ship-order.md](./apis/batch-ship-order.md) |
| 2 | batch_update_tpf_warehouse_tracking_status | POST | `api/v2/logistics/batch_update_tpf_warehouse_tracking_status` | `batch_update_tpf_warehouse_tracking_status.py` | [apis/batch-update-tpf-warehouse-tracking-status.md](./apis/batch-update-tpf-warehouse-tracking-status.md) |
| 3 | check_polygon_update_status | GET | `api/v2/logistics/check_polygon_update_status` | `check_polygon_update_status.py` | [apis/check-polygon-update-status.md](./apis/check-polygon-update-status.md) |
| 4 | create_booking_shipping_document | POST | `api/v2/logistics/create_booking_shipping_document` | `create_booking_shipping_document.py` | [apis/create-booking-shipping-document.md](./apis/create-booking-shipping-document.md) |
| 5 | create_shipping_document | POST | `api/v2/logistics/create_shipping_document` | `create_shipping_document.py` | [apis/create-shipping-document.md](./apis/create-shipping-document.md) |
| 6 | create_shipping_document_job | POST | `api/v2/logistics/create_shipping_document_job` | `create_shipping_document_job.py` | [apis/create-shipping-document-job.md](./apis/create-shipping-document-job.md) |
| 7 | delete_address | POST | `api/v2/logistics/delete_address` | `delete_address.py` | [apis/delete-address.md](./apis/delete-address.md) |
| 8 | delete_special_operating_hour | POST | `api/v2/logistics/delete_special_operating_hour` | `delete_special_operating_hour.py` | [apis/delete-special-operating-hour.md](./apis/delete-special-operating-hour.md) |
| 9 | download_booking_shipping_document | GET | `api/v2/logistics/download_booking_shipping_document` | `download_booking_shipping_document.py` | [apis/download-booking-shipping-document.md](./apis/download-booking-shipping-document.md) |
| 10 | download_shipping_document | GET | `api/v2/logistics/download_shipping_document` | `download_shipping_document.py` | [apis/download-shipping-document.md](./apis/download-shipping-document.md) |
| 11 | download_shipping_document_job | GET | `api/v2/logistics/download_shipping_document_job` | `download_shipping_document_job.py` | [apis/download-shipping-document-job.md](./apis/download-shipping-document-job.md) |
| 12 | download_to_label | GET | `api/v2/logistics/download_to_label` | `download_to_label.py` | [apis/download-to-label.md](./apis/download-to-label.md) |
| 13 | get_address_list | GET | `api/v2/logistics/get_address_list` | `get_address_list.py` | [apis/get-address-list.md](./apis/get-address-list.md) |
| 14 | get_booking_shipping_document_data_info | GET | `api/v2/logistics/get_booking_shipping_document_data_info` | `get_booking_shipping_document_data_info.py` | [apis/get-booking-shipping-document-data-info.md](./apis/get-booking-shipping-document-data-info.md) |
| 15 | get_booking_shipping_document_parameter | GET | `api/v2/logistics/get_booking_shipping_document_parameter` | `get_booking_shipping_document_parameter.py` | [apis/get-booking-shipping-document-parameter.md](./apis/get-booking-shipping-document-parameter.md) |
| 16 | get_booking_shipping_document_result | GET | `api/v2/logistics/get_booking_shipping_document_result` | `get_booking_shipping_document_result.py` | [apis/get-booking-shipping-document-result.md](./apis/get-booking-shipping-document-result.md) |
| 17 | get_booking_shipping_parameter | GET | `api/v2/logistics/get_booking_shipping_parameter` | `get_booking_shipping_parameter.py` | [apis/get-booking-shipping-parameter.md](./apis/get-booking-shipping-parameter.md) |
| 18 | get_booking_tracking_info | GET | `api/v2/logistics/get_booking_tracking_info` | `get_booking_tracking_info.py` | [apis/get-booking-tracking-info.md](./apis/get-booking-tracking-info.md) |
| 19 | get_booking_tracking_number | GET | `api/v2/logistics/get_booking_tracking_number` | `get_booking_tracking_number.py` | [apis/get-booking-tracking-number.md](./apis/get-booking-tracking-number.md) |
| 20 | get_channel_list | GET | `api/v2/logistics/get_channel_list` | `get_channel_list.py` | [apis/get-channel-list.md](./apis/get-channel-list.md) |
| 21 | get_mart_packaging_info | GET | `api/v2/logistics/get_mart_packaging_info` | `get_mart_packaging_info.py` | [apis/get-mart-packaging-info.md](./apis/get-mart-packaging-info.md) |
| 22 | get_mass_shipping_parameter | POST | `api/v2/logistics/get_mass_shipping_parameter` | `get_mass_shipping_parameter.py` | [apis/get-mass-shipping-parameter.md](./apis/get-mass-shipping-parameter.md) |
| 23 | get_mass_tracking_number | POST | `api/v2/logistics/get_mass_tracking_number` | `get_mass_tracking_number.py` | [apis/get-mass-tracking-number.md](./apis/get-mass-tracking-number.md) |
| 24 | get_operating_hour_restrictions | GET | `api/v2/logistics/get_operating_hour_restrictions` | `get_operating_hour_restrictions.py` | [apis/get-operating-hour-restrictions.md](./apis/get-operating-hour-restrictions.md) |
| 25 | get_operating_hours | GET | `api/v2/logistics/get_operating_hours` | `get_operating_hours.py` | [apis/get-operating-hours.md](./apis/get-operating-hours.md) |
| 26 | get_pause_status | GET | `api/v2/logistics/get_pause_status` | `get_pause_status.py` | [apis/get-pause-status.md](./apis/get-pause-status.md) |
| 27 | get_shipping_document_data_info | GET | `api/v2/logistics/get_shipping_document_data_info` | `get_shipping_document_data_info.py` | [apis/get-shipping-document-data-info.md](./apis/get-shipping-document-data-info.md) |
| 28 | get_shipping_document_job_status | GET | `api/v2/logistics/get_shipping_document_job_status` | `get_shipping_document_job_status.py` | [apis/get-shipping-document-job-status.md](./apis/get-shipping-document-job-status.md) |
| 29 | get_shipping_document_parameter | GET | `api/v2/logistics/get_shipping_document_parameter` | `get_shipping_document_parameter.py` | [apis/get-shipping-document-parameter.md](./apis/get-shipping-document-parameter.md) |
| 30 | get_shipping_document_result | GET | `api/v2/logistics/get_shipping_document_result` | `get_shipping_document_result.py` | [apis/get-shipping-document-result.md](./apis/get-shipping-document-result.md) |
| 31 | get_shipping_parameter | GET | `api/v2/logistics/get_shipping_parameter` | `get_shipping_parameter.py` | [apis/get-shipping-parameter.md](./apis/get-shipping-parameter.md) |
| 32 | get_tracking_info | GET | `api/v2/logistics/get_tracking_info` | `get_tracking_info.py` | [apis/get-tracking-info.md](./apis/get-tracking-info.md) |
| 33 | get_tracking_number | GET | `api/v2/logistics/get_tracking_number` | `get_tracking_number.py` | [apis/get-tracking-number.md](./apis/get-tracking-number.md) |
| 34 | mass_ship_order | POST | `api/v2/logistics/mass_ship_order` | `mass_ship_order.py` | [apis/mass-ship-order.md](./apis/mass-ship-order.md) |
| 35 | set_address_config | POST | `api/v2/logistics/set_address_config` | `set_address_config.py` | [apis/set-address-config.md](./apis/set-address-config.md) |
| 36 | set_mart_packaging_info | POST | `api/v2/logistics/set_mart_packaging_info` | `set_mart_packaging_info.py` | [apis/set-mart-packaging-info.md](./apis/set-mart-packaging-info.md) |
| 37 | set_pause_status | POST | `api/v2/logistics/set_pause_status` | `set_pause_status.py` | [apis/set-pause-status.md](./apis/set-pause-status.md) |
| 38 | ship_booking | POST | `api/v2/logistics/ship_booking` | `ship_booking.py` | [apis/ship-booking.md](./apis/ship-booking.md) |
| 39 | ship_order | POST | `api/v2/logistics/ship_order` | `ship_order.py` | [apis/ship-order.md](./apis/ship-order.md) |
| 40 | update_address | POST | `api/v2/logistics/update_address` | `update_address.py` | [apis/update-address.md](./apis/update-address.md) |
| 41 | update_channel | POST | `api/v2/logistics/update_channel` | `update_channel.py` | [apis/update-channel.md](./apis/update-channel.md) |
| 42 | update_operating_hours | POST | `api/v2/logistics/update_operating_hours` | `update_operating_hours.py` | [apis/update-operating-hours.md](./apis/update-operating-hours.md) |
| 43 | update_self_collection_order_logistics | POST | `api/v2/logistics/update_self_collection_order_logistics` | `update_self_collection_order_logistics.py` | [apis/update-self-collection-order-logistics.md](./apis/update-self-collection-order-logistics.md) |
| 44 | update_shipping_order | POST | `api/v2/logistics/update_shipping_order` | `update_shipping_order.py` | [apis/update-shipping-order.md](./apis/update-shipping-order.md) |
| 45 | update_tracking_status | POST | `api/v2/logistics/update_tracking_status` | `update_tracking_status.py` | [apis/update-tracking-status.md](./apis/update-tracking-status.md) |
| 46 | upload_serviceable_polygon | POST | `api/v2/logistics/upload_serviceable_polygon` | `upload_serviceable_polygon.py` | [apis/upload-serviceable-polygon.md](./apis/upload-serviceable-polygon.md) |
通用入口：`logistics_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

### 发货流程

| API | 要点 |
|-----|------|
| `get_shipping_parameter` | 必填 `order_sn`；发货前获取 pickup/dropoff 参数 — [apis/get-shipping-parameter.md](./apis/get-shipping-parameter.md) |
| `ship_order` | POST `body`：执行发货 — [apis/ship-order.md](./apis/ship-order.md) |
| `get_tracking_number` | 必填 `order_sn`；获取运单号 — [apis/get-tracking-number.md](./apis/get-tracking-number.md) |
| `get_tracking_info` | 物流轨迹查询 — [apis/get-tracking-info.md](./apis/get-tracking-info.md) |

### 面单/文档

| API | 要点 |
|-----|------|
| `get_shipping_document_parameter` | 必填 `order_sn` — [apis/get-shipping-document-parameter.md](./apis/get-shipping-document-parameter.md) |
| `create_shipping_document` | 创建面单 — [apis/create-shipping-document.md](./apis/create-shipping-document.md) |
| `get_shipping_document_result` | 查询面单生成结果 — [apis/get-shipping-document-result.md](./apis/get-shipping-document-result.md) |
| `download_shipping_document` | 下载面单 PDF — [apis/download-shipping-document.md](./apis/download-shipping-document.md) |
| `create_shipping_document_job` | 异步批量面单任务 — [apis/create-shipping-document-job.md](./apis/create-shipping-document-job.md) |

### 地址与渠道

| API | 要点 |
|-----|------|
| `get_address_list` | 揽收/退货地址列表 — [apis/get-address-list.md](./apis/get-address-list.md) |
| `get_channel_list` | 可用物流渠道 — [apis/get-channel-list.md](./apis/get-channel-list.md) |
| `update_address` / `set_address_config` | 地址管理 |

### Booking 发货

`get_booking_shipping_parameter`、`ship_booking`、`get_booking_tracking_number` 及 booking 面单系列 — 见上表。

### 批量与其他

`mass_ship_order`、`batch_ship_order`、`get_mass_shipping_parameter` 等批量接口；Mart 包装、配送 polygon、pause 状态等见上表及官方文档。

---

## 网关错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 1002 | 参数/未登录 | 检查 shopId 与 API Key |
| 1003 | 代理/网络异常 | 重试 |
| 1004 | 无授权记录 | auth skill |
| 1005 | path 未白名单 | 确认 `api/v2/logistics/...` |

---

## curl 示例

```bash
export KEY=$LINKFOX_AGENT_API_KEY
BASE=${LINKFOX_TOOL_GATEWAY}

# 发货参数
curl -X POST $BASE/shopee/developerProxy -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/logistics/get_shipping_parameter",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890",
    "queryString": "order_sn=240101ABC"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-logistics","sentiment":"POSITIVE",
       "category":"OTHER","content":"物流发货查询正常"}'
```
