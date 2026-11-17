# set_note

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/set_note.py` |
| Method / path | POST `api/v2/order/set_note` |
| 官方文档 | [set_note](https://open.shopee.com/documents/v2/v2.order.set_note?module=94&type=1) |
| 用途 | Shopee Open API `set_note` |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `order_sn` | — | 是 | 见 notes / 官方文档 |
| `note` | — | 是 | 见 notes / 官方文档 |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/set_note.py '{"shopId": "67890", "order_sn": "<order_sn>", "note": "<note>"}'

# 通用入口
python scripts/order_api.py '{"api": "set_note", "shopId": "67890", "order_sn": "<order_sn>", "note": "<note>"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`setNote`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.set_note?module=94&type=1)

**Body（必填）**：`order_sn`、`note`

---
