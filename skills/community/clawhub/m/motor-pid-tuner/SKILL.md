---
name: motor-pid-tuner
version: 1.1.0
display_name: 电机PID调参器
display_name_en: Motor PID Tuner
description_zh: 输入电机参数，算出FOC电流环/速度环/位置环PI参数并给调参诊断：震荡、超调、稳态误差怎么破，29种模式含参数辨识、阶跃仿真、稳定性裕度、保护阈值，支持STM32/GD32/C2000代码生成。
description_en: PI/PID tuning and diagnostics for motor FOC current/speed/position loops with 29 modes covering parameter identification, step response, stability margins, protection thresholds, Q-format quantization and code generation for STM32/GD32/C2000.
description: 电机控制PID/PI参数计算与调参诊断工具。当用户需要计算电机FOC电流环/速度环/位置环PI参数、PID调参、电机控制参数整定、PID参数不知道怎么定、电机转起来抖动/震荡/嗡嗡响排查、电机响应慢/超调大、电机控制入门、Ziegler-Nichols调参、电机参数辨识、PID代码生成、调参故障诊断（震荡/超调/稳态误差）、阶跃响应仿真、参数灵敏度分析、离散化方法对比、弱磁控制参数、观测器增益计算、电机参数库查询、带宽自动建议、MATLAB导出、SVPWM代码生成、多平台适配（STM32/GD32/C2000）、参数反算、抗积分饱和（anti-windup）、死区补偿、多采样率控制、稳定性裕度分析（相位裕度/幅值裕度）、参数合理性校验、故障保护阈值（过流/过压/过温/堵转/I2t）、温度补偿（Rs/磁链温漂）、无感启动策略（I/F开环/高频注入）时使用。覆盖PMSM/BLDC/有刷直流电机的PI/PID控制器设计。
author: fangcun
---


# Motor PID Tuner 1.1.0

> **Update**: new "30-second start" — a tested command path from the built-in motor preset library to one-shot three-loop calculation, so new users no longer need to digest the 29-mode table.

> **Update**: `report_gen.py --format html` is live — a single-file HTML tuning report (embedded SVG step-response curves, three-loop parameter cards, protection thresholds, color-coded validation), ready to share or archive.

> **Update**: all fallback error messages localized with self-service troubleshooting hints (`python main.py <mode> --help`); frontmatter version aligned across the suite.

> **Update**: fixed a misleading warning in validate mode when parameters are incomplete; added positional-loop discrete-domain Kd note.

## When to Use It

- **Motor parameters in hand, no idea how to start PID**: give Rs/Ls/J/Kt and the desired bandwidth, get all three FOC loops (current/speed/position) as PI/PID in continuous, discrete and Q-format — no formula digging.
- **Oscillation / overshoot / steady-state error while tuning**: describe the symptom, get a diagnosis and countermeasures (which way to move Kp/Ki, whether anti-windup is needed).
- **Need a tuning report to share**: `--format html` generates a visual report in one shot — parameters + curves + protection thresholds + advice on one page.
- **Pre-production protection and validation**: overcurrent/overvoltage/overtemperature/stall thresholds, parameter sanity checks, temperature sensitivity.

Computes FOC three-loop (current/speed/position) PI/PID gains from motor physics and desired bandwidth. 29 work modes in `main.py` plus a standalone report generator (`report_gen.py`), covering the full flow from gain calculation to code generation, production protection to sensorless startup.

> **Invocation**: `python main.py --mode <mode> [args...]` — mode names are `current`/`speed`/`position` etc. (not `current_loop`). Reports use the separate script `python report_gen.py`.

## 30-Second Start

Not sure where parameters come from? Use the built-in preset library, then compute in one shot (all commands tested):

```bash
# 1) List 10 built-in common motor presets (2207/2804/5010/6354/8318 etc.)
python main.py --mode preset

# 2) Get one motor's full parameters (psi_f / J auto-derived)
python main.py --mode preset --preset-name 2207-1500KV

# 3) All three loops at once: feed the parameters in (--bw is the current-loop bandwidth;
#    speed/position loops auto-scale at 10:1:0.1)
python main.py --mode all --rs 0.052 --ls 0.0000085 --j 0.001 --kt 0.0065 --psi-f 0.00061905 --pole-pairs 7 --bw 1000 --vbus 12 --imax 20
```

