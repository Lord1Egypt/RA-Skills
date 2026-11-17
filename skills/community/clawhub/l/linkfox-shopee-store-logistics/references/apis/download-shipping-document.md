# download_shipping_document

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/download_shipping_document.py` |
| Method / path | GET `api/v2/logistics/download_shipping_document` |
| 官方文档 | [download_shipping_document](https://open.shopee.com/documents/v2/v2.logistics.download_shipping_document?module=95&type=1) |
| 用途 | Download shipping label PDF |

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
- Registry notes：Download shipping label PDF

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/download_shipping_document.py '{"shopId": "67890"}'

# 通用入口
python scripts/logistics_api.py '{"api": "download_shipping_document", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`downloadShippingDocument`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
