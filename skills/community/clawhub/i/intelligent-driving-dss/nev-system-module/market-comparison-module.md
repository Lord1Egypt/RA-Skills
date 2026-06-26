# 市场对比模块（Market Comparison Module）

## 功能概述
本模块提供新能源车型的市场对比分析能力，支持根据用户需求筛选和推荐匹配的车型，并提供竞争分析和优劣势对比。

## 查询接口定义

### 1. 车型筛选接口（Model Selection API）

**用途：** 根据用户核心需求推荐匹配的新能源车型。

**参数说明：**
```json
{
  "user_needs": {
    "primary_usage": ["commute","family","business"],
    "budget_max": 300000,
    "range_requirement_km": 500,
    "charging_preference": "home"
  },
  "exclude_criteria": {
    "no_autopilot_feature": false,
    "max_length_mm": 4800
  }
}
```

**返回结果：**
```json
{
  "recommended_models": [
    {
      "model_id": "BYD-YUAN-E",
      "match_score": 92,
      "key_features": ["high_range","safe_battery"]
    }
  ],
  "alternative_options": [...]
}
```

### 2. 市场定位接口（Market Positioning API）

**用途：** 分析车型在市场中的定位，了解同类竞争情况。

**参数：**
- target_model：目标车型名称
- price_range_min：最低价区间
- price_range_max：最高价区间

**返回：**
```json
{
  "target": {
    "brand": "比亚迪",
    "model": "元 PLUS",
    "price_position": "中端市场领导者",
    "key_competitors": ["Xiaomi-Yu7","LiAuto-AVI"]
  },
  "competitors_analysis": [
    {
      "competitor": "小米 SU7",
      "strengths": ["智能座舱","品牌营销"],
      "weaknesses": ["续航表现"],
      "market_share_percent": 12.5
    }
  ]
}
```

### 3. 竞品优劣势分析接口（Competitor Analysis API）

**用途：** 详细对比目标车型与竞品的优劣势。

**参数：**
- target_model：目标车型
- competitors：竞品列表

**返回示例：**
```json
{
  "target": {
    "model": "极氪 001",
    "advantages": [
      "高性能四驱系统，零百加速 3.8 秒",
      "800V 高压快充技术，充电效率高",
      "激光雷达配置，L2+级自动驾驶"
    ],
    "disadvantages": ["价格偏高","保值率待验证"]
  },
  "comparison_matrix": {
    "performance_score": 95,
    "comfort_score": 88,
    "smart_features_score": 90,
    "value_for_money_score": 75
  }
}
```

## 数据结构定义

### 市场对比基础数据模型

#### 车型信息（Vehicle）
| 字段 | 类型 | 说明 |
|------|------|------|
| vin | string | 车架号 |
| brand | enum | 品牌（比亚迪/蔚来/小鹏/小米/理想/吉利等） |
| model | string | 车型名称 |
| type | enum | BEV/PHEV/FCEV/HEV |
| year | integer | 上市年份 |
| battery_capacity_kwh | number | 电池容量（kWh） |

#### 性能参数（Performance）
| 字段 | 类型 | 说明 |
|------|------|------|
| range_nedc | number | NEDC 续航 |
| range_cltc | number | CLTC 续航 |
| acceleration_0_100 | number | 零百加速（秒） |
| max_power_kw | number | 最大功率（kW） |

#### 市场信息（MarketInfo）
| 字段 | 类型 | 说明 |
|------|------|------|
| manufacturer_price | number | 官方指导价 |
| market_average_price | number | 市场平均成交价 |
| price_positioning | enum | 高端/中端/经济 |

#### 充电信息（ChargingInfo）
| 字段 | 类型 | 说明 |
|------|------|------|
| charging_power_kw | number | 最高充电功率 |
| supporting_standards | array | 支持的充电标准 |

## 典型应用场景

### 场景 1：购车咨询助手
用户咨询："我想买一辆续航 500km 以上、预算 25 万左右的家用电动车，有什么推荐？"

**处理流程：**
1. 调用车型筛选接口（model selection API）
2. 根据价格区间和续航要求筛选候选车型
3. 返回 3-5 款匹配度最高的车型
4. 提供各车型的优劣势对比

### 场景 2：竞品分析工具
用户需要了解："小米 SU7 相比极氪 001，在哪些方面更有优势？"

**处理流程：**
1. 获取两款车型的详细参数数据
2. 调用竞品分析接口（competitor analysis API）
3. 输出优劣势对比矩阵
4. 给出购买建议

### 场景 3：市场动态监控
持续跟踪新能源市场价格变化、配置更新等信息。

## 与法律法规的关联

本模块的数据采集和使用需遵循《中华人民共和国道路交通安全法》相关条款：

- **数据采集规范：** 第 90 条（罚款程序）、第 93 条（违章停车处罚）涉及的价格信息需标注"市场参考价"，不得误导消费者
- **信息披露要求：** 所有续航数据、能耗指标必须符合 WLTP/CLTC 测试标准，与实测结果偏差不得超过 10%
- **消费者权益保护：** 不得提供虚假性能参数或隐瞒安全隐患

---
_此模块应与 core-traffic-rules 模块配合使用，确保购车决策基于合法合规的数据来源。_*
