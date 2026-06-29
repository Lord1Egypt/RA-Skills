# 进阶主题：PFC / Flyback / LLC / 磁件

## 一、Boost PFC（功率因数校正）

### 何时使用
- 离线电源 >75W 常需 PF>0.9、THD<10%
- 在整流桥后加 Boost，输出 400V 母线（220V 输入）

### CRM/BCM 设计要点
- 电感：**L = Vin_peak² / (2·Po·fsw_min)**
- 最大占空比（线电压峰值）：**D_max = 1 − Vin_peak / Vo**
- Vo 必须 > √2·Vin_rms
- 开关频率随线电压/负载变化；轻载频率升高

### 与后级配合
- Vo=400V → LLC 或 Flyback 隔离
- 注意 Boost 右半平面零点 → 电流模式补偿

---

## 二、Flyback 反激（DCM）

### 设计流程
1. 定 Po、Vin 范围、Vo、fsw
2. 初选匝比 **n = Ns/Np**：n ≈ Vo·(1−D)/(Vin·D)，D 取 0.35~0.45
3. **D = n·Vo / (Vin + n·Vo)**
4. 励磁电感（DCM）：**Lm = Vin²·D²·T / (2·Pin)**
5. 峰值电流：**Ipk = Vin·D·T / Lm**
6. 开关电压：**Vds ≈ Vin + Vo/n**（加漏感尖峰 20~30%）

### 常见坑
- 漏感能量 → RC Snubber 或 RCD clamp
- 多输出：加权匝比，主输出反馈
- 变压器 AP 法选磁芯（见下）

---

## 三、LLC 谐振变换

### 谐振频率
**fr = 1 / (2π√(Lr·Cr))**

### FHA 增益（近似）
- **fn = fsw / fr**（归一化频率）
- **m = Lm / Lr**
- **Q = √(Lr/Cr) / Rac**，Rac = (8/π²)·n²·Vo²/Po

### 工作区域
| fn | 典型特性 |
|----|----------|
| fn < 1 | 低于谐振，升压，原边 ZVS 区 |
| fn = 1 | 谐振点，增益≈1 |
| fn > 1 | 高于谐振，降压，效率区 |

### 设计步骤
1. 定 fr 接近 fsw（如 fsw = 1.2·fr）
2. 选 Cr（nF 级）→ 算 Lr
3. 选 m = 5~10 → Lm = m·Lr
4. 用脚本校核增益是否覆盖 Vin 范围
5. **必须仿真/实验**验证 ZVS 与增益曲线

---

## 四、磁芯选型（AP 法简述）

**AP = Ae·Aw ≥ (2·Po·104) / (ΔB·f·Ku·J·1000)**（单位混合，工程估算）

| 参数 | 含义 |
|------|------|
| Ae | 有效截面积 (cm²) |
| Aw | 窗口面积 (cm²) |
| ΔB | 磁通摆幅 (T)，一般 0.2~0.35 |
| J | 电流密度 (A/mm²)，自然冷却 4~5 |
| Ku | 窗口填充系数 0.3~0.4 |

Flyback/Forward 用 AP 法；LLC 变压器注意 Lm 与 Lr 分离（气隙）。

---

## 五、软开关简述

| 类型 | 条件 | 典型拓扑 |
|------|------|----------|
| ZVS | 关断前 Vds→0 | LLC 原边、PSFB |
| ZCS | 关断前 I→0 | 谐振逆变、QR Flyback |
| CRM | 边界模式，fsw 可变 | PFC Boost、QR 反激 |

---

## 六、仿真建议

| 拓扑 | 推荐观察量 |
|------|------------|
| 整流 | Vd、Id、α 触发脉冲、断续边界 |
| 逆变 | 相电流、线电压 FFT、死区效应 |
| DC-DC | IL 波形、CCM/DCM 边界、Vds |
| LLC | 谐振电流、Vds ZVS、增益 vs fn |

不编造仿真数据；给参数与应观察波形特征。完整 Simulink 模块见 [simulink-templates.md](simulink-templates.md)。

---

## 七、QR Flyback（BCM）

- **Lm** = Vin_min² / (2·Pin·fsw_max)
- **fsw(Vin)** ≈ Vin² / Vin_min² · fsw_max
- **Ipk** = √(2·Pin / (Lm·fsw))
- ZCS 开通；注意 EMI 与最高频率限制

---

## 八、三相 NPC 三电平

- **Vl_peak** ≈ (√3/4)·Vdc·M
- 器件耐压 **Vdc/2**；中点电位需平衡
- 对比两电平 SVPWM：THD 更低、dv/dt 更小
