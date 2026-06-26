# Maxwell 2D 仿真参数配置模板库

## 1. 永磁同步电机（PMSM）静磁场仿真配置

### 几何参数模板（8极36槽）

```
定子外径 Dso  = 90 mm
定子内径 Dsi  = 54 mm
气隙直径 Dgap = 53 mm
转子外径 Dri  = 52.5 mm
转子内径 Dri_shaft = 16 mm
铁心长度 L    = 50 mm
极数 2p       = 8
槽数 Q        = 36
气隙长度 δ    = 0.5 mm
```

### 材料设置模板

**定子/转子铁心（35YT310）**
```
材料类型：Silicon Steel (Nonlinear B-H)
命名：35YT310
BH曲线关键点：
  B(T)   H(A/m)
  0.0    0
  0.5    100
  1.0    250
  1.5    500
  1.7    800
  1.8    1200
  1.9    2000
  2.0    3500
电导率：2.0e6 S/m（叠压方向）
层压系数：0.95
```

**永磁体（N42SH）**
```
材料类型：Nonlinear Magnetic / Hard B-H
命名：N42SH_NdFeB
剩磁 Br = 1.25 T
矫顽力 Hc = 955 kA/m
最大磁能积：(BH)max = 318 kJ/m³
温度系数：-0.11 %/℃
居里温度：80℃
各向异性：强
充磁方向：Radial（径向）
  8极：N-S-N-S-N-S-N-S（交替）
```

### 边界条件配置（1/4对称模型）

```
【上边界】theta = 0°
  Type: Vector Potential
  Value: A = 0

【右边界】r = R_max（外空气包外圆）
  Type: Balloon
  （无限元效果，无需设值）

【斜边界】45°对称线
  Type: Master/Slave（主从边界）
  Master边界：指定角度 = 0°
  Slave边界：自动对齐

【模型外空气包】
  外扩尺寸：≥20% 模型最大尺寸
  网格：默认三角形，Maximum Length ≤ 2mm
```

### 求解器参数模板

**静磁场求解**
```
Solver: Maxwell 2D → Magnetostatic
收敛标准：Energy Error < 0.001（高精度）
自适应求解：开启
  Refinement per pass: 5
  Number of passes: 10
  Convergence tolerance: 1%
网格加密区域：
  气隙：Maximum Length < 0.08 mm
  永磁体：Maximum Length < 0.15 mm
  定子槽口：Maximum Length < 0.1 mm
  轭部：Maximum Length < 0.5 mm
```

**瞬态场求解**
```
Solver: Maxwell 2D → Transient
时间步长设置：
  Tstep = 1 / (freq × P × 20)
  示例：8极50Hz → Tstep = 1/(50×4×20) = 0.00025s
  总求解时间：1个完整电周期 = 1/f_elec = 0.02s @ 50Hz
  所以时间步数：0.02/0.00025 = 80步

初始角度设置：
  theta_init = 0°（d轴对齐位置）
  或通过外电路 initial conditions 设置

转速设置：
  机械转速 ω_m = 2π × n / 60 rad/s
  示例：n=3000rpm → ω_m = 314 rad/s
```

## 2. 分数槽集中绕组（6极9槽）仿真配置

```
几何：
  定子外径 Dso = 50 mm
  定子内径 Dsi = 30 mm
  极数 2p = 6
  槽数 Q = 9
  q = 9/(6×3) = 0.5（分数槽集中绕组）

特点：
  - 绕组端部短，铜损低
  - 齿槽转矩大，需斜槽/斜极
  - 适合低速大转矩应用

建模注意：
  每相串联匝数 Nph = 每槽匝数 × 槽数/相数
  短距系数 = 1（集中绕组默认整距）
  分布系数：q=0.5 → kd = 0.966
```

## 3. 永磁体工作点扫描（Optimetrics）

```
扫描变量：永磁体厚度 hm
扫描范围：2mm ~ 5mm，步长 0.5mm
提取量：
  - 气隙磁密 Bg (theta=0°)
  - 平均转矩 T_avg
  - 齿槽转矩 T_cog

目标：
  找到 Bg=0.8T 对应的最小 hm
  （满足磁性能 + 成本最小化）
```

## 4. 典型网格加密方案

### 气隙网格（最关键）

```
气隙区域：0.5mm，分5层加密
  方案A：Inside Region 加密
    Maxwell 2D → Mesh Operations → Inside Selection
    物体：气隙圆环区域
    Maximum Length：0.08 mm
    
  方案B：长度控制（更精确）
    每层厚度：0.1mm
    共5层覆盖0.5mm气隙
```

### 永磁体网格

```
Maximum Length：0.15 mm
（确保一个极距内 ≥ 10 个单元）
对 N42SH 以上牌号尤其重要（高 Br 易饱和）
```

### 轭部网格

```
定子轭部：Maximum Length ≤ 0.5 mm
（避免轭部磁通积分误差）
转子轭部：Maximum Length ≤ 0.3 mm
（高转速转子需更密）
```

## 5. 反电动势提取后处理

### 方法A：静磁场角度参数化

```
1. 定义参数：theta = 0°~360°，步长10°
2. 每个角度做一次静磁场求解
3. 提取气隙中心路径 B(theta)
4. 后处理计算：
   Phi(theta) = ∫ B(r,theta) dA
   E_phase = Nph × dPhi/dt
          = Nph × ω × dPhi/dθ

Python 计算脚本：
  import numpy as np
  theta = np.linspace(0, 2*np.pi, 37)
  Phi = ... # 从 Maxwell 导出
  Ke = np.trapz(Phi, theta) / (2*np.pi) × ω × Nph
```

### 方法B：瞬态场电压探针

```
1. 在绕组端子插入 Voltage_Probe
2. 设置 Probe：线间电压或相电压
3. 求解后查看 Voltage - Time 曲线
4. 用FFT分析谐波含量
```

## 6. 损耗提取

### 铁损计算

```
Core Loss 模型开启：
  硅钢片损耗系数（35YT310）：
    Kh = 0.032（磁滞损耗系数）
    Kc = 0.00024（涡流损耗系数）
    Ke = 0（附加损耗）
  频率：f = freq × np（电气频率）

提取方式：
  Maxwell → Results → Loss Reports → Core Loss
  单位：W/kg 或 总W
```

### 铜损计算

```
方法：后处理公式
  P_cu = 3 × I_rms² × R_phase
  
其中 R_phase 需要：
  1. 材料电导率设置正确（Copper, σ=5.8e7 S/m）
  2. 绕组区域体积准确
  3. 或直接用万用表测量
  
集肤效应（高频）：
  @ 1kHz：等效电阻增加约 5%
  @ 10kHz：等效电阻增加约 50%
```

## 7. 常用检查清单

```
□ 几何无重叠/间隙（Tools → Audit）
□ 材料 BH 曲线覆盖工作点（检查 B<2.0T 区域）
□ 气隙网格 < 0.1mm（否则收敛差）
□ 边界条件正确（对称模型不要漏 Balloon）
□ 永磁体充磁方向正确（8极交替）
□ 求解器收敛（Energy Error < 0.001）
□ 结果合理性检查（Bg < 1.3T, T 在预期范围）
```
