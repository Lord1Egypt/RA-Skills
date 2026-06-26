---
name: maxwell-fea-simulation
description: Maxwell 2D有限元仿真助手 | 用于无刷电机、永磁同步电机、磁路仿真，包含静磁场/瞬态仿真设置、边界条件、参数化扫描、结果提取。当需要进行Maxwell仿真建模、激励设置、求解分析、或提取仿真结果时触发。
---

# Maxwell 2D FEA 仿真助手

专注电机工程领域的 Maxwell 2D 仿真，覆盖静磁场、瞬态场、参数化扫描等典型仿真场景。

## 仿真类型与适用场景

| 仿真类型 | 求解器 | 适用场景 |
|----------|--------|----------|
| 静磁场（Magnetostatic） | Maxwell 2D | 永磁体工作点、气隙磁密、空载反电动势 |
| 瞬态场（Transient） | Maxwell 2D | 力矩特性、负载响应、齿槽转矩、纹波 |
| 涡流场（Eddy Current） | Maxwell 2D | 高速电机套筒损耗、制动盘 |
| 静电力场（Electrostatic） | Maxwell 2D | 电容传感器、静电电机 |

## 仿真建模标准流程

### 1. 几何建模

**常用参数（单位：mm）**

| 参数 | 说明 | 示例 |
|------|------|------|
| 定子外径 | Dso | 90 |
| 定子内径 | Dsi | 54 |
| 转子外径 | Dri | 53 |
| 转子内径 | Dri_shaft | 16 |
| 气隙长度 | g | 0.5 |
| 铁心长度 | L | 50 |
| 极数 | 2p | 8 |
| 槽数 | Q | 36 |

**建模原则**
- 优先使用 1/4 或 1/2 对称模型减少计算量
- 定子外圆和转子内圆建议加空气包域（边界层外扩≥20%模型尺寸）
- 斜槽：用多截面或斜极方式建模

### 2. 材料定义

**定子/转子铁心**

```
材料类型：Silicon Steel（硅钢片）
常用牌号：
  - 35YT310：B_H曲线 + 损耗曲线
  - M19_29Gauss：美标对应
  - DW310-35：国产牌号
设置项：BH曲线、层压方向（0°/90°叠压）、电导率
```

**永磁体**

```
材料类型：Nonlinear Magnetic（非线性磁性）
牌号：N42SH、N35UH、35EH 等
关键参数：
  - 剩磁 Br（T）：如 N42SH → Br≈1.25T
  - 矫顽力 Hc（kA/m）：如 N42SH → Hc≈955kA/m
  - 温度系数：Br温度系数约 -0.1%/℃
设置：各向异性充磁方向（Radial / Circumferential）
```

**铜线/绕组**

```
材料：Copper（退火铜）
电导率：5.8e7 S/m（20℃）
温度修正：每℃约 +0.4%
```

### 3. 边界条件

| 边界类型 | 设置方法 | 适用场景 |
|----------|----------|----------|
| Balloon边界 | Set balloon | 开放边界（默认） |
| Vector Potential = 0 | 主从边界副边界 | 周期对称模型 |
| 狄利克雷边界 | 指定 A=0 | 建模对称轴 |

**典型设置（1/4对称模型）**

```
上边界（α=0°）：Vector Potential = 0
右边界（r=R_max）：Balloon（或 A=0）
模型外空气包外圆：Balloon边界
```

### 4. 激励设置

**永磁体激励**

```
方法1：等效面电流
  面电流密度 Jc = Hc / δ（δ为等效厚度）

方法2：直接赋材料
  材料类型选永磁体牌号
  充磁方向：Radial（径向充磁）
    8极：每极充磁方向交替（NSNS...）
```

**绕组激励**

```
绕组类型：Stranded（绞线，忽略涡流）
匝数设置：每个线圈单元的串联匝数
电流赋值：瞬态场用随时间变化的电流表达式
  示例：I_phaseA = Imax * sin(2*pi*freq*time)
```

**绕组建模方式**

```
方案A：绕组 band 方式
  定子槽内画 coil 区域 → 赋电流密度 J = N*I/SlotArea
  槽内填充率（槽满率）通常 0.45~0.55

方案B：外电路耦合（External Circuit）
  定义绕组端子 → 连接 voltage source
  适合反电动势测试
```

### 5. 求解设置

**静磁场求解器**

```
求解类型：Magnetostatic
收敛标准：Energy Error < 0.001（或 0.0001 高精度）
自适应求解：开启， refinement per pass = 5
网格加密：永磁体/气隙区域加密
  气隙内侧：Maximum Length < 0.1mm
  磁钢区域：Maximum Length < 0.2mm
```

**瞬态场求解器**

```
时间步长：Tstep = 1/（freq × 360×P）/ 20
  8极电机 @ 3000rpm @ 50Hz → Tstep = 1/(50×360×4)/20 ≈ 0.00007s
  最小步长：建议 < 周期/180
求解时间：至少 1 个完整电周期
后处理：提取 T_N（力矩）和 EMF（反电动势）
```

