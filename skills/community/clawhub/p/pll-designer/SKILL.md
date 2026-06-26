---
name: pll-bandwidth-calc
description: 锁相环（PLL）PI 控制器参数计算工具。用于电力电子/新能源领域的锁相环设计与调试。支持两种计算方向：(1) 根据目标带宽和阻尼比正向计算 PI 参数（KPLLp/KPLLi）；(2) 根据已知 PI 标幺值参数反推闭环带宽和阻尼比。当用户提到"锁相环"、"PLL"、"PLL带宽"、"PI参数"、"KPLLp"、"KPLLi"、"阻尼比"、"自然频率"等关键词时触发。
---

# PLL 带宽计算工具

基于二阶系统理论的锁相环 PI 控制器参数设计与分析工具。

## 系统模型说明

本工具基于以下 SRF-PLL（同步旋转坐标系锁相环）线性化模型：

- 开环传递函数：`G(s) = U_mag * (Kp*s + Ki) / s^2`
- 闭环特征方程：`s^2 + U_mag*Kp*s + U_mag*Ki = 0`
- 自然角频率：`wn = sqrt(U_mag * Ki)`
- 阻尼比：`zeta = U_mag*Kp / (2*wn)`
- 带宽扩展系数：`C = sqrt(1 + 2*zeta^2 + sqrt(2 + 4*zeta^2 + 4*zeta^4))`
- 闭环带宽：`f_BW = wn * C / (2*pi)`

其中 `U_mag = Unom/sqrt(3)*sqrt(2)` 为相电压峰值（前馈解耦项）。

## 标幺值换算

物理值与标幺值的换算关系（基准值 = 额定角频率 / 相电压峰值）：

```
KPLLp_pu = KPLLp * U_mag / w0
KPLLi_pu = KPLLi * U_mag / w0
```

其中 `w0 = 2*pi*f0`。

## ⚠️ 交互规则（必须遵守）

**在执行任何计算之前，若用户未明确提供以下参数，必须主动询问，不得使用默认值静默计算：**

1. **`Unom`（线电压有效值，V）** — 必问，不同电压等级结果差异显著
   - 常见值：690V（风电变流器）、380V（工业低压）、10kV/35kV（中压）等
   - 询问示例："请问您的系统线电压有效值是多少 V？（如 690V、380V 等）"

2. **`f_BW_target`（目标带宽，Hz）** — 正向设计时必问（若未提供）

3. **`KPLLp_pu` / `KPLLi_pu`** — 反向分析时必问（若未提供）

以下参数有合理默认值，**用户未提供时可直接使用，但需在结果中注明**：
- `f0 = 50 Hz`（电网频率，中国/欧洲标准）
- `zeta = 0.707`（最优阻尼比）

## 使用方式

### 方向一：正向设计（目标带宽 → PI 参数）

用户提供目标带宽，可选提供电压、频率、阻尼比，计算 PI 参数。

**调用 MATLAB 函数：**
```matlab
[KPLLp_pu, KPLLi_pu, KPLLp, KPLLi] = get_pll_pi_parameters(f_BW_target)
[KPLLp_pu, KPLLi_pu, KPLLp, KPLLi] = get_pll_pi_parameters(f_BW_target, Unom, f0, zeta)
```

**典型示例：**
```matlab
% 目标带宽 20Hz，默认 690V/50Hz/zeta=0.707
[Kp_pu, Ki_pu, Kp, Ki] = get_pll_pi_parameters(20)

% 自定义参数
[Kp_pu, Ki_pu, Kp, Ki] = get_pll_pi_parameters(30, 380, 50, 0.707)
```

### 方向二：反向分析（PI 参数 → 带宽/阻尼比）

用户提供已知的 PI 标幺值参数，反推带宽和阻尼比。

**调用 MATLAB 函数：**
```matlab
[f_BW, zeta, wn, KPLLp, KPLLi] = calc_pll_bandwidth(KPLLp_pu, KPLLi_pu)
[f_BW, zeta, wn, KPLLp, KPLLi] = calc_pll_bandwidth(KPLLp_pu, KPLLi_pu, Unom, f0)
```

**典型示例：**
```matlab
% 已知标幺值参数，默认 690V/50Hz
[f_BW, zeta, wn, Kp, Ki] = calc_pll_bandwidth(0.05, 0.8)
```

## MATLAB 脚本文件

- `scripts/get_pll_pi_parameters.m` — 正向设计函数
- `scripts/calc_pll_bandwidth.m` — 反向分析函数

## 默认参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| Unom | 690 V | 电网线电压有效值（风电变流器典型值） |
| f0 | 50 Hz | 电网额定基波频率 |
| zeta | 0.707 | 阻尼比（临界阻尼，最优响应） |

## 直接计算（无需 MATLAB）

当用户只需要数值结果时，可直接用以下公式计算，无需运行 MATLAB：

**正向（已知 f_BW_target, zeta）：**
1. `C = sqrt(1 + 2*zeta^2 + sqrt(2 + 4*zeta^2 + 4*zeta^4))`
2. `wn = 2*pi*f_BW_target / C`
3. `U_mag = Unom/sqrt(3)*sqrt(2)`
4. `KPLLp = 2*zeta*wn / U_mag`
5. `KPLLi = wn^2 / U_mag`
6. `KPLLp_pu = KPLLp * U_mag / (2*pi*f0)`
7. `KPLLi_pu = KPLLi * U_mag / (2*pi*f0)`

**反向（已知 KPLLp_pu, KPLLi_pu）：**
1. `U_mag = Unom/sqrt(3)*sqrt(2)`, `w0 = 2*pi*f0`
2. `KPLLp = KPLLp_pu * w0 / U_mag`
3. `KPLLi = KPLLi_pu * w0 / U_mag`
4. `wn = sqrt(U_mag * KPLLi)`
5. `zeta = U_mag*KPLLp / (2*wn)`
6. `C = sqrt(1 + 2*zeta^2 + sqrt(2 + 4*zeta^2 + 4*zeta^4))`
7. `f_BW = wn*C / (2*pi)`
