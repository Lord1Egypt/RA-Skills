---
id: product-query-api
slug: product-query-api
name: 渠道商优选商城产品查询 API
description: 供 OpenClaw 调用，用于分页检索 HDL 渠道商优选商城的商品信息。支持按名称、品牌、型号、协议、ERP 编码等多维度筛选，并提供极致详细的 SKU 及递归配件信息。
version: 1.3.0
tools: [queryProductPage]
tags: [api, product, mall, documentation]
permissions: [authenticated]
priority: 50
---

# 1. 强制认证与安全约束
- **无 Token 不调用 (STRICT)**: 严禁在没有有效 `accessToken` 的情况下调用此接口。
- **强制前置校验**: 在发起请求前，AI 必须确认 `accessToken` 存在。若不存在，必须先执行分步登录流程。
- **401 处理**: 若接口返回 401（未授权），AI 必须立即尝试 `refreshToken`，成功后静默重试此请求。
- **凭据源**: 系统变量必须从根目录下的 `.env` 文件（路径：`../.env`）读取，严禁询问用户。

# 2. 接口详细说明

## 2.1 渠道商优选商城产品分页查询 (queryProductPage)
- **接口地址**: `https://gateway.hdlcontrol.com/crm-wisdom/agent/product/page`
- **请求方式**: `POST`
- **认证方式**: `Bearer Token` (Header: `Authorization`)

