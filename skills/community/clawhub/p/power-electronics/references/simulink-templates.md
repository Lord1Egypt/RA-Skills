# Simulink / Simscape 仿真模板

用户请求仿真时：**读取本文件对应拓扑**，给出模块清单、参数设置与观测点。不编造仿真波形数值。

---

## 通用设置

| 项 | 推荐 |
|----|------|
| 求解器 | ode23tb 或 discrete (powergui) |
| 步长 | Ts = 1/(50·fsw) ~ 1/(100·fsw) |
| powergui | 连续 → 离散化时设 Sample time |

---

## 1. Buck 斩波器（DC-DC）

### 模块清单

```
Vin (DC Source) → Switch (MOSFET/IGBT) → L → C → Rload
                      ↓
                   Diode (Freewheeling, 阴极接 Vin-)
PWM Generator → Switch gate
Voltage Measurement: Vo, IL (Series RLC branch 测电流)
```

### 参数示例（48V→12V/5A）

| 模块 | 参数 |
|------|------|
| Vin | 48 V |
| Switch | Ron=0.01, Rs=1e6, Cs=inf |
| Diode | Ron=0.01, Vf=0.8 |
| L | 47e-6 H，R=0.01 |
| C | 220e-6 F，ESR=0.05 |
| Rload | 12/5 = 2.4 Ω |
| PWM | f=100e3 Hz，D=0.25 |

### 观测
- IL 纹波三角波（CCM）
- Vo 稳态 ≈ 12V
- 开关 Vds 关断时 ≈ Vin

---

## 2. 三相两电平逆变 + SVPWM（DC-AC）

### 模块清单

```
Vdc (DC Source) → Universal Bridge (3 arms, 6 switches)
                 → Three-Phase Series RLC Load (Y 或 Δ)
SVPWM 子系统 / Repeating Sequence → 6 路 PWM
```

### SVPWM 子系统要点
- 输入：Vdc, M, fo, fsw
-  Clarke 变换得 Vα, Vβ → 扇区 1~6
- 计算 T1, T2, T0 → 七段式占空比
- 或使用 MATLAB Function：`svpwm(vdc, m, theta)`

### 参数示例

| 模块 | 参数 |
|------|------|
| Vdc | 600 V |
| Bridge | Ron=0.001, Snubber off |
| Load | R=10Ω, L=5mH（Y） |
| fo | 50 Hz |
| fsw | 10 kHz |
| M | 0.85 |

### 观测
- 线电压 Vab 五电平近似正弦（两电平时为 PWM 方波包络）
- FFT：基波 50Hz，开关频率边带
- 死区：可选 2~5μs 插入互补 PWM

---

## 3. 三相 NPC 三电平逆变（DC-AC）

### 模块清单

```
Vdc → 2× 电容分压 (各 Vdc/2) → Neutral point N
每相桥臂：4 开关 + 2 钳位二极管 (T 型 / I 型 NPC)
Three-Phase Load (Y 接，中性点可选接 N)
NPC SVM 调制子系统（61 矢量或简化三电平 SVM）
中点平衡：注入零序 / 冗余状态选择
```

### 与两电平差异

| 项 | 两电平 | NPC |
|----|--------|-----|
| 器件耐压 | Vdc | Vdc/2 |
| 相电压电平 | 2 | 3 |
| 线电压电平 | 3 | 5 |
| 中点电位 | 无 | 需平衡控制 |

### 参数示例

| 模块 | 参数 |
|------|------|
| Vdc | 600 V（每电容 300V） |
| fo | 50 Hz, M=0.9 |
| 负载 | 电机或 R-L |

### 观测
- 相电压 三电平阶梯
- 中点电流 i_np：长期平均应 ≈ 0
- 器件 Vds 应力 ≈ Vdc/2

脚本校核：
```bash
python scripts/power_calc.py --transform dc-ac --topology three-phase-npc --vdc 600 --m 0.9
```

---

## 4. 单相全控桥整流（AC-DC）

### 模块清单

```
AC Source (220V, 50Hz) → Universal Bridge (2 脉冲/4 晶闸管)
                      → Series RLC (L 平波 + R 负载)
                      → Voltage/Current Measurement
Pulse Generator (Thyristor) ×2：相位差 180°，触发角 α
```

### 参数示例

| 模块 | 参数 |
|------|------|
| AC | 220V RMS, 50Hz |
| α | 30° → Pulse delay = α/(360°×T) |
| L | 10mH（保证连续） |
| R | 2Ω |

### 观测
- Vd 平均 ≈ 0.9×220×cos30° ≈ 171V（单相）
- 触发脉冲与导通角
- α 小于 α_crit 时出现断续

---

## 5. QR Flyback（DC-DC 隔离）

Simulink 完整 Flyback 需自定义变压器；简化用**受控源 + 理想变压器**：

```
Vin → Switch → Lm (magnetizing) → Ideal Transformer (Np:Ns)
              → Secondary Diode → Cout → Rload
QR 控制：检测 demagnetization (Vds 尖峰/辅助绕组) → 恒 ton 或恒 Ipk 关断
Variable fsw：Scope 记录开关周期
```

### 参数
- Vin: 90~264V（用阶跃或扫频输入测试 QR 频率变化）
- fsw_max 设计点：100kHz @ 90V 满载

```bash
python scripts/power_calc.py --transform dc-dc --topology flyback-qr --vin-min 90 --vin-max 264 --vo 12 --io 2 --fsw-max 100 --n-ratio 0.15
```

---

## 6. Simscape 替代路径

若用 **Simscape Electrical**：
- `MOSFET` / `IGBT` + `Diode` 替代 Universal Bridge
- `Inductor`, `Capacitor`, `Resistor` 带寄生参数
- `Controlled PWM Voltage` 驱动栅极

---

## 7. 报告模板（仿真作业）

```markdown
## 仿真模型
- 拓扑 + Simulink 版本
- 主要模块截图说明

## 参数表
[与上文一致]

## 波形
- 截图：Vo/IL/触发脉冲/线电压 FFT
- 测量值 vs 手算误差

## 结论
- CCM/DCM、调制比、THD、应力是否满足
```

Agent 输出仿真指导时引用本节，**不提供虚假数值曲线**。
