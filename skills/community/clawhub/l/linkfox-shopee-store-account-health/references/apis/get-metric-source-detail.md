# get_metric_source_detail — 指标来源明细

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_metric_source_detail.py` |
| Method / path | GET `api/v2/account_health/get_metric_source_detail` |
| 官方文档 | [v2.account_health.get_metric_source_detail](https://open.shopee.com/documents/v2/v2.account_health.get_metric_source_detail?module=103&type=1) |
| 用途 | 按 `metric_id` 查询指标来源明细（受影响订单 / listing 等） |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `metric_id` | int | **是** | 指标 ID（通常来自 `get_shop_performance` 的 `metric_list[].metric_id`） |
| `page_no` | int | 否 | 页码，从 **1** 起；默认 **1** |
| `page_size` | int | 否 | 每页条数，范围 **1–100**；默认 **10** |

- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query

### 支持的 `metric_id` 与返回列表字段（节选）

| metric_id | 含义 | 主要列表字段 |
|-----------|------|--------------|
| `1` / `85` | Late Shipment Rate | `lsr_order_list` |
| `3` / `88` | Non-Fulfilment Rate | `nfr_order_list` |
| `4` | Preparation Time | `apt_order_list` |
| `12` | Pre-order Listing % | `pre_order_listing_list` |
| `25` / `2001–2003` | Fast Handover Rate | `fhr_order_list` |
| `42` / `91` | Cancellation Rate | `cancellation_order_list` |
| `43` / `92` | Return-refund Rate | `return_refund_order_list` |
| `52` / `53` | Listing Violations | `violation_listing_list` |

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_metric_source_detail.py '{"shopId":"67890","metric_id":3,"page_no":1,"page_size":20}'

python scripts/account_health_api.py '{"api":"get_metric_source_detail","shopId":"67890","metric_id":52,"page_size":50}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getMetricSourceDetail`**
3. 常见字段：`total_count`，以及上表对应的 `*_list`（内容随 `metric_id` 变化）
