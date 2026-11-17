# linkfox-shopee-store-orders — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Order 模块**全部 22 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方文档：[Order module](https://open.shopee.com/documents/v2/v2.order.get_order_list?module=94&type=1)

## 通用约定

- **Base URL**：`https://tool-gateway.linkfox.com`
- **Method**：POST（网关），上游 Method 见各接口
- **Auth**：Header `Authorization: <api_key>`（`LINKFOXAGENT_API_KEY`）
- **流程**：`POST /shopee/storeTokens` → `POST /shopee/developerProxy`
- **path**：须 `api/v2/order/...`（不含域名）
- **紫鸟代理**：自动追加 `partner_id`、`timestamp`、`sign`；`access_token`/`shop_id` 由 `developerProxy` 写入

**developerProxy Request**：
| 参数 | 必填 | 说明 |
|------|------|------|
| `path` | 是 | 如 `api/v2/order/get_order_list` |
| `method` | 是 | `GET` / `POST` |
| `accessToken` | 是 | 店铺 token |
| `shopId` / `merchantId` | 二选一 | 转发为 `shop_id` / `merchant_id` |
| `queryString` | GET 时 | 业务 query，不含 `?` |
| `body` | POST 时 | JSON 字符串 |
| `contentType` | 否 | 默认 `application/json` |

**developerProxy Response**：
```json
{"httpStatus": 200, "contentType": "application/json", "body": "{\"error\":\"\",\"response\":{...}}"}
```

脚本在 `httpStatus==200` 时解析 `body` 为 `{responseKey}` / `{responseKey}Response`。

---

## Order 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | get_order_list | GET | `api/v2/order/get_order_list` | `get_order_list.py` | [apis/get-order-list.md](./apis/get-order-list.md) |
| 2 | get_order_detail | GET | `api/v2/order/get_order_detail` | `get_order_detail.py` | [apis/get-order-detail.md](./apis/get-order-detail.md) |
| 3 | get_shipment_list | GET | `api/v2/order/get_shipment_list` | `get_shipment_list.py` | [apis/get-shipment-list.md](./apis/get-shipment-list.md) |
| 4 | search_package_list | POST | `api/v2/order/search_package_list` | `search_package_list.py` | [apis/search-package-list.md](./apis/search-package-list.md) |
| 5 | get_package_detail | GET | `api/v2/order/get_package_detail` | `get_package_detail.py` | [apis/get-package-detail.md](./apis/get-package-detail.md) |
| 6 | split_order | POST | `api/v2/order/split_order` | `split_order.py` | [apis/split-order.md](./apis/split-order.md) |
| 7 | unsplit_order | POST | `api/v2/order/unsplit_order` | `unsplit_order.py` | [apis/unsplit-order.md](./apis/unsplit-order.md) |
| 8 | cancel_order | POST | `api/v2/order/cancel_order` | `cancel_order.py` | [apis/cancel-order.md](./apis/cancel-order.md) |
| 9 | handle_buyer_cancellation | POST | `api/v2/order/handle_buyer_cancellation` | `handle_buyer_cancellation.py` | [apis/handle-buyer-cancellation.md](./apis/handle-buyer-cancellation.md) |
| 10 | set_note | POST | `api/v2/order/set_note` | `set_note.py` | [apis/set-note.md](./apis/set-note.md) |
| 11 | get_pending_buyer_invoice_order_list | GET | `api/v2/order/get_pending_buyer_invoice_order_list` | `get_pending_buyer_invoice_order_list.py` | [apis/get-pending-buyer-invoice-order-list.md](./apis/get-pending-buyer-invoice-order-list.md) |
| 12 | get_buyer_invoice_info | POST | `api/v2/order/get_buyer_invoice_info` | `get_buyer_invoice_info.py` | [apis/get-buyer-invoice-info.md](./apis/get-buyer-invoice-info.md) |
| 13 | upload_invoice_doc | POST | `api/v2/order/upload_invoice_doc` | `upload_invoice_doc.py` | [apis/upload-invoice-doc.md](./apis/upload-invoice-doc.md) |
| 14 | download_invoice_doc | GET | `api/v2/order/download_invoice_doc` | `download_invoice_doc.py` | [apis/download-invoice-doc.md](./apis/download-invoice-doc.md) |
| 15 | handle_prescription_check | POST | `api/v2/order/handle_prescription_check` | `handle_prescription_check.py` | [apis/handle-prescription-check.md](./apis/handle-prescription-check.md) |
| 16 | get_warehouse_filter_config | GET | `api/v2/order/get_warehouse_filter_config` | `get_warehouse_filter_config.py` | [apis/get-warehouse-filter-config.md](./apis/get-warehouse-filter-config.md) |
| 17 | get_booking_list | GET | `api/v2/order/get_booking_list` | `get_booking_list.py` | [apis/get-booking-list.md](./apis/get-booking-list.md) |
| 18 | get_booking_detail | GET | `api/v2/order/get_booking_detail` | `get_booking_detail.py` | [apis/get-booking-detail.md](./apis/get-booking-detail.md) |
| 19 | generate_fbs_invoices | POST | `api/v2/order/generate_fbs_invoices` | `generate_fbs_invoices.py` | [apis/generate-fbs-invoices.md](./apis/generate-fbs-invoices.md) |
| 20 | get_fbs_invoices_result | POST | `api/v2/order/get_fbs_invoices_result` | `get_fbs_invoices_result.py` | [apis/get-fbs-invoices-result.md](./apis/get-fbs-invoices-result.md) |
| 21 | download_fbs_invoices | POST | `api/v2/order/download_fbs_invoices` | `download_fbs_invoices.py` | [apis/download-fbs-invoices.md](./apis/download-fbs-invoices.md) |
| 22 | get_estimiate_cancel_value | POST | `api/v2/order/get_estimiate_cancel_value` | `get_estimiate_cancel_value.py` | [apis/get-estimiate-cancel-value.md](./apis/get-estimiate-cancel-value.md) |

通用入口：`order_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-orders","sentiment":"POSITIVE",
       "category":"OTHER","content":"订单接口正常"}'
```
