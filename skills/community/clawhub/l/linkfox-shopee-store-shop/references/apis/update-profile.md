# update_profile

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/update_profile.py` |
| Method / path | POST `api/v2/shop/update_profile` |
| 官方文档 | [update_profile](https://open.shopee.com/documents/v2/v2.shop.update_profile?module=92&type=1) |
| 用途 | At least one body field; shop_name change limited to once per 30 days |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `shop_name` | — | 否（POST body） | 见 notes / 官方文档 |
| `shop_logo` | — | 否（POST body） | 见 notes / 官方文档 |
| `description` | — | 否（POST body） | 见 notes / 官方文档 |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：At least one body field; shop_name change limited to once per 30 days

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/update_profile.py '{"shopId": "67890"}'

# 通用入口
python scripts/shop_api.py '{"api": "update_profile", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`updateProfile`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.shop.update_profile?module=92&type=1)

**Body（至少一项）**：
| 字段 | 说明 |
|------|------|
| `shop_name` | 新店名（30 天内仅可改一次） |
| `shop_logo` | Shopee 图片 URL |
| `description` | 描述（≤500 字符） |

---
