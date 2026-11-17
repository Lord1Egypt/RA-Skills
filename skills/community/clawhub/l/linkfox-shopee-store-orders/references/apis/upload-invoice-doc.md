# upload_invoice_doc

| 项 | 值 |
|----|-----|
| 脚本 | `scripts/upload_invoice_doc.py` |
| Method / path | POST `api/v2/order/upload_invoice_doc` |
| 官方文档 | [upload_invoice_doc](https://open.shopee.com/documents/v2/v2.order.upload_invoice_doc?module=94&type=1) |
| 用途 | Official API uses multipart/form-data; pass full body via body key if gateway supports it. PH/BR. |

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
- Registry notes：Official API uses multipart/form-data; pass full body via body key if gateway supports it. PH/BR.

---

## 调用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/upload_invoice_doc.py '{"shopId": "67890"}'

# 通用入口
python scripts/order_api.py '{"api": "upload_invoice_doc", "shopId": "67890"}'
```

---

## 响应要点

1. 先看 **`developerProxy.httpStatus`** / `errcode`
2. 再读 **`uploadInvoiceDoc`**（Shopee `response` 解析结果）
3. 字段以官方文档为准

---

## 补充说明（自原 references/api.md）

[官方文档](https://open.shopee.com/documents/v2/v2.order.upload_invoice_doc?module=94&type=1)

**说明**：官方为 **multipart/form-data**（`order_sn`、`file_type`、`file`）。若 LinkFox 网关 `body` 仅支持 JSON 字符串，可能无法直接上传二进制；需确认网关能力或使用专用上传链路。

**区域**：PH、BR

---
