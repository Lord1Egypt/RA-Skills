# 能耗动态计算模型（Energy Consumption Dynamic Calculation）

## 1. 基础公式框架

### **1.1 电动汽车能耗计算公式**

$$E_{total} = \int_0^{D} (P_{motor}(v) + P_{auxiliary}(t)) \cdot dt$$

其中：
- $E_{total}$: 总能耗（kWh）
- $P_{motor}$: 电机输出功率（kW）
- $P_{auxiliary}$: 车载辅助设备功耗（空调、灯光等，kW）
- $D$: 行驶距离（km）

### **1.2 分解为工况组件**

$$P_{total} = P_{roll} + P_{accel} + P_{grade} + P_{aero} + P_{elec}$$

#### **各分量公式：**

**滚动阻力功率：**
$$P_{roll} = (m \cdot g \cdot f_r + W_{load}) \cdot v$$
- $m$: 车辆自重（kg）
- $g$: 重力加速度 9.8 m/s²
- $f_r$: 滚动阻力系数（0.005~0.015，取决于路面材质、胎压）
- $W_{load}$: 载重质量（kg）

**加速阻力功率：**
$$P_{accel} = \frac{m \cdot a \cdot v}{3600}$$
- $a$: 加速度（m/s²），$a = \Delta v / t$

**坡度阻力功率：**
$$P_{grade} = m \cdot g \cdot \sin(\theta) \cdot v$$
- $\theta$: 坡度角度，$\tan(\theta) = i\% / 100$（如 5% 坡度则$\theta ≈ 2.86°$）

**风阻功率：**
$$P_{aero} = \frac{1}{2} \cdot C_d \cdot A \cdot \rho \cdot v^3$$
- $C_d$: 风阻系数（轿车 0.2~0.4，SUV 0.3~0.45）
- $A$: 正投影面积（m²，轿车约 2.0~2.5 m²）
- $\rho$: 空气密度（kg/m³，标准状态 1.225 kg/m³，海拔越高密度越小）

**电驱系统效率：**
$$P_{elec} = \frac{P_{motor}}{\eta_{overall}}$$
- $\eta_{overall}$: 总效率（电机效率 × 电控效率 × 传动效率），通常 0.75~0.85

### **1.3 基础能耗估算公式（简化版）**

$$E = E_0 \cdot k_1 \cdot k_2 \cdot k_3 \cdot k_4$$

其中：
- $E_0$: WLTP/CLTC 基准能耗（kWh/100km）
- $k_1$: 温度系数（低温时每降 10°C，能耗增加约 8%~10%）
- $k_2$: 载重系数（载重/自重比值）
- $k_3$: 坡度系数（$\sin(\theta) / \sin(\theta_0)$）
- $k_4$: 风速修正系数（逆风时增加，顺风时减少）

---

## 2. 外部因素输入模型（Dynamic Factors）

### **2.1 坡度影响模型（Gradient Factor）**

#### **分级处理：**
| 坡度 | 符号表示 | $\sin(\theta)$近似值 | 能耗影响倍数$k_3$ | 备注 |
|------|---------|---------------------|-------------------|------|
| 平坦路面 | 0% | 0 | 1.0 | 基准 |
| 轻微坡度（缓坡） | ±1~2% | 0.0175~0.0349 | 1.0~1.05 | 几乎无影响 |
| 中等坡度 | ±3~5% | 0.0524~0.0872 | 1.05~1.15 | 需考虑 |
| 陡坡路段 | ≥6% | ≥0.1045 | ≥1.15 | 显著增加能耗 |

#### **计算示例：**
假设：车辆自重$m=1500kg$，载重$W_{load}=500kg$，坡度$i=3\%$（$\theta≈1.72°$）
- $\sin(\theta) ≈ 0.030$
- $P_{grade} = 1500×9.8×0.030×v = 441×v$（W）

当$v=60km/h=16.7m/s$：
- $P_{grade} = 441×16.7 ≈ 7364W = 7.36kW$
- 额外能耗率 = $7.36/(m×g×v) = 7.36/(1500×9.8×16.7/1000) ≈ 0.029kWh/km$

**结论：** 每公里约增加 0.03kWh（约 3%~5% 的基准能耗）

### **2.2 载重影响模型（Payload Factor）**

#### **分级处理：**
| 载重状态 | $W_{load}/(m+98)$比值 | 对总质量比贡献 | 能耗影响倍数$k_2$ | 备注 |
|---------|---------------------|---------------|-------------------|------|
| 空载（无乘客） | 0~0.1×自重 | <10% | 1.0~1.03 | 几乎无影响 |
| 标准配置（5人） | 200~300kg | 10%~15% | 1.05~1.08 | 轻微增加 |
| 满载加行李 | 400~600kg | 20%~25% | 1.10~1.15 | 显著增加 |

