# 获取区域可用物流商 — `bg.logistics.companies.get`

| 项 | 值 |
|----|-----|
| **脚本** | `scripts/global_self_fulfilled_logistics_companies_get.py` |
| **Partner 文档** | https://partner-global.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896（按 `type` 在 Partner Global 后台打开） ||
| **网关** | `POST /temu/proxy`，`type`=`bg.logistics.companies.get`，业务载荷放在 Body 的 `params` |

**Description:** Obtain full logistics providers that support shipping at the corresponding region（获取指定区域下支持发货的全部物流服务商列表）。

> **网关鉴权字段**由本 skill 网关脚本处理；业务参数见下方 `request`。建议使用 **`tokenPurpose=order-shipping`**。自发货确认物流、创建运单前，通常需先调用本接口取得 `logisticsServiceProviderId` 等。

---

## Request 结构（官方顶层）

```text
params
└── request (OBJECT, 选填)
    └── regionId              ← 必填
```

### `request` 内字段

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| regionId | INTEGER | **是** | Region ID（区域 ID）。完整编码表见 Partner 文档：[regionId 编码说明](https://partner.temu.com/documentation?menu_code=7289390cfd724be4a196f11ebe45a896)。全球站常用示例：**211**（USA，与 `linkfox-temu-order-global` 订单接口一致）。 |

> 官方表将顶层 **`request`** 标为选填（False），但 **`request.regionId`** 为必填；实际调用时**应始终传入 `request` 且包含 `regionId`**，否则无法按区域筛选物流商。

### 网关 `params` 写法

```json
{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "regionId": 211
  }
}
```

---

## Response（Temu `body` 解析后）

```text
response
├── success          ← 请求级是否成功
├── errorCode
├── errorMsg
└── result[]         ← 物流服务商列表（OBJECT 数组）
    ├── logisticsServiceProviderId
    ├── logisticsServiceProviderName
    └── logisticsBrandName
```

### 顶层字段

| 参数 | 类型 | 说明 |
|------|------|------|
| success | BOOLEAN | success（当前请求是否成功，True 成功，False 失败） |
| errorCode | INTEGER | error code（错误码） |
| errorMsg | STRING | error message（错误信息） |
| result | OBJECT[] | 该区域下支持发货的物流服务商列表；无数据时可能为空数组 `[]` |

### `result[]` 元素字段

| 参数 | 类型 | 说明 |
|------|------|------|
| logisticsServiceProviderId | INTEGER | logistics Service Provider Id（物流服务商 ID；后续发货/创建运单等接口常作为承运商标识入参） |
| logisticsServiceProviderName | STRING | logistics Service Provider Name（物流服务商名称） |
| logisticsBrandName | STRING | logistics Brand Name（物流品牌名称；Partner 原文描述为 “logistics Service Provider Name”，与 `logisticsServiceProviderName` 字段区分，以实际返回为准） |

> 调用成功时先判断 **`response.success === true`**，再遍历 **`result`** 选用 `logisticsServiceProviderId` / `logisticsServiceProviderName`。`errorCode` / `errorMsg` 非空或 `success === false` 时以错误信息为准。

---

## 示例

```bash
export LINKFOXAGENT_API_KEY="<key>"

# 专用脚本（全球站 regionId=211）
python scripts/global_self_fulfilled_logistics_companies_get.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "request": {
    "regionId": 211
  }
}'
```

```bash
# 通用代理（等价）
python scripts/temu_global_proxy.py '{
  "accessToken": "TOKEN",
  "tokenPurpose": "order-shipping",
  "type": "bg.logistics.companies.get",
  "params": {
    "request": {
      "regionId": 211
    }
  }
}'
```

---

## 典型用法

1. 从订单接口（如 `bg.order.detail.v2.get`）或业务上下文确认 **`regionId`**（全球站多为 **211**）。
2. 调用本接口获取该区域可用 **`logisticsServiceProviderId`** 列表。
3. 用户或后续脚本选择承运商后，再调用自发货相关创建运单 / 确认发货等接口（待接入）。