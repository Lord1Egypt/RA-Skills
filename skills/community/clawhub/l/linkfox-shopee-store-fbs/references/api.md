# linkfox-shopee-store-fbs — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **FBS 模块**全部 4 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.fbs.query_br_shop_enrollment_status](https://open.shopee.com/documents/v2/v2.fbs.query_br_shop_enrollment_status?module=126&type=1)

## 通用约定

- **path**：须 `api/v2/fbs/...`
- **标识**：通常传 **`shopId`**（巴西 FBS 相关接口）
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.fbs.{api}?module=126&type=1`

---

## FBS 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | query_br_shop_block_status | GET | `api/v2/fbs/query_br_shop_block_status` | `query_br_shop_block_status.py` | [apis/query-br-shop-block-status.md](./apis/query-br-shop-block-status.md) |
| 2 | query_br_shop_enrollment_status | GET | `api/v2/fbs/query_br_shop_enrollment_status` | `query_br_shop_enrollment_status.py` | [apis/query-br-shop-enrollment-status.md](./apis/query-br-shop-enrollment-status.md) |
| 3 | query_br_shop_invoice_error | GET | `api/v2/fbs/query_br_shop_invoice_error` | `query_br_shop_invoice_error.py` | [apis/query-br-shop-invoice-error.md](./apis/query-br-shop-invoice-error.md) |
| 4 | query_br_sku_block_status | GET | `api/v2/fbs/query_br_sku_block_status` | `query_br_sku_block_status.py` | [apis/query-br-sku-block-status.md](./apis/query-br-sku-block-status.md) |
通用入口：`fbs_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

| API | 要点 |
|-----|------|
| `query_br_shop_enrollment_status` | 巴西 FBS 店铺入驻状态 — [apis/query-br-shop-enrollment-status.md](./apis/query-br-shop-enrollment-status.md) |
| `query_br_shop_invoice_error` | 巴西 FBS 店铺发票错误 — [apis/query-br-shop-invoice-error.md](./apis/query-br-shop-invoice-error.md) |
| `query_br_shop_block_status` | 巴西 FBS 店铺封禁状态 — [apis/query-br-shop-block-status.md](./apis/query-br-shop-block-status.md) |
| `query_br_sku_block_status` | 巴西 FBS SKU 封禁状态 — [apis/query-br-sku-block-status.md](./apis/query-br-sku-block-status.md) |

---

## curl 示例

```bash
curl -X POST https://tool-gateway.linkfox.com/shopee/developerProxy \
  -H "Authorization: $LINKFOXAGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/fbs/query_br_shop_enrollment_status",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-fbs","sentiment":"POSITIVE",
       "category":"OTHER","content":"FBS状态查询正常"}'
```
