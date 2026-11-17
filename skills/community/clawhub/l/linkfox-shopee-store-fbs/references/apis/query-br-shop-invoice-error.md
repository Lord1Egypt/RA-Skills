# query_br_shop_invoice_error

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/query_br_shop_invoice_error.py` |
| Method / path | GET `api/v2/fbs/query_br_shop_invoice_error` |
| 官方文档 | [query_br_shop_invoice_error](https://open.shopee.com/documents/v2/v2.fbs.query_br_shop_invoice_error?module=126&type=1) |
| 用途 | Brazil FBS shop invoice errors |

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
- Registry notes：Brazil FBS shop invoice errors

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/query_br_shop_invoice_error.py '{"shopId": "67890"}'

# 通用入口
python scripts/fbs_api.py '{"api": "query_br_shop_invoice_error", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`queryBrShopInvoiceError`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
