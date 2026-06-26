---
id: shopping-cart-api
slug: shopping-cart-api
name: 购物车 API
description: 供 OpenClaw 调用，用于将产品添加到购物车。支持配置 SKU 数量、产品扩展规格、配件详情及关联项目信息。
version: 1.1.0
tools: [addToShoppingCart]
tags: [api, cart, documentation]
permissions: [authenticated]
priority: 55
---

# 1. 强制认证与安全约束
- **无 Token 不调用 (STRICT)**: 严禁在没有有效 `accessToken` 的情况下调用此接口。
- **强制前置校验**: 在发起请求前，AI 必须确认 `accessToken` 存在。若不存在，必须先执行分步登录流程。
- **401 处理**: 若接口返回 401（未授权），AI 必须立即尝试 `refreshToken`，成功后静默重试此请求。
- **凭据源**: 系统变量必须从根目录下的 `.env` 文件（路径：`../.env`）读取，严禁询问用户。

# 2. 接口概述
该技能包含核心接口：用于**添加商品到购物车**。

# 2. 接口详细说明

## 2.1 添加到购物车 (addToShoppingCart)
- **接口地址**: `https://gateway.hdlcontrol.com/crm-wisdom/agent/shoppingCart/save`
- **请求方式**: `POST`
- **认证方式**: `Bearer Token` (Header: `Authorization`)
- **签名算法**: 参考 [sign-encryption-api](../sign-encryption-api/SKILL.md)

---

# 2. 添加到购物车接口 (ShoppingCartsSaveDTO)

## 2.1 请求参数详解
| 字段名 | 类型 | 必选 | 描述 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| **skuNum** | Integer | **是** | 订购数量 (1-9999)。 | `1` |
| **skuId** | Long | **是** | 商品 SKU ID。 | `1851828437464506370` |
| **productId** | Long | **是** | 产品 ID。 | `1481808207389118466` |
| **erpNo** | String | **是** | ERP 编码（品号）。 | `"308013573"` |
| `laserMark` | String | 否 | 是否需要镭雕: `YES`, `NO`。 | `"NO"` |
| `projectId` | Long | 否 | 关联的项目 ID。 | `123456789` |
| `projectName` | String | 否 | 项目名称。 | `"河东智能家居项目"` |
| `projectType` | String | 否 | 项目类型。 | `"DOMESTIC"` |
| `productSpecsExtDataList` | List | 否 | 产品扩展规格数据。 | (见下文) |
| `accessoriesSkuExtDataList` | List | 否 | 配件扩展规格数据。 | (见下文) |
| `appKey` | String | **是** | (BaseDTO) 应用标识，固定从 `.env` 读取 `${HDL_APP_KEY}`。 | `${HDL_APP_KEY}` |
| `timestamp` | Long | **是** | (BaseDTO) 13位毫秒级时间戳。 | `1774423171000` |
| `sign` | String | **是** | (BaseDTO) 安全签名，计算详见 [sign-encryption-api](../sign-encryption-api/SKILL.md)。 | `"abc123xyz..."` |

### 2.1.2 完整请求示例 (JSON)
```json
{
  "skuNum": 2,
  "skuId": 1851828437464506370,
  "productId": 1481808207389118466,
  "erpNo": "308013573",
  "projectId": 123456789,
  "projectName": "河东智能家居项目",
  "appKey": "${HDL_APP_KEY}",
  "timestamp": 1774423171000,
  "sign": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
}
```

### 2.1.3 响应结构 (Result<Boolean>)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `code` | Integer | 状态码 (0 表示成功)。 |
| `isSuccess` | Boolean | 是否执行成功。 |
| `data` | Boolean | 返回结果。 |
| `msg` | String | 提示消息。 |

### 2.1.4 响应示例
```json
{
  "code": 0,
  "isSuccess": true,
  "data": true,
  "msg": "添加成功"
}
```

---

## 2.4 产品扩展规格详解 (productSpecsExtDataList)
该字段用于描述产品的个性化定制需求（如：镭雕内容、特殊材质、颜色定制等）。配件扩展规格 `accessoriesSkuExtDataList` 也遵循此结构。

### 2.4.1 ProductSpecsExt 结构
| 字段名 | 类型 | 描述 | 示例 |
| :--- | :--- | :--- | :--- |
| `specsName` | String | 规格名称（如“刻字内容”）。 | `"刻字内容"` |
| `tag` | String | 规格标签。 | `"laser_text"` |
| `productSpecsValueType`| Integer| 值类型：`0`(固定文本), `1`(用户输入)。 | `1` |
| `hasRequired` | Integer| 是否必填：`0`(必填), `1`(非必填)。 | `0` |
| `specsVarList` | List | 规格项列表（仅在类型为 0 时常用）。 | (见下文) |

### 2.4.2 SpecsVar 结构
- `name` (String): 选项名称。
- `checked` (Boolean): 是否选中。

### 2.4.3 扩展规格 JSON 示例
```json
"productSpecsExtDataList": [
  {
    "specsName": "镭雕内容",
    "tag": "engraving",
    "productSpecsValueType": 1,
    "hasRequired": 0,
    "specsVarList": [
      {
        "name": "客厅主灯",
        "checked": true
      }
    ]
  }
]
```

---

# 3. 调用策略与提示
1. **加车确认**: 成功将商品添加到购物车后，AI 应告知用户：“[商品名] 已成功添加到购物车。”
2. **多 SKU 处理**: 如果用户选择了多个不同规格的产品，需多次调用 `addToShoppingCart`。
3. **规格完整性**: 在调用接口前，确保已通过产品查询接口获取了正确的 `skuId` 和 `erpNo`。
