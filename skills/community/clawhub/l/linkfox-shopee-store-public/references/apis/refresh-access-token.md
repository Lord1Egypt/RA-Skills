# refresh_access_token

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/refresh_access_token.py` |
| Method / path | POST `api/v2/public/refresh_access_token` |
| 官方文档 | [refresh_access_token](https://open.shopee.com/documents/v2/v2.public.refresh_access_token?module=104&type=1) |
| 用途 | Refresh access token; pass full body |

经 **`POST /shopee/developerProxy`** 转发。Public 多为 Partner / OAuth 级接口，**通常无需** `shopId`/`merchantId`；日常授权优先走 `linkfox-shopee-store-auth`。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 否 | Public 接口通常可省略 |
| `merchantId` | string | 否 | Public 接口通常可省略 |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Refresh access token; pass full body

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/refresh_access_token.py '{"shopId": "67890"}'

# 通用入口
python scripts/public_api.py '{"api": "refresh_access_token", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`refreshAccessToken`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
