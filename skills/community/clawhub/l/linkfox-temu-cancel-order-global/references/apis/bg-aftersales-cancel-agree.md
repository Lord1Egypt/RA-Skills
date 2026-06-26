# 同意取消订单 — `bg.aftersales.cancel.agree`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_cancel_aftersales_cancel_agree.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation（`menu_code` / `sub_menu_code` 以 Partner 后台该接口页为准） |
| **网关** | `POST /temu/proxy`，`type`=`bg.aftersales.cancel.agree`，业务载荷放在 Body 的 `params` |

**Description:** Agree cancel order（同意买家发起的取消订单申请）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。  
> `parentAfterSalesSn`、`parentOrderSn` 通常来自 [bg-aftersales-cancel-list-get.md](./bg-aftersales-cancel-list-get.md) 列表接口返回（`afterSalesStatusGroup=8` 待处理）。

---

## Request 结构（官方业务参数）

```text
params
└── request (OBJECT, 选填)
    ├── parentAfterSalesSn (STRING, 是)
    └── parentOrderSn (STRING, 是)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| parentAfterSalesSn | STRING | **是** | Parent after-sales order number（父售后单号），**不能为空** |
| parentOrderSn | STRING | **是** | Parent order number（父订单号），**不能为空** |

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentAfterSalesSn": "PAS-123456789",
    "parentOrderSn": "PO-123456789"
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── result (OBJECT)
├── success
├── errorCode
└── errorMsg
```

### `response` 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| result | OBJECT | Empty field（官方未展开子字段；成功时通常为空对象） |
| success | BOOLEAN | Whether it was successful or not（是否成功） |
| errorCode | INTEGER | Error code（错误码） |
| errorMsg | STRING | Error message（错误信息） |

### `result`

| 参数 | 类型 | 说明 |
|------|------|------|
| _(无子字段)_ | — | Partner 文档标注为 Empty field；若实际响应含其它字段，以 Temu 返回 JSON 为准 |

---

## 示例

```bash
python scripts/global_cancel_aftersales_cancel_agree.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "parentAfterSalesSn": "PAS-123456789",
    "parentOrderSn": "PO-123456789"
  }
}'
```

典型流程：`bg.aftersales.cancel.list.get`（`afterSalesStatusGroup=8`）取得 `parentAfterSalesSn` + `parentOrderSn` → 本接口**同意取消** → 可再查列表确认状态变为已同意（`9`）或用 `linkfox-temu-order-global` 刷新订单状态。
