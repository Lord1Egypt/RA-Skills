---
name: power-electronics
description: 电力电子技术专家——四大变换 AC-DC/DC-AC/DC-DC/AC-AC。整流/PFC、SPWM/SVPWM/NPC三电平、Buck/Boost/Flyback/QR/LLC、相控/斩波。含 Simulink 仿真模板与 ClawHub 可发布。触发词：电力电子、NPC、QR反激、Simulink、PFC、SVPWM。
version: 1.3.0
triggers:
  - "电力电子"
  - "四大变换"
  - "PFC"
  - "Flyback"
  - "QR"
  - "LLC"
  - "NPC"
  - "三电平"
  - "Simulink"
  - "整流"
  - "逆变"
  - "SVPWM"
  - "Buck"
  - "Boost"
tools:
  - bash
  - read
  - write
config:
  default_fsw_khz:
    type: number
    default: 100
    description: "DC-DC 默认开关频率 (kHz)"
  ripple_ratio:
    type: number
    default: 0.3
    description: "CCM 电感纹波比"
  cap_ripple_ratio:
    type: number
    default: 0.01
    description: "输出电容纹波比"
  mains_freq_hz:
    type: number
    default: 50
    description: "工频 (Hz)"
---

# 电力电子技术 Skill v1.3

四大变换 + 进阶拓扑 + Simulink 仿真指导。流程：识别类型 → 脚本验证 → 手算 → 结构化输出。

## 资源索引

| 文件 | 用途 |
|------|------|
| [four-conversions.md](references/four-conversions.md) | 四大变换总览 |
| [formulas.md](references/formulas.md) | 公式速查 |
| [topologies.md](references/topologies.md) | 拓扑选型 |
| [advanced.md](references/advanced.md) | PFC/Flyback/LLC/QR |
| [examples.md](references/examples.md) | 典型例题 |
| [simulink-templates.md](references/simulink-templates.md) | **Simulink 模块与参数** |
| [PUBLISHING.md](PUBLISHING.md) | ClawHub 发布指南 |

---

## 脚本速查 `scripts/power_calc.py`

### 新增 v1.3

| 命令 | 功能 |
|------|------|
| `--topology flyback-qr` | QR/BCM 反激 Lm、频率范围、Ipk |
| `--topology three-phase-npc` | NPC 三电平线/相电压、器件 Vdc/2 应力 |
| 仿真请求 | 读 [simulink-templates.md](references/simulink-templates.md) |

```bash
# QR 反激：90~264V 输入，12V/2A，最高 100kHz
python scripts/power_calc.py --transform dc-dc --topology flyback-qr --vin-min 90 --vin-max 264 --vo 12 --io 2 --fsw-max 100 --n-ratio 0.15

# 三相 NPC 三电平
python scripts/power_calc.py --transform dc-ac --topology three-phase-npc --vdc 600 --m 0.9

# 其余命令见 v1.2（整流/PFC/LLC/SVPWM 等）
```

### DC-AC topology 列表

`single-h-bridge-spwm` | `three-phase-spwm` | `three-phase-svpwm` | **`three-phase-npc`**

### DC-DC topology 列表

`buck` | `boost` | `buck-boost` | `flyback` | **`flyback-qr`** | `llc`

---

## 分主题要点

### QR Flyback
- 边界模式：每周期 demagnetize 完毕 → 开关损耗低
- 设计：Vin_min + 满载 @ fsw_max → **Lm = Vin_min²/(2·Pin·fsw_max)**
- **fsw ∝ Vin²**；轻载频率更高，需 EMI 滤波
- 脚本：`flyback-qr` + `--vin-min` `--vin-max` `--fsw-max`

### 三相 NPC 逆变
- 直流侧两电容分压，**器件耐压 Vdc/2**
- 相电压 3 电平，线电压 5 电平
- 线电压基波峰值（线性）：**Vl_peak ≈ (√3/4)·Vdc·M**
- 必须中点电位平衡；Simulink 见模板 §3

### Simulink 仿真
- 用户要仿真 → **打开 simulink-templates.md 对应章节**
- 给模块清单、参数表、观测点、报告模板
- **禁止编造波形数值**；可给预期量级与手算对比

---

## 输出格式

```markdown
## 问题复述
## 变换类型与拓扑
## 计算过程
## 结果汇总
## 器件应力
## 工程建议
## Simulink 建议（如适用，引用模板章节）
## 易错提醒
```

---

## 检查清单

- QR：Vin_min/Vin_max 与 fsw 范围
- NPC：Vdc/2 应力 vs 两电平 Vdc；中点平衡
- Simulink：solver 步长、powergui、死区
- 发布：见 [PUBLISHING.md](PUBLISHING.md)
