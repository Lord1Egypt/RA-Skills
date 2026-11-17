# get_model_list

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_model_list.py` |
| Method / path | GET `api/v2/product/get_model_list` |
| 官方文档 | [get_model_list](https://open.shopee.com/documents/v2/v2.product.get_model_list?module=89&type=1) |
| 用途 | SKU/model list for item |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `item_id` | — | **是** | Query 必填（见 notes / 官方文档） |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：SKU/model list for item

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_model_list.py '{"shopId": "67890", "item_id": 123}'

# 通用入口
python scripts/product_api.py '{"api": "get_model_list", "shopId": "67890", "item_id": 123}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getModelList`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
