# generate_fbs_invoices

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/generate_fbs_invoices.py` |
| Method / path | POST `api/v2/order/generate_fbs_invoices` |
| 官方文档 | [generate_fbs_invoices](https://open.shopee.com/documents/v2/v2.order.generate_fbs_invoices?module=94&type=1) |
| 用途 | BR FBS; batch_download.start/end YYYYMMDD |

经 **`POST /shopee/developerProxy`** 转发；依赖 **`linkfox-shopee-store-auth`** 选店（通常传 `shopId` 或 `merchantId`）。

---

## 脚本 JSON 入参

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `shopId` | string | 与 `merchantId` 二选一 | 店铺 ID（推荐；Public 等无店铺接口可省略） |
| `merchantId` | string | 与 `shopId` 二选一 | 商户 ID |
| `batch_download` | — | 否（POST body） | 见 notes / 官方文档 |
| `batch_download` | object | 否（可嵌在 body） | 嵌套对象；或整体传 `body` / `requestBody` |

- Method：**POST**
- POST：传 `body` / `requestBody`，或把 `body_fields` 列在 JSON 顶层
- `shopId` / `merchantId` / `skipDepCheck` 等为网关选店保留字段，不会进 Shopee query/body
- Registry notes：BR FBS; batch_download.start/end YYYYMMDD

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/generate_fbs_invoices.py '{"shopId": "67890"}'

# 通用入口
python scripts/order_api.py '{"api": "generate_fbs_invoices", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`generateFbsInvoices`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.generate_fbs_invoices?module=94&type=1)

**Body（必填）**：`batch_download`（`start`/`end` YYYYMMDD、`document_type`、`file_type`；可选 `document_status`）

**区域**：BR FBS

---
