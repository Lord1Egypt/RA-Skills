# linkfox-shopee-store-account-health — 参数与字段参考

Shopee **Account Health 模块**全部 6 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.account_health.get_shop_performance](https://open.shopee.com/documents/v2/v2.account_health.get_shop_performance?module=103&type=1)

## 通用约定

- **path**：须 `api/v2/account_health/...`
- **标识**：通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.account_health.{api}?module=103&type=1`
- **单接口入参/响应**：见下方 **`apis/`**

---

## Account Health 模块总览

| # | API | Method | path | 脚本 | 说明文档 |
|---|-----|--------|------|------|----------|
| 1 | get_shop_performance | GET | `api/v2/account_health/get_shop_performance` | `get_shop_performance.py` | [apis/get-shop-performance.md](./apis/get-shop-performance.md) |
| 2 | get_metric_source_detail | GET | `api/v2/account_health/get_metric_source_detail` | `get_metric_source_detail.py` | [apis/get-metric-source-detail.md](./apis/get-metric-source-detail.md) |
| 3 | get_penalty_point_history | GET | `api/v2/account_health/get_penalty_point_history` | `get_penalty_point_history.py` | [apis/get-penalty-point-history.md](./apis/get-penalty-point-history.md) |
| 4 | get_punishment_history | GET | `api/v2/account_health/get_punishment_history` | `get_punishment_history.py` | [apis/get-punishment-history.md](./apis/get-punishment-history.md) |
| 5 | get_listings_with_issues | GET | `api/v2/account_health/get_listings_with_issues` | `get_listings_with_issues.py` | [apis/get-listings-with-issues.md](./apis/get-listings-with-issues.md) |
| 6 | get_late_orders | GET | `api/v2/account_health/get_late_orders` | `get_late_orders.py` | [apis/get-late-orders.md](./apis/get-late-orders.md) |

通用入口：`account_health_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

| API | 要点 |
|-----|------|
| `get_shop_performance` | 店铺绩效与健康指标总览 — [apis/get-shop-performance.md](./apis/get-shop-performance.md) |
| `get_metric_source_detail` | 按 `metric_id` 查指标来源明细 — [apis/get-metric-source-detail.md](./apis/get-metric-source-detail.md) |
| `get_penalty_point_history` | 扣分历史 — [apis/get-penalty-point-history.md](./apis/get-penalty-point-history.md) |
| `get_punishment_history` | 处罚历史（必填 `punishment_status`）— [apis/get-punishment-history.md](./apis/get-punishment-history.md) |
| `get_listings_with_issues` | 存在健康问题的 listing — [apis/get-listings-with-issues.md](./apis/get-listings-with-issues.md) |
| `get_late_orders` | 逾期订单 — [apis/get-late-orders.md](./apis/get-late-orders.md) |

---

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/shopee/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/account_health/get_shop_performance",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-account-health","sentiment":"POSITIVE",
       "category":"OTHER","content":"账户健康查询正常"}'
```
