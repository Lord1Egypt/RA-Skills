# get_token_by_resend_code

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/get_token_by_resend_code.py` |
| Method / path | POST `api/v2/public/get_token_by_resend_code` |
| 官方文档 | [get_token_by_resend_code](https://open.shopee.com/documents/v2/v2.public.get_token_by_resend_code?module=104&type=1) |
| 用途 | Get token by resend code; pass full body |

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
- Registry notes：Get token by resend code; pass full body

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/get_token_by_resend_code.py '{"shopId": "67890"}'

# 通用入口
python scripts/public_api.py '{"api": "get_token_by_resend_code", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`getTokenByResendCode`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
