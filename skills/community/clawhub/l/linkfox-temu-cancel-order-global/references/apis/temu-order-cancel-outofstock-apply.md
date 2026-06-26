# 缺货取消申请 — `temu.order.cancel.outofstock.apply`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_seller_cancel_order_cancel_outofstock_apply.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation（`menu_code` / `sub_menu_code` 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`temu.order.cancel.outofstock.apply`，业务载荷放在 Body 的 `params` |

**Description:** The user takes the initiative to initiate a stock-out situation, which will be submitted to the risk control department for review（商家主动发起缺货情况，提交风控部门审核）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> `parentOrderSn`、`orderSnList` 通常来自 `linkfox-temu-order-global` 订单列表/详情接口。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填) — lack stock apply request
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
response — lack stock apply response
├── success
├── errorCode
├── errorMsg
└── result
    ├── applyResult
    └── failReasonList[]
        ├── parentOrderSn
        ├── orderSn
        └── reasonList[]
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | lack stock apply result |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| applyResult | BOOLEAN | lack stock apply result（缺货申请结果）：`true` = apply success（申请成功）；`false` = apply fail（申请失败） |
| failReasonList | OBJECT[] | apply fail reason list（申请失败原因列表）；`applyResult=true` 时通常为空或不返回 |

### `failReasonList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| parentOrderSn | STRING | parent order sn（父订单号） |
| orderSn | STRING | order sn（子订单号） |
| reasonList | STRING[] | apply fail reason code list（申请失败原因码列表） |

---

## 示例

```bash
python scripts/global_seller_cancel_order_cancel_outofstock_apply.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentOrderSn": "PO-123456789",
    "orderSnList": ["O-111111111"]
  }
}'
```

典型流程：`linkfox-temu-order-global` 查 `parentOrderSn` / `orderSn` → 本接口提交缺货取消申请（风控审核）→ 根据 `applyResult` 与 `failReasonList` 确认是否受理。
