# 取消合作仓履约单 — `bg.cooperativewarehouse.fulfill.cancel`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_co_warehouse_cooperativewarehouse_fulfill_cancel.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fd19c5c9a430407a8c587d7f3e492c4a&sub_menu_code=085d46b8a6604228b371e0706ac4af7d |
| **网关** | `POST /temu/proxy`，`type`=`bg.cooperativewarehouse.fulfill.cancel`，业务载荷放在 Body 的 `params` |

**Description:** cooperation warehouse ERP order

（取消已提交至**合作仓（Cooperative Warehouse）**的 **ERP 履约单**；按 **`erpFulfillNo`** 标识要取消的履约单。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，且 **`managementType=semi-managed`**（本 skill 仅 Semi-managed）。  
> **前置依赖：**  
> - 须已完成 [**`bg.cooperativewarehouse.token.authorization`**](./bg-cooperativewarehouse-token-authorization.md) 绑定合作仓服务商。  
> - **`erpFulfillNo`** 通常来自 [**`bg.cooperativewarehouse.fulfill.submit`**](./bg-cooperativewarehouse-fulfill-submit.md) 提交成功后的返回，或 **`bg.cooperativewarehouse.fulfill.query`**（待接入）查询结果。  
> - 若履约单不存在，返回错误码 **170020004**。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── erpFulfillNo (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| erpFulfillNo | STRING | **是** | erpFulfillNo（合作仓 **ERP 履约单号**；卖家/ERP 侧用于标识该笔合作仓履约请求的唯一编号，须与提交履约时使用的 **`erpFulfillNo`** 一致） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`erpFulfillNo`** 为必填（True）。Partner **Request Example** CURL 将 **`erpFulfillNo`** 写在顶层；经 LinkFox 网关时建议放在 **`params.request.erpFulfillNo`**。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "request": {
    "erpFulfillNo": "ERP-FULFILL-20260101001"
  }
}
```

---

## Response（Temu `body` 解析后）

Partner **Response** 表顶层为 **`response`** 对象；**`result`** 子行在导出 HTML 中为折叠状态，下列子层级按 **Response 表 + Response Example** 全部展开。

```text
response（或解析后的根对象）
├── success
├── errorCode
├── errorMsg
└── result (OBJECT)
    ├── erpFulfillNo (STRING)
    └── cwFulfillNo (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果对象（取消履约结果） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| erpFulfillNo | STRING | ERP fulfillment order number（ERP 履约单号；与请求 **`erpFulfillNo`** 对应，用于确认已受理取消的履约单） |
| cwFulfillNo | STRING | Cooperative warehouse fulfillment order number（合作仓侧履约单号；Temu/合作仓系统生成的履约单标识，与 **`erpFulfillNo`** 关联，便于在 **`fulfill.query`** 等接口中追踪） |

> 调用成功时先判断 **`success === true`**，再核对 **`result.erpFulfillNo`** 与请求一致。取消是否最终生效可能还须通过 **`bg.cooperativewarehouse.fulfill.query`**（待接入）或订单状态复核。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 170020001 | This ERP provider is not supported. | 检查合作仓服务商是否受支持 |
| 170020002 | This mall is not authorized to the cooperative warehouse service provider. | 先完成 [**token.authorization**](./bg-cooperativewarehouse-token-authorization.md) |
| 170020003 | The parameter is illegal, please check and try again. | 检查 **`erpFulfillNo`** 格式 |
| 170020004 | This fulfillment order not exists, please check if the fulfillment number is correct. | 核对 **`erpFulfillNo`** 是否存在、是否已取消 |
| 170020005 | This cooperative warehouse customer code is not match the authorized customer code. | 客户编码与授权不一致，重新授权 |

<details>
<summary>完整错误码列表（5 条，Partner 原文）</summary>

| 错误码 | 错误信息 |
|--------|----------|
| 170020001 | This ERP provider is not supported. |
| 170020002 | This mall is not authorized to the cooperative warehouse service provider. |
| 170020003 | The parameter is illegal, please check and try again. |
| 170020004 | This fulfillment order not exists, please check if the fulfillment number is correct. |
| 170020005 | This cooperative warehouse customer code is not match the authorized customer code. |

</details>

---

## 典型用法

```text
1. bg.cooperativewarehouse.provider.list      → 选择 warehouseProviderCode
2. bg.cooperativewarehouse.token.authorization → 合作仓授权
3. bg.cooperativewarehouse.fulfill.submit      → 提交履约，获得 erpFulfillNo
4. bg.cooperativewarehouse.fulfill.cancel      → 本接口：按 erpFulfillNo 取消
5. bg.cooperativewarehouse.fulfill.query       → 查询取消后状态（待接入）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_co_warehouse_cooperativewarehouse_fulfill_cancel.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "erpFulfillNo": "ERP-FULFILL-20260101001"
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.cooperativewarehouse.fulfill.cancel",
  "params": {
    "request": {
      "erpFulfillNo": "ERP-FULFILL-20260101001"
    }
  }
}'
```
