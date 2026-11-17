# get_tracking_number

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_tracking_number.py` |
| Method / path | GET `api/v2/logistics/get_tracking_number` |
| 官方文档 | [get_tracking_number](https://open.shopee.com/documents/v2/v2.logistics.get_tracking_number?module=95&type=1) |
| 用途 | Get tracking number for order |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `order_sn` | — | **是** | Query 必填（见 notes / 官方文档） |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Get tracking number for order

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_tracking_number.py '{"shopId": "67890", "order_sn": "<order_sn>"}'

# 通用入口
python scripts/logistics_api.py '{"api": "get_tracking_number", "shopId": "67890", "order_sn": "<order_sn>"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getTrackingNumber`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
