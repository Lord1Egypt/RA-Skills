# get_authorised_reseller_brand

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_authorised_reseller_brand.py` |
| Method / path | GET `api/v2/shop/get_authorised_reseller_brand` |
| 官方文档 | [get_authorised_reseller_brand](https://open.shopee.com/documents/v2/v2.shop.get_authorised_reseller_brand?module=92&type=1) |
| 用途 | page_size min 1 max 30 |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `page_size` | — | **是** | Query 必填（见 notes / 官方文档） |
| `page_no` | — | **是** | Query 必填（见 notes / 官方文档） |

- Method：**GET**
- GET：业务字段放 JSON **顶层**，runner 拼进 `queryString`（不含 `?`）
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：page_size min 1 max 30

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_authorised_reseller_brand.py '{"shopId": "67890", "page_no": 1, "page_size": 20}'

# 通用入口
python scripts/shop_api.py '{"api": "get_authorised_reseller_brand", "shopId": "67890", "page_no": 1, "page_size": 20}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getAuthorisedResellerBrand`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.shop.get_authorised_reseller_brand?module=92&type=1)

**Query（必填）**：`page_no`（从 1 起）、`page_size`（1–30）

**Response 要点**：`is_authorised_reseller`、`total_count`、`more`、`authorised_brand_list[]`

---