Step 3 outputs: three-loop Kp/Ki/Kd (continuous + discrete), bandwidth-ratio check, Q-format C macros, feedforward coefficients. Current loop only is even simpler: `python main.py --mode current --rs 0.052 --ls 0.0000085 --bw 1000` — three args.

## Workflow

### 1. Identify the user need

Typical asks: "compute current-loop PI" / "how to tune the speed loop" / "position PD"; "Rs=0.5 Ls=2mH, 1kHz bandwidth"; "motor keeps oscillating" / "overshoot too big"; "Ziegler-Nichols"; "generate PID / STM32 / full FOC code"; "Q-format fixed point, MCSDK style"; "feedforward" / "cross-coupling decoupling"; "simulate step response"; "Rs +30% with temperature — impact?"; "forward Euler vs Tustin"; "field weakening"; "sensorless observer gains (SMO)"; "PWM 20kHz — what bandwidth"; "export MATLAB"; "SVPWM code"; "anti-windup" / "integrator runaway"; "dead-time compensation"; "multi-rate loops"; "phase/gain margin, Bode"; "sanity check my parameters"; "overcurrent/stall/I2t protection"; "temperature compensation"; "I/F start, HFI, zero-speed"; "GD32/TI C2000 adaptation"; "reverse-compute bandwidth from Kp/Ki"; "walk me through the inputs".

### 2. Interactive guidance

When the user is unsure which parameters are needed, use `--mode interactive --target <loop>` to get the required-parameter list, then ask one by one. Friendlier than demanding everything at once.

### 3. Collect parameters

Gather what the need dictates; ask for missing critical parameters. Also available: `--mode preset` (motor library), `--mode suggest-bw --pwm-freq <kHz>` (auto bandwidth advice).

**⚠️ CLI argument mapping (read before calling)**: symbols below (Rs/Ls/J/Kt...) are physics notation; actual `main.py` CLI args are **all lowercase**. Never pass uppercase notation as CLI args:

| Symbol | CLI arg | Unit |
|---|---|---|
| Rs | `--rs` | ohm |
| Ls | `--ls` | H (convert mH to H) |
| J | `--j` | kg*m^2 |
| B | `--b` | N*m*s/rad |
| Kt | `--kt` | N*m/A |
| bandwidth | `--bw` | Hz |
| bus voltage | `--vbus` | V |
| max current | `--imax` | A |
| flux psi_f | `--psi-f` | Wb |
| pole pairs | `--pole-pairs` | pairs |
| sample period | `--ts` | s |
| damping | `--zeta` | - |

**all-mode bandwidth scaling**: with `--mode all`, `--bw` is the **current-loop** bandwidth; speed loop auto-scales to 1/10 and position loop to 1/100 (built-in 10:1:0.1 ratio; override via `--speed-ratio` / `--pos-ratio`). Computing speed/position loops standalone: give their own bandwidth (speed typically 50-200 Hz).

**Current-loop PI needs**: Rs (stator resistance, ohm), Ls (stator inductance, H — mind the mH conversion), bandwidth (typically 500-2000 Hz).

**Speed-loop PI needs**: J (inertia), B (friction, 0 if unknown), Kt (torque constant), bandwidth (typically 50-200 Hz), zeta (default 0.707; 1.0 for critical damping).

**Position-loop PD/PID needs**: J, Kt (as above), bandwidth (typically 10-50 Hz), zeta (default 0.707).

**Ziegler-Nichols needs**: Kc (critical gain), Tc (oscillation period, s), controller type P/PI.

**Tuning diagnosis needs**: symptom description (oscillation/overshoot/slow/steady-state error/noise) plus current gains if any.

### 4. Run the calculator

After collecting parameters, call `main.py`:

