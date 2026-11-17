# update_top_picks

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/update_top_picks.py` |
| Method / path | POST `api/v2/top_picks/update_top_picks` |
| 官方文档 | [update_top_picks](https://open.shopee.com/documents/v2/v2.top_picks.update_top_picks?module=100&type=1) |
| 用途 | Update top picks collection |

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
- Registry notes：Update top picks collection

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/update_top_picks.py '{"shopId": "67890"}'

# 通用入口
python scripts/top_picks_api.py '{"api": "update_top_picks", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`updateTopPicks`**（Shopee `response` 解析结果）
3. 字段以官方文档为准
