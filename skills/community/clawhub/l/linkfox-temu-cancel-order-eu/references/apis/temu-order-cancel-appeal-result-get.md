# 查询取消申请结果 — `temu.order.cancel.appeal.result.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/eu_seller_cancel_order_cancel_appeal_result_get.py` |
| **Partner 文档** | https://partner-eu.temu.com/documentation?menu_code=dbd3d395963a408984b8ae7dbc5f64f9（按 `type` 在 Partner EU 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`temu.order.cancel.appeal.result.get`，业务载荷放在 Body 的 `params` |

**Description:** Merchant queries the status of cancellation order appeal records（商家查询取消订单申诉记录的状态）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> `applySnList` 中的申请单号通常来自 [temu-order-cancel-appeal-apply.md](./temu-order-cancel-appeal-apply.md) 返回的 `result.applySn`。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    └── applySnList[] (STRING[], 是)
```

### `request`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| applySnList | STRING[] | **是** | Apply sn list（取消申请单号列表） |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "applySnList": ["APPLY-SN-123456789"]
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success
├── errorCode
├── errorMsg
└── result
    └── itemList[]
        ├── applySn
        └── status
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success |
| errorCode | INTEGER | error code |
| errorMsg | STRING | error message |
| result | OBJECT | Result |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| itemList | OBJECT[] | result item list（取消申请结果列表） |

### `itemList[]`

| 参数 | 类型 | 说明 |
|------|------|------|
| applySn | STRING | Apply sn（取消申请单号） |
| status | INTEGER | Apply cancel status（取消申请状态），见下表 |

#### `status`

| 值 | 说明 |
|----|------|
| `1` | Auditing（审核中） |
| `2` | Approved（已通过） |
| `3` | Rejected（已拒绝） |
| `4` | Apply failed（申请失败） |
| `5` | Canceled（已取消） |

---

## 示例

```bash
python scripts/eu_seller_cancel_order_cancel_appeal_result_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "applySnList": ["APPLY-SN-123456789"]
  }
}'
```

典型流程：`temu.order.cancel.appeal.apply` 提交申请取得 `applySn` → 本接口轮询 `status`（`1` 审核中 → `2` 通过 / `3` 拒绝 / `4` 失败 / `5` 已取消）→ 可用 `linkfox-temu-order-eu` 刷新订单状态。