```bash
python main.py --mode <mode> [args...]
```

**Modes (29):**

| Group | mode | Function |
|-------|------|----------|
| Core | `current` | current-loop PI |
| Core | `speed` | speed-loop PI |
| Core | `position` | position-loop PID |
| Core | `zn` | Ziegler-Nichols |
| Core | `all` | three loops + Q-format + feedforward |
| Diagnose | `diagnose` | tuning diagnosis (5 symptom classes) |
| Fixed-point | `qformat` | Q-format conversion (MCSDK-style) |
| Feedforward | `feedforward` | FF compensation parameters |
| Codegen | `code` | single-loop / full C code |
| Simulate | `simulate` | step-response simulation |
| Analysis | `sensitivity` | parameter sensitivity |
| Analysis | `discretize` | discretization method comparison |
| Advanced | `fieldweak` | field-weakening parameters |
| Advanced | `observer` | observer gains (SMO/Luenberger) |
| Utility | `preset` | motor parameter library |
| Utility | `suggest-bw` | bandwidth suggestion |
| Export | `export` | MATLAB export |
| Code | `svpwm` | full 7-segment SVPWM code |
| Code | `platform` | multi-platform (STM32/GD32/C2000) |
| Interactive | `interactive` | guided parameter entry |
| Reverse | `reverse` | gains to bandwidth/damping |
| Production | `antiwindup` | anti-windup strategies (clamping/back-calc/track-back) |
| Production | `deadtime-comp` | dead-time compensation params + code |
| Production | `multirate` | multi-rate control guidance |
| Analysis | `stability` | stability margins (phase/gain, Bode data) |
| Validation | `validate` | physical sanity check |
| Production | `protection` | fault protection thresholds (OC/OV/OT/stall/I2t) |
| Production | `tempcomp` | temperature compensation (Rs/flux drift + code) |
| Sensorless | `startup` | sensorless startup (I/F + HFI) |
| Report | `report` | one-shot full tuning report (Markdown) |

**Mode parameters** (abbreviated — `--help` per mode has full detail):

- Core (current/speed/position/all): `--rs --ls --j --b --kt --bw --zeta --ts`; all adds `--vbus --imax --psi-f --pole-pairs`; optional `--rshunt --aop --vref` (derive imax)
- simulate: `--loop --kp --ki --kd`, loop-specific physics, `--ts --steps(2000) --ref(1.0) --output-limit`
- sensitivity: `--loop(=current)`, physics, `--variation(=30, percent)`
- discretize: `--kp --ki --kd --ts --method(forward/backward/tustin/all)`
- fieldweak: `--psi-f --ls --vbus --pole-pairs --rated-speed --max-speed`
- observer: `--rs --ls --psi-f --pole-pairs --bw`, `--observer-type(smo/luenberger/all)`, `--max-speed`
- preset: `--preset-name` (optional; omit to list all)
- suggest-bw: `--pwm-freq (kHz)`, optional `--rs --ls`
- export: `--loop --kp --ki --kd` + physics, `--format(=matlab)`
- svpwm: `--vbus`, `--deadtime(=500ns)`
- platform: `--platform-choice(stm32/gd32/c2000)`, `--pwm-freq`, `--vbus`, `--imax`
- interactive: `--target(current/speed/position/all)`
- reverse: `--kp --ki --kd --loop` + physics, `--no-speed-loop`
- antiwindup: `--loop --kp --ki --output-limit`, `--aw-method(clamping/backcalc/trackback/all)`, `--ts`
- deadtime-comp: `--vbus --pwm-freq --deadtime`, optional `--rated-current`
- multirate: `--pwm-freq --bw`, `--speed-ratio(10) --pos-ratio(10)`
- stability: `--loop --kp --ki --kd --ts` + physics
- validate: physics args (all optional; only passed args are validated)
- protection: `--rated-current --vbus --device-type(IGBT/MOSFET)`
- tempcomp: physics, `--temp-min(25) --temp-max(125) --temp-points(5)`, `--magnet-type(NdFeB/SmCo/Ferrite)`
- startup: physics, `--rated-speed --pwm-freq --rated-current`, `--startup-method(if/hfi/all)`, `--transition-speed`
- report (via `python report_gen.py`): `--rs --ls(mH!) --j --kt [--b --psi-f --pole-pairs --vbus --imax --pwm-freq --bw-current --zeta --ts --motor-model --platform]`, options `--no-position --no-protection --with-stability -o <file>`. **Unit warning**: `report_gen.py --ls` takes **mH** (auto-converts); `main.py --ls` takes **H**. Section numbering is dynamic (no psi_f → no feedforward section).

