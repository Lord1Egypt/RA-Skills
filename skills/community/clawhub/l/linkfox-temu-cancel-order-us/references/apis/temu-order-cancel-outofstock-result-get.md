# 查询缺货取消审核结果 — `temu.order.cancel.outofstock.result.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_seller_cancel_order_cancel_outofstock_result_get.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation（`menu_code` / `sub_menu_code` 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`temu.order.cancel.outofstock.result.get`，业务载荷放在 Body 的 `params` |

**Description:** After applying for out-of-stock, since out-of-stock itself is an asynchronous operation, you need to obtain the latest out-of-stock review status through the query interface（提交缺货取消申请后，由于缺货本身是异步操作，需要通过本查询接口获取最新的缺货审核状态）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> `parentOrderSn`、`orderSnList` 通常来自 `linkfox-temu-order-us` 订单列表/详情接口，或与 [temu-order-cancel-outofstock-apply.md](./temu-order-cancel-outofstock-apply.md) 提交时使用的参数一致。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填) — lack stock query request from ams
    ├── parentOrderSn (STRING, 是)
    └── orderSnList[] (STRING[], 是)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentOrderSn | STRING | **是** | parent order sn（父订单号） |
| orderSnList | STRING[] | **是** | order sn list（子订单号列表） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789",
    "orderSnList": ["O-111111111", "O-222222222"]
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response — lack stock query response from ams
├── success (BOOLEAN)
├── errorCode (INTEGER)
├── errorMsg (STRING)
└── result (OBJECT) — Specific information
    └── applyResultInfoList[] (OBJECT[]) — lack stock order apply result info list
        ├── orderSn (STRING)
        └── applyStatus (INTEGER)
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（请求是否成功） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | Specific information（具体结果信息） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| applyResultInfoList | OBJECT[] | lack stock order apply result info list（缺货取消申请结果信息列表） |

### `applyResultInfoList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| orderSn | STRING | order sn（子订单号） |
| applyStatus | INTEGER | lack stock apply status（缺货申请审核状态） |

---

## 示例

```bash
python scripts/us_seller_cancel_order_cancel_outofstock_result_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789",
    "orderSnList": ["O-111111111"]
  }
}'
```

典型流程：`temu.order.cancel.outofstock.apply` 提交缺货取消申请（风控审核）→ 本接口查询 `applyStatus` 获取最新审核状态 → 根据状态决定后续操作。
