# linkfox-shopee-store-payment — 参数与字段参考

> 单接口入参/响应说明已拆到 **`apis/`**（按 API 一份）；本文件保留模块总览与 Feedback。
Shopee **Payment 模块**全部 18 个 API，经 **`POST /shopee/developerProxy`** 转发。

授权见 **`linkfox-shopee-store-auth`**。官方索引：[v2.payment.get_escrow_detail](https://open.shopee.com/documents/v2/v2.payment.get_escrow_detail?module=97&type=1)

## 通用约定

- **Base URL**：`https://tool-gateway.linkfox.com`
- **Method**：POST（网关），上游 Method 见各接口
- **Auth**：Header `Authorization: <api_key>`（`LINKFOXAGENT_API_KEY`）
- **流程**：`POST /shopee/storeTokens` → `POST /shopee/developerProxy`
- **path**：须 `api/v2/payment/...`
- **标识**：店铺级 API，通常传 **`shopId`**
- **官方文档 URL 规则**：`https://open.shopee.com/documents/v2/v2.payment.{api}?module=97&type=1`

---

## Payment 模块总览

| # | API | Method | path | 脚本 | 官方文档 |
|---|-----|--------|------|------|----------|
| 1 | generate_income_report | POST | `api/v2/payment/generate_income_report` | `generate_income_report.py` | [apis/generate-income-report.md](./apis/generate-income-report.md) |
| 2 | generate_income_statement | POST | `api/v2/payment/generate_income_statement` | `generate_income_statement.py` | [apis/generate-income-statement.md](./apis/generate-income-statement.md) |
| 3 | get_billing_transaction_info | GET | `api/v2/payment/get_billing_transaction_info` | `get_billing_transaction_info.py` | [apis/get-billing-transaction-info.md](./apis/get-billing-transaction-info.md) |
| 4 | get_escrow_detail | GET | `api/v2/payment/get_escrow_detail` | `get_escrow_detail.py` | [apis/get-escrow-detail.md](./apis/get-escrow-detail.md) |
| 5 | get_escrow_detail_batch | POST | `api/v2/payment/get_escrow_detail_batch` | `get_escrow_detail_batch.py` | [apis/get-escrow-detail-batch.md](./apis/get-escrow-detail-batch.md) |
| 6 | get_escrow_list | GET | `api/v2/payment/get_escrow_list` | `get_escrow_list.py` | [apis/get-escrow-list.md](./apis/get-escrow-list.md) |
| 7 | get_income_detail | GET | `api/v2/payment/get_income_detail` | `get_income_detail.py` | [apis/get-income-detail.md](./apis/get-income-detail.md) |
| 8 | get_income_overview | GET | `api/v2/payment/get_income_overview` | `get_income_overview.py` | [apis/get-income-overview.md](./apis/get-income-overview.md) |
| 9 | get_income_report | GET | `api/v2/payment/get_income_report` | `get_income_report.py` | [apis/get-income-report.md](./apis/get-income-report.md) |
| 10 | get_income_statement | GET | `api/v2/payment/get_income_statement` | `get_income_statement.py` | [apis/get-income-statement.md](./apis/get-income-statement.md) |
| 11 | get_item_installment_status | GET | `api/v2/payment/get_item_installment_status` | `get_item_installment_status.py` | [apis/get-item-installment-status.md](./apis/get-item-installment-status.md) |
| 12 | get_payment_method_list | GET | `api/v2/payment/get_payment_method_list` | `get_payment_method_list.py` | [apis/get-payment-method-list.md](./apis/get-payment-method-list.md) |
| 13 | get_payout_detail | GET | `api/v2/payment/get_payout_detail` | `get_payout_detail.py` | [apis/get-payout-detail.md](./apis/get-payout-detail.md) |
| 14 | get_payout_info | GET | `api/v2/payment/get_payout_info` | `get_payout_info.py` | [apis/get-payout-info.md](./apis/get-payout-info.md) |
| 15 | get_shop_installment_status | GET | `api/v2/payment/get_shop_installment_status` | `get_shop_installment_status.py` | [apis/get-shop-installment-status.md](./apis/get-shop-installment-status.md) |
| 16 | get_wallet_transaction_list | GET | `api/v2/payment/get_wallet_transaction_list` | `get_wallet_transaction_list.py` | [apis/get-wallet-transaction-list.md](./apis/get-wallet-transaction-list.md) |
| 17 | set_item_installment_status | POST | `api/v2/payment/set_item_installment_status` | `set_item_installment_status.py` | [apis/set-item-installment-status.md](./apis/set-item-installment-status.md) |
| 18 | set_shop_installment_status | POST | `api/v2/payment/set_shop_installment_status` | `set_shop_installment_status.py` | [apis/set-shop-installment-status.md](./apis/set-shop-installment-status.md) |
通用入口：`payment_api.py`（JSON 含 `"api": "<上表 API 名>"`）。

---

## 常用接口说明

### 托管/结算

| API | 要点 |
|-----|------|
| `get_escrow_detail` | 必填 `order_sn`；订单托管/结算明细 — [apis/get-escrow-detail.md](./apis/get-escrow-detail.md) |
| `get_escrow_list` | 托管列表；时间范围筛选 — [apis/get-escrow-list.md](./apis/get-escrow-list.md) |
| `get_escrow_detail_batch` | POST 批量查 escrow — [apis/get-escrow-detail-batch.md](./apis/get-escrow-detail-batch.md) |

### 打款/钱包

| API | 要点 |
|-----|------|
| `get_payout_detail` | 打款明细 — [apis/get-payout-detail.md](./apis/get-payout-detail.md) |
| `get_payout_info` | 打款汇总 — [apis/get-payout-info.md](./apis/get-payout-info.md) |
| `get_wallet_transaction_list` | 钱包流水 — [apis/get-wallet-transaction-list.md](./apis/get-wallet-transaction-list.md) |
| `get_billing_transaction_info` | 账单交易信息 — [apis/get-billing-transaction-info.md](./apis/get-billing-transaction-info.md) |

### 分期

| API | 要点 |
|-----|------|
| `get_shop_installment_status` / `set_shop_installment_status` | 店铺分期开关 |
| `get_item_installment_status` / `set_item_installment_status` | 商品分期 |

### 收入报表

| API | 要点 |
|-----|------|
| `generate_income_statement` / `get_income_statement` | 异步生成/获取 income statement |
| `generate_income_report` / `get_income_report` | 异步生成/获取 income report |
| `get_income_overview` / `get_income_detail` | 收入概览与明细 |

### 其他

| API | 要点 |
|-----|------|
| `get_payment_method_list` | 可用支付方式 — [apis/get-payment-method-list.md](./apis/get-payment-method-list.md) |

---

## 网关错误码

| errcode | 含义 | 建议 |
|---------|------|------|
| 1002 | 参数/未登录 | 检查 shopId 与 API Key |
| 1003 | 代理/网络异常 | 重试 |
| 1004 | 无授权记录 | auth skill |
| 1005 | path 未白名单 | 确认 `api/v2/payment/...` |

---

## curl 示例

```bash
export KEY=$LINKFOXAGENT_API_KEY
BASE=https://tool-gateway.linkfox.com

curl -X POST $BASE/shopee/developerProxy -H "Authorization: $KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "api/v2/payment/get_escrow_detail",
    "method": "GET",
    "accessToken": "xxx",
    "shopId": "67890",
    "queryString": "order_sn=240101ABC"
  }'
```

---

## Feedback API

```bash
curl -X POST https://skill-api.linkfox.com/api/v1/public/feedback \
  -H "Content-Type: application/json" \
  -d '{"skillName":"linkfox-shopee-store-payment","sentiment":"POSITIVE",
       "category":"OTHER","content":"托管明细查询正常"}'
```