#### **物理原理：**
滚动阻力功率正比于质量：
$$P_{roll} = (m \cdot g \cdot f_r + W_{load}) \cdot v$$
- 每增加 1kg 负载，滚动阻力增加约$g·f_r ≈ 9.8×0.01=0.098N$
- 在市区低速（20km/h）时，滚动阻力影响明显

### **2.3 环境温度模型（Temperature Factor）**

#### **电池热效率影响：**
| 温度区间 | BMS 策略 | 能耗影响倍数$k_1$ | 原因说明 |
|---------|---------|-------------------|---------|
| >25°C | 主动预冷 | 0.98~1.05 | 空调负荷增加抵消部分收益 |
| 15~25°C | 保温模式 | 0.95~1.0 | 最舒适区间 |
| 5~15°C | 被动保温 | 1.0~1.15 | 电池活性下降，充放电效率降低 |
| -5~5°C | 主动加热 | 1.1~1.25 | PTC/热泵系统耗电，预热过程高能耗 |
| < -5°C | 极限保护 | 1.2~1.4 | 电池容量衰减严重，需限制放电功率 |

#### **冬季低温效应：**
假设：-10°C 环境下，基准能耗 16kWh/100km
$$E_{actual} = E_0 \cdot k_1·f_{heater} = 16×1.15×1.3 ≈ 24kWh/100km$$

**解释：**
- $k_1=1.15$: 电池活性下降导致充放电效率降低
- $f_{heater}=1.3$: 座舱加热系统额外耗电（热泵约 2~3kW）

### **2.4 风速与空气密度修正（Wind Density Factor）**

#### **海拔修正：**
$$\rho_h = \rho_0 \cdot (1 - \frac{h}{H})$$
- $h$: 海拔高度（m）
- $H$: 地球半径约 6371km，简化公式：$\rho_h ≈ \rho_0·(1-h/2890)$

| 海拔 | $\rho$值 (kg/m³) | 对风阻功率影响 | 备注 |
|------|------------------|---------------|------|
| 海平面（0m） | 1.225 | 基准 | - |
| 昆明/重庆（800m） | 1.194 | 减少约 2.5% | 空气稀薄，风阻减小 |
| 拉萨（3650m） | 1.048 | 减少约 15% | 高原地区明显 |

#### **风速修正：**
有效风速 = $v_{relative} = v_{car} \pm v_{wind}$

$$P_{aero\_effective} = \frac{1}{2} C_d A \rho (v + v_{wind})^3$$

| 场景 | $v_{wind}$符号 | 对能耗影响 | 备注 |
|------|----------------|-----------|------|
| 逆风 | -$v$值 | 增加约$(v+v_w)^3/v^3$倍 | 高速时影响显著 |
| 顺风 | $+$v值 | 减少约$(v-v_w)^3/v^3$倍 | 高速时可降低能耗 |

---

## 3. 综合能耗预测算法（API）

### **输入参数结构：**
```json
{
  "vehicle": {
    "mass_kg": 1500,
    "base_range_cltc_kmh": 420,
    "cd_factor": 0.28,
    "area_m2": 2.3,
    "fr_coefficient": 0.009
  },
  "payload": {
    "passengers": 4,
    "luggage_kg": 100,
    "total_payload_kg": 450
  },
  "route": {
    "distance_km": 200,
    "average_grade_percent": 1.5,  // 平均坡度%
    "elevation_gain_m": 300          // 爬升高度
  },
  "environment": {
    "ambient_temp_c": 5,             // 环境温度°C
    "wind_speed_kmh": 20,            // 风速（正为顺风，负为逆风）
    "altitude_m": 100                // 海拔高度
  },
  "auxiliary_load": {
    "heater_kw": 0,                  // 加热器功率（冬季）
    "ac_kw": 3.5                     // 空调功率（夏季）
  }
}
```

### **计算输出结构：**
```json
{
  "energy_consumption": {
    "estimated_kwh_100km": 22.5,       // 预测能耗 kWh/100km
    "total_energy_kwh": 45.0,           // 全程总能耗
    "range_actual_km": 367              // 实际续航
  },
  "factor_breakdown": {
    "temperature_factor": 1.12,         // 温度修正系数
    "payload_factor": 1.08,             // 载重修正系数
    "grade_factor": 1.15,               // 坡度修正系数
    "wind_factor": 1.03                 // 风速修正系数
  },
  "recommendations": [
    "低温环境下建议提前预热电池",
    "爬升路段建议采用能量回收模式",
    "逆风行驶可考虑降低车速以省电"
  ]
}
```

