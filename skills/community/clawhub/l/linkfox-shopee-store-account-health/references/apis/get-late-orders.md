# get_late_orders — 逾期订单

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_late_orders.py` |
| Method / path | GET `api/v2/account_health/get_late_orders` |
| 官方文档 | [v2.account_health.get_late_orders](https://open.shopee.com/documents/v2/v2.account_health.get_late_orders?module=103&type=1) |
| 用途 | 查询逾期未发货订单，便于优先处理 |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `page_no` | int | 否 | 页码，从 **1** 起；默认 **1** |
| `page_size` | int | 否 | 每页条数，范围 **1–100**；默认 **10** |

- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_late_orders.py '{"shopId":"67890","page_no":1,"page_size":20}'

# 通用入口
python scripts/account_health_api.py '{"api":"get_late_orders","shopId":"67890","page_no":1,"page_size":20}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getLateOrders`**（Shopee `response` 解析结果）
3. 常见字段：`total_count`、`late_order_list[]`（如 `order_sn`、`shipping_deadline`、`late_by_days`）