**参数化扫描**

```
扫描变量：电流 I、角度 theta、永磁体厚度 hm、槽深 h
扫描方式：Optimetrics → 添加 Parametric Sweep
  变化范围：如 I = 0~20A，步长 2A
结果提取：Map Fields 或 Table
```

## 典型仿真案例

### 案例1：空载反电动势（静磁场）

```
目标：计算 8极36槽电机 3000rpm 时的空载反电动势
方法：静磁场 + 角度参数化

设置步骤：
1. 定义转子角度参数 theta（0°~360°，步长10°）
2. 设置静磁场求解
3. 提取气隙磁通密度 B(theta)
4. 后处理计算：E = N * dΦ/dt = N * ω * dΦ/dθ
5. 或用瞬态场直接测量线间电压波形
```

### 案例2：齿槽转矩（Cogging Torque）

```
目标：计算无电流激励下的齿槽转矩
方法：瞬态场，绕组开路

设置步骤：
1. 绕组电流设为 0（开路）
2. 转速设为额定转速（如 3000rpm）
3. 求解 1 个完整机械周期
4. 提取 Torque，转子角度为横坐标
结果：齿槽转矩峰值通常 1%~3% 额定转矩
```

### 案例3：额定力矩（瞬态场）

```
目标：计算 FOC 控制下的额定力矩
方法：瞬态场 + 外电路

设置步骤：
1. 定义 d轴电流 Id = 0 控制
2. q轴电流 Iq = 额定相电流峰值
3. 设置初始角度为 d轴对齐位置
4. 求解 1 个电周期后取平均值
```

## 网格质量评估

| 区域 | 建议网格尺寸 | 优先级 |
|------|------------|--------|
| 气隙 | ≤0.08mm | 最高 |
| 永磁体 | ≤0.15mm | 高 |
| 槽口/槽楔 | ≤0.1mm | 高 |
| 定子/转子轭部 | ≤0.5mm | 中 |
| 空气包外层 | ≤2mm | 低 |

**网格质量检查**
- 三角形单元（Default），三角形比例 Aspect Ratio < 3:1
- 禁用梯形单元（inaccurate）
- 气隙至少有 5 层单元

## 结果提取与后处理

**常用后处理量**

| 物理量 | 提取方法 | 单位 |
|--------|----------|------|
| 气隙磁密 Bg | 路径积分（B_vector） | T |
| 反电动势 E | Voltage_transient 探针 | V |
| 电磁转矩 T | Torque 探针 | N·m |
| 铁损 P_fe | Losses → Core Loss | W |
| 铜损 P_cu | I²R 计算 | W |
| 效率 η | P_out / (P_out + P_fe + P_cu) | % |

**力矩提取关键点**
- 瞬态场 Torque 探针放在转子区域
- 转矩脉动 = (T_max - T_min) / T_avg × 100%
- 关注 6k 次谐波（k=1,2,3...）

## 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 收敛困难 | 气隙网格太粗、边界条件错误 | 加密气隙网格至 <0.1mm |
| 力矩为负 | 电流方向错误 | 检查绕组相序 |
| 磁密过高 | 磁钢过厚/规格选错 | 核实 Br 和 Hc |
| 反电动势偏低 | 匝数不够/气隙过大 | 检查绕组连接和 N |
| 网格报错 | 模型有间隙/重叠 | 用 Audit 检查几何 |

## 参考脚本与资源

- `scripts/maxwell_simulation_checklist.py` - 仿真检查清单
- `scripts/maxwell_post_processor.py` - **仿真结果后处理脚本**（齿槽转矩、反电动势、气隙磁密、力矩转速分析）
- `references/material_library.md` - 常用材料参数库
- `references/mesh_guidelines.md` - 网格设置规范
- `references/simulation_templates.md` - **仿真参数配置模板库**（静磁场/瞬态场配置、求解器参数、Optimetrics 扫描）

### 快速使用 maxwell_post_processor.py

```bash
# 齿槽转矩分析（演示数据）
python scripts/maxwell_post_processor.py --mode cogging_torque --pole_pairs 4

# 反电动势谐波分析
python scripts/maxwell_post_processor.py --mode back_emf --fundamental_freq 200 --pole_pairs 4

# 气隙磁密分析
python scripts/maxwell_post_processor.py --mode air_gap_flux

# 力矩转速特性（给定电流矢量）
python scripts/maxwell_post_processor.py --mode torque_speed --pole_pairs 4

# 实际数据导入（CSV格式）
python scripts/maxwell_post_processor.py --mode cogging_torque \
    --file "torque_data.csv" --angle "angle_deg" --torque "torque_nm"
```

> **注意**：`maxwell_post_processor.py` 无需 Maxwell 软件，仅用于后处理 CSV/数组数据。
> 如需与 Maxwell 直接交互（建模、求解控制），需安装 `pyedb`（ANSYS Python API）。
