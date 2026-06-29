# 典型例题（四大变换）

Agent 遇到类似题型时，按步骤求解并调用脚本验证。

---

## AC-DC

### 例1：三相全控桥
**题**：相电压 U2=220V，α=30°，阻感负载 Id=10A 连续。求 Vd、Pd。

**解**：
- Vd = 2.34·U2·cos30° = 2.34×220×0.866 = **445.7 V**
- Pd = Vd·Id = **4457 W**

```bash
python scripts/power_calc.py --transform ac-dc --topology three-bridge-controlled --u2 220 --alpha 30 --io 10
```

### 例2：阻感负载临界角
**题**：U2=220V，R=2Ω，L=10mH，α=30°，判电流是否连续。

**解**：
- α_crit = arctan(ωL/R) = arctan(2π×50×0.01/2) ≈ **57.5°**
- α=30° < α_crit → **电流断续**，不能用 Vd=0.9U2cosα

```bash
python scripts/power_calc.py --transform ac-dc --topology single-bridge-rl --u2 220 --alpha 30 --r 2 --l-mh 10
```

### 例3：Boost PFC
**题**：220V 输入，400V 母线，300W，最低开关频率 40kHz。求 CRM 电感。

```bash
python scripts/power_calc.py --transform ac-dc --topology boost-pfc --u2 220 --vo 400 --po 300 --fsw 40
```

---

## DC-AC

### 例4：三相 SVPWM
**题**：Vdc=600V，M=0.85，求线电压基波有效值；θ=45° 时扇区与时间。

**解**：
- Vl_peak = (√3/3)·600·0.85 = 294.5 V
- Vl_rms = 294.5/√2 = **208.2 V**

```bash
python scripts/power_calc.py --transform dc-ac --topology three-phase-svpwm --vdc 600 --m 0.85 --theta 45 --fsw 10
```

### 例5：单相 SPWM
**题**：Vdc=311V，M=0.9，求输出基波有效值。

**解**：Vo1_peak = 0.9×311/2 = 139.95 V → Vo1_rms = **98.9 V**

---

## DC-DC

### 例6：Buck 设计
**题**：48V→12V/5A，fsw=100kHz，纹波 k=0.3。求 D、L、C。

```bash
python scripts/power_calc.py --transform dc-dc --topology buck --vin 48 --vo 12 --io 5 --fsw 100
```

### 例7：Buck DCM 判定
**题**：Vin=48V，Vo=12V，L=10μH，Io=5A，fsw=100kHz，判 CCM/DCM。

```bash
python scripts/power_calc.py --transform dc-dc --topology buck --vin 48 --vo 12 --io 5 --fsw 100 --mode analyze --l 10
```

### 例8：Flyback 设计
**题**：Vin=24V，Vo=12V/2A，Ns/Np=0.5，fsw=100kHz，η=0.85。

```bash
python scripts/power_calc.py --transform dc-dc --topology flyback --vin 24 --vo 12 --io 2 --fsw 100 --n-ratio 0.5
```

### 例9：LLC 参数校核
**题**：Vin=400V，Vo=12V，Po=120W，Lr=5μH，Cr=100nF，Lm=50μH，fsw=100kHz，n=0.03。

```bash
python scripts/power_calc.py --transform dc-dc --topology llc --vin 400 --vo 12 --po 120 --lr 5 --cr 100 --lm 50 --fsw 100 --n-ratio 0.03
```

---

## AC-AC

### 例10：相控调压
**题**：220V，α=60°，求输出有效值。

**解**：Vo = 220·√[(π−π/3+sin120°/2)/π] ≈ **197.3 V**

```bash
python scripts/power_calc.py --transform ac-ac --topology single-phase-control --u2 220 --alpha 60
```

### 例11：交流斩波
**题**：220V，D=0.6，求 Vo_rms。

**解**：Vo = 220·√0.6 = **170.5 V**

---

## 综合

### 例12：功率因数
**题**：全控桥 α=45°，求位移功率因数。

**解**：PF ≈ cos45° = **0.707**

```bash
python scripts/power_calc.py --transform ac-dc --topology rectifier-pf --alpha 45
```

---

## v1.3 新增

### 例13：QR Flyback
**题**：宽输入 90~264V，12V/2A，Ns/Np=0.15，fsw_max=100kHz。

```bash
python scripts/power_calc.py --transform dc-dc --topology flyback-qr --vin-min 90 --vin-max 264 --vo 12 --io 2 --fsw-max 100 --n-ratio 0.15
```

### 例14：三相 NPC
**题**：Vdc=600V，M=0.9，求线电压基波有效值及器件耐压。

**解**：Vl_peak=(√3/4)·600·0.9≈234.6V → Vl_rms≈**165.9V**；器件 **300V**

```bash
python scripts/power_calc.py --transform dc-ac --topology three-phase-npc --vdc 600 --m 0.9
```

### 例15：Simulink 三相逆变
**题**：搭建 SVPWM 三相逆变模型。

→ 打开 [simulink-templates.md §2](simulink-templates.md)，按模块清单搭建，fo=50Hz，fsw=10kHz。
