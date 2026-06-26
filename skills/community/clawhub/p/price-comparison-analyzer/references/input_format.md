# 电商比价输入数据格式规范

## 目录
- [概览](#概览)
- [核心数据结构](#核心数据结构)
- [字段说明](#字段说明)
- [验证规则](#验证规则)
- [完整示例](#完整示例)

## 概览
本规范定义了电商比价分析器的输入数据格式。所有输入数据必须符合此格式，才能被脚本正确处理。

## 核心数据结构

### 1. 产品定义（必填）
```json
{
  "product_name": "Apple iPhone 15 128GB 黑色",
  "brand": "Apple",
  "key_specs": "A2890/6.1英寸/128GB/黑色"
}
```

### 2. 价格数据（必填）
```json
{
  "price_list": [5199, 5299, 4899, 5499, 5200]
}
```

### 3. 平台详情（必填）
```json
{
  "platform_info": [
    {
      "platform": "京东",
      "price": 5299,
      "conditions": "官方自营，无额外券",
      "seller_type": "official"
    },
    {
      "platform": "拼多多",
      "price": 4899,
      "conditions": "百亿补贴，限新用户",
      "seller_type": "subsidized"
    }
  ]
}
```

## 字段说明

### 必填字段

#### product_name（必填）
- **类型**: string
- **说明**: 商品名称，应包含品牌、型号、关键规格
- **长度**: 3-200 字符
- **示例**: "Apple iPhone 15 128GB 黑色", "华为 Mate 60 Pro 12GB+256GB 雅川青"

#### price_list（必填）
- **类型**: array of number
- **说明**: 所有采集到的价格列表（原始价格，未考虑任何折扣）
- **元素类型**: float/int
- **取值范围**: > 0
- **示例**: [5199, 5299, 4899, 5499, 5200]

### 可选字段

#### brand（可选）
- **类型**: string
- **说明**: 品牌名，用于商品语义对齐
- **示例**: "Apple", "华为", "小米", "Sony"

#### key_specs（可选）
- **类型**: string
- **说明**: 关键规格描述，用于排除不可比商品
- **示例**: "A2890/6.1英寸/128GB/黑色", "i7-13700H/16GB/512GB"

#### platforms（可选）
- **类型**: array of string
- **说明**: 指定比价平台列表
- **推荐值**: ["京东", "天猫", "拼多多", "抖音", "小红书", "亚马逊", "淘宝"]
- **默认**: ["京东", "天猫", "拼多多"]

#### region（可选）
- **类型**: string
- **说明**: 地区，影响税费、仓储、渠道
- **示例**: "中国大陆", "香港", "美国"

#### time_window（可选）
- **类型**: string
- **说明**: 价格采集时间范围
- **示例**: "最近7天", "最近30天", "当前"

#### user_priority（可选）
- **类型**: string
- **说明**: 用户优先级，影响推荐结果
- **推荐值**: "最低价优先", "官方/正品优先", "售后/发票优先"
- **默认**: "官方/正品优先"

#### platform_info（可选但推荐）
- **类型**: array of object
- **说明**: 平台详细信息列表
- **每个对象包含**:
  - platform (string): 平台名称
  - price (number): 价格
  - conditions (string): 价格条件描述
  - seller_type (string): 卖家类型（official/authorized/third-party/subsidized）

## 验证规则

### 1. 必填字段验证
- `product_name` 必须存在且非空
- `price_list` 必须存在且至少包含一个有效价格

### 2. 数据类型验证
- 所有价格必须是数字类型（int 或 float）
- 价格必须大于 0
- 价格建议不超过 1,000 万

### 3. 业务逻辑验证
- 同一商品的价格列表应该来自可比的 SKU
- `platform_info` 中的价格应包含在 `price_list` 中
- `seller_type` 值必须在预定义范围内

### 4. 格式规范
- 商品名称应避免使用营销词汇（如"热销"、"爆款"）
- 条件描述应简洁明确（如"官方自营"而不是"京东自营官方直营店"）

## 完整示例

### 最小可用示例
```json
{
  "product_name": "iPhone 15 128GB",
  "price_list": [5199, 5299, 4899, 5499, 5200]
}
```

### 完整示例
```json
{
  "product_name": "Apple iPhone 15 128GB 黑色",
  "brand": "Apple",
  "key_specs": "A2890/6.1英寸/128GB/黑色",
  "platforms": ["京东", "天猫", "拼多多"],
  "region": "中国大陆",
  "time_window": "最近7天",
  "user_priority": "官方/正品优先",
  "price_list": [5199, 5299, 4899, 5499, 5200, 5300, 5100],
  "platform_info": [
    {
      "platform": "京东",
      "price": 5299,
      "conditions": "官方自营，无额外券",
      "seller_type": "official"
    },
    {
      "platform": "拼多多",
      "price": 4899,
      "conditions": "百亿补贴，限新用户",
      "seller_type": "subsidized"
    },
    {
      "platform": "天猫",
      "price": 5199,
      "conditions": "官方旗舰店，需领券200",
      "seller_type": "official"
    }
  ]
}
```

### 测试用例 1：标准场景
```json
{
  "product_name": "华为 Mate 60 Pro 12GB+256GB",
  "price_list": [6999, 6899, 7199, 6799, 7299],
  "platform_info": [
    {"platform": "京东", "price": 6999, "conditions": "官方自营", "seller_type": "official"},
    {"platform": "天猫", "price": 6899, "conditions": "官方旗舰店", "seller_type": "official"},
    {"platform": "拼多多", "price": 6799, "conditions": "百亿补贴", "seller_type": "subsidized"}
  ]
}
```

### 测试用例 2：异常价格检测
```json
{
  "product_name": "Sony WH-1000XM5",
  "price_list": [2999, 2990, 2980, 2995, 1500],
  "platform_info": [
    {"platform": "京东", "price": 2999, "conditions": "官方自营", "seller_type": "official"},
    {"platform": "天猫", "price": 2990, "conditions": "官方旗舰店", "seller_type": "official"},
    {"platform": "淘宝", "price": 1500, "conditions": "疑似翻新", "seller_type": "third-party"}
  ]
}
```

### 测试用例 3：复杂条件场景
```json
{
  "product_name": "戴森 V15 Detect",
  "price_list": [4990, 4899, 5290, 5490],
  "platform_info": [
    {"platform": "京东", "price": 5290, "conditions": "官方自营，无折扣", "seller_type": "official"},
    {"platform": "拼多多", "price": 4990, "conditions": "百亿补贴，限新用户", "seller_type": "subsidized"},
    {"platform": "天猫", "price": 4899, "conditions": "需领券300+满减200", "seller_type": "official"}
  ]
}
```

## 注意事项

1. **SKU 一致性**: 确保所有价格来自相同的商品规格，不同配置（如颜色、容量、版本）不应混合在同一个 `price_list` 中。

2. **价格时效性**: `time_window` 字段建议设置，以便智能体判断价格的时效性。

3. **条件完整性**: `conditions` 字段应尽量完整描述获得该价格所需的所有条件，包括：
   - 是否需要优惠券
   - 是否是会员专享价
   - 是否有限时/限量
   - 是否有地区限制

4. **数据采集**: 智能体在采集价格时应遵循以下原则：
   - 优先采集官方渠道价格
   - 标注特殊条件（如"百亿补贴"、"秒杀"）
   - 记录采集时间
   - 区分展示价和到手价

## 验证工具

使用 `data_validator.py` 脚本验证输入数据：

```bash
python data_validator.py '<json_data>'
```

示例：
```bash
python data_validator.py '{"product_name": "iPhone 15", "price_list": [5000, 5200]}'
```

输出：
```json
{
  "is_valid": true,
  "errors": [],
  "warnings": []
}
```
