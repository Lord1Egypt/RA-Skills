# get_warehouse_filter_config

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_warehouse_filter_config.py` |
| Method / path | GET `api/v2/order/get_warehouse_filter_config` |
| 官方文档 | [get_warehouse_filter_config](https://open.shopee.com/documents/v2/v2.order.get_warehouse_filter_config?module=94&type=1) |
| 用途 | Multi-warehouse shops |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Multi-warehouse shops

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_warehouse_filter_config.py '{"shopId": "67890"}'

# 通用入口
python scripts/order_api.py '{"api": "get_warehouse_filter_config", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getWarehouseFilterConfig`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.get_warehouse_filter_config?module=94&type=1)

无额外业务参数（仅店铺公共 query）。多仓店铺返回仓库过滤配置。

---