### 2.1.1 请求参数 (JSON Body)
| 字段名 | 类型 | 必选 | 描述 | 示例 |
| :--- | :--- | :--- | :--- | :--- |
| **pageNo** | Long | **是** | 当前页码，从 1 开始。 | `1` |
| **pageSize** | Long | **是** | 每页条数，建议范围 1-50。 | `10` |
| `productName` | String | 否 | 产品名称，支持模糊匹配。 | `"方悦面板"` |
| `brandName` | String | 否 | 产品品牌名称。 | `"广州河东"` |
| `productModel` | String | 否 | 产品型号（通常为字母+数字，可能带特殊符号）。 | `"HDL-MPL6B-TILE48"` |
| `erpNo` | String | 否 | SKU 品号（ERP 编码）。 | `"308020540"` |
| `protocolType` | String | 否 | 协议类型: `BUSPRO`, `KNX`, `ZIGBEE`, `DALI`, `BUSPRO_WIRELESS`, `OTHER`。 | `"BUSPRO"` |
| `productType` | String | 否 | 产品类型: `CORE_PRODUCT`(HDL产品), `THREE_PRODUCTS`(生态集成产品)。 | `"CORE_PRODUCT"` |
| `panelSeries` | String | 否 | 面板系列: `FANG_YUE_2_1`, `YAN_1_0`, `SHANG_JIN_SHAN_1_0` 等。 | `"FANG_YUE_2_1"` |
| `luminaireSeries` | String | 否 | 灯具系列: `SHAOHUA_SERIES`(射灯&筒灯), `LIUGUANG_SERIES`(格栅灯) 等。 | `"格栅灯"` |
| `categoryCode` | String | 否 | 产品分类编码。 | `"C001"` |
| `supplierName` | String | 否 | 供应商名称。 | `"广州河东"` |
| `productSaleTypes` | List<String>| 否 | 产品在售类型，通常由系统填充。 | `["STANDARDS"]` |
| `zoneType` | String | 否 | 区域类型。 | `"DOMESTIC"` |
| `accessToken` | String | 否 | **(BaseDTO)** 用户身份令牌（系统自动处理）。来源：[user-auth-api](file:///Users/super_song/Project/hdl-project/hdl-mcp-server/src/main/resources/.claude/skills/user-auth-api/SKILL.md)。 | `"Bearer eyJhbG..."` |
| `appKey` | String | 否 | **(BaseDTO)** 应用标识。固定为 `${HDL_APP_KEY}`。 | `${HDL_APP_KEY}` |
| `timestamp` | Long | 否 | **(BaseDTO)** 当前 13 位毫秒级时间戳。 | `1774425423000` |
| `sign` | String | 否 | **(BaseDTO)** 安全签名。生成算法参考：[sign-encryption-api](file:///Users/super_song/Project/hdl-project/hdl-mcp-server/src/main/resources/.claude/skills/sign-encryption-api/SKILL.md)。注意：使用 `AppSecret: ${HDL_APP_SECRET}` 进行签名。 | `"abc123xyz..."` |
| `requestId` | String | 否 | **(BaseDTO)** 请求唯一 ID。 | `"req_001"` |

## 2.2 完整请求 JSON 示例
```json
{
  "pageNo": 1,
  "pageSize": 10,
  "productName": "方悦面板 2.1",
  "brandName": "广州河东",
  "productModel": "HDL-MPL6B-TILE48",
  "erpNo": "308020540",
  "protocolType": "ZIGBEE",
  "productType": "CORE_PRODUCT",
  "panelSeries": "FANG_YUE_2_1",
  "luminaireSeries": "SHAOHUA_SERIES",
  "categoryCode": "C001",
  "supplierName": "广州河东",
  "productSaleTypes": ["STANDARDS"],
  "zoneType": "DOMESTIC",
  "accessToken": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "appKey": "hdl-mcp-server",
  "timestamp": 1774423171,
  "sign": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
  "requestId": "550e8400-e29b-41d4-a716-446655440000"
}
```

# 3. 响应参数详解 (List<AgentMallProductVO>)

## 3.1 完整字段列表

### AgentMallProductVO (主产品)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `id` | String | 产品唯一主键 ID。 |
| `productName` | String | 产品名称。 |
| `productModel` | String | 产品型号。 |
| `protocol` | String | 协议名称。 |
| `unit` | String | 单位。 |
| `imageUrl` | String | **产品展示图片 URL (AI 必须展示此图片)**。 |
| `supplierName` | String | 供应商。 |
| `tags` | List<String> | 标签，如 `["NEW", "HOT"]`。 |
| `skuList` | List<VO> | **核心：SKU 列表**。 |

### AgentMallProductSkuVO (规格详情)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `skuId` | Long | SKU 唯一标识。 |
| `productId` | Long | 所属产品 ID。 |
| `erpNo` | String | ERP 编码（品号）。 |
| `price` | BigDecimal | 市场指导价。 |
| `unifiedPrice` | BigDecimal | **渠道统一价（商城实际成交价）**。 |
| `specsData` | String | 规格 JSON 字符串（描述颜色、材质等）。 |
| `accessoriesProductList` | List<VO> | **配件列表**。 |

### AgentProductAccessoriesVO (关联配件)
| 字段名 | 类型 | 描述 |
| :--- | :--- | :--- |
| `productNameCn` | String | 配件名称。 |
| `productModel` | String | 配件型号。 |
| `productUnitName` | String | 单位。 |
| `erpNo` | String | ERP 编码。 |
| `specsVarList` | List<String> | 规格摘要列表。 |
| `marketPrice` | BigDecimal | 市场价。 |
| `unifiedPrice` | BigDecimal | 渠道价。 |
| `specsData` | String | 规格详情 JSON。 |

## 3.2 完整响应 JSON 示例 (含多级嵌套)
```json
[
  {
    "id": "1481808207389118466",
    "productName": "方悦面板 2.1",
    "productModel": "HDL-MPL6B-TILE48",
    "protocol": "ZigBee",
    "unit": "个",
    "supplierName": "广州河东",
    "tags": ["NEW", "HOT"],
    "skuList": [
      {
        "skuId": 1851828437464506370,
        "productId": 1481808207389118466,
        "erpNo": "308013573",
        "price": 710.00,
        "unifiedPrice": 650.00,
        "specsData": "[{\"k\":\"颜色\",\"v\":\"黑色\"},{\"k\":\"材质\",\"v\":\"金属\"}]",
        "accessoriesProductList": [
          {
            "productNameCn": "面板底座",
            "productModel": "HDL-BASE-01",
            "productUnitName": "个",
            "erpNo": "308011842",
            "specsVarList": ["白色", "通用型"],
            "marketPrice": 50.00,
            "unifiedPrice": 45.00,
            "specsData": "[{\"k\":\"颜色\",\"v\":\"白色\"}]",
            "accessoriesProductList": []
          }
        ]
      },
      {
        "skuId": 1851828437464506371,
        "productId": 1481808207389118466,
        "erpNo": "308013574",
        "price": 750.00,
        "unifiedPrice": 690.00,
        "specsData": "[{\"k\":\"颜色\",\"v\":\"乌梅紫\"},{\"k\":\"材质\",\"v\":\"金属\"}]",
        "accessoriesProductList": [
          {
            "productNameCn": "装饰边框",
            "productModel": "HDL-FRAME-02",
            "productUnitName": "个",
            "erpNo": "308022991",
            "specsVarList": ["金色"],
            "marketPrice": 30.00,
            "unifiedPrice": 25.00,
            "specsData": "[{\"k\":\"颜色\",\"v\":\"金色\"}]"
          }
        ]
      }
    ]
  }
]
```

# 4. 调用策略与提示
1. **优先提取核心价格**: AI 在回答用户时，应始终以 `unifiedPrice` 作为实际购买价格。
2. **多 SKU 决策**: 如果一个产品下有多个 SKU（如颜色不同），AI 应当列出这些选项供用户选择。
3. **配件联动**: 如果 `accessoriesProductList` 不为空，AI 必须主动提醒用户：“该产品建议搭配 [配件名] 使用，价格为 [unifiedPrice]”。
4. **分页处理**: 默认返回 10 条。如果用户需要更多，引导其输入“下一页”。
