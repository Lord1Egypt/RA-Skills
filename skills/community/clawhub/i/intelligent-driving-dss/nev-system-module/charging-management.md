# 充电管理（Charging Management）

## 概述
充电管理模块负责规划充电策略、监测充电状态、优化充电效率和成本控制，确保新能源车主获得最佳的充电体验。

## 核心功能

### 1. 智能充电规划（Smart Charging Planning）

**目标：** 在满足用车需求的前提下，选择最佳的时间和地点充电。

**输入参数：**
```json
{
  "current_soc": 45,      // 当前电量%
  "expected_departure_time": "08:30",
  "estimated_distance_to_travel_km": 200,
  "preferred_charging_hours": ["22:00-24:00"], // 谷电时段
  "max_charging_price_kw": 1.5
}
```

**输出结果：**
```json
{
  "recommended_action": {
    "action": "delay_charging",
    "start_time": "22:30",
    "location": "home_home_stall",
    "expected_cost_yuan": 15.6
  },
  "alternative_options": [
    {
      "location": "workplace_station",
      "distance_km": 1.2,
      "charging_price_yuan_kwh": 0.8,
      "available_hours": "08:00-19:00"
    }
  ]
}
```

### 2. 充电桩类型适配（Charging Station Adaptation）

**充电标准：**
| 等级 | 功率 | 适用车型 | 充电时间（30kWh） | 费用（元/kWh） |
|------|------|---------|------------------|---------------|
| Level 1 | 7kW | BEV/PHEV | 4-5 小时 | 0.8-1.5 |
| Level 2 | 22kW | BEV/PHEV | 1.5-2 小时 | 0.8-2.0 |
| DC 快充 | 60-120kW | BEV | 30-45 分钟（10%-80%） | 1.2-2.5 |
| DC 超充 | 350kW+ | 800V 平台车型 | 15-25 分钟 | 2.0-4.0 |

**适配策略：**
```python
def select_charging_station(station_list, vehicle_type):
    if vehicle_type == "BEV":
        return min(filter(lambda s: s.power_kw >= 60, station_list), 
                     key=lambda s: s.cost_per_kwh)  # 快充优先
    else:
        return min(filter(lambda s: s.power_kw <= 22, station_list),
                     key=lambda s: s.cost_per_kwh + s.distance_km * 0.3)  # 慢充就近
```

### 3. 充电状态监测（Charging Status Monitoring）

**监测参数：**
- **充电电流/电压：** 实时反馈充电功率
- **电池温度：** 确保不过热充电
- **SOC 变化率：** 判断充电速度是否正常
- **故障代码：** 识别充电枪接触不良、充电桩故障等

**状态码定义：**
| 代码 | 含义 | 应对措施 |
|------|------|---------|
| C001 | 充电正常 | 无需操作 |
| C002 | 电池温度过高 | 暂停充电，降温后继续 |
| C003 | 接触不良 | 重新插拔充电枪 |
| C004 | 充电桩故障 | 切换充电桩或联系运维 |
| C005 | 超时未充满 | 检查线路或更换大功率充电站 |

### 4. 充电成本优化算法（Cost Optimization）

**目标函数：** Minimize Cost_total = Σ(P_kwh × Price_kWh)

**约束条件：**
1. SOC ≥ minimum_soc_departure（出发前最低电量）
2. T_charge ∈ preferred_hours（谷电时段优先）
3. 不超过电池最大充电功率

**优化示例：**
```python
# 假设当前电量 45%，需要在明早 8:00 到达目的地
# 推荐方案：今晚 22:00-24:00 充电（谷电，电价便宜）
# 预计成本：30kWh × 1.0元/kWh = 30 元

# 备选方案：就近慢充站
# 预计成本：(SOC_needed - SOC_current) × 1.8元 + 停车费
```

### 5. V2L/V2G 反向充电支持（Vehicle-to-Load/Grid）

**V2L（车对外放电）：**
- **适用场景：** 露营、应急供电
- **功率输出：** 3kW（家用插座级）、6kW（大功率电器）
- **注意事项：** 不建议频繁使用，会消耗电池寿命

**V2G（车网互动）：**
- **工作原理：** 电价低谷时充电，高峰时向电网售电
- **盈利模式：** 峰谷价差收益 + 电网补贴
- **法规依据：** 《新能源汽车充电设施接入规范》

## 与法律法规的关联

### 1. 充电设施建设
依据《中华人民共和国道路交通安全法》第三十三条：
> "新建、改建、扩建的公共建筑、商业街区、居住区、大（中）型建筑等，应当配建、增建停车场；停车泊位不足的，应当及时改建或者扩建..."

**解读：** 城市规划中应预留新能源汽车充电桩的建设空间。

### 2. 充电安全规范
依据《电动汽车充电设施安全要求》(GB/T 37615-2019)：
- **充电枪防护：** 必须配备漏电保护器
- **过充保护：** SOC ≥ 98% 时自动停止快充
- **热失控预警：** 电池温度异常时立即切断高压电

### 3. 电费收取规范
依据《关于促进电动汽车有序发展的指导意见》：
- **服务费上限：** 充电服务费不超过每千瓦时 1.5 元（各地略有差异）
- **信息公开：** 应公示电价、服务费、收费标准

---
*本模块与 core-traffic-rules 的交通法规配合使用，确保充电行为符合法律法规要求。*
