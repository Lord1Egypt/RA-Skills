# get_shop_performance — 店铺绩效总览

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_shop_performance.py` |
| Method / path | GET `api/v2/account_health/get_shop_performance` |
| 官方文档 | [v2.account_health.get_shop_performance](https://open.shopee.com/documents/v2/v2.account_health.get_shop_performance?module=103&type=1) |
| 用途 | 查询店铺账户健康绩效指标总览（履约 / listing / 客服等） |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |

- 本接口**无**额外 Shopee 业务 query 参数
- GET：业务字段放 JSON **顶层**；`shopId` / `merchantId` / `skipDepCheck` 为网关选店保留字段，不会进 Shopee query

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_shop_performance.py '{"shopId":"67890"}'

python scripts/account_health_api.py '{"api":"get_shop_performance","shopId":"67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getShopPerformance`**
3. 常见字段：`overall_performance`（如 `rating`、各类 failed 计数）、`metric_list[]`（`metric_id`、`metric_name`、`current_period`、`last_period`、`target`、`unit`）
4. 下钻某指标明细时，把 `metric_id` 交给 `get_metric_source_detail`（见 [get-metric-source-detail.md](./get-metric-source-detail.md)）

### 常用 `metric_id`（节选）

| ID | 含义 |
|----|------|
| `1` | Late Shipment Rate |
| `3` | Non-Fulfilment Rate |
| `12` | Pre-order Listing % |
| `25` | Fast Handover Rate |
| `42` | Cancellation Rate |
| `43` | Return-refund Rate |
| `52` | Severe Listing Violations |
