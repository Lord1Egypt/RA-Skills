# 合作仓 Token 授权 — `bg.cooperativewarehouse.token.authorization`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/us_co_warehouse_cooperativewarehouse_token_authorization.py` |
| **Partner 文档** | https://partner-us.temu.com/documentation?menu_code=fd19c5c9a430407a8c587d7f3e492c4a&sub_menu_code=607fb76a2ef943d78e97dadbeca71aad |
| **网关** | `POST /temu/proxy`，`type`=`bg.cooperativewarehouse.token.authorization`，业务载荷放在 Body 的 `params` |

**Description:** Cooperative warehouse token authorization

（将卖家在**合作仓服务商（ERP/WMS）**侧取得的访问凭证授权绑定到 Temu 店铺，使平台可代店铺调用该合作仓履约能力。）

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 **`request`**。建议使用 **`tokenPurpose=order-shipping`**，且 **`managementType=semi-managed`**（本 skill 仅 Semi-managed）。  
> **前置依赖：**  
> - **`warehouseProviderCode`** 通常来自 [**`bg.cooperativewarehouse.provider.list`**](./bg-cooperativewarehouse-provider-list.md) 返回的 **`warehouseProviderList[].warehouseProviderCode`**。  
> - **`cwAccessToken`**、**`cwCustomerCode`** 由合作仓服务商侧颁发/分配，须与所选 **`warehouseProviderCode`** 对应。  
> - **`cwAppKey`** 为选填，部分 ERP 服务商要求与 **`cwAccessToken`** 一并提交。  
> **后续：** 授权成功后可用 [**`bg.cooperativewarehouse.fulfill.submit`**](./bg-cooperativewarehouse-fulfill-submit.md) 提交合作仓履约；查询见 **`bg.cooperativewarehouse.fulfill.query`**（待接入）。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    ├── cwAppKey (STRING, 选填)
    ├── cwAccessToken (STRING, 必填)
    ├── cwCustomerCode (STRING, 必填)
    └── warehouseProviderCode (STRING, 必填)
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| cwAppKey | STRING | 否 | cwAppKey（合作仓/ERP 侧应用 Key；部分服务商授权流程需要，Partner 表为选填） |
| cwAccessToken | STRING | **是** | cwAccessToken（合作仓服务商颁发的访问令牌；用于 Temu 校验卖家已在该服务商完成授权） |
| cwCustomerCode | STRING | **是** | cwCustomerCode（合作仓客户编码；须与服务商侧授权的客户身份一致，错误码 **170020005**） |
| warehouseProviderCode | STRING | **是** | warehouseProviderCode（合作仓服务商编码；与 [**provider.list**](./bg-cooperativewarehouse-provider-list.md) 中 **`warehouseProviderCode`** 一致） |

> 官方 Request 表将顶层 **`request`** 标为选填（False），但 **`cwAccessToken`**、**`cwCustomerCode`**、**`warehouseProviderCode`** 为必填。Partner **Request Example** CURL 将业务字段写在顶层；经 LinkFox 网关时建议放在 **`params.request`** 下（亦可由 `extract_business_params` 放在 `params` 顶层转发）。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "managementType": "semi-managed",
  "request": {
    "cwAppKey": "YOUR_CW_APP_KEY",
    "cwAccessToken": "YOUR_CW_ACCESS_TOKEN",
    "cwCustomerCode": "YOUR_CW_CUSTOMER_CODE",
    "warehouseProviderCode": "PROVIDER_CODE_FROM_LIST"
  }
}
```

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "cwAccessToken": "YOUR_CW_ACCESS_TOKEN",
    "cwCustomerCode": "YOUR_CW_CUSTOMER_CODE",
    "warehouseProviderCode": "PROVIDER_CODE_FROM_LIST"
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
    ├── authorizationSuccess (BOOLEAN)
    └── authorizationFailReason (STRING)
```

### 顶层字段（`response` 内，或根级）

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT | 业务结果对象（授权结果） |

### `result` 内字段

| 参数 | 类型 | 说明 |
|------|------|------|
| authorizationSuccess | BOOLEAN | Whether cooperative warehouse token authorization succeeded（合作仓 Token 授权是否成功；**`true`** 表示授权通过，**`false`** 表示未通过，须结合 **`authorizationFailReason`** 排查） |
| authorizationFailReason | STRING | Authorization failure reason（授权失败原因说明；**`authorizationSuccess`** 为 **`true`** 时可能为空或占位文案，以 Temu 实际返回为准） |

> 调用成功时先判断 **`success === true`**，再读 **`result.authorizationSuccess`**。若为 **`false`**，根据 **`authorizationFailReason`** 与下方业务错误码修正 **`cwAccessToken`** / **`cwCustomerCode`** / **`warehouseProviderCode`**，或确认店铺已在服务商侧完成授权（**170020002**）。

---

## 常见业务错误码（Partner Error Code）

| 错误码 | 错误信息（原文） | 处理建议 |
|--------|------------------|----------|
| 170020001 | This ERP provider is not supported. | 更换支持的 **`warehouseProviderCode`** / ERP 服务商 |
| 170020002 | This mall is not authorized to the cooperative warehouse service provider. | 店铺未对该合作仓服务商授权，先在服务商侧完成授权 |
| 170020003 | The parameter is illegal, please check and try again. | 检查入参格式与必填字段 |
| 170020004 | This fulfillment order not exists, please check if the fulfillment number is correct. | 履约单号不存在（本接口较少见，以 Partner 为准） |
| 170020005 | This cooperative warehouse customer code is not match the authorized customer code. | **`cwCustomerCode`** 与服务商侧已授权客户编码不一致 |

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
1. bg.cooperativewarehouse.provider.list      → 获取 warehouseProviderCode、permitsStatus
2. bg.cooperativewarehouse.token.authorization → 本接口：提交 cwAccessToken / cwCustomerCode 完成绑定
3. bg.cooperativewarehouse.fulfill.submit      → 提交合作仓履约
4. bg.cooperativewarehouse.fulfill.query         → 查询履约结果（待接入）
```

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

python scripts/us_co_warehouse_cooperativewarehouse_token_authorization.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "cwAppKey": "YOUR_CW_APP_KEY",
    "cwAccessToken": "YOUR_CW_ACCESS_TOKEN",
    "cwCustomerCode": "YOUR_CW_CUSTOMER_CODE",
    "warehouseProviderCode": "PROVIDER_CODE_FROM_LIST"
  }
}'
```

```bash
python scripts/temu_us_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.cooperativewarehouse.token.authorization",
  "params": {
    "request": {
      "cwAccessToken": "YOUR_CW_ACCESS_TOKEN",
      "cwCustomerCode": "YOUR_CW_CUSTOMER_CODE",
      "warehouseProviderCode": "PROVIDER_CODE_FROM_LIST"
    }
  }
}'
```