The scripts output structured JSON — parse it and present to the user.

### 5. Present results

- List computed Kp/Ki/Kd with units
- Show the formulas used (brief)
- Report the bandwidth-ratio check (inner loop 5-10x the outer)
- Give tuning advice (fine-tuning direction from theory)
- simulate: time-domain metrics (rise time, overshoot, settling)
- sensitivity: percent impact and sensitivity rating
- Generate C code if requested

### 6. Supplementary notes

**Bandwidth rules of thumb**: current loop < PWM frequency / 10; speed = current / 5-10; position = speed / 5-10; `--mode suggest-bw` automates this.

**Why reality diverges from theory**: Rs rises with temperature (+30-50%) — quantify via `--mode sensitivity`; magnetic saturation lowers Ls; sampling and computation delay; quantization and noise. Start at 70% of theoretical gains and increase stepwise.

**Discretization reminder**: discrete-domain Ki = continuous Ki x Ts; compare methods via `--mode discretize --method all`; Tustin is most accurate but heavier. Position-loop discrete Kd = Kd_continuous / Ts — large values are normal (Kd=8882.64 at Ts=50us gives ~1.78e6); scale before Q-format or use float.

**Q-format fixed point** (MCSDK-compatible): normalize (Kp_pu = Kp x Imax / Vmax, Vmax = Vbus/sqrt(3)); discretize (Ki_d = Ki_pu x Ts); encode (value = raw / DIV, DIV = largest power of two keeping raw in [-32767, 32767]); emit `PID_KP_DEFAULT / PID_KPDIV / PID_KPDIV_LOG`.

**Feedforward**: dq voltage equations have cross-coupling and back-EMF terms PI alone cannot handle: Vd_ff = -we x Ls x Iq; Vq_ff = +we x Ls x Id + we x psi_f.

**Field weakening**: above base speed, back-EMF nears the bus limit — inject negative Id: base speed n_base = Vmax / (psi_f x 2pi x pole_pairs) x 60; Id_fw = (Vmax/we - psi_f) / Ls; demag limit Id_fw_max = -psi_f / Ls.

**Observer gains**: SMO sliding gain must exceed max back-EMF; LPF phase lag needs compensation. Luenberger: full-order poles at 2-5x current-loop bandwidth.

**Full code generation** (`code --full`): motor_controller.h + .c with d/q current PI + feedforward interface, speed PI, optional position PD, anti-windup (clamping), init + FOC ISR templates.

**SVPWM codegen**: complete 7-segment SVPWM C function — sector detection, T1/T2, compare values, dead-time handling.

**Platform adaptation**: STM32 (TIM1 center-aligned PWM + injected ADC), GD32 (TIMER0 + regular group, register-map differences), TI C2000 (ePWM AQ+TB + ADC SOC trigger).

**Preset library**: 10 common BLDC/PMSM motors (2207/2804/5010/6354/8318 etc.) — pick a model, Rs/Ls/Kt/pole-pairs auto-filled.

## Output Example

```
Current-loop PI result
Motor: Rs=0.5 ohm, Ls=2.0 mH, target BW=1000 Hz (wc=6283 rad/s)
PI (continuous): Kp = Ls x wc = 12.57 V/A; Ki = Rs x wc = 3141.6 V/(A*s)
PI (discrete, Ts=50us): Kp = 12.57; Ki = 0.157
Bandwidth check: OK
Advice: start from Kp=8.8 (70%), watch current step response
```