### **算法伪代码：**
```python
def calculate_energy_consumption(input):
    # 基础参数
    m = input["vehicle"]["mass_kg"] + input["payload"]["total_payload_kg"]
    f_r = input["vehicle"]["fr_coefficient"]
    cd = input["vehicle"]["cd_factor"]
    A = input["vehicle"]["area_m2"]
    rho = 1.225 * (1 - input["environment"]["altitude_m"]/2890)
    
    # 速度假设（用于计算风阻）
    v_avg_kmh = 60  # 默认市区平均速度
    v_avg_ms = v_avg_kmh / 3.6
    
    # 坡度角度转换
    theta_rad = math.atan(input["route"]["average_grade_percent"] / 100)
    
    # 计算各分量功率（按 km/h）
    P_roll = m * 9.8 * f_r * v_avg_ms + input["payload"]["total_payload_kg"] * 9.8 * f_r * v_avg_ms
    P_accel = 0.5 * m * 1.0 * v_avg_ms / 3600  # 假设加速度为 1m/s²
    P_grade = m * 9.8 * math.sin(theta_rad) * v_avg_ms
    P_aero = 0.5 * cd * A * rho * (v_avg_ms + input["environment"]["wind_speed_kmh"]/3.6)**3
    
    P_total = P_roll + P_accel + P_grade + P_aero
    eta_system = 0.82  # 系统综合效率
    
    P_motor = P_total / eta_system
    
    # 辅助能耗
    P_aux = input["auxiliary_load"]["heater_kw"] or input["auxiliary_load"]["ac_kw"] or 0.5
    
    E_per_kmh = (P_motor + P_aux) * 3600 / 1000
    
    # 温度修正系数
    temp = input["environment"]["ambient_temp_c"]
    if temp < 5:
        k_temp = 1 + (5 - temp) * 0.04   # 每降 1°C增加 4%
    elif temp > 25:
        k_temp = 1 - (temp - 25) * 0.03  # 每升 1°C减少 3%（空调负荷）
    else:
        k_temp = 1.0
    
    E_adjusted = E_per_kmh * k_temp
    
    # 实际续航估算
    range_cltc = input["vehicle"]["base_range_cltc_kmh"]
    consumption_base = (50 / range_cltc) * 100  # 假设基准能耗 16kWh/100km
    
    E_100km_actual = consumption_base * k_temp * (m/1500) * (1 + input["route"]["average_grade_percent"]/100)
    
    return {
        "estimated_kwh_100km": round(E_100km_actual, 2),
        "range_actual_km": round(range_cltc / E_100km_actual * 100, 0)
    }
```

---

## 4. 典型场景案例演示

### **案例 1：北京→天津（平原，轻微上坡）**
```json
{
  "scenario": {
    "origin": "Beijing",
    "destination": "Tianjin",
    "distance_km": 120,
    "route_type": "highway"
  },
  "input": {
    "vehicle": {"mass_kg": 1500},
    "payload": {"total_payload_kg": 300},
    "route": {"average_grade_percent": 0.8, "elevation_gain_m": 150},
    "environment": {"ambient_temp_c": 22, "wind_speed_kmh": 10, "altitude_m": 30},
    "auxiliary_load": {"heater_kw": 0, "ac_kw": 2.5}
  },
  "output": {
    "estimated_kwh_100km": 18.5,
    "total_energy_kwh": 22.2,
    "range_actual_km": 396
  }
}
```

### **案例 2：山区爬坡路段（重庆→成都）**
```json
{
  "scenario": {
    "origin": "Chongqing",
    "destination": "Chengdu",
    "distance_km": 150,
    "route_type": "mountainous"
  },
  "input": {
    "vehicle": {"mass_kg": 1600},
    "payload": {"total_payload_kg": 500},
    "route": {"average_grade_percent": 3.5, "elevation_gain_m": 980},
    "environment": {"ambient_temp_c": 28, "wind_speed_kmh": -15, "altitude_m": 800},
    "auxiliary_load": {"heater_kw": 0, "ac_kw": 3.8}
  },
  "output": {
    "estimated_kwh_100km": 26.8,
    "total_energy_kwh": 40.2,
    "range_actual_km": 376
  }
}
```

---
*本模块与 core-traffic-rules 交通法规配合，确保能耗数据符合 WLTP/CLTC 标准，不得虚假宣传续航里程。*
