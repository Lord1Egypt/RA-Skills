# get_estimiate_cancel_value

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_estimiate_cancel_value.py` |
| Method / path | POST `api/v2/order/get_estimiate_cancel_value` |
| 官方文档 | [get_estimiate_cancel_value](https://open.shopee.com/documents/v2/v2.order.get_estimiate_cancel_value?module=94&type=1) |
| 用途 | Official spelling: estimiate (not estimate) |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `order_sn` | — | 是 | 见 notes / 官方文档 |
| `partial_cancel_item_list` | — | 是 | 见 notes / 官方文档 |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Official spelling: estimiate (not estimate)

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_estimiate_cancel_value.py '{"shopId": "67890", "order_sn": "<order_sn>", "partial_cancel_item_list": "<partial_cancel_item_list>"}'

# 通用入口
python scripts/order_api.py '{"api": "get_estimiate_cancel_value", "shopId": "67890", "order_sn": "<order_sn>", "partial_cancel_item_list": "<partial_cancel_item_list>"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getEstimiateCancelValue`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.get_estimiate_cancel_value?module=94&type=1)

> 官方 API 名拼写为 **estimiate**（非 estimate）。

**Body（必填）**：`order_sn`、`partial_cancel_item_list[]`（`item_id`、`model_id`、`model_quantity`；可选 `order_item_id`、`promotion_group_id`）

---

## 网关错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 1002 | 参数/未登录 | 检查 shopId 与 API Key |
| 1003 | 代理/网络异常 | 重试 |
| 1004 | 无授权记录 | auth skill |
| 1005 | path 未白名单 | 确认 `api/v2/order/...` |

紫鸟代理 HTTP：`400` 路径错误、`403` IP 白名单、`408` 超时、`5xx` 上游透传。

---
