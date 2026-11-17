# unban_user_comment

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/unban_user_comment.py` |
| Method / path | POST `api/v2/livestream/unban_user_comment` |
| 官方文档 | [unban_user_comment](https://open.shopee.com/documents/v2/v2.livestream.unban_user_comment?module=125&type=1) |
| 用途 | Unban user from commenting |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：Unban user from commenting

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/unban_user_comment.py '{"shopId": "67890"}'

# 通用入口
python scripts/livestream_api.py '{"api": "unban_user_comment", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`unbanUserComment`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
