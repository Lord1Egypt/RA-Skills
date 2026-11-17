#!/usr/bin/env python3
"""
电机PID调参器 1.0.0 - 核心计算引擎 (29种模式)
支持FOC三环PI/PID参数计算、ZN法、调参诊断、C代码生成、阶跃仿真、灵敏度分析、弱磁控制、观测器增益、SVPWM、多平台适配等

公式来源（多源交叉验证）：
- 电流环零极点对消法: Kp=Ls*ωc, Ki=Rs*ωc
  来源: CSDN/博客园/21ic多篇FOC调参文章一致
- 速度环二阶系统法: Kp=(2ζωc*J-B)/Kt, Ki=ωc²*J/Kt
  来源: 博客园《现代永磁同步电机FOC控制技术指南》推导
- Ziegler-Nichols法: PI: Kp=0.45Kc, Ki=0.54Kc/Tc
  来源: SimpleFOC官方文档
"""

import argparse
import json
import math
import sys

# 位置环数字域Kd提示（Kd按Kd/Ts离散后数值巨大属正常，定点化需注意）
KD_DIGITAL_NOTE = ("数字域 Kd = Kd_continuous / Ts 数值较大属正常现象，"
                   "定点化实现时建议先对 Kd 缩放（如按 2^-n 移位）或直接使用浮点运算，避免 Q 格式溢出。")


# ============================================================
# 核心计算函数
# ============================================================

def calculate_current_loop_pi(Rs, Ls, bandwidth_hz):
    """
    电流环PI参数计算（零极点对消法）
    
    原理: PI控制器零点抵消电机极点(Rs/Ls)，闭环简化为一阶系统
    闭环传递函数: G_cl(s) = ωc / (s + ωc)
    
    参数:
        Rs: 定子电阻 (Ω)
        Ls: 定子电感 (H)
        bandwidth_hz: 期望电流环带宽
    
    返回:
        Kp: 比例增益, Ki: 积分增益
    """
    if Rs <= 0 or Ls <= 0 or bandwidth_hz <= 0:
        raise ValueError("Rs, Ls, bandwidth必须为正数")
    
    omega_c = 2 * math.pi * bandwidth_hz  # rad/s
    Kp = Ls * omega_c          # V/A
    Ki = Rs * omega_c           # V/(A·s)
    
    # 电气时间常数
    tau_elec = Ls / Rs          # s
    
    return {
        "Kp": Kp,
        "Ki": Ki,
        "omega_c": omega_c,
        "tau_elec": tau_elec,
        "method": "零极点对消法 (Pole-Zero Cancellation)",
        "formula": f"Kp = Ls × ωc = {Ls:.6e} × {omega_c:.2f} = {Kp:.4f} V/A\n"
                   f"Ki = Rs × ωc = {Rs} × {omega_c:.2f} = {Ki:.4f} V/(A·s)",
        "derivation": (
            "电机dq轴电压方程(忽略交叉耦合): Vq = Rs·Iq + Ls·dIq/dt\n"
            "被控对象: Gp(s) = 1/(Ls·s + Rs)\n"
            "PI控制器: Gc(s) = Kp + Ki/s\n"
            "零极点对消: 令 Ki/Kp = Rs/Ls (PI零点抵消电机极点)\n"
            "闭环简化为一阶: G_cl(s) = ωc/(s + ωc), 其中 ωc = Kp/Ls"
        )
    }


def calculate_speed_loop_pi(J, B, Kt, bandwidth_hz, zeta=0.707):
    """
    速度环PI参数计算（标准二阶系统法）
    
    原理: 电流环近似为增益1，速度环被控对象为机械模型
    闭环特征方程配置为标准二阶: s² + 2ζωn·s + ωn²
    
    参数:
        J: 转动惯量 (kg·m²)
        B: 摩擦系数 (N·m·s/rad)
        Kt: 转矩常数 (N·m/A)
        bandwidth_hz: 期望速度环
        zeta: 阻尼比 (默认0.707, 临界阻尼=1.0)
    
    返回:
        Kp: 比例增益, Ki: 积分增益
    """
    if J <= 0 or Kt <= 0 or bandwidth_hz <= 0:
        raise ValueError("J, Kt, bandwidth必须为正数")
    if not (0 < zeta <= 2):
        raise ValueError("阻尼比zeta应在(0, 2]范围内")
    
    omega_c = 2 * math.pi * bandwidth_hz  # rad/s
    
    # 二阶系统法: J·s² + (B + Kt·Kp)·s + Kt·Ki = 0
    # 对比标准形: s² + 2ζωn·s + ωn²
    # → Kt·Kp + B = 2ζωn·J → Kp = (2ζωn·J - B) / Kt
    # → Kt·Ki = ωn²·J → Ki = ωn²·J / Kt
    Kp = (2 * zeta * omega_c * J - B) / Kt   # A·s/rad
    Ki = (omega_c ** 2 * J) / Kt              # A/rad
    
    if Kp < 0:
        print(f"⚠️ 警告: Kp为负值({Kp:.4f})，可能B过大或带宽过低，建议增大带宽")
    
    # 机械时间常数
    tau_mech = J * 1.0 / Kt  # 简化估计
    
    return {
        "Kp": Kp,
        "Ki": Ki,
        "omega_c": omega_c,
        "zeta": zeta,
        "tau_mech": tau_mech,
        "method": "标准二阶系统法 (Second-Order System)",
        "formula": f"Kp = (2ζωc·J - B) / Kt = (2×{zeta}×{omega_c:.2f}×{J:.6e} - {B}) / {Kt} = {Kp:.6f} A·s/rad\n"
                   f"Ki = ωc²·J / Kt = {omega_c:.2f}²×{J:.6e} / {Kt} = {Ki:.6f} A/rad",
        "derivation": (
            "电流环近似为理想增益1，速度环被控对象: Gp(s) = Kt/(J·s + B)\n"
            "PI控制器: Gc(s) = Kp + Ki/s\n"
            "闭环特征方程: J·s² + (B + Kt·Kp)·s + Kt·Ki = 0\n"
            f"对比标准二阶 s² + 2ζωn·s + ωn², 令 ωn = ωc = {omega_c:.2f} rad/s, ζ = {zeta}\n"
            "→ Kp = (2ζωc·J - B)/Kt, Ki = ωc²·J/Kt"
        )
    }


def calculate_position_loop_pid(J, Kt, bandwidth_hz, zeta=0.707, has_speed_loop=True, B=0):
    """
    位置环PID参数计算
    
    两种模式:
    1. 级联控制(有速度环): 位置环输出速度指令，被控对象近似为积分器1/s
       PD控制: Kp=ωc², Kd=2ζωc
    2. 单环控制(无速度环): 位置环直接输出转矩指令
       PD控制: Kp=ωc²·J/Kt, Kd=2ζωc·J/Kt
    
    参数:
        J: 转动惯量 (kg·m²)
        Kt: 转矩常数 (N·m/A)
        bandwidth_hz: 期望位置环
        zeta: 阻尼比 (默认0.707)
        has_speed_loop: 是否有速度环(级联控制)
        B: 摩擦系数(仅单环模式使用)
    """
    if J <= 0 or Kt <= 0 or bandwidth_hz <= 0:
        raise ValueError("J, Kt, bandwidth必须为正数")
    
    omega_c = 2 * math.pi * bandwidth_hz
    
    if has_speed_loop:
        # 级联控制: 速度环近似理想，位置环被控对象 = 1/s
        # PD: (Kp + Kd·s) / (s + Kp + Kd·s) → s² + Kd·s + Kp
        # ωn² = Kp, 2ζωn = Kd
        Kp = omega_c ** 2       # 1/s²
        Kd = 2 * zeta * omega_c  # 1/s
        Ki = 0
        mode_desc = "级联控制(有速度环)，被控对象=1/s"
    else:
        # 单环控制: 被控对象 = Kt/(J·s²)
        # PD: (Kp + Kd·s)·Kt / (J·s² + Kt·(Kp + Kd·s))
        # ωn² = Kp·Kt/J, 2ζωn = Kd·Kt/J
        Kp = omega_c ** 2 * J / Kt    # rad/s² per rad
        Kd = 2 * zeta * omega_c * J / Kt  # rad/s per rad/s
        Ki = 0
        mode_desc = "单环控制(无速度环)，被控对象=Kt/(J·s²)"
    
    return {
        "Kp": Kp,
        "Ki": Ki,
        "Kd": Kd,
        "omega_c": omega_c,
        "zeta": zeta,
        "mode": mode_desc,
        "method": "PD控制器 + 二阶系统配置",
        "formula": f"Kp = {'ωc²' if has_speed_loop else 'ωc²·J/Kt'} = {Kp:.6f}\n"
                   f"Kd = {'2ζωc' if has_speed_loop else '2ζωc·J/Kt'} = {Kd:.6f}\n"
                   f"Ki = 0 (位置环通常不用积分)",
        "derivation": (
            f"模式: {mode_desc}\n"
            "PD控制器: C(s) = Kp + Kd·s\n"
            "闭环特征方程配置为标准二阶: s² + 2ζωn·s + ωn²\n"
            f"ωn = ωc = {omega_c:.2f} rad/s, ζ = {zeta}\n"
            f"{'Kp = ωc², Kd = 2ζωc' if has_speed_loop else 'Kp = ωc²·J/Kt, Kd = 2ζωc·J/Kt'}"
        )
    }


def ziegler_nichols_tuning(Kc, Tc, controller_type="PI"):
    """
    Ziegler-Nichols临界增益法
    
    参数:
        Kc: 临界增益(系统等幅振荡时的Kp)
        Tc: 临界振荡周期
        controller_type: "P", "PI", "PID"
    """
    if Kc <= 0 or Tc <= 0:
        raise ValueError("Kc和Tc必须为正数")
    
    if controller_type == "P":
        Kp = 0.5 * Kc
        Ki = 0
        Kd = 0
    elif controller_type == "PI":
        Kp = 0.45 * Kc
        Ki = 0.54 * Kc / Tc
        Kd = 0
    elif controller_type == "PID":
        Kp = 0.6 * Kc
        Ki = 1.2 * Kc / Tc
        Kd = 0.075 * Kc * Tc
    else:
        raise ValueError(f"不支持的控制器类型: {controller_type}")
    
    return {
        "Kp": Kp,
        "Ki": Ki,
        "Kd": Kd,
        "Kc": Kc,
        "Tc": Tc,
        "method": f"Ziegler-Nichols法 ({controller_type})",
        "formula": f"Kp = {Kp:.4f}, Ki = {Ki:.4f}, Kd = {Kd:.4f}",
        "derivation": (
            f"Ziegler-Nichols临界增益法\n"
            f"临界增益 Kc = {Kc}, 临界周期 Tc = {Tc}s\n"
            f"控制器类型: {controller_type}\n"
            f"{'Kp = 0.5·Kc' if controller_type == 'P' else ''}"
            f"{'Kp = 0.45·Kc, Ki = 0.54·Kc/Tc' if controller_type == 'PI' else ''}"
            f"{'Kp = 0.6·Kc, Ki = 1.2·Kc/Tc, Kd = 0.075·Kc·Tc' if controller_type == 'PID' else ''}"
        )
    }


# ============================================================
# Q格式定点化
# ============================================================

def calculate_q_format(Kp, Ki, Kd=0, Ts=50e-6, vbus=24.0, imax=10.0, q_format=15):
    """
    Q格式定点化 - 将物理域PI参数转为MCSDK风格的定点数

    转换链: 物理域(V/A) → 标幺化(per-unit) → 离散化 → Q格式定点(int16+DIV)

    参数:
        Kp: 比例增益 (物理域, V/A 或 A·s/rad)
        Ki: 积分增益 (物理域, V/(A·s) 或 A/rad)
        Kd: 微分增益 (物理域, 默认0)
        Ts: 采样周期
        vbus: 母线电压 (V)
        imax: 最大电流 (A), 用于标幺化
        q_format: Q格式位数 (默认15, 即Q15)

    返回:
        定点化参数 + DIV值 + C代码宏定义
    """
    if imax <= 0 or vbus <= 0:
        raise ValueError("imax和vbus必须为正数")

    Vmax = vbus / math.sqrt(3)  # SVPWM最大线性相电压

    # Step 1: 标幺化
    Kp_pu = Kp * imax / Vmax
    Ki_pu = Ki * imax / Vmax
    Kd_pu = Kd * imax / Vmax if Kd != 0 else 0

    # Step 2: 离散化
    Ki_d = Ki_pu * Ts
    Kd_d = Kd_pu / Ts if Kd != 0 else 0

    # Step 3: Q格式编码 - value = raw / DIV, DIV为2的幂
    def encode_q(value, max_raw=32767):
        if value == 0:
            return 1, 0
        div_max = int(max_raw / abs(value))
        if div_max < 1:
            div_max = 1
        div_exp = int(math.floor(math.log2(div_max))) if div_max >= 1 else 0
        div = 2 ** div_exp
        raw = round(value * div)
        if abs(raw) > max_raw:
            div = div // 2
            raw = round(value * div)
        return div, raw

    kp_div, kp_raw = encode_q(Kp_pu)
    ki_div, ki_raw = encode_q(Ki_d)
    kd_div, kd_raw = encode_q(Kd_d) if Kd != 0 else (1, 0)

    # 验证精度
    kp_actual = kp_raw / kp_div if kp_div != 0 else 0
    ki_actual = ki_raw / ki_div if ki_div != 0 else 0
    kp_error = abs(Kp_pu - kp_actual) / abs(Kp_pu) * 100 if Kp_pu != 0 else 0
    ki_error = abs(Ki_d - ki_actual) / abs(Ki_d) * 100 if Ki_d != 0 else 0

    # 构建C宏定义
    kd_macro = ""
    if Kd != 0:
        kd_macro = "\n#define PID_KD_DEFAULT    (%d)" % kd_raw
        kd_div_macro = "\n#define PID_KDDIV         (%d)" % kd_div
        kd_div_log = "\n#define PID_KDDIV_LOG     (%d)" % (int(math.log2(kd_div)) if kd_div > 0 else 0)
    else:
        kd_div_macro = ""
        kd_div_log = ""

    c_macros = (
        "#define PID_KP_DEFAULT    (%d)\n"
        "#define PID_KI_DEFAULT    (%d)%s\n"
        "#define PID_KPDIV         (%d)\n"
        "#define PID_KIDIV         (%d)%s\n"
        "#define PID_KPDIV_LOG     (%d)\n"
        "#define PID_KIDIV_LOG     (%d)%s"
    ) % (
        kp_raw, ki_raw, kd_macro,
        kp_div, ki_div, kd_div_macro,
        int(math.log2(kp_div)) if kp_div > 0 else 0,
        int(math.log2(ki_div)) if ki_div > 0 else 0,
        kd_div_log
    )

    return {
        "per_unit": {
            "Kp_pu": round(Kp_pu, 6),
            "Ki_pu": round(Ki_pu, 6),
            "Kd_pu": round(Kd_pu, 6),
            "Ki_digital_pu": Ki_d,
            "Kd_digital_pu": Kd_d,
            "I_base": imax,
            "V_base": round(Vmax, 4),
        },
        "q_format": {
            "Q": q_format,
            "Kp_raw": kp_raw,
            "KpDIV": kp_div,
            "KpDIV_LOG": int(math.log2(kp_div)) if kp_div > 0 else 0,
            "Ki_raw": ki_raw,
            "KiDIV": ki_div,
            "KiDIV_LOG": int(math.log2(ki_div)) if ki_div > 0 else 0,
            "Kd_raw": kd_raw,
            "KdDIV": kd_div,
            "KdDIV_LOG": int(math.log2(kd_div)) if kd_div > 0 else 0,
        },
        "verification": {
            "Kp_actual_pu": round(kp_actual, 6),
            "Kp_quantization_error_pct": round(kp_error, 4),
            "Ki_actual_pu": round(ki_actual, 6),
            "Ki_quantization_error_pct": round(ki_error, 4),
        },
        "c_macros": c_macros,
        "method": "标幺化 + Q格式定点化 (Per-unit + Q-format Fixed-point)",
        "derivation": (
            "Step 1 标幺化:\n"
            "  I_base = %.1fA, V_base = Vbus/sqrt(3) = %.1f/sqrt(3) = %.4fV\n"
            "  Kp_pu = Kp * I_base / V_base = %s * %.1f / %.4f = %.6f\n"
            "  Ki_pu = Ki * I_base / V_base = %s * %.1f / %.4f = %.6f\n"
            "Step 2 离散化:\n"
            "  Ki_d = Ki_pu * Ts = %.6f * %s = %.10f\n"
            "Step 3 Q格式编码:\n"
            "  Kp: raw=%d, DIV=%d, actual=%.6f, error=%.4f%%\n"
            "  Ki: raw=%d, DIV=%d, actual=%.6f, error=%.4f%%"
        ) % (
            imax, vbus, Vmax,
            Kp, imax, Vmax, Kp_pu,
            Ki, imax, Vmax, Ki_pu,
            Ki_pu, Ts, Ki_d,
            kp_raw, kp_div, kp_actual, kp_error,
            ki_raw, ki_div, ki_actual, ki_error
        )
    }


# ============================================================
# 前馈补偿
# ============================================================

def calculate_feedforward(Rs, Ls, psi_f=0.0, pole_pairs=1):
    """
    前馈补偿参数计算

    dq轴电压方程(完整):
    Vd = Rs*Id + Ls*dId/dt - omega_e*Ls*Iq
    Vq = Rs*Iq + Ls*dIq/dt + omega_e*Ls*Id + omega_e*psi_f

    PI控制器输出Vd_pi/Vq_pi补偿Rs和Ls项
    前馈补偿交叉耦合和反电动势:
    Vd_ff = -omega_e * Ls * Iq
    Vq_ff = +omega_e * Ls * Id + omega_e * psi_f

    参数:
        Rs: 定子电阻 (Ω)
        Ls: 定子电感 (H)
        psi_f: 永磁体磁链 (Wb), 0表示不加反电动势前馈
        pole_pairs: 极对数
    """
    if Ls <= 0:
        raise ValueError("Ls必须为正数")

    K_cross_d = Ls   # Vd_ff = -K_cross_d * omega_e * Iq
    K_cross_q = Ls   # Vq_ff = +K_cross_q * omega_e * Id
    K_emf = psi_f     # Vq_ff += K_emf * omega_e

    # 构建C代码片段
    ff_code = (
        "/* Feedforward compensation coefficients */\n"
        "#define FF_CROSS_COUPLE_D   (%.6ef)   /* Ls: d-axis cross-coupling (H) */\n"
        "#define FF_CROSS_COUPLE_Q   (%.6ef)   /* Ls: q-axis cross-coupling (H) */\n"
        "#define FF_BACK_EMF         (%.6ef)   /* psi_f: PM flux linkage (Wb) */\n"
        "#define POLE_PAIRS          (%d)\n"
        "\n"
        "/* Feedforward calculation (call in current loop) */\n"
        "static inline void feedforward_update(float omega_e, float id_meas, float iq_meas,\n"
        "                                       float *vd_ff, float *vq_ff) {\n"
        "    /* d-axis cross-coupling: Vd_ff = -omega_e * Ls * Iq */\n"
        "    *vd_ff = -omega_e * FF_CROSS_COUPLE_D * iq_meas;\n"
        "    \n"
        "    /* q-axis cross-coupling + back-EMF: Vq_ff = omega_e * Ls * Id + omega_e * psi_f */\n"
        "    *vq_ff = omega_e * FF_CROSS_COUPLE_Q * id_meas + omega_e * FF_BACK_EMF;\n"
        "}"
    ) % (Ls, Ls, psi_f, pole_pairs)

    has_emf = psi_f > 0
    vq_ff_str = "omega_e * Ls * Id + omega_e * psi_f" if has_emf else "omega_e * Ls * Id"

    return {
        "cross_coupling": {
            "K_cross_d": K_cross_d,
            "K_cross_q": K_cross_q,
            "Vd_ff_formula": "Vd_ff = -omega_e * Ls * Iq",
            "Vq_ff_formula": "Vq_ff = +omega_e * Ls * Id",
        },
        "back_emf": {
            "K_emf": K_emf,
            "Vq_emf_formula": "Vq_emf = omega_e * psi_f" if has_emf else "未配置反电动势前馈(psi_f=0)",
        },
        "pole_pairs": pole_pairs,
        "omega_relation": "omega_e = %d * omega_m (电角速度 = %d * 机械角速度)" % (pole_pairs, pole_pairs),
        "complete_vq_ff": "Vq_ff = %s" % vq_ff_str,
        "code": ff_code,
        "method": "dq轴解耦前馈补偿 (Cross-coupling + Back-EMF Feedforward)",
        "derivation": (
            "dq轴完整电压方程:\n"
            "  Vd = Rs*Id + Ls*dId/dt - omega_e*Ls*Iq\n"
            "  Vq = Rs*Iq + Ls*dIq/dt + omega_e*Ls*Id + omega_e*psi_f\n"
            "PI控制器补偿Rs和Ls项(电阻+电感动态)\n"
            "前馈补偿剩余耦合项:\n"
            "  Vd_ff = -omega_e * Ls * Iq = -omega_e * %s * Iq\n"
            "  Vq_ff = omega_e * Ls * Id + omega_e * %s = omega_e * %s * Id + omega_e * %s\n"
            "最终输出: Vd = Vd_pi + Vd_ff, Vq = Vq_pi + Vq_ff"
        ) % (Ls, psi_f, Ls, psi_f)
    }


# ============================================================
# 辅助功能
# ============================================================

def check_bandwidth_ratio(current_bw, speed_bw, position_bw=None):
    """检查三环带宽比是否合理（内环应为外环5-10倍）"""
    warnings = []
    info = []
    
    if current_bw and speed_bw:
        ratio = current_bw / speed_bw
        if ratio < 3:
            warnings.append(f"电流环/速度环带宽比 = {ratio:.1f}，严重过低（建议5-10），两环耦合风险高")
        elif ratio < 5:
            warnings.append(f"电流环/速度环带宽比 = {ratio:.1f}，建议≥5，速度环可能跟不上电流环")
        elif ratio > 50:
            warnings.append(f"电流环/速度环带宽比 = {ratio:.1f}，严重过高（建议5-10），速度环响应可能过慢")
        elif ratio > 10:
            info.append(f"电流环/速度环带宽比 = {ratio:.1f}，可以适当提高速度环带宽")
        else:
            info.append(f"电流环/速度环带宽比 = {ratio:.1f} ✓")
    
    if speed_bw and position_bw:
        ratio = speed_bw / position_bw
        if ratio < 3:
            warnings.append(f"速度环/位置环带宽比 = {ratio:.1f}，严重过低（建议5-10）")
        elif ratio < 5:
            warnings.append(f"速度环/位置环带宽比 = {ratio:.1f}，建议≥5")
        elif ratio > 50:
            warnings.append(f"速度环/位置环带宽比 = {ratio:.1f}，严重过高（建议5-10）")
        elif ratio > 10:
            info.append(f"速度环/位置环带宽比 = {ratio:.1f}，可以适当提高位置环带宽")
        else:
            info.append(f"速度环/位置环带宽比 = {ratio:.1f} ✓")
    
    return {"warnings": warnings, "info": info}


def discretize_params(Kp, Ki, Kd, Ts):
    """连续域参数离散化（前向欧拉法）"""
    if Ts is None or Ts <= 0:
        raise ValueError("采样周期Ts必须为正数")
    return {
        "Kp_digital": Kp,
        "Ki_digital": Ki * Ts,
        "Kd_digital": Kd / Ts if Kd != 0 else 0,
        "Ts": Ts,
        "method": "前向欧拉法: Ki_d = Ki·Ts, Kd_d = Kd/Ts"
    }


def diagnose_symptoms(symptom, current_params=None):
    """
    调参诊断: 根据症状给出调参建议
    
    参数:
        symptom: 症状关键词
        current_params: 当前参数 dict
    """
    symptom_lower = symptom.lower()
    
    diagnoses = {
        "震荡": {
            "振荡": None,
            "oscillation": None,
        },
        "超调": {
            "overshoot": None,
        },
        "响应慢": {
            "慢": None,
            "slow": None,
        },
        "稳态误差": {
            "静差": None,
            "steady": None,
        },
        "噪声": {
            "noise": None,
            "抖动": None,
        },
    }
    
    results = []
    
    # 匹配症状
    if any(k in symptom_lower for k in ["震荡", "振荡", "oscillation", "振"]):
        results.append({
            "症状": "输出震荡/振荡",
            "原因分析": "Kp过大或Ki过大导致闭环增益过高，系统稳定裕度不足",
            "调整建议": [
                "1. 首先减小Ki（积分项），通常减半",
                "2. 如果仍震荡，减小Kp 20-30%",
                "3. 检查带宽比：内环是否≥外环5倍",
                "4. 检查采样周期是否过大（延迟引入相位滞后）",
                "5. 如果是速度环震荡，检查电流环是否已整定好",
            ],
            "优先级": "先减Ki → 再减Kp → 查带宽比"
        })
    
    if any(k in symptom_lower for k in ["超调", "overshoot"]):
        results.append({
            "症状": "阶跃响应超调过大",
            "原因分析": "阻尼比偏低，Kp相对Ki过大",
            "调整建议": [
                "1. 减小Kp 10-20%",
                "2. 或增大Ki（提高阻尼）",
                "3. 速度环可尝试增大阻尼比ζ（0.707→1.0）",
                "4. 加入微分项D（位置环）：Kd从0.001×Kp开始加",
                "5. 检查前馈是否引入了额外超调",
            ],
            "优先级": "减Kp → 加D → 调ζ"
        })
    
    if any(k in symptom_lower for k in ["慢", "slow", "响应慢", "迟钝"]):
        results.append({
            "症状": "响应速度慢",
            "原因分析": "带宽设置过低或Kp偏小",
            "调整建议": [
                "1. 增大Kp 20%（观察是否出现超调）",
                "2. 适当增大Ki加快稳态收敛",
                "3. 提高目标带宽（检查是否受PWM频率限制：BW < fpwm/10）",
                "4. 检查是否存在前馈补偿缺失",
                "5. 确认采样周期足够小（Ts ≤ 1/(10×BW)）",
            ],
            "优先级": "增Kp → 提带宽 → 查Ts"
        })
    
    if any(k in symptom_lower for k in ["稳态", "静差", "steady", "误差"]):
        results.append({
            "症状": "存在稳态误差",
            "原因分析": "积分增益Ki不足或积分饱和",
            "调整建议": [
                "1. 增大Ki（积分项消除稳态误差）",
                "2. 检查积分限幅是否设置过小",
                "3. 确认积分项未被抗饱和机制意外抑制",
                "4. 如果是速度环，检查是否有摩擦补偿缺失",
                "5. 考虑加入前馈补偿（重力/摩擦）",
            ],
            "优先级": "增Ki → 查限幅 → 加前馈"
        })
    
    if any(k in symptom_lower for k in ["噪声", "抖动", "noise", "jitter"]):
        results.append({
            "症状": "输出噪声大/高频抖动",
            "原因分析": "微分项放大噪声或采样噪声过大",
            "调整建议": [
                "1. 如果有D项，减小Kd或加低通滤波",
                "2. 对反馈信号加一阶低通滤波（截止频率≈5×BW）",
                "3. 检查ADC采样是否受开关噪声干扰",
                "4. 减小Kp（降低对噪声的灵敏度）",
                "5. 检查编码器分辨率是否足够",
            ],
            "优先级": "减Kd/加滤波 → 滤反馈 → 减Kp"
        })
    
    if not results:
        results.append({
            "症状": symptom,
            "原因分析": "未匹配到已知症状模式，请详细描述问题现象",
            "调整建议": [
                "常见症状关键词：震荡、超调、响应慢、稳态误差、噪声",
                "也可以直接提供电机参数，使用带宽法计算理论PI参数作为起点",
            ],
            "优先级": "请补充描述"
        })
    
    return {"diagnoses": results}


def generate_c_code(loop_type, Kp, Ki, Kd=0, Ts=50e-6, output_limit=None, platform="stm32"):
    """
    生成PID/PI控制器的C代码
    
    参数:
        loop_type: "current" / "speed" / "position"
        Kp, Ki, Kd: 控制器参数（数字域）
        Ts: 采样周期
        output_limit: 输出限幅
        platform: "stm32" / "generic"
    """
    # 离散化
    Ki_d = Ki * Ts
    Kd_d = Kd / Ts if Kd != 0 else 0
    
    if output_limit is None:
        if loop_type == "current":
            output_limit = 12.0  # V，假设12V母线
        elif loop_type == "speed":
            output_limit = 10.0  # A，假设10A最大电流
        else:
            output_limit = 100.0  # RPM或rad/s
    
    loop_name = {"current": "Current", "speed": "Speed", "position": "Position"}[loop_type]
    
    has_d = Kd != 0
    controller_type_str = "PI+D" if has_d else "PI"
    kd_comment = f", Kd={Kd:.6f}" if has_d else ""
    
    # Pre-build derivative code block
    if has_d:
        derivative_code = """
    /* Derivative term (on measurement to avoid setpoint kick) */
    float derivative = -(feedback - pi->prev_fb);
    output += pi->Kd * derivative;
    pi->prev_fb = feedback;"""
        prev_fb_decl = "    float prev_fb;       /* Previous feedback for derivative */\n"
    else:
        derivative_code = ""
        prev_fb_decl = ""
    
    code = f"""/*=============================================
 * {loop_name} Loop {controller_type_str} Controller
 * Auto-generated by Motor PID Tuner
 * Kp={Kp:.6f}, Ki={Ki:.6f}{kd_comment}
 * Ts={Ts*1e6:.0f}us, Output limit=+/-{output_limit}
 *=============================================*/

typedef struct {{
    float Kp;           /* Proportional gain */
    float Ki;           /* Integral gain (discretized) */
    float Kd;           /* Derivative gain (discretized) */
    float integral;     /* Integral accumulator */
{prev_fb_decl}    float output_max;   /* Output upper limit */
    float output_min;   /* Output lower limit */
}} {loop_name}PI_t;

/* Initialize {loop_name} loop controller */
void {loop_name}_PI_Init({loop_name}PI_t *pi) {{
    pi->Kp = {Kp:.6f}f;
    pi->Ki = {Ki_d:.8f}f;
    pi->Kd = {Kd_d:.8f}f;
    pi->integral = 0.0f;
    pi->output_max = {output_limit}f;
    pi->output_min = -{output_limit}f;
}}

/* {loop_name} loop {controller_type_str} update - call at control rate */
float {loop_name}_PI_Update({loop_name}PI_t *pi, float setpoint, float feedback) {{
    float error = setpoint - feedback;
    
    /* Proportional term */
    float output = pi->Kp * error;
    
    /* Integral term with anti-windup (clamping) */
    float integral_new = pi->integral + pi->Ki * error;
    float output_test = output + integral_new;
    
    /* Anti-windup: only integrate if not saturated */
    if (output_test > pi->output_max) {{
        if (error < 0) {{
            pi->integral = integral_new;
        }}
        output = pi->output_max;
    }} else if (output_test < pi->output_min) {{
        if (error > 0) {{
            pi->integral = integral_new;
        }}
        output = pi->output_min;
    }} else {{
        pi->integral = integral_new;
        output = output_test;
    }}
{derivative_code}
    return output;
}}
"""
    return code


# ============================================================
# 完整代码模板生成
# ============================================================

def generate_full_code(current_result, speed_result, position_result=None,
                       ff_result=None, q_result=None, Ts=50e-6, vbus=24.0):
    """
    生成完整的电机控制器C代码(.h + .c)

    包含:
    - 电流环PI(含前馈补偿接口)
    - 速度环PI
    - 位置环PD(可选)
    - 抗积分饱和(clamping)
    - 初始化函数
    - FOC控制主函数模板
    """
    curr_kp = current_result["Kp"]
    curr_ki = current_result["Ki"]
    spd_kp = speed_result["Kp"]
    spd_ki = speed_result["Ki"]

    has_pos = position_result is not None
    has_ff = ff_result is not None
    has_q = q_result is not None

    pos_kp = position_result["Kp"] if has_pos else 0
    pos_kd = position_result["Kd"] if has_pos else 0

    # 离散化
    curr_ki_d = curr_ki * Ts
    spd_ki_d = spd_ki * Ts
    pos_kd_d = pos_kd / Ts if has_pos and pos_kd != 0 else 0

    Vmax = vbus / math.sqrt(3)

    # --- 构建 .h 文件 ---
    h_lines = []
    h_lines.append("/*=============================================")
    h_lines.append(" * motor_controller.h")
    h_lines.append(" * Auto-generated by Motor PID Tuner")
    h_lines.append(" *")
    h_lines.append(" * Current loop: Kp=%.6f, Ki=%.6f (Ts=%dus)" % (curr_kp, curr_ki, Ts * 1e6))
    h_lines.append(" * Speed loop:   Kp=%.6f, Ki=%.6f" % (spd_kp, spd_ki))
    if has_pos:
        h_lines.append(" * Position loop: Kp=%.6f, Kd=%.6f" % (pos_kp, pos_kd))
    h_lines.append(" * Vbus=%.1fV, Vmax=%.4fV" % (vbus, Vmax))
    h_lines.append(" *=============================================*/")
    h_lines.append("#ifndef MOTOR_CONTROLLER_H")
    h_lines.append("#define MOTOR_CONTROLLER_H")
    h_lines.append("")
    h_lines.append("#include <stdint.h>")
    h_lines.append("")

    # 前馈宏定义
    if has_ff:
        h_lines.append("/* Feedforward parameters */")
        h_lines.append("#define FF_LS              (%.6ef)" % ff_result["cross_coupling"]["K_cross_d"])
        h_lines.append("#define FF_PSI_F           (%.6ef)" % ff_result["back_emf"]["K_emf"])
        h_lines.append("#define POLE_PAIRS         (%d)" % ff_result["pole_pairs"])
        h_lines.append("")

    # Q格式宏定义
    if has_q:
        q = q_result["q_format"]
        h_lines.append("/* Q-format parameters (for fixed-point implementation) */")
        h_lines.append("#define CURRENT_KP_RAW     (%d)" % q["Kp_raw"])
        h_lines.append("#define CURRENT_KI_RAW     (%d)" % q["Ki_raw"])
        h_lines.append("#define CURRENT_KPDIV      (%d)" % q["KpDIV"])
        h_lines.append("#define CURRENT_KIDIV      (%d)" % q["KiDIV"])
        h_lines.append("#define CURRENT_KPDIV_LOG  (%d)" % q["KpDIV_LOG"])
        h_lines.append("#define CURRENT_KIDIV_LOG  (%d)" % q["KiDIV_LOG"])
        h_lines.append("")

    # 结构体定义
    h_lines.append("/* PI Controller Structure */")
    h_lines.append("typedef struct {")
    h_lines.append("    float Kp;")
    h_lines.append("    float Ki;          /* Discretized: Ki * Ts */")
    h_lines.append("    float Kd;          /* Discretized: Kd / Ts */")
    h_lines.append("    float integral;")
    h_lines.append("    float prev_feedback;")
    h_lines.append("    float output_max;")
    h_lines.append("    float output_min;")
    h_lines.append("} PI_Controller_t;")
    h_lines.append("")
    h_lines.append("/* Motor Controller Structure */")
    h_lines.append("typedef struct {")
    h_lines.append("    PI_Controller_t current_d;")
    h_lines.append("    PI_Controller_t current_q;")
    h_lines.append("    PI_Controller_t speed;")
    if has_pos:
        h_lines.append("    PI_Controller_t position;")
    h_lines.append("    float vbus;")
    h_lines.append("    float Ts;")
    h_lines.append("} MotorController_t;")
    h_lines.append("")

    # 函数声明
    h_lines.append("void MotorController_Init(MotorController_t *mc);")
    h_lines.append("")
    if has_ff:
        h_lines.append("/* Current loop: returns Vd, Vq (with feedforward) */")
        h_lines.append("void CurrentLoop_Update(MotorController_t *mc,")
        h_lines.append("                         float id_ref, float iq_ref,")
        h_lines.append("                         float id_meas, float iq_meas,")
        h_lines.append("                         float omega_e,")
        h_lines.append("                         float *vd_out, float *vq_out);")
    else:
        h_lines.append("/* Current loop: returns Vd, Vq */")
        h_lines.append("void CurrentLoop_Update(MotorController_t *mc,")
        h_lines.append("                         float id_ref, float iq_ref,")
        h_lines.append("                         float id_meas, float iq_meas,")
        h_lines.append("                         float *vd_out, float *vq_out);")
    h_lines.append("")
    h_lines.append("/* Speed loop: returns Iq reference */")
    h_lines.append("float SpeedLoop_Update(MotorController_t *mc, float speed_ref, float speed_meas);")
    h_lines.append("")
    if has_pos:
        h_lines.append("/* Position loop: returns speed reference */")
        h_lines.append("float PositionLoop_Update(MotorController_t *mc, float pos_ref, float pos_meas);")
        h_lines.append("")
    h_lines.append("#endif /* MOTOR_CONTROLLER_H */")

    header = "\n".join(h_lines)

    # --- 构建 .c 文件 ---
    c_lines = []
    c_lines.append("/*=============================================")
    c_lines.append(" * motor_controller.c")
    c_lines.append(" * Auto-generated by Motor PID Tuner")
    c_lines.append(" *=============================================*/")
    c_lines.append('#include "motor_controller.h"')
    c_lines.append("")

    # 初始化函数
    c_lines.append("/* Initialize all controllers */")
    c_lines.append("void MotorController_Init(MotorController_t *mc) {")
    c_lines.append("    /* Current loop (d-axis) */")
    c_lines.append("    mc->current_d.Kp = %.6ff;" % curr_kp)
    c_lines.append("    mc->current_d.Ki = %.8ff;" % curr_ki_d)
    c_lines.append("    mc->current_d.Kd = 0.0f;")
    c_lines.append("    mc->current_d.integral = 0.0f;")
    c_lines.append("    mc->current_d.prev_feedback = 0.0f;")
    c_lines.append("    mc->current_d.output_max = %.4ff;" % Vmax)
    c_lines.append("    mc->current_d.output_min = -%.4ff;" % Vmax)
    c_lines.append("    ")
    c_lines.append("    /* Current loop (q-axis) - same params as d-axis */")
    c_lines.append("    mc->current_q = mc->current_d;")
    c_lines.append("    ")
    c_lines.append("    /* Speed loop */")
    c_lines.append("    mc->speed.Kp = %.6ff;" % spd_kp)
    c_lines.append("    mc->speed.Ki = %.8ff;" % spd_ki_d)
    c_lines.append("    mc->speed.Kd = 0.0f;")
    c_lines.append("    mc->speed.integral = 0.0f;")
    c_lines.append("    mc->speed.prev_feedback = 0.0f;")
    c_lines.append("    mc->speed.output_max = 10.0f;   /* Max current (A) */")
    c_lines.append("    mc->speed.output_min = -10.0f;")
    if has_pos:
        c_lines.append("    ")
        c_lines.append("    /* Position loop (PD) */")
        c_lines.append("    mc->position.Kp = %.6ff;" % pos_kp)
        c_lines.append("    mc->position.Ki = 0.0f;")
        c_lines.append("    mc->position.Kd = %.8ff;" % pos_kd_d)
        c_lines.append("    mc->position.integral = 0.0f;")
        c_lines.append("    mc->position.prev_feedback = 0.0f;")
        c_lines.append("    mc->position.output_max = 500.0f;  /* Max speed (rad/s) */")
        c_lines.append("    mc->position.output_min = -500.0f;")
    c_lines.append("    ")
    c_lines.append("    mc->vbus = %.1ff;" % vbus)
    c_lines.append("    mc->Ts = %ff;" % Ts)
    c_lines.append("}")
    c_lines.append("")

    # 前馈函数
    if has_ff:
        c_lines.append("/* Feedforward: cross-coupling + back-EMF compensation */")
        c_lines.append("static void feedforward_update(float omega_e,")
        c_lines.append("                                float id_meas, float iq_meas,")
        c_lines.append("                                float *vd_ff, float *vq_ff) {")
        c_lines.append("    /* d-axis cross-coupling: Vd_ff = -omega_e * Ls * Iq */")
        c_lines.append("    *vd_ff = -omega_e * FF_LS * iq_meas;")
        c_lines.append("    ")
        c_lines.append("    /* q-axis cross-coupling + back-EMF */")
        c_lines.append("    *vq_ff = omega_e * FF_LS * id_meas + omega_e * FF_PSI_F;")
        c_lines.append("}")
        c_lines.append("")

    # PI更新函数(内部)
    c_lines.append("/* PI update with anti-windup (clamping) */")
    c_lines.append("static float pi_update(PI_Controller_t *pi, float setpoint, float feedback) {")
    c_lines.append("    float error = setpoint - feedback;")
    c_lines.append("    float output = pi->Kp * error;")
    c_lines.append("    float integral_new = pi->integral + pi->Ki * error;")
    c_lines.append("    float output_test = output + integral_new;")
    c_lines.append("    ")
    c_lines.append("    if (output_test > pi->output_max) {")
    c_lines.append("        if (error < 0) pi->integral = integral_new;")
    c_lines.append("        output = pi->output_max;")
    c_lines.append("    } else if (output_test < pi->output_min) {")
    c_lines.append("        if (error > 0) pi->integral = integral_new;")
    c_lines.append("        output = pi->output_min;")
    c_lines.append("    } else {")
    c_lines.append("        pi->integral = integral_new;")
    c_lines.append("        output = output_test;")
    c_lines.append("    }")
    c_lines.append("    ")
    c_lines.append("    return output;")
    c_lines.append("}")
    c_lines.append("")

    # 电流环更新函数
    if has_ff:
        c_lines.append("/* Current loop update (both d and q axes, with feedforward) */")
        c_lines.append("void CurrentLoop_Update(MotorController_t *mc,")
        c_lines.append("                         float id_ref, float iq_ref,")
        c_lines.append("                         float id_meas, float iq_meas,")
        c_lines.append("                         float omega_e,")
        c_lines.append("                         float *vd_out, float *vq_out) {")
        c_lines.append("    float vd = pi_update(&mc->current_d, id_ref, id_meas);")
        c_lines.append("    float vq = pi_update(&mc->current_q, iq_ref, iq_meas);")
        c_lines.append("    ")
        c_lines.append("    /* Feedforward compensation */")
        c_lines.append("    float vd_ff = 0.0f, vq_ff = 0.0f;")
        c_lines.append("    feedforward_update(omega_e, id_meas, iq_meas, &vd_ff, &vq_ff);")
        c_lines.append("    vd += vd_ff;")
        c_lines.append("    vq += vq_ff;")
        c_lines.append("    ")
        c_lines.append("    *vd_out = vd;")
        c_lines.append("    *vq_out = vq;")
        c_lines.append("}")
    else:
        c_lines.append("/* Current loop update (both d and q axes) */")
        c_lines.append("void CurrentLoop_Update(MotorController_t *mc,")
        c_lines.append("                         float id_ref, float iq_ref,")
        c_lines.append("                         float id_meas, float iq_meas,")
        c_lines.append("                         float *vd_out, float *vq_out) {")
        c_lines.append("    *vd_out = pi_update(&mc->current_d, id_ref, id_meas);")
        c_lines.append("    *vq_out = pi_update(&mc->current_q, iq_ref, iq_meas);")
        c_lines.append("}")
    c_lines.append("")

    # 速度环更新函数
    c_lines.append("/* Speed loop update (output = Iq reference) */")
    c_lines.append("float SpeedLoop_Update(MotorController_t *mc, float speed_ref, float speed_meas) {")
    c_lines.append("    return pi_update(&mc->speed, speed_ref, speed_meas);")
    c_lines.append("}")
    c_lines.append("")

    # 位置环更新函数
    if has_pos:
        c_lines.append("/* Position loop update (PD controller, output = speed reference) */")
        c_lines.append("float PositionLoop_Update(MotorController_t *mc, float pos_ref, float pos_meas) {")
        c_lines.append("    float error = pos_ref - pos_meas;")
        c_lines.append("    float output = mc->position.Kp * error;")
        c_lines.append("    /* Derivative on measurement to avoid setpoint kick */")
        c_lines.append("    float derivative = -(pos_meas - mc->position.prev_feedback);")
        c_lines.append("    output += mc->position.Kd * derivative;")
        c_lines.append("    mc->position.prev_feedback = pos_meas;")
        c_lines.append("    /* Clamp */")
        c_lines.append("    if (output > mc->position.output_max) output = mc->position.output_max;")
        c_lines.append("    if (output < mc->position.output_min) output = mc->position.output_min;")
        c_lines.append("    return output;")
        c_lines.append("}")
        c_lines.append("")

    # FOC中断服务函数模板
    c_lines.append("/*=============================================")
    c_lines.append(" * FOC Control ISR Template")
    c_lines.append(" * Call this function at PWM frequency")
    c_lines.append(" * (e.g., in TIM1 UP interrupt for STM32)")
    c_lines.append(" *=============================================*/")
    c_lines.append("/*")
    c_lines.append("void FOC_ISR_Template(MotorController_t *mc) {")
    c_lines.append("    // 1. Read ADC (phase currents)")
    c_lines.append("    float i_a = (float)ADC1->DR * ADC_TO_AMP;")
    c_lines.append("    float i_b = (float)ADC2->DR * ADC_TO_AMP;")
    c_lines.append("    float i_c = -i_a - i_b; // Kirchhoff")
    c_lines.append("    ")
    c_lines.append("    // 2. Clarke transform: abc -> alpha-beta")
    c_lines.append("    float i_alpha = i_a;")
    c_lines.append("    float i_beta = (2*i_b + i_a) * 0.57735026919f; // 1/sqrt(3)")
    c_lines.append("    ")
    c_lines.append("    // 3. Park transform: alpha-beta -> d-q")
    c_lines.append("    //    Requires rotor angle from encoder/observer")
    c_lines.append("    float sin_val = sinf(angle);")
    c_lines.append("    float cos_val = cosf(angle);")
    c_lines.append("    float id_meas = i_alpha * cos_val + i_beta * sin_val;")
    c_lines.append("    float iq_meas = -i_alpha * sin_val + i_beta * cos_val;")
    c_lines.append("    ")
    c_lines.append("    // 4. Speed/Position loop (outer loops, lower rate)")
    c_lines.append("    //    Run speed loop at 1/N of current loop rate")
    c_lines.append("    if (++speed_loop_counter >= SPEED_LOOP_DIV) {")
    c_lines.append("        speed_loop_counter = 0;")
    c_lines.append("        iq_ref = SpeedLoop_Update(mc, speed_ref, speed_meas);")
    c_lines.append("        id_ref = 0.0f; // Id=0 control for SPMSM")
    c_lines.append("    }")
    c_lines.append("    ")
    c_lines.append("    // 5. Current loop (inner loop, every ISR)")
    if has_ff:
        c_lines.append("    float omega_e = pole_pairs * speed_meas;")
        c_lines.append("    float vd_out, vq_out;")
        c_lines.append("    CurrentLoop_Update(mc, id_ref, iq_ref, id_meas, iq_meas,")
        c_lines.append("                       omega_e, &vd_out, &vq_out);")
    else:
        c_lines.append("    float vd_out, vq_out;")
        c_lines.append("    CurrentLoop_Update(mc, id_ref, iq_ref, id_meas, iq_meas,")
        c_lines.append("                       &vd_out, &vq_out);")
    c_lines.append("    ")
    c_lines.append("    // 6. Inverse Park: d-q -> alpha-beta")
    c_lines.append("    float valpha = vd_out * cos_val - vq_out * sin_val;")
    c_lines.append("    float vbeta  = vd_out * sin_val + vq_out * cos_val;")
    c_lines.append("    ")
    c_lines.append("    // 7. SVPWM: alpha-beta -> duty cycles")
    c_lines.append("    //    (Insert your SVPWM implementation here)")
    c_lines.append("    ")
    c_lines.append("    // 8. Write PWM compare registers")
    c_lines.append("    // TIM1->CCR1 = duty_a;")
    c_lines.append("    // TIM1->CCR2 = duty_b;")
    c_lines.append("    // TIM1->CCR3 = duty_c;")
    c_lines.append("}")
    c_lines.append("*/")

    source = "\n".join(c_lines)

    return {"header": header, "source": source}



# ============================================================
# v4 新增功能: 阶跃响应仿真
# ============================================================

def simulate_step_response(loop_type, Kp, Ki, Kd, Ts, plant_params, steps=2000, ref=1.0, output_limit=None):
    """
    离散时间阶跃响应仿真
    模拟PI/PID控制器+电机模型的闭环阶跃响应
    """
    if loop_type == "current":
        Rs = plant_params["Rs"]
        Ls = plant_params["Ls"]
        if output_limit is None:
            output_limit = 12.0
    elif loop_type == "speed":
        J = plant_params["J"]
        B = plant_params["B"]
        Kt = plant_params["Kt"]
        if output_limit is None:
            output_limit = 10.0
    elif loop_type == "position":
        if output_limit is None:
            output_limit = 500.0
    else:
        raise ValueError("loop_type must be current/speed/position")

    # State variables
    state = 0.0  # plant output (current, speed, or position)
    integral = 0.0
    prev_fb = 0.0

    time_series = []
    peak = 0.0
    settled = False
    settle_time = None
    rise_10 = None
    rise_90 = None

    Ki_d = Ki * Ts
    Kd_d = Kd / Ts if Kd != 0 else 0.0

    for i in range(steps):
        t = i * Ts
        error = ref - state

        # PI output
        output = Kp * error

        # Integral with anti-windup (clamping)
        integral_new = integral + Ki_d * error
        output_test = output + integral_new
        if output_test > output_limit:
            if error < 0:
                integral = integral_new
            output = output_limit
        elif output_test < -output_limit:
            if error > 0:
                integral = integral_new
            output = -output_limit
        else:
            integral = integral_new
            output = output_test

        # Derivative (on measurement)
        if Kd_d != 0:
            derivative = -(state - prev_fb)
            output += Kd_d * derivative
        prev_fb = state

        # Plant update (Euler integration)
        if loop_type == "current":
            # di/dt = (V - Rs*i) / Ls
            state += Ts * (output - Rs * state) / Ls
        elif loop_type == "speed":
            # dω/dt = (Kt*i - B*ω) / J
            state += Ts * (Kt * output - B * state) / J
        elif loop_type == "position":
            # dθ/dt = ω (integrator)
            state += Ts * output

        # Track metrics
        if state > peak:
            peak = state

        if rise_10 is None and state >= 0.1 * ref:
            rise_10 = t
        if rise_90 is None and state >= 0.9 * ref:
            rise_90 = t

        if abs(state - ref) < 0.02 * abs(ref) and not settled:
            if i > 10:  # skip initial transient
                settled = True
                settle_time = t
        elif abs(state - ref) >= 0.02 * abs(ref):
            settled = False
            settle_time = None

        # Sample every 10 steps
        if i % 10 == 0:
            time_series.append([round(t, 8), round(output, 8), round(state, 8)])

    # Calculate performance metrics
    steady_state_error = ref - state
    overshoot = ((peak - ref) / ref * 100) if ref != 0 else 0
    if overshoot < 0:
        overshoot = 0

    rise_time = None
    if rise_10 is not None and rise_90 is not None:
        rise_time = rise_90 - rise_10

    return {
        "loop_type": loop_type,
        "time_series": time_series,
        "performance": {
            "rise_time_10_to_90_s": round(rise_time, 8) if rise_time else None,
            "settling_time_2pct_s": round(settle_time, 8) if settle_time else None,
            "overshoot_pct": round(overshoot, 4),
            "steady_state_error": round(steady_state_error, 8),
            "peak_value": round(peak, 8),
            "final_value": round(state, 8),
        },
        "controller_params": {
            "Kp": Kp, "Ki": Ki, "Kd": Kd,
            "Ki_digital": round(Ki_d, 10),
            "Kd_digital": round(Kd_d, 10),
            "Ts": Ts, "steps": steps, "ref": ref,
            "output_limit": output_limit,
        },
        "method": "离散时间阶跃响应仿真 (Discrete-time Step Response Simulation)",
        "formula": "PI/PID + 电机模型离散仿真, 抗积分饱和(clamping), Ts步长Euler积分",
    }


# ============================================================
# v4 新增功能: 参数灵敏度分析
# ============================================================

def sensitivity_analysis(base_params, loop_type, variation_pct=30):
    """
    电机参数变化对PI参数的灵敏度分析
    """
    results = []
    omega_c = 2 * math.pi * base_params["bw"]
    zeta = base_params.get("zeta", 0.707)

    if loop_type == "current":
        Rs = base_params["Rs"]
        Ls = base_params["Ls"]
        Kp_base = Ls * omega_c
        Ki_base = Rs * omega_c

        for param_name, base_val, calc_kp, calc_ki in [
            ("Rs", Rs, lambda v: Kp_base, lambda v: v * omega_c),
            ("Ls", Ls, lambda v: v * omega_c, lambda v: Ki_base),
        ]:
            for delta in [-variation_pct, +variation_pct]:
                new_val = base_val * (1 + delta / 100)
                new_kp = calc_kp(new_val)
                new_ki = calc_ki(new_val)
                kp_dev = (new_kp - Kp_base) / Kp_base * 100 if Kp_base != 0 else 0
                ki_dev = (new_ki - Ki_base) / Ki_base * 100 if Ki_base != 0 else 0
                max_dev = max(abs(kp_dev), abs(ki_dev))
                if max_dev < 10:
                    rating = "低"
                elif max_dev < 25:
                    rating = "中"
                else:
                    rating = "高"
                results.append({
                    "param": param_name, "variation_pct": delta,
                    "original": base_val, "new_value": new_val,
                    "Kp_base": round(Kp_base, 8), "Kp_new": round(new_kp, 8),
                    "Ki_base": round(Ki_base, 8), "Ki_new": round(new_ki, 8),
                    "Kp_deviation_pct": round(kp_dev, 4),
                    "Ki_deviation_pct": round(ki_dev, 4),
                    "sensitivity": rating,
                })

    elif loop_type == "speed":
        J = base_params["J"]
        B = base_params.get("B", 0)
        Kt = base_params["Kt"]
        Kp_base = (2 * zeta * omega_c * J - B) / Kt
        Ki_base = omega_c ** 2 * J / Kt

        for param_name, base_val, calc_kp, calc_ki in [
            ("J", J,
             lambda v: (2 * zeta * omega_c * v - B) / Kt,
             lambda v: omega_c ** 2 * v / Kt),
            ("Kt", Kt,
             lambda v: (2 * zeta * omega_c * J - B) / v,
             lambda v: omega_c ** 2 * J / v),
        ]:
            for delta in [-variation_pct, +variation_pct]:
                new_val = base_val * (1 + delta / 100)
                new_kp = calc_kp(new_val)
                new_ki = calc_ki(new_val)
                kp_dev = (new_kp - Kp_base) / abs(Kp_base) * 100 if Kp_base != 0 else 0
                ki_dev = (new_ki - Ki_base) / abs(Ki_base) * 100 if Ki_base != 0 else 0
                max_dev = max(abs(kp_dev), abs(ki_dev))
                if max_dev < 10:
                    rating = "低"
                elif max_dev < 25:
                    rating = "中"
                else:
                    rating = "高"
                results.append({
                    "param": param_name, "variation_pct": delta,
                    "original": base_val, "new_value": new_val,
                    "Kp_base": round(Kp_base, 8), "Kp_new": round(new_kp, 8),
                    "Ki_base": round(Ki_base, 8), "Ki_new": round(new_ki, 8),
                    "Kp_deviation_pct": round(kp_dev, 4),
                    "Ki_deviation_pct": round(ki_dev, 4),
                    "sensitivity": rating,
                })

    return {
        "loop_type": loop_type,
        "variation_pct": variation_pct,
        "base_bandwidth_hz": base_params["bw"],
        "base_Kp": round(Kp_base, 8) if loop_type in ("current", "speed") else None,
        "base_Ki": round(Ki_base, 8) if loop_type in ("current", "speed") else None,
        "results": results,
        "method": "参数灵敏度分析 (Parameter Sensitivity Analysis)",
        "formula": "对Rs/Ls(J/Kt)施加±%d%%变化, 计算Kp/Ki偏差百分比, 评级: 低<10%%, 中10-25%%, 高>25%%" % variation_pct,
    }


# ============================================================
# v4 新增功能: 多种离散化方法对比
# ============================================================

def discretize_params_advanced(Kp, Ki, Kd, Ts, method="forward"):
    """
    三种离散化方法对比: 前向欧拉/后向欧拉/Tustin(双线性)
    """
    if Ts is None or Ts <= 0:
        raise ValueError("采样周期Ts必须为正数（不能为0或负），否则离散化无意义")
    methods = {
        "forward": {
            "name": "前向欧拉 (Forward Euler)",
            "Ki_d": Ki * Ts,
            "Kd_d": Kd / Ts if Kd != 0 else 0,
            "integral_code": "integral += Ki_d * error;",
            "stability": "条件稳定, 可能产生不稳定零点",
        },
        "backward": {
            "name": "后向欧拉 (Backward Euler)",
            "Ki_d": Ki * Ts,
            "Kd_d": Kd / Ts if Kd != 0 else 0,
            "integral_code": "integral += Ki_d * error;  // 误差用当前步(实现差异在采样时序)",
            "stability": "无条件稳定",
        },
        "tustin": {
            "name": "Tustin双线性 (Bilinear/Tustin)",
            "Ki_d": Ki * Ts / 2,
            "Kd_d": 2 * Kd / Ts if Kd != 0 else 0,
            "integral_code": "integral += Ki_d * (error + prev_error);",
            "stability": "精度最高, 保持频率响应形状",
        },
    }

    if method == "all":
        output = {}
        for key, info in methods.items():
            output[key] = {
                "name": info["name"],
                "Kp_digital": Kp,
                "Ki_digital": round(info["Ki_d"], 10),
                "Kd_digital": round(info["Kd_d"], 10),
                "integral_update_code": info["integral_code"],
                "stability": info["stability"],
            }
        return {
            "method": "多种离散化方法对比 (Discretization Comparison)",
            "comparison": output,
            "Ts": Ts,
            "original_params": {"Kp": Kp, "Ki": Ki, "Kd": Kd},
            "recommendation": "工程实践推荐Tustin法(精度最高), 资源受限时用前向欧拉",
        }
    else:
        info = methods.get(method, methods["forward"])
        return {
            "method": info["name"],
            "Kp_digital": Kp,
            "Ki_digital": round(info["Ki_d"], 10),
            "Kd_digital": round(info["Kd_d"], 10),
            "integral_update_code": info["integral_code"],
            "stability": info["stability"],
            "Ts": Ts,
            "original_params": {"Kp": Kp, "Ki": Ki, "Kd": Kd},
        }


# ============================================================
# v4 新增功能: 弱磁控制参数计算
# ============================================================

def calculate_field_weakening(psi_f, Ls, Vbus, pole_pairs, rated_speed_rpm, max_speed_rpm):
    """
    弱磁控制(Field Weakening)参数计算
    """
    if psi_f <= 0 or Ls <= 0 or Vbus <= 0:
        raise ValueError("psi_f, Ls, Vbus必须为正数")

    Vmax = Vbus / math.sqrt(3)
    omega_base = Vmax / psi_f  # rad/s (electrical)
    n_base = omega_base * 60 / (2 * math.pi * pole_pairs)  # rpm (mechanical)

    # Maximum weakening current (demagnetization limit)
    Id_fw_max = -psi_f / Ls

    # K_fw coefficient for proportional FW control
    K_fw = 1.0 / Ls

    # Generate 5 points from base speed to max speed
    fw_points = []
    if max_speed_rpm > n_base:
        for i in range(5):
            ratio = i / 4.0
            n = n_base + (max_speed_rpm - n_base) * ratio
            omega_e = 2 * math.pi * pole_pairs * n / 60  # rad/s electrical
            if omega_e > omega_base:
                Id_fw = (Vmax / omega_e - psi_f) / Ls
                if Id_fw < Id_fw_max:
                    Id_fw = Id_fw_max
            else:
                Id_fw = 0.0
            fw_points.append({
                "speed_rpm": round(n, 2),
                "omega_e_rad_s": round(omega_e, 4),
                "Id_fw_A": round(Id_fw, 6),
            })
    else:
        fw_points.append({
            "speed_rpm": round(n_base, 2),
            "omega_e_rad_s": round(omega_base, 4),
            "Id_fw_A": 0.0,
        })

    # C code snippet
    c_code = (
        "/* Field Weakening Control */\n"
        "#define FW_K               (%.6ef)   /* 1/Ls */\n"
        "#define FW_ID_MAX_NEG      (%.6ef)   /* -psi_f/Ls demagnetization limit */\n"
        "#define FW_OMEGA_BASE      (%.6ef)   /* base electrical speed rad/s */\n"
        "#define FW_VMAX            (%.6ef)   /* Vbus/sqrt(3) */\n"
        "\n"
        "float calc_Id_fw(float omega_e) {\n"
        "    if (omega_e <= FW_OMEGA_BASE) return 0.0f;\n"
        "    float Id_fw = (FW_VMAX / omega_e - %.6ef) * FW_K;\n"
        "    if (Id_fw < FW_ID_MAX_NEG) Id_fw = FW_ID_MAX_NEG;\n"
        "    return Id_fw;\n"
        "}"
    ) % (K_fw, Id_fw_max, omega_base, Vmax, psi_f)

    return {
        "base_speed_rpm": round(n_base, 2),
        "rated_speed_rpm": rated_speed_rpm,
        "max_speed_rpm": max_speed_rpm,
        "omega_base_rad_s": round(omega_base, 4),
        "Vmax": round(Vmax, 4),
        "Id_fw_max_demag_A": round(Id_fw_max, 6),
        "K_fw": round(K_fw, 6),
        "fw_curve_points": fw_points,
        "c_code": c_code,
        "method": "弱磁控制参数计算 (Field Weakening Control)",
        "formula": (
            "基速: omega_base = Vmax/psi_f = %.4f/%.6f = %.4f rad/s, n_base = %.2f rpm\n"
            "弱磁电流: Id_fw = (Vmax/omega_e - psi_f) / Ls (当omega_e > omega_base)\n"
            "退磁极限: Id_fw_max = -psi_f/Ls = %.6f A"
        ) % (Vmax, psi_f, omega_base, n_base, Id_fw_max),
    }


# ============================================================
# v4 新增功能: 观测器增益计算
# ============================================================

def calculate_observer_gains(Rs, Ls, psi_f, pole_pairs, bandwidth_hz, observer_type="smo", max_speed_rpm=3000):
    """
    观测器增益计算: SMO(滑模) / Luenberger(龙伯格)
    """
    result = {}

    omega_obs = 2 * math.pi * bandwidth_hz * 2  # observer bandwidth = 2x current loop
    zeta_obs = 0.707

    if observer_type in ("smo", "all"):
        omega_e_max = 2 * math.pi * pole_pairs * max_speed_rpm / 60
        K_smo = omega_e_max * psi_f * 1.5
        f_cutoff = bandwidth_hz * 2
        omega_cutoff = 2 * math.pi * f_cutoff
        # Phase compensation at max speed
        theta_comp_max = math.atan2(omega_e_max, omega_cutoff) if omega_cutoff > 0 else 0

        smo_c_code = (
            "/* SMO Observer */\n"
            "#define SMO_K              (%.6ef)   /* K_smo = omega_e_max * psi_f * 1.5 */\n"
            "#define SMO_FCUTOFF        (%.4f)     /* Low-pass filter cutoff Hz */\n"
            "#define SMO_RS_OVER_LS     (%.6ef)   /* Rs/Ls */\n"
            "#define SMO_INV_LS         (%.6ef)   /* 1/Ls */\n"
            "\n"
            "static float i_alpha_est = 0, i_beta_est = 0;\n"
            "static float z_alpha = 0, z_beta = 0;\n"
            "static float emf_alpha_f = 0, emf_beta_f = 0;\n"
            "\n"
            "void smo_update(float valpha, float vbeta, float ialpha, float ibeta, float Ts) {\n"
            "    float i_alpha_err = i_alpha_est - ialpha;\n"
            "    float i_beta_err = i_beta_est - ibeta;\n"
            "    z_alpha = (i_alpha_err > 0) ? SMO_K : -SMO_K;\n"
            "    z_beta = (i_beta_err > 0) ? SMO_K : -SMO_K;\n"
            "    i_alpha_est += Ts * (-SMO_RS_OVER_LS * i_alpha_est + SMO_INV_LS * valpha - SMO_INV_LS * z_alpha);\n"
            "    i_beta_est += Ts * (-SMO_RS_OVER_LS * i_beta_est + SMO_INV_LS * vbeta - SMO_INV_LS * z_beta);\n"
            "    float alpha = 6.28318530718 * SMO_FCUTOFF * Ts;\n"
            "    emf_alpha_f += alpha * (z_alpha - emf_alpha_f);\n"
            "    emf_beta_f += alpha * (z_beta - emf_beta_f);\n"
            "}"
        ) % (K_smo, f_cutoff, Rs / Ls, 1.0 / Ls)

        result["smo"] = {
            "K_smo": round(K_smo, 6),
            "omega_e_max": round(omega_e_max, 4),
            "f_cutoff_hz": round(f_cutoff, 4),
            "theta_comp_max_deg": round(math.degrees(theta_comp_max), 4),
            "Rs_over_Ls": round(Rs / Ls, 6),
            "inv_Ls": round(1.0 / Ls, 6),
            "c_code": smo_c_code,
            "method": "滑模观测器 (Sliding Mode Observer)",
            "formula": "K_smo = omega_e_max * psi_f * 1.5 = %.4f * %.6f * 1.5 = %.6f" % (omega_e_max, psi_f, K_smo),
        }

    if observer_type in ("luenberger", "all"):
        L1 = 2 * zeta_obs * omega_obs * Ls
        L2 = omega_obs ** 2 * Ls

        luenberger_c_code = (
            "/* Luenberger Full-Order Observer */\n"
            "#define OBS_L1             (%.6ef)   /* Current error gain */\n"
            "#define OBS_L2             (%.6ef)   /* Back-EMF error gain */\n"
            "#define OBS_RS_OVER_LS     (%.6ef)\n"
            "#define OBS_INV_LS         (%.6ef)\n"
            "#define OBS_INV_PSI_F      (%.6ef)\n"
            "\n"
            "static float i_alpha_est = 0, i_beta_est = 0;\n"
            "static float emf_alpha = 0, emf_beta = 0;\n"
            "\n"
            "void luenberger_update(float valpha, float vbeta, float ialpha, float ibeta, float Ts) {\n"
            "    float i_err_a = i_alpha_est - ialpha;\n"
            "    float i_err_b = i_beta_est - ibeta;\n"
            "    i_alpha_est += Ts * (-OBS_RS_OVER_LS * i_alpha_est + OBS_INV_LS * (valpha - emf_alpha) - OBS_L1 * i_err_a);\n"
            "    i_beta_est += Ts * (-OBS_RS_OVER_LS * i_beta_est + OBS_INV_LS * (vbeta - emf_beta) - OBS_L1 * i_err_b);\n"
            "    emf_alpha += Ts * (OBS_L2 * i_err_a);\n"
            "    emf_beta += Ts * (OBS_L2 * i_err_b);\n"
            "}"
        ) % (L1, L2, Rs / Ls, 1.0 / Ls, 1.0 / psi_f if psi_f > 0 else 0)

        result["luenberger"] = {
            "L1": round(L1, 6),
            "L2": round(L2, 6),
            "omega_obs_rad_s": round(omega_obs, 4),
            "zeta_obs": zeta_obs,
            "Rs_over_Ls": round(Rs / Ls, 6),
            "inv_Ls": round(1.0 / Ls, 6),
            "c_code": luenberger_c_code,
            "method": "龙伯格全阶观测器 (Luenberger Full-Order Observer)",
            "formula": (
                "omega_obs = 2*pi*BW*2 = %.4f rad/s, zeta=0.707\n"
                "L1 = 2*zeta*omega_obs*Ls = %.6f\n"
                "L2 = omega_obs^2 * Ls = %.6f"
            ) % (omega_obs, L1, L2),
        }

    if observer_type == "all":
        result["comparison"] = {
            "smo": "适合高速, 结构简单, 但有抖振问题",
            "luenberger": "全阶观测器, 平滑无抖振, 但需要精确参数",
            "recommendation": "低成本方案选SMO, 高精度方案选Luenberger",
        }

    return result


# ============================================================
# v4 新增功能: 电机参数库
# ============================================================

MOTOR_PRESETS = {
    "2207-1500KV": {
        "Rs": 0.052, "Ls": 8.5e-6, "Kt": 0.0065, "pole_pairs": 7,
        "rated_current": 20, "max_current": 30,
        "description": "航模穿越机电机, 22mm定子, 高速低电感",
    },
    "2804-380KV": {
        "Rs": 0.235, "Ls": 3.2e-5, "Kt": 0.0252, "pole_pairs": 7,
        "rated_current": 8, "max_current": 12,
        "description": "小型云台电机, 28mm定子, 中速",
    },
    "5010-340KV": {
        "Rs": 0.113, "Ls": 1.5e-4, "Kt": 0.0425, "pole_pairs": 10,
        "rated_current": 12, "max_current": 18,
        "description": "大型云台/载重电机, 50mm定子",
    },
    "6354-260KV": {
        "Rs": 0.039, "Ls": 2.8e-5, "Kt": 0.0578, "pole_pairs": 7,
        "rated_current": 40, "max_current": 60,
        "description": "电动滑板/机器人驱动电机, 63mm定子",
    },
    "8318-100KV": {
        "Rs": 0.045, "Ls": 6.2e-4, "Kt": 0.0955, "pole_pairs": 20,
        "rated_current": 25, "max_current": 35,
        "description": "大型载重电机, 83mm定子, 高转矩",
    },
    "GBM2804-120KV": {
        "Rs": 0.65, "Ls": 1.8e-4, "Kt": 0.0796, "pole_pairs": 7,
        "rated_current": 3, "max_current": 5,
        "description": "Gimbal Motor, 低速大转矩, 高电阻",
    },
    "B5045-330KV": {
        "Rs": 0.025, "Ls": 3.0e-5, "Kt": 0.029, "pole_pairs": 5,
        "rated_current": 35, "max_current": 50,
        "description": "中型多旋翼电机, 50mm定子",
    },
    "4250-650KV": {
        "Rs": 0.041, "Ls": 1.5e-5, "Kt": 0.0146, "pole_pairs": 5,
        "rated_current": 30, "max_current": 45,
        "description": "穿越机电机, 42mm定子, 高速",
    },
    "2306-2400KV": {
        "Rs": 0.028, "Ls": 3.8e-6, "Kt": 0.0041, "pole_pairs": 12,
        "rated_current": 18, "max_current": 28,
        "description": "5寸穿越机电机, 23mm定子, 超高KV",
    },
    "AK80-9": {
        "Rs": 0.5, "Ls": 2.0e-3, "Kt": 0.09, "pole_pairs": 14,
        "rated_current": 12, "max_current": 20,
        "description": "MIT Cheetah关节电机, 大电感大转矩",
    },
}


def get_motor_preset(preset_name=None):
    """获取电机预设参数"""
    if preset_name is None:
        presets_list = []
        for name, params in MOTOR_PRESETS.items():
            presets_list.append({
                "name": name,
                "description": params["description"],
                "Rs": params["Rs"],
                "Ls": params["Ls"],
                "Kt": params["Kt"],
                "pole_pairs": params["pole_pairs"],
                "rated_current_A": params["rated_current"],
            })
        return {
            "available_presets": presets_list,
            "count": len(presets_list),
            "method": "电机参数库 (Motor Parameter Database)",
            "usage": "使用 --preset-name \"型号\" 查看完整参数",
        }

    if preset_name not in MOTOR_PRESETS:
        return {
            "error": "未找到电机型号: %s" % preset_name,
            "available": list(MOTOR_PRESETS.keys()),
        }

    p = MOTOR_PRESETS[preset_name]
    psi_f = p["Kt"] / (1.5 * p["pole_pairs"])
    J_est = 0.001

    return {
        "name": preset_name,
        "Rs": p["Rs"],
        "Ls": p["Ls"],
        "Kt": p["Kt"],
        "psi_f": round(psi_f, 8),
        "pole_pairs": p["pole_pairs"],
        "rated_current_A": p["rated_current"],
        "max_current_A": p["max_current"],
        "J_estimated": J_est,
        "description": p["description"],
        "method": "电机参数库 (Motor Parameter Database)",
        "formula": "psi_f = Kt / (1.5 * pole_pairs) = %.6f / (1.5 * %d) = %.8f Wb" % (p["Kt"], p["pole_pairs"], psi_f),
    }


# ============================================================
# v4 新增功能: 自动带宽建议
# ============================================================

def suggest_bandwidth(pwm_freq_hz, motor_params=None):
    """
    根据PWM频率自动建议三环带宽
    """
    pwm_freq_hz_actual = pwm_freq_hz * 1000  # kHz to Hz

    # Current loop bandwidth
    bw_current = min(pwm_freq_hz_actual / 10, 2000)

    if motor_params and "Rs" in motor_params and "Ls" in motor_params:
        tau_elec = motor_params["Ls"] / motor_params["Rs"]
        bw_elec_limit = 1 / (2 * math.pi * tau_elec) * 0.5
        bw_current = min(bw_current, bw_elec_limit)
        elec_constraint = True
    else:
        elec_constraint = False

    bw_speed = bw_current / 10
    bw_position = bw_speed / 10

    Ts_suggest = 1 / (2 * pwm_freq_hz_actual)

    return {
        "pwm_freq_hz": pwm_freq_hz_actual,
        "current_loop": {
            "bandwidth_hz": round(bw_current, 2),
            "bandwidth_rad_s": round(2 * math.pi * bw_current, 4),
        },
        "speed_loop": {
            "bandwidth_hz": round(bw_speed, 2),
            "bandwidth_rad_s": round(2 * math.pi * bw_speed, 4),
        },
        "position_loop": {
            "bandwidth_hz": round(bw_position, 2),
            "bandwidth_rad_s": round(2 * math.pi * bw_position, 4),
        },
        "sampling_period_s": round(Ts_suggest, 8),
        "bandwidth_ratios": {
            "current_to_speed": 10,
            "speed_to_position": 10,
            "status": "合理 (内环≥外环10倍)",
        },
        "constraints": {
            "pwm_constraint": "BW_current < fpwm/10 = %d/10 = %d Hz" % (pwm_freq_hz_actual, pwm_freq_hz_actual // 10),
            "elec_constraint_applied": elec_constraint,
        },
        "method": "自动带宽建议 (Auto Bandwidth Suggestion)",
        "formula": "BW_current = min(fpwm/10, 2000Hz), BW_speed = BW_current/10, BW_position = BW_speed/10",
    }


# ============================================================
# v4 新增功能: MATLAB格式导出
# ============================================================

def export_matlab(params, loop_type):
    """
    生成MATLAB .m文件代码
    """
    Kp = params["Kp"]
    Ki = params["Ki"]
    Kd = params.get("Kd", 0)

    if loop_type == "current":
        Rs = params.get("Rs", 0.5)
        Ls = params.get("Ls", 2e-3)
        code = (
            "%% Motor Current Loop Analysis\n"
            "%% Auto-generated by Motor PID Tuner\n\n"
            "Rs = %.6f;  %% Stator resistance (Ohm)\n"
            "Ls = %.6e;  %% Stator inductance (H)\n"
            "Kp = %.6f;  %% Proportional gain\n"
            "Ki = %.6f;  %% Integral gain\n\n"
            "%% Plant: Gp = 1/(Ls*s + Rs)\n"
            "Gp = tf(1, [Ls, Rs]);\n\n"
            "%% Controller: Gc = Kp + Ki/s = (Kp*s + Ki)/s\n"
            "Gc = tf([Kp, Ki], [1, 0]);\n\n"
            "%% Closed-loop: Gcl = Gc*Gp / (1 + Gc*Gp)\n"
            "Gcl = feedback(Gc * Gp, 1);\n\n"
            "%% Step response\n"
            "figure;\n"
            "step(Gcl);\n"
            "title('Current Loop Step Response');\n"
            "xlabel('Time (s)');\n"
            "ylabel('Current (A)');\n"
            "grid on;\n\n"
            "%% Bode plot\n"
            "figure;\n"
            "bode(Gcl);\n"
            "title('Current Loop Bode Plot');\n"
            "grid on;\n\n"
            "%% Stability margins\n"
            "[Gm, Pm, Wcg, Wcp] = margin(Gcl);\n"
            "fprintf('Gain Margin: %%.2f dB at %%.2f rad/s\\n', 20*log10(Gm), Wcg);\n"
            "fprintf('Phase Margin: %%.2f deg at %%.2f rad/s\\n', Pm, Wcp);\n"
        ) % (Rs, Ls, Kp, Ki)

    elif loop_type == "speed":
        J = params.get("J", 1e-5)
        B = params.get("B", 0)
        Kt = params.get("Kt", 0.01)
        code = (
            "%% Motor Speed Loop Analysis\n"
            "%% Auto-generated by Motor PID Tuner\n\n"
            "J = %.6e;   %% Inertia (kg.m^2)\n"
            "B = %.6f;   %% Friction (N.m.s/rad)\n"
            "Kt = %.6f;  %% Torque constant (N.m/A)\n"
            "Kp = %.6f;  %% Proportional gain\n"
            "Ki = %.6f;  %% Integral gain\n\n"
            "%% Plant: Gp = Kt/(J*s + B)\n"
            "Gp = tf(Kt, [J, B]);\n\n"
            "%% Controller: Gc = (Kp*s + Ki)/s\n"
            "Gc = tf([Kp, Ki], [1, 0]);\n\n"
            "%% Closed-loop\n"
            "Gcl = feedback(Gc * Gp, 1);\n\n"
            "%% Step response\n"
            "figure;\n"
            "step(Gcl);\n"
            "title('Speed Loop Step Response');\n"
            "xlabel('Time (s)');\n"
            "ylabel('Speed (rad/s)');\n"
            "grid on;\n\n"
            "%% Bode plot\n"
            "figure;\n"
            "bode(Gcl);\n"
            "title('Speed Loop Bode Plot');\n"
            "grid on;\n\n"
            "[Gm, Pm, Wcg, Wcp] = margin(Gcl);\n"
            "fprintf('Gain Margin: %%.2f dB at %%.2f rad/s\\n', 20*log10(Gm), Wcg);\n"
            "fprintf('Phase Margin: %%.2f deg at %%.2f rad/s\\n', Pm, Wcp);\n"
        ) % (J, B, Kt, Kp, Ki)

    else:
        code = (
            "%% Motor Position Loop Analysis\n"
            "%% Auto-generated by Motor PID Tuner\n\n"
            "Kp = %.6f;  %% Proportional gain\n"
            "Kd = %.6f;  %% Derivative gain\n\n"
            "%% Plant: integrator 1/s (cascaded with speed loop)\n"
            "Gp = tf(1, [1, 0]);\n\n"
            "%% Controller: PD = Kp + Kd*s\n"
            "Gc = tf([Kd, Kp], 1);\n\n"
            "%% Closed-loop\n"
            "Gcl = feedback(Gc * Gp, 1);\n\n"
            "%% Step response\n"
            "figure;\n"
            "step(Gcl);\n"
            "title('Position Loop Step Response');\n"
            "xlabel('Time (s)');\n"
            "ylabel('Position (rad)');\n"
            "grid on;\n\n"
            "%% Bode plot\n"
            "figure;\n"
            "bode(Gcl);\n"
            "title('Position Loop Bode Plot');\n"
            "grid on;\n"
        ) % (Kp, Kd)

    return {
        "loop_type": loop_type,
        "format": "matlab",
        "code": code,
        "method": "MATLAB格式导出 (MATLAB Export)",
    }


# ============================================================
# v4 新增功能: 完整SVPWM代码生成
# ============================================================

def generate_svpwm_code(vbus, deadtime_ns=500):
    """
    生成完整七段式SVPWM C代码
    """
    Vmax = vbus / math.sqrt(3)
    deadtime_s = deadtime_ns * 1e-9

    code = (
        "/*=============================================\n"
        " * Seven-Segment SVPWM Generator\n"
        " * Auto-generated by Motor PID Tuner\n"
        " * Vbus=%.1fV, Vmax=%.4fV, Deadtime=%dns\n"
        " *=============================================*/\n"
        "\n"
        "#include <math.h>\n"
        "\n"
        "#define SVPWM_VBUS          (%.1ff)\n"
        "#define SVPWM_VMAX          (%.6ff)   /* Vbus/sqrt(3) */\n"
        "#define SVPWM_DEADTIME_NS   (%d)\n"
        "#define SQRT3              (1.7320508075688772f)\n"
        "#define INV_SQRT3          (0.5773502691896258f)\n"
        "\n"
        "/* SVPWM: Valpha, Vbeta -> duty_a, duty_b, duty_c (0.0~1.0) */\n"
        "void svpwm_calc(float valpha, float vbeta, float *duty_a, float *duty_b, float *duty_c) {\n"
        "    /* Step 1: Inverse Clarke to get phase voltages reference */\n"
        "    float va = valpha;\n"
        "    float vb = -0.5f * valpha + 0.5f * SQRT3 * vbeta;\n"
        "    float vc = -0.5f * valpha - 0.5f * SQRT3 * vbeta;\n"
        "\n"
        "    /* Step 2: Sector determination */\n"
        "    int n1 = (vb > 0) ? 1 : 0;\n"
        "    int n2 = (vc > 0) ? 1 : 0;\n"
        "    int n3 = (va > 0) ? 1 : 0;\n"
        "    /* Alternative: use sign of (vb-vc), (vc-va), (va-vb) */\n"
        "    float a = vbeta;\n"
        "    float b = -0.5f * vbeta + 0.5f * SQRT3 * valpha;\n"
        "    float c = -0.5f * vbeta - 0.5f * SQRT3 * valpha;\n"
        "    int na = (a > 0) ? 1 : 0;\n"
        "    int nb = (b > 0) ? 1 : 0;\n"
        "    int nc = (c > 0) ? 1 : 0;\n"
        "    int sector = na + 2*nb + 4*nc;\n"
        "    if (sector == 0) sector = 1;\n"
        "\n"
        "    /* Step 3: T1, T2 calculation */\n"
        "    float x = SQRT3 * vbeta / SVPWM_VMAX;\n"
        "    float y = (1.5f * valpha + 0.5f * SQRT3 * vbeta) / SVPWM_VMAX;\n"
        "    float z = (-1.5f * valpha + 0.5f * SQRT3 * vbeta) / SVPWM_VMAX;\n"
        "    float t1 = 0, t2 = 0;\n"
        "    switch (sector) {\n"
        "        case 1: t1 = -z; t2 =  x; break;  /* Sector 1 */\n"
        "        case 2: t1 =  z; t2 =  y; break;  /* Sector 2 */\n"
        "        case 3: t1 =  x; t2 = -y; break;  /* Sector 3 */\n"
        "        case 4: t1 = -x; t2 =  z; break;  /* Sector 4 */\n"
        "        case 5: t1 = -y; t2 = -z; break;  /* Sector 5 */\n"
        "        case 6: t1 =  y; t2 = -x; break;  /* Sector 6 */\n"
        "        default: t1 = 0; t2 = 0; break;\n"
        "    }\n"
        "    /* Over-modulation clamp */\n"
        "    if (t1 + t2 > 1.0f) {\n"
        "        float k = 1.0f / (t1 + t2);\n"
        "        t1 *= k;\n"
        "        t2 *= k;\n"
        "    }\n"
        "\n"
        "    /* Step 4: Tcm calculation (seven-segment) */\n"
        "    float t0 = 0.5f * (1.0f - t1 - t2);\n"
        "    float tcm_a = 0, tcm_b = 0, tcm_c = 0;\n"
        "    switch (sector) {\n"
        "        case 1: tcm_a = t1 + t2 + t0; tcm_b = t2 + t0;     tcm_c = t0;          break;\n"
        "        case 2: tcm_a = t1 + t0;      tcm_b = t1 + t2 + t0; tcm_c = t0;          break;\n"
        "        case 3: tcm_a = t0;           tcm_b = t1 + t2 + t0; tcm_c = t2 + t0;     break;\n"
        "        case 4: tcm_a = t0;           tcm_b = t1 + t0;      tcm_c = t1 + t2 + t0; break;\n"
        "        case 5: tcm_a = t2 + t0;      tcm_b = t0;           tcm_c = t1 + t2 + t0; break;\n"
        "        case 6: tcm_a = t1 + t2 + t0; tcm_b = t0;           tcm_c = t1 + t0;      break;\n"
        "        default: tcm_a = 0.5f; tcm_b = 0.5f; tcm_c = 0.5f; break;\n"
        "    }\n"
        "\n"
        "    /* Step 5: Duty cycle output (0.0 ~ 1.0) */\n"
        "    *duty_a = tcm_a;\n"
        "    *duty_b = tcm_b;\n"
        "    *duty_c = tcm_c;\n"
        "\n"
        "    /* Step 6: Dead time compensation (optional) */\n"
        "    /* Deadtime = %d ns, applied by hardware timer */\n"
        "    /* For STM32: TIM1->BDTR.DTG = deadtime_ns / (1/fpwm_clk * 2) */\n"
        "}\n"
    ) % (vbus, Vmax, deadtime_ns, vbus, Vmax, deadtime_ns, deadtime_ns)

    return {
        "vbus": vbus,
        "Vmax": round(Vmax, 6),
        "deadtime_ns": deadtime_ns,
        "code": code,
        "method": "七段式SVPWM代码生成 (Seven-Segment SVPWM)",
        "formula": "扇区判断N=sign(A)+2*sign(B)+4*sign(C), T1/T2由x/y/z计算, Tcm七段排列",
    }


# ============================================================
# v4 新增功能: 多平台代码适配
# ============================================================

def generate_platform_code(platform, params):
    """
    多平台硬件初始化代码生成: STM32 / GD32 / C2000
    """
    pwm_freq = params.get("pwm_freq_khz", 20)
    vbus = params.get("vbus", 24)
    imax = params.get("imax", 10)

    if platform == "stm32":
        code = (
            "/*=============================================\n"
            " * STM32 FOC Hardware Init (TIM1 + ADC + DMA)\n"
            " * PWM: %d kHz Center-Aligned, Vbus=%.1fV, Imax=%.1fA\n"
            " *=============================================*/\n"
            "\n"
            "/* TIM1 PWM Configuration (Center-aligned mode) */\n"
            "void TIM1_PWM_Init(void) {\n"
            "    /* Enable TIM1 clock */\n"
            "    RCC->APB2ENR |= RCC_APB2ENR_TIM1EN;\n"
            "    \n"
            "    /* Center-aligned mode 1 */\n"
            "    TIM1->CR1 = TIM_CR1_CMS_0;\n"
            "    \n"
            "    /* Set PWM frequency: ARR = fpclk / (2 * pwm_freq) */\n"
            "    /* Assuming 168MHz APB2: ARR = 168e6/(2*%d000) = %d */\n"
            "    TIM1->PSC = 0;\n"
            "    TIM1->ARR = %d;\n"
            "    \n"
            "    /* CH1-3 as PWM output, CH4 for ADC trigger */\n"
            "    TIM1->CCER |= TIM_CCER_CC1E | TIM_CCER_CC2E | TIM_CCER_CC3E;\n"
            "    TIM1->CCMR1 |= TIM_CCMR1_OC1M_1 | TIM_CCMR1_OC1M_2;  /* PWM mode 1 */\n"
            "    TIM1->CCMR1 |= TIM_CCMR1_OC2M_1 | TIM_CCMR1_OC2M_2;\n"
            "    TIM1->CCMR2 |= TIM_CCMR2_OC3M_1 | TIM_CCMR2_OC3M_2;\n"
            "    \n"
            "    /* Dead time: ~%dns at 168MHz */\n"
            "    TIM1->BDTR |= (42 << TIM_BDTR_DTG_Pos);  /* DT = DTG * 2 / 168e6 */\n"
            "    TIM1->BDTR |= TIM_BDTR_MOE;  /* Main output enable */\n"
            "    \n"
            "    TIM1->CR1 |= TIM_CR1_CEN;\n"
            "}\n"
            "\n"
            "/* ADC Injected Channel for Current Sensing */\n"
            "void ADC_CurrentSense_Init(void) {\n"
            "    RCC->APB2ENR |= RCC_APB2ENR_ADC1EN | RCC_APB2ENR_ADC2EN;\n"
            "    \n"
            "    /* Dual mode, injected simultaneous */\n"
            "    ADC->CCR |= ADC_CCR_DUAL_0 | ADC_CCR_DUAL_2;\n"
            "    \n"
            "    /* Trigger from TIM1 TRGO (update event) */\n"
            "    ADC1->CR2 |= ADC_CR2_JEXTSEL_2;  /* TIM1 TRGO */\n"
            "    ADC1->CR2 |= ADC_CR2_JEXTEN_0;   /* Rising edge */\n"
            "    \n"
            "    /* JSQR: 2 injected channels, 12-bit */\n"
            "    /* ADC1: Phase A current (PA0), ADC2: Phase B current (PA1) */\n"
            "    ADC1->JSQR = (1 << 15);  /* 1 conversion, channel 1 */\n"
            "    ADC2->JSQR = (2 << 15);  /* 1 conversion, channel 2 */\n"
            "    \n"
            "    ADC1->CR2 |= ADC_CR2_ADON;\n"
            "    ADC2->CR2 |= ADC_CR2_ADON;\n"
            "}\n"
        ) % (pwm_freq, vbus, imax, pwm_freq, int(168e6 / (2 * pwm_freq * 1000)), int(168e6 / (2 * pwm_freq * 1000)), 500)

    elif platform == "gd32":
        code = (
            "/*=============================================\n"
            " * GD32 FOC Hardware Init (TIMER0 + ADC)\n"
            " * PWM: %d kHz Center-Aligned, Vbus=%.1fV, Imax=%.1fA\n"
            " * Note: GD32 register names differ from STM32\n"
            " *=============================================*/\n"
            "\n"
            "/* TIMER0 PWM Configuration (equivalent to STM32 TIM1) */\n"
            "void TIMER0_PWM_Init(void) {\n"
            "    rcu_periph_clock_enable(RCU_TIMER0);\n"
            "    \n"
            "    /* Center-aligned mode */\n"
            "    TIMER_CTL0(TIMER0) |= TIMER_CTL0_CAM_0;\n"
            "    \n"
            "    /* ARR = fpclk / (2 * pwm_freq) */\n"
            "    /* Assuming 120MHz APB2: ARR = 120e6/(2*%d000) = %d */\n"
            "    TIMER_PSC(TIMER0) = 0;\n"
            "    TIMER_CAR(TIMER0) = %d;\n"
            "    \n"
            "    /* CH0-2 PWM output */\n"
            "    TIMER_CH0CV(TIMER0) = 0;  /* duty_a */\n"
            "    TIMER_CH1CV(TIMER0) = 0;  /* duty_b */\n"
            "    TIMER_CH2CV(TIMER0) = 0;  /* duty_c */\n"
            "    \n"
            "    /* Dead time config */\n"
            "    TIMER_CCHP(TIMER0) |= (42 << TIMER_CCHP_DTCFG_Pos);\n"
            "    TIMER_CCHP(TIMER0) |= TIMER_CCHP_POEN;\n"
            "    \n"
            "    TIMER_CTL0(TIMER0) |= TIMER_CTL0_CEN;\n"
            "}\n"
            "\n"
            "/* ADC Regular Group for Current Sensing */\n"
            "void ADC_CurrentSense_Init(void) {\n"
            "    rcu_periph_clock_enable(RCU_ADC0);\n"
            "    \n"
            "    /* ADC triggered by TIMER0 */\n"
            "    adc_external_trigger_source_config(ADC0, ADC_REGULAR_CHANNEL,\n"
            "                                        ADC0_1_EXTTRIG_T0_CH0);\n"
            "    \n"
            "    /* Rule group: 2 channels for phase currents */\n"
            "    adc_regular_channel_config(ADC0, 0, ADC_CHANNEL_0, ADC_SAMPLETIME_15);\n"
            "    adc_regular_channel_config(ADC0, 1, ADC_CHANNEL_1, ADC_SAMPLETIME_15);\n"
            "    \n"
            "    adc_enable(ADC0);\n"
            "}\n"
        ) % (pwm_freq, vbus, imax, pwm_freq, int(120e6 / (2 * pwm_freq * 1000)), int(120e6 / (2 * pwm_freq * 1000)))

    elif platform == "c2000":
        code = (
            "/*=============================================\n"
            " * TI C2000 FOC Hardware Init (ePWM + ADC SOC)\n"
            " * PWM: %d kHz Center-Aligned, Vbus=%.1fV, Imax=%.1fA\n"
            " *=============================================*/\n"
            "\n"
            "/* ePWM1 Configuration (Center-aligned / Up-Down count) */\n"
            "void ePWM1_Init(void) {\n"
            "    /* Enable ePWM clock */\n"
            "    SysCtl_enablePeripheral(SYSCTL_PERIPH_CLK_EPWM1);\n"
            "    \n"
            "    /* Up-Down count mode (center-aligned) */\n"
            "    EPwm1Regs.TBCTL.bit.CTRMODE = TB_COUNT_UPDOWN;\n"
            "    EPwm1Regs.TBCTL.bit.PHSEN = TB_DISABLE;\n"
            "    \n"
            "    /* TBPRD = SYSCLK / (2 * pwm_freq) */\n"
            "    /* Assuming 100MHz: TBPRD = 100e6/(2*%d000) = %d */\n"
            "    EPwm1Regs.TBPRD = %d;\n"
            "    EPwm1Regs.TBCTL.bit.HSPCLKDIV = TB_DIV1;\n"
            "    EPwm1Regs.TBCTL.bit.CLKDIV = TB_DIV1;\n"
            "    \n"
            "    /* AQ: set on CAU, clear on CAD (PWM mode) */\n"
            "    EPwm1Regs.AQCTLA.bit.CAU = AQ_SET;\n"
            "    EPwm1Regs.AQCTLA.bit.CAD = AQ_CLEAR;\n"
            "    EPwm1Regs.AQCTLB.bit.CAU = AQ_SET;\n"
            "    EPwm1Regs.AQCTLB.bit.CAD = AQ_CLEAR;\n"
            "    \n"
            "    /* Dead band module */\n"
            "    EPwm1Regs.DBCTL.bit.OUT_MODE = DB_FULL_ENABLE;\n"
            "    EPwm1Regs.DBCTL.bit.POLSEL = DB_ACTV_HIC;\n"
            "    EPwm1Regs.DBFED = 50;  /* FED = 50 TBCLK cycles (~500ns) */\n"
            "    EPwm1Regs.DBRED = 50;  /* RED = 50 TBCLK cycles (~500ns) */\n"
            "    \n"
            "    /* ADC SOC trigger on TBCTR=0 (PRD event) */\n"
            "    EPwm1Regs.ETSEL.bit.SOCASEL = ET_CTR_PRD;\n"
            "    EPwm1Regs.ETSEL.bit.SOCAEN = 1;\n"
            "    EPwm1Regs.ETPS.bit.SOCAPRD = ET_1ST;\n"
            "}\n"
            "\n"
            "/* ADC SOC Configuration for Current Sensing */\n"
            "void ADC_CurrentSense_Init(void) {\n"
            "    /* SOC0: Phase A current, triggered by ePWM1 SOCA */\n"
            "    AdcaRegs.ADCSOC0CTL.bit.CHSEL = 0;   /* ADCINA0 */\n"
            "    AdcaRegs.ADCSOC0CTL.bit.TRIGSEL = 5;  /* ePWM1 ADCSOCA */\n"
            "    AdcaRegs.ADCSOC0CTL.bit.ACQPS = 14;   /* 15 SYSCLK cycles */\n"
            "    \n"
            "    /* SOC1: Phase B current */\n"
            "    AdcbRegs.ADCSOC0CTL.bit.CHSEL = 0;   /* ADCINB0 */\n"
            "    AdcbRegs.ADCSOC0CTL.bit.TRIGSEL = 5;\n"
            "    AdcbRegs.ADCSOC0CTL.bit.ACQPS = 14;\n"
            "    \n"
            "    /* Enable ADC */\n"
            "    AdcaRegs.ADCCTL1.bit.ADCPWDN = 1;\n"
            "    AdcbRegs.ADCCTL1.bit.ADCPWDN = 1;\n"
            "}\n"
        ) % (pwm_freq, vbus, imax, pwm_freq, int(100e6 / (2 * pwm_freq * 1000)), int(100e6 / (2 * pwm_freq * 1000)))

    else:
        code = "不支持的平台: %s, 可选 stm32/gd32/c2000" % platform

    return {
        "platform": platform,
        "pwm_freq_khz": pwm_freq,
        "vbus": vbus,
        "imax": imax,
        "code": code,
        "method": "多平台代码适配 (Multi-Platform Code Adaptation)",
        "platform_notes": {
            "stm32": "TIM1高级定时器, BDTR死区, ADC注入组双模",
            "gd32": "TIMER0, 寄存器名不同(CAR vs ARR, CCHP vs BDTR)",
            "c2000": "ePWM模块(AQ+DB), ADC SOC硬件触发, 无需DMA",
        },
    }


# ============================================================
# v4 新增功能: 交互式参数引导
# ============================================================

def interactive_guide(target):
    """
    交互式参数引导: 输出参数需求清单
    """
    guides = {
        "current": {
            "loop": "电流环 (Current Loop)",
            "required_params": [
                {"name": "Rs", "unit": "Ω", "desc": "定子电阻", "typical": "0.01~1.0"},
                {"name": "Ls", "unit": "H", "desc": "定子电感", "typical": "1e-6~1e-3"},
                {"name": "bw", "unit": "Hz", "desc": "期望电流环带宽", "typical": "500~2000"},
            ],
            "optional_params": [
                {"name": "ts", "unit": "s", "desc": "采样周期", "typical": "50e-6"},
                {"name": "vbus", "unit": "V", "desc": "母线电压", "typical": "12/24/48"},
                {"name": "imax", "unit": "A", "desc": "最大电流(标幺化用)", "typical": "5~50"},
                {"name": "psi-f", "unit": "Wb", "desc": "永磁体磁链(前馈用)", "typical": "0.001~0.1"},
                {"name": "pole-pairs", "unit": "", "desc": "极对数", "typical": "5~20"},
            ],
            "example": "python main.py --mode current --rs 0.5 --ls 2e-3 --bw 1000",
        },
        "speed": {
            "loop": "速度环 (Speed Loop)",
            "required_params": [
                {"name": "J", "unit": "kg·m²", "desc": "转动惯量", "typical": "1e-6~1e-3"},
                {"name": "Kt", "unit": "N·m/A", "desc": "转矩常数", "typical": "0.005~0.1"},
                {"name": "bw", "unit": "Hz", "desc": "期望速度环带宽", "typical": "50~200"},
            ],
            "optional_params": [
                {"name": "B", "unit": "N·m·s/rad", "desc": "摩擦系数", "typical": "0~0.01"},
                {"name": "zeta", "unit": "", "desc": "阻尼比", "typical": "0.707~1.0"},
                {"name": "ts", "unit": "s", "desc": "采样周期", "typical": "1e-4~1e-3"},
            ],
            "example": "python main.py --mode speed --j 1e-5 --kt 0.01 --bw 100",
        },
        "position": {
            "loop": "位置环 (Position Loop)",
            "required_params": [
                {"name": "J", "unit": "kg·m²", "desc": "转动惯量", "typical": "1e-6~1e-3"},
                {"name": "Kt", "unit": "N·m/A", "desc": "转矩常数", "typical": "0.005~0.1"},
                {"name": "bw", "unit": "Hz", "desc": "期望位置环带宽", "typical": "5~50"},
            ],
            "optional_params": [
                {"name": "zeta", "unit": "", "desc": "阻尼比", "typical": "0.707~1.0"},
                {"name": "no-speed-loop", "unit": "", "desc": "单环模式(无速度环)", "typical": "flag"},
            ],
            "example": "python main.py --mode position --j 1e-5 --kt 0.01 --bw 20",
        },
    }

    if target == "all":
        return {
            "target": "all",
            "loops": guides,
            "method": "交互式参数引导 (Interactive Parameter Guide)",
            "note": "请根据目标环路提供参数, Agent将逐个询问后执行计算",
        }
    else:
        if target not in guides:
            return {"error": "不支持的target: %s, 可选 current/speed/position/all" % target}
        return {
            "target": target,
            **guides[target],
            "method": "交互式参数引导 (Interactive Parameter Guide)",
        }


# ============================================================
# v4 新增功能: 参数反算
# ============================================================

def reverse_calculate(Kp, Ki, Kd, loop_type, motor_params):
    """
    从PI/PID参数反算等效带宽和阻尼比
    """
    if loop_type == "current":
        Rs = motor_params["Rs"]
        Ls = motor_params["Ls"]
        omega_c = Kp / Ls
        bw_hz = omega_c / (2 * math.pi)
        Ki_expected = Rs * omega_c
        ki_match = abs(Ki - Ki_expected) / abs(Ki_expected) * 100 if Ki_expected != 0 else 0

        return {
            "loop_type": "current",
            "Kp": Kp, "Ki": Ki,
            "equivalent_bandwidth_hz": round(bw_hz, 4),
            "equivalent_omega_c_rad_s": round(omega_c, 4),
            "Ki_consistency_check": {
                "Ki_expected": round(Ki_expected, 6),
                "Ki_actual": Ki,
                "deviation_pct": round(ki_match, 4),
                "status": "一致" if ki_match < 5 else "偏差较大, 可能参数非零极点对消法设计",
            },
            "bandwidth_assessment": _assess_bandwidth(bw_hz, "current"),
            "method": "电流环参数反算 (Current Loop Reverse Calculation)",
            "formula": "omega_c = Kp/Ls = %.6f/%.6e = %.4f rad/s, BW = %.4f Hz" % (Kp, Ls, omega_c, bw_hz),
        }

    elif loop_type == "speed":
        J = motor_params["J"]
        B = motor_params.get("B", 0)
        Kt = motor_params["Kt"]
        omega_c = math.sqrt(Ki * Kt / J) if Ki > 0 and J > 0 else 0
        bw_hz = omega_c / (2 * math.pi)
        zeta = (Kp * Kt + B) / (2 * math.sqrt(Ki * Kt * J)) if Ki > 0 and J > 0 else 0

        return {
            "loop_type": "speed",
            "Kp": Kp, "Ki": Ki,
            "equivalent_bandwidth_hz": round(bw_hz, 4),
            "equivalent_omega_c_rad_s": round(omega_c, 4),
            "equivalent_damping_ratio": round(zeta, 4),
            "damping_assessment": _assess_damping(zeta),
            "bandwidth_assessment": _assess_bandwidth(bw_hz, "speed"),
            "method": "速度环参数反算 (Speed Loop Reverse Calculation)",
            "formula": (
                "omega_c = sqrt(Ki*Kt/J) = sqrt(%.6f*%.6f/%.6e) = %.4f rad/s\n"
                "zeta = (Kp*Kt+B)/(2*sqrt(Ki*Kt*J)) = %.4f"
            ) % (Ki, Kt, J, omega_c, zeta),
        }

    elif loop_type == "position":
        has_speed_loop = not motor_params.get("no_speed_loop", False)
        if has_speed_loop:
            omega_c = math.sqrt(Kp) if Kp > 0 else 0
            bw_hz = omega_c / (2 * math.pi)
            zeta = Kd / (2 * math.sqrt(Kp)) if Kp > 0 else 0
            mode = "级联控制(有速度环)"
        else:
            J = motor_params["J"]
            Kt = motor_params["Kt"]
            omega_c = math.sqrt(Kp * Kt / J) if Kp > 0 and J > 0 else 0
            bw_hz = omega_c / (2 * math.pi)
            zeta = Kd * Kt / (2 * math.sqrt(Kp * Kt * J)) if Kp > 0 and J > 0 else 0
            mode = "单环控制(无速度环)"

        return {
            "loop_type": "position",
            "Kp": Kp, "Ki": Ki, "Kd": Kd,
            "mode": mode,
            "equivalent_bandwidth_hz": round(bw_hz, 4),
            "equivalent_omega_c_rad_s": round(omega_c, 4),
            "equivalent_damping_ratio": round(zeta, 4),
            "damping_assessment": _assess_damping(zeta),
            "bandwidth_assessment": _assess_bandwidth(bw_hz, "position"),
            "method": "位置环参数反算 (Position Loop Reverse Calculation)",
            "formula": "omega_c = sqrt(Kp) = %.4f, zeta = Kd/(2*sqrt(Kp)) = %.4f" % (omega_c, zeta),
        }


def _assess_bandwidth(bw_hz, loop_type):
    """评估带宽合理性"""
    ranges = {
        "current": (500, 2000),
        "speed": (50, 200),
        "position": (5, 50),
    }
    lo, hi = ranges.get(loop_type, (0, 999999))
    if bw_hz < lo:
        return "偏低, 响应可能较慢 (典型范围 %d~%d Hz)" % (lo, hi)
    elif bw_hz > hi:
        return "偏高, 可能引起噪声或振荡 (典型范围 %d~%d Hz)" % (lo, hi)
    else:
        return "合理 (在典型范围 %d~%d Hz 内)" % (lo, hi)


def _assess_damping(zeta):
    """评估阻尼比"""
    if zeta < 0.5:
        return "欠阻尼, 超调大 (%.3f < 0.5)" % zeta
    elif zeta < 0.8:
        return "适中, 有轻微超调 (0.5 <= %.3f < 0.8)" % zeta
    elif zeta <= 1.2:
        return "良好, 接近临界阻尼 (0.8 <= %.3f <= 1.2)" % zeta
    else:
        return "过阻尼, 响应迟缓 (%.3f > 1.2)" % zeta



# ============================================================
# v5 新增功能：抗饱和、死区补偿、多采样率、稳定性分析、参数校验、
#              故障保护、温度补偿、无感启动
# ============================================================
import cmath

# --- 传递函数分析辅助函数 ---

def _eval_poly(coeffs, s):
    """Horner法计算多项式: coeffs[0]*s^(n-1) + ... + coeffs[n-1]"""
    result = 0
    for c in coeffs:
        result = result * s + c
    return result

def _eval_tf(num_coeffs, den_coeffs, omega):
    """计算传递函数 G(jw) = num(jw) / den(jw)"""
    s = complex(0, omega)
    num = _eval_poly(num_coeffs, s)
    den = _eval_poly(den_coeffs, s)
    if abs(den) < 1e-15:
        return complex(1e15, 0)
    return num / den

def _find_gain_crossover(num_coeffs, den_coeffs, omega_min=0.1, omega_max=1e9):
    """找到增益穿越频率 |G(jw)| = 1"""
    g_min = abs(_eval_tf(num_coeffs, den_coeffs, omega_min))
    g_max = abs(_eval_tf(num_coeffs, den_coeffs, omega_max))
    if g_min < 1 and g_max < 1:
        return None
    if g_min > 1 and g_max > 1:
        return None
    lo, hi = omega_min, omega_max
    for _ in range(100):
        mid = (lo + hi) / 2
        g = abs(_eval_tf(num_coeffs, den_coeffs, mid))
        if abs(g - 1.0) < 1e-8:
            return mid
        if g > 1:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def _find_phase_crossover(num_coeffs, den_coeffs, omega_min=0.01, omega_max=1e9):
    """找到相位穿越频率 phase(G(jw)) = -180度"""
    prev_phase = None
    prev_omega = None
    omega = omega_min
    while omega < omega_max:
        g = _eval_tf(num_coeffs, den_coeffs, omega)
        phase = math.degrees(cmath.phase(g))
        while phase > 0:
            phase -= 360
        while phase < -360:
            phase += 360
        if prev_phase is not None:
            for target in [-180, -540]:
                if (prev_phase > target and phase <= target) or (prev_phase < target and phase >= target):
                    lo, hi = prev_omega, omega
                    for _ in range(100):
                        mid = (lo + hi) / 2
                        g_mid = _eval_tf(num_coeffs, den_coeffs, mid)
                        p_mid = math.degrees(cmath.phase(g_mid))
                        while p_mid > 0:
                            p_mid -= 360
                        while p_mid < -360:
                            p_mid += 360
                        if abs(p_mid - target) < 0.01:
                            return mid
                        if p_mid > target:
                            lo = mid
                        else:
                            hi = mid
                    return (lo + hi) / 2
        prev_phase = phase
        prev_omega = omega
        omega *= 1.05
    return None


# ============================================================
# 1. 抗积分饱和策略 (Anti-windup)
# ============================================================

def calculate_antiwindup(loop_type, Kp, Ki, output_limit, Ts, method="all"):
    """
    抗积分饱和策略：Clamping / Back-calculation / Tracking
    """
    results = {"loop_type": loop_type, "Kp": Kp, "Ki": Ki, "output_limit": output_limit}
    methods_list = ["clamping", "backcalc", "trackback"] if method == "all" else [method]
    results["methods"] = {}

    for m in methods_list:
        info = {"method_name": m}

        if m == "clamping":
            info["description"] = (
                "条件积分法：输出饱和且误差方向一致时停止积分。\n"
                "优点：实现简单，计算量小。缺点：退出饱和有延迟。"
            )
            info["c_code"] = (
                "// Anti-windup: Clamping (条件积分)\n"
                "typedef struct {\n"
                "    float Kp, Ki;\n"
                "    float integral;\n"
                "    float out_min, out_max;\n"
                "} PI_Clamp_t;\n"
                "\n"
                "float PI_Clamp_Update(PI_Clamp_t *pi, float error, float Ts) {\n"
                "    float u_unsat = pi->Kp * error + pi->integral;\n"
                "    float u_sat = u_unsat;\n"
                "    if (u_sat > pi->out_max) u_sat = pi->out_max;\n"
                "    if (u_sat < pi->out_min) u_sat = pi->out_min;\n"
                "    // 仅在未饱和或误差有助于退出饱和时积分\n"
                "    int saturating = (u_unsat > pi->out_max) || (u_unsat < pi->out_min);\n"
                "    int exiting = (u_unsat > pi->out_max && error < 0) ||\n"
                "                  (u_unsat < pi->out_min && error > 0);\n"
                "    if (!saturating || exiting) {\n"
                "        pi->integral += pi->Ki * error * Ts;\n"
                "    }\n"
                "    return u_sat;\n"
                "}\n"
            )

        elif m == "backcalc":
            Kt_aw = Ki / Kp if Kp > 0 else 0.1
            Kt_aw = round(Kt_aw, 6)
            info["description"] = (
                "反算法：饱和差值乘以抗饱和增益Kt_aw反馈到积分器。\n"
                "修正项: Kt_aw * (u_sat - u_unsat) * Ts\n"
                "优点：退出平滑。缺点：需调Kt_aw。"
            )
            info["parameters"] = {"Kt_aw": Kt_aw, "Kt_aw_formula": "Kt_aw = Ki/Kp"}
            info["c_code"] = (
                "// Anti-windup: Back-calculation (反算法)\n"
                "typedef struct {\n"
                "    float Kp, Ki, Kt_aw;\n"
                "    float integral;\n"
                "    float out_min, out_max;\n"
                "} PI_BackCalc_t;\n"
                "\n"
                "float PI_BackCalc_Update(PI_BackCalc_t *pi, float error, float Ts) {\n"
                "    float u_unsat = pi->Kp * error + pi->integral;\n"
                "    float u_sat = u_unsat;\n"
                "    if (u_sat > pi->out_max) u_sat = pi->out_max;\n"
                "    if (u_sat < pi->out_min) u_sat = pi->out_min;\n"
                "    float aw = pi->Kt_aw * (u_sat - u_unsat);\n"
                "    pi->integral += pi->Ki * error * Ts + aw * Ts;\n"
                "    return u_sat;\n"
                "}\n"
            )

        elif m == "trackback":
            tau_t = Ts * 10
            Kt_track = 1.0 / tau_t if tau_t > 0 else 100
            Kt_track = round(Kt_track, 6)
            info["description"] = (
                "跟踪法：带跟踪时间常数tau_t的反算法。\n"
                "修正项: (1/tau_t) * (u_sat - u_unsat) * Ts\n"
                "优点：跟踪速度可调。缺点：需调tau_t。"
            )
            info["parameters"] = {
                "tau_t_s": round(tau_t, 8),
                "Kt_track": Kt_track,
                "tau_t_formula": "tau_t = 10 * Ts"
            }
            info["c_code"] = (
                "// Anti-windup: Tracking (跟踪法)\n"
                "typedef struct {\n"
                "    float Kp, Ki, Kt_track;\n"
                "    float integral;\n"
                "    float out_min, out_max;\n"
                "} PI_Track_t;\n"
                "\n"
                "float PI_Track_Update(PI_Track_t *pi, float error, float Ts) {\n"
                "    float u_unsat = pi->Kp * error + pi->integral;\n"
                "    float u_sat = u_unsat;\n"
                "    if (u_sat > pi->out_max) u_sat = pi->out_max;\n"
                "    if (u_sat < pi->out_min) u_sat = pi->out_min;\n"
                "    pi->integral += pi->Ki * error * Ts +\n"
                "                     pi->Kt_track * (u_sat - u_unsat) * Ts;\n"
                "    return u_sat;\n"
                "}\n"
            )

        info["implementation_notes"] = (
            "适用环路: %s\n采样周期: %.1f us\n限幅: [%.4f, %.4f]\n"
            "建议: 量产代码可clamping+backcalc组合使用" % (loop_type, Ts*1e6, -output_limit, output_limit)
        )
        results["methods"][m] = info

    return results


# ============================================================
# 2. 死区补偿 (Dead-time Compensation)
# ============================================================

def calculate_deadtime_comp(vbus, pwm_freq_khz, deadtime_ns, rated_current=None):
    """
    死区电压误差计算与补偿策略
    """
    T_pwm = 1.0 / (pwm_freq_khz * 1000)  # PWM周期 (s)
    t_dead = deadtime_ns * 1e-9           # 死区时间 (s)
    duty_error = t_dead / T_pwm           # 占空比误差

    # 每相峰值电压误差
    dv_peak = vbus * duty_error

    # 平均电压误差 (基波幅值, 6次谐波在dq帧表现为6次纹波)
    dv_avg = (4.0 / math.pi) * dv_peak

    # 基波电流畸变 (假设电气频率下的阻抗近似为Rs)
    di_distortion = None
    if rated_current and rated_current > 0:
        # 电压畸变占额定电压比例 (近似)
        v_fundamental = vbus / math.sqrt(3)  # 相电压幅值
        thd_voltage = dv_avg / v_fundamental * 100 if v_fundamental > 0 else 0
        di_distortion = thd_voltage

    result = {
        "vbus": vbus,
        "pwm_freq_khz": pwm_freq_khz,
        "pwm_period_us": round(T_pwm * 1e6, 2),
        "deadtime_ns": deadtime_ns,
        "deadtime_s": round(t_dead, 10),
        "duty_cycle_error_pct": round(duty_error * 100, 4),
        "voltage_error_peak_per_phase_V": round(dv_peak, 4),
        "voltage_error_avg_V": round(dv_avg, 4),
        "analysis": {
            "peak_error_formula": "dV_peak = Vdc * (t_dead / T_pwm) = %.2f * (%.2e / %.2e) = %.4f V" % (
                vbus, t_dead, T_pwm, dv_peak),
            "avg_error_formula": "dV_avg = (4/pi) * dV_peak = %.4f V" % dv_avg,
            "effect": (
                "死区导致每相电压在电流过零附近跳变，产生6次谐波纹波(dq帧)。\n"
                "在abc帧表现为5次和7次谐波，引起转矩脉动和效率下降。"
            )
        }
    }

    if di_distortion is not None:
        result["voltage_thd_pct"] = round(di_distortion, 2)

    # 补偿策略
    result["compensation"] = {
        "strategy": "根据电流极性在每相电压命令上叠加补偿量",
        "abc_frame": "V_comp_x = sign(i_x) * dV_peak",
        "dq_frame": "Vd_comp = dV_avg * cos(theta_i), Vq_comp = dV_avg * sin(theta_i)",
        "c_code": (
            "// Dead-time Compensation (abc帧)\n"
            "// 在SVPWM输出后、比较器寄存器写入前补偿\n"
            "#define VBUS 24.0f\n"
            "#define DEADTIME_NS 500\n"
            "#define PWM_FREQ_KHZ 20.0f\n"
            "static const float dt_comp = VBUS * (DEADTIME_NS * 1e-9f) * (PWM_FREQ_KHZ * 1e3f);\n"
            "\n"
            "void apply_deadtime_comp(float *vd, float *vq, float id, float iq,\n"
            "                         float theta_elec) {\n"
            "    // dq -> alpha-beta\n"
            "    float valpha = *vd * cosf(theta_elec) - *vq * sinf(theta_elec);\n"
            "    float vbeta  = *vd * sinf(theta_elec) + *vq * cosf(theta_elec);\n"
            "    // alpha-beta -> abc (简化, 仅用alpha-beta补偿)\n"
            "    float ia = valpha;\n"
            "    float ib = -0.5f * valpha + 0.866f * vbeta;\n"
            "    float ic = -0.5f * valpha - 0.866f * vbeta;\n"
            "    // 补偿\n"
            "    if (ia > 0) valpha += dt_comp; else valpha -= dt_comp;\n"
            "    // ...同理补偿ib, ic\n"
            "    // alpha-beta -> dq 回写\n"
            "    *vd = valpha * cosf(theta_elec) + vbeta * sinf(theta_elec);\n"
            "    *vq = -valpha * sinf(theta_elec) + vbeta * cosf(theta_elec);\n"
            "}\n"
        )
    }

    result["recommendations"] = (
        "1. 补偿量dV_peak = %.4f V，占母线电压 %.2f%%\n" % (dv_peak, dv_peak/vbus*100) +
        "2. 电流过零点附近补偿方向切换，建议加滞环防止抖动\n"
        "3. 若dV_peak > 5%% Vdc，建议必须补偿；当前为 %.2f%%" % (dv_peak/vbus*100)
    )

    return result


# ============================================================
# 3. 多采样率控制指导 (Multi-rate Control)
# ============================================================

def calculate_multirate(pwm_freq_khz, bw_current_hz, speed_ratio=10, pos_ratio=10):
    """
    多采样率控制：电流环/速度环/位置环不同采样率指导
    """
    f_pwm = pwm_freq_khz * 1000  # Hz
    Ts_current = 1.0 / f_pwm     # s

    # 速度环采样率
    f_speed = f_pwm / speed_ratio
    Ts_speed = 1.0 / f_speed

    # 位置环采样率
    f_pos = f_speed / pos_ratio
    Ts_pos = 1.0 / f_pos

    # 带宽约束检查
    bw_speed = bw_current_hz / 10  # 典型级联比
    bw_pos = bw_speed / 10

    # 采样率约束: f_sample >= 10 * BW
    check_current = f_pwm / bw_current_hz
    check_speed = f_speed / bw_speed
    check_pos = f_pos / bw_pos

    # CPU负载估算 (假设各环执行时间)
    t_exec_current = 5   # us (FOC核心计算: Park/Clarke/PI/SVPWM)
    t_exec_speed = 2     # us (速度PI + 滤波)
    t_exec_pos = 1       # us (位置PD)

    cpu_load_current = t_exec_current / (Ts_current * 1e6) * 100
    cpu_load_speed = t_exec_speed / (Ts_speed * 1e6) * 100
    cpu_load_total = cpu_load_current + t_exec_speed / (Ts_current * 1e6) * 100 + t_exec_pos / (Ts_current * 1e6) * 100

    result = {
        "pwm_freq_khz": pwm_freq_khz,
        "sampling_rates": {
            "current_loop": {
                "freq_hz": f_pwm,
                "period_us": round(Ts_current * 1e6, 2),
                "exec_in": "PWM ISR (最高优先级)"
            },
            "speed_loop": {
                "freq_hz": round(f_speed, 1),
                "period_us": round(Ts_speed * 1e6, 2),
                "ratio": "1/%d of current" % speed_ratio,
                "exec_in": "Timer ISR or decimation counter in PWM ISR"
            },
            "position_loop": {
                "freq_hz": round(f_pos, 1),
                "period_us": round(Ts_pos * 1e6, 2),
                "ratio": "1/%d of speed" % pos_ratio,
                "exec_in": "Main loop or low-priority ISR"
            }
        },
        "bandwidth_constraints": {
            "current_bw_hz": bw_current_hz,
            "speed_bw_hz": round(bw_speed, 1),
            "position_bw_hz": round(bw_pos, 1),
            "current_oversampling": round(check_current, 1),
            "speed_oversampling": round(check_speed, 1),
            "position_oversampling": round(check_pos, 1),
            "assessment": (
                "过采样比 = f_sample / BW, 推荐 >= 10\n"
                "电流环: %.1fx %s\n" % (check_current, "OK" if check_current >= 10 else "WARNING: <10x") +
                "速度环: %.1fx %s\n" % (check_speed, "OK" if check_speed >= 10 else "WARNING: <10x") +
                "位置环: %.1fx %s" % (check_pos, "OK" if check_pos >= 10 else "WARNING: <10x")
            )
        },
        "cpu_load_estimate": {
            "current_loop_pct": round(cpu_load_current, 2),
            "speed_loop_pct": round(t_exec_speed / (Ts_current * 1e6) * 100, 2),
            "position_loop_pct": round(t_exec_pos / (Ts_current * 1e6) * 100, 2),
            "total_pct": round(cpu_load_total, 2),
            "note": "估算基于典型执行时间(电流5us/速度2us/位置1us), 实际取决于MCU和代码优化"
        },
        "isr_priority": {
            "pwm_isr": "最高优先级 (电流环), 不可被其他ISR抢占",
            "speed_isr": "中等优先级, 可被PWM ISR抢占",
            "position_loop": "最低优先级, 主循环或低优先级ISR"
        },
        "c_code_skeleton": (
            "// Multi-rate Control Skeleton\n"
            "// 全局计数器实现降采样\n"
            "static uint16_t speed_counter = 0;\n"
            "static uint16_t pos_counter = 0;\n"
            "#define SPEED_RATIO %d\n" % speed_ratio +
            "#define POS_RATIO %d\n" % pos_ratio +
            "\n"
            "// PWM ISR - 最高优先级, 每PWM周期执行\n"
            "void PWM_ISR(void) {\n"
            "    // 1. ADC采样 (电流/电压)\n"
            "    // 2. Clarke/Park变换\n"
            "    // 3. 电流环PI (每次都执行)\n"
            "    current_loop_pi();\n"
            "    // 4. SVPWM输出\n"
            "    svpwm_output();\n"
            "\n"
            "    // 速度环: 每SPEED_RATIO次执行一次\n"
            "    if (++speed_counter >= SPEED_RATIO) {\n"
            "        speed_counter = 0;\n"
            "        speed_loop_pi();\n"
            "    }\n"
            "    // 位置环: 每SPEED_RATIO*POS_RATIO次执行一次\n"
            "    if (++pos_counter >= SPEED_RATIO * POS_RATIO) {\n"
            "        pos_counter = 0;\n"
            "        position_loop_pd();\n"
            "    }\n"
            "}\n"
        ),
        "design_notes": (
            "1. 速度环降采样比 %d:1, 位置环再降 %d:1\n" % (speed_ratio, pos_ratio) +
            "2. 速度估算需在速度环周期内做滑动平均, 减少微分噪声\n"
            "3. 位置环输出作为速度环参考, 注意单位转换(rad/s vs rpm)\n"
            "4. 若CPU负载>80%%, 考虑: a)降低PWM频率 b)优化代码 c)用DMA搬运ADC"
        )
    }

    return result


# ============================================================
# 4. 稳定性裕度分析 (Stability Margins)
# ============================================================

def calculate_stability(loop_type, Kp, Ki, Kd, Ts, motor_params, no_speed_loop=False):
    """
    计算开环传递函数的相位裕度和幅值裕度
    """
    result = {"loop_type": loop_type, "Kp": Kp, "Ki": Ki, "Kd": Kd, "Ts": Ts}

    # 构造开环传递函数 G_ol(s) = num(s) / den(s)
    if loop_type == "current":
        Rs = motor_params.get("Rs", 0)
        Ls = motor_params.get("Ls", 0)
        if Rs <= 0 or Ls <= 0:
            raise ValueError("电流环稳定性分析需要 Rs 和 Ls")
        # G_ol(s) = (Kp*s + Ki) / (s*(Ls*s + Rs))
        num = [Kp, Ki]
        den = [Ls, Rs, 0]
        result["transfer_function"] = "G_ol(s) = (Kp*s + Ki) / [s * (Ls*s + Rs)]"

    elif loop_type == "speed":
        J = motor_params.get("J", 0)
        B = motor_params.get("B", 0)
        Kt = motor_params.get("Kt", 0)
        if J <= 0 or Kt <= 0:
            raise ValueError("速度环稳定性分析需要 J 和 Kt")
        # G_ol(s) = (Kp*s + Ki) * Kt / [s * (J*s + B)]
        num = [Kp * Kt, Ki * Kt]
        den = [J, B, 0]
        result["transfer_function"] = "G_ol(s) = (Kp*s + Ki) * Kt / [s * (J*s + B)]"

    elif loop_type == "position":
        J = motor_params.get("J", 0)
        B = motor_params.get("B", 0)
        Kt = motor_params.get("Kt", 0)
        if J <= 0 or Kt <= 0:
            raise ValueError("位置环稳定性分析需要 J 和 Kt")
        if no_speed_loop:
            # 单环: G_ol(s) = (Kp + Kd*s) * Kt / (J*s^2 + B*s)
            num = [Kd * Kt, Kp * Kt]
            den = [J, B, 0]
            result["transfer_function"] = "G_ol(s) = (Kd*s + Kp) * Kt / [s * (J*s + B)]"
        else:
            # 级联: 需要速度环带宽
            bw_speed = motor_params.get("bw_speed", 100)
            omega_s = 2 * math.pi * bw_speed
            # 速度闭环 (简化): G_speed_cl(s) = omega_s / (s + omega_s)
            # 位置开环: G_ol(s) = (Kp + Kd*s) * omega_s / [s * (s + omega_s)]
            num = [Kd * omega_s, Kp * omega_s]
            den = [1, omega_s, 0, 0]
            result["transfer_function"] = "G_ol(s) = (Kd*s + Kp) * w_s / [s * (s + w_s)], w_s=2*pi*%d" % bw_speed
    else:
        raise ValueError("不支持的环路类型: %s" % loop_type)

    # 增益穿越频率
    gc_freq = _find_gain_crossover(num, den)
    if gc_freq is not None:
        gc_hz = gc_freq / (2 * math.pi)
        g_at_gc = _eval_tf(num, den, gc_freq)
        phase_at_gc = math.degrees(cmath.phase(g_at_gc))
        # 相位裕度
        pm = 180 + phase_at_gc
        while pm > 360:
            pm -= 360

        # ZOH延迟 (半采样周期延迟)
        zoh_phase_lag = gc_freq * Ts / 2 * (180 / math.pi)
        pm_with_zoh = pm - zoh_phase_lag

        result["gain_crossover"] = {
            "frequency_rad_s": round(gc_freq, 2),
            "frequency_hz": round(gc_hz, 2),
            "phase_deg": round(phase_at_gc, 2),
            "phase_margin_deg": round(pm, 2),
            "zoh_phase_lag_deg": round(zoh_phase_lag, 2),
            "phase_margin_with_zoh_deg": round(pm_with_zoh, 2)
        }
    else:
        result["gain_crossover"] = {"error": "在搜索范围内未找到增益穿越频率"}

    # 相位穿越频率
    pc_freq = _find_phase_crossover(num, den)
    if pc_freq is not None:
        pc_hz = pc_freq / (2 * math.pi)
        g_at_pc = _eval_tf(num, den, pc_freq)
        mag_at_pc = abs(g_at_pc)
        gm_db = -20 * math.log10(mag_at_pc) if mag_at_pc > 0 else float('inf')

        result["phase_crossover"] = {
            "frequency_rad_s": round(pc_freq, 2),
            "frequency_hz": round(pc_hz, 2),
            "magnitude": round(mag_at_pc, 6),
            "gain_margin_db": round(gm_db, 2)
        }
    else:
        result["phase_crossover"] = {"info": "在搜索范围内无相位穿越（系统无条件稳定或为纯积分器）"}

    # 稳定性评估
    pm_final = result.get("gain_crossover", {}).get("phase_margin_with_zoh_deg")
    gm_final = result.get("phase_crossover", {}).get("gain_margin_db")

    assessment = []
    if pm_final is not None:
        if pm_final > 45:
            assessment.append("相位裕度 %.1f° > 45°: 稳定裕度充足" % pm_final)
        elif pm_final > 30:
            assessment.append("相位裕度 %.1f° (30°~45°): 基本稳定，但裕度偏小" % pm_final)
        elif pm_final > 0:
            assessment.append("相位裕度 %.1f° (0°~30°): 稳定性差，振荡风险高" % pm_final)
        else:
            assessment.append("相位裕度 %.1f° < 0°: 不稳定!" % pm_final)

    if gm_final is not None:
        if gm_final > 6:
            assessment.append("幅值裕度 %.1f dB > 6 dB: 增益裕度充足" % gm_final)
        elif gm_final > 0:
            assessment.append("幅值裕度 %.1f dB (0~6 dB): 增益裕度偏小" % gm_final)
        else:
            assessment.append("幅值裕度 %.1f dB < 0 dB: 不稳定!" % gm_final)

    if pm_final is None and gm_final is None:
        assessment.append("纯积分器类型: 理论上无条件稳定 (PM=90°), 但需关注ZOH延迟影响")

    # 频域关键点 (Bode图数据)
    bode_points = []
    for f in [10, 50, 100, 500, 1000, 5000, 10000, 50000]:
        omega = 2 * math.pi * f
        g = _eval_tf(num, den, omega)
        mag_db = 20 * math.log10(abs(g)) if abs(g) > 0 else -200
        phase = math.degrees(cmath.phase(g))
        bode_points.append({
            "freq_hz": f,
            "magnitude_db": round(mag_db, 2),
            "phase_deg": round(phase, 1)
        })
    result["bode_data"] = bode_points
    result["assessment"] = "\n".join(assessment)

    return result


# ============================================================
# 5. 参数合理性校验 (Parameter Validation)
# ============================================================

def validate_params(Rs=None, Ls=None, psi_f=None, J=None, Kt=None, B=None,
                    pole_pairs=None, Ts=None, bw=None, pwm_freq_khz=None,
                    psi_f_provided=True):
    """
    电机参数物理合理性与控制稳定性校验

    psi_f_provided: psi_f 是否由调用方显式提供（新增）。
    为False时跳过Kt与1.5*psi_f*极对数一致性检查，避免psi_f缺失时的误导性警告。
    """
    checks = []
    warnings = []
    errors = []

    # --- 范围检查 ---
    range_specs = [
        ("Rs", Rs, 0.001, 100, "Omega"),
        ("Ls", Ls, 1e-7, 10, "H"),
        ("psi_f", psi_f, 1e-4, 5, "Wb"),
        ("J", J, 1e-8, 1, "kg*m^2"),
        ("Kt", Kt, 1e-4, 100, "N*m/A"),
        ("B", B, 0, 10, "N*m*s/rad"),
        ("pole_pairs", pole_pairs, 1, 50, ""),
        ("Ts", Ts, 1e-6, 0.01, "s"),
        ("bw", bw, 10, 50000, "Hz"),
        ("pwm_freq", pwm_freq_khz, 1, 100, "kHz"),
    ]

    for name, val, lo, hi, unit in range_specs:
        if val is None:
            continue
        if val < lo or val > hi:
            msg = "%s = %s %s 超出典型范围 [%s, %s] %s" % (name, val, unit, lo, hi, unit)
            if name in ("Rs", "Ls", "psi_f", "J", "Kt"):
                errors.append(msg)
            else:
                warnings.append(msg)
        else:
            checks.append("%s = %s %s: 范围正常" % (name, val, unit))

    # --- 物理一致性检查 ---
    # psi_f未由用户提供时跳过该检查（psi_f缺失时Kt对比无意义，偏差100%警告属误导）
    if psi_f_provided and psi_f is not None and pole_pairs is not None and Kt is not None:
        kt_expected = 1.5 * psi_f * pole_pairs
        kt_ratio = Kt / kt_expected if kt_expected > 0 else 0
        if kt_ratio < 0.5 or kt_ratio > 2.0:
            warnings.append(
                "Kt(%.6f) 与 1.5*psi_f*极对数(%.6f) 偏差 %.0f%%, 检查参数一致性" % (
                    Kt, kt_expected, abs(1 - kt_ratio) * 100))
        else:
            checks.append("Kt vs 1.5*psi_f*极对数: 一致 (偏差%.1f%%)" % (abs(1 - kt_ratio) * 100))

    if Rs is not None and Ls is not None and Rs > 0 and Ls > 0:
        tau = Ls / Rs
        if tau < 1e-4:
            warnings.append("电气时间常数 Ls/Rs = %.2e s < 0.1ms, 电感可能偏小" % tau)
        elif tau > 0.1:
            warnings.append("电气时间常数 Ls/Rs = %.2e s > 100ms, 电阻可能偏小或电感偏大" % tau)
        else:
            checks.append("电气时间常数 Ls/Rs = %.2e s: 正常" % tau)

    # --- 控制稳定性检查 ---
    if bw is not None and Ts is not None:
        omega_c = 2 * math.pi * bw
        wc_ts = omega_c * Ts
        if wc_ts > 0.3:
            errors.append("omega_c*Ts = %.4f > 0.3, 数字实现不稳定风险高!" % wc_ts)
        elif wc_ts > 0.1:
            warnings.append("omega_c*Ts = %.4f (0.1~0.3), 稳定但裕度偏小" % wc_ts)
        else:
            checks.append("omega_c*Ts = %.4f < 0.1: 数字实现稳定" % wc_ts)

    if bw is not None and pwm_freq_khz is not None:
        f_pwm = pwm_freq_khz * 1000
        ratio = f_pwm / bw
        if ratio < 10:
            errors.append("PWM频率/带宽 = %.1f < 10, 带宽过高!" % ratio)
        elif ratio < 20:
            warnings.append("PWM频率/带宽 = %.1f (10~20), 建议提高PWM频率或降低带宽" % ratio)
        else:
            checks.append("PWM频率/带宽 = %.1f >= 20: 充足" % ratio)

    if psi_f is not None and pole_pairs is not None:
        # 反电动势检查 (假设额定转速3000rpm)
        n_rated = 3000
        omega_rated = 2 * math.pi * pole_pairs * n_rated / 60
        e_rated = psi_f * omega_rated
        checks.append("额定3000rpm反电动势: %.2f V (需 < Vdc/sqrt(3))" % e_rated)

    # --- 总评 ---
    if errors:
        overall = "FAIL: %d个严重问题" % len(errors)
    elif warnings:
        overall = "WARNING: %d个潜在问题" % len(warnings)
    else:
        overall = "PASS: 所有检查通过"

    return {
        "overall": overall,
        "passed_checks": checks,
        "warnings": warnings,
        "errors": errors,
        "summary": {
            "total_checks": len(checks) + len(warnings) + len(errors),
            "passed": len(checks),
            "warnings": len(warnings),
            "errors": len(errors)
        }
    }


# ============================================================
# 6. 故障保护阈值计算 (Fault Protection)
# ============================================================

def calculate_protection(rated_current, vbus, device_type="MOSFET", imax=None):
    """
    过流/过压/欠压/过温/堵转保护阈值计算与代码生成
    """
    I_rated = rated_current
    V_rated = vbus

    # 过流阈值
    overcurrent = {
        "rated_current_A": I_rated,
        "warning_A": round(I_rated * 1.2, 3),
        "derating_A": round(I_rated * 1.1, 3),
        "trip_A": round(I_rated * 1.5, 3),
        "hardware_trip_A": round(I_rated * 2.0, 3),
        "note": "软件保护(1.5x) + 硬件比较器(2.0x)双重保护"
    }

    # 过压/欠压
    overvoltage = {
        "rated_vbus_V": V_rated,
        "ov_warning_V": round(V_rated * 1.1, 2),
        "ov_trip_V": round(V_rated * 1.2, 2),
        "uv_warning_V": round(V_rated * 0.8, 2),
        "uv_trip_V": round(V_rated * 0.7, 2),
        "note": "泵升电压需单独设置制动电阻阈值"
    }

    # 过温
    if device_type.upper() == "IGBT":
        temp = {
            "device": "IGBT",
            "derating_temp_C": 80,
            "warning_temp_C": 100,
            "trip_temp_C": 150,
            "junction_limit_C": 175
        }
    else:
        temp = {
            "device": "MOSFET",
            "derating_temp_C": 100,
            "warning_temp_C": 120,
            "trip_temp_C": 150,
            "junction_limit_C": 175
        }

    # 堵转检测
    stall = {
        "speed_threshold_rpm": 30,
        "duration_ms": 200,
        "current_threshold_A": round(I_rated * 0.8, 3),
        "action": "断开PWM输出, 等待手动复位或超时重启",
        "note": "速度<阈值且电流>阈值持续>duration时判定堵转"
    }

    # I2t 保护
    t_thermal_motor = 10.0    # 电机热时间常数 10s
    t_thermal_dev = 0.1       # 器件热时间常数 100ms
    i2t = {
        "motor": {
            "thermal_time_const_s": t_thermal_motor,
            "trip_integral": round(I_rated**2 * t_thermal_motor, 4),
            "formula": "I2t_trip = I_rated^2 * tau_thermal = %.3f^2 * %.1f = %.4f A^2*s" % (
                I_rated, t_thermal_motor, I_rated**2 * t_thermal_motor)
        },
        "device": {
            "thermal_time_const_s": t_thermal_dev,
            "trip_integral": round(I_rated**2 * t_thermal_dev, 6),
            "formula": "I2t_trip = I_rated^2 * tau_thermal = %.3f^2 * %.1f = %.6f A^2*s" % (
                I_rated, t_thermal_dev, I_rated**2 * t_thermal_dev)
        }
    }

    # C代码
    c_code = (
        "// Fault Protection Code\n"
        "#define I_RATED %.3ff\n" % I_rated +
        "#define I_TRIP (%.3ff * I_RATED)\n" % 1.5 +
        "#define I_WARN (%.3ff * I_RATED)\n" % 1.2 +
        "#define V_OV_TRIP (%.2ff * %.2ff)\n" % (1.2, V_rated) +
        "#define V_UV_TRIP (%.2ff * %.2ff)\n" % (0.7, V_rated) +
        "#define TEMP_TRIP %d\n" % temp["trip_temp_C"] +
        "#define STALL_SPEED_RPM 30\n"
        "#define STALL_DURATION_MS 200\n"
        "\n"
        "typedef struct {\n"
        "    float i2t_motor;\n"
        "    float i2t_device;\n"
        "    uint32_t stall_timer;\n"
        "    uint8_t fault;\n"
        "} Protection_t;\n"
        "\n"
        "void protection_check(Protection_t *p, float i_a, float i_b, float i_c,\n"
        "                       float vbus, float temp_c, float speed_rpm, float Ts) {\n"
        "    float i_max = fabsf(i_a);\n"
        "    if (fabsf(i_b) > i_max) i_max = fabsf(i_b);\n"
        "    if (fabsf(i_c) > i_max) i_max = fabsf(i_c);\n"
        "\n"
        "    // 过流 (立即动作)\n"
        "    if (i_max > I_TRIP) { p->fault |= 0x01; return; }\n"
        "\n"
        "    // I2t 积分\n"
        "    float i_ratio = i_max / I_RATED;\n"
        "    p->i2t_motor += (i_ratio * i_ratio - 1.0f) * Ts;\n"
        "    p->i2t_device += (i_ratio * i_ratio - 1.0f) * Ts;\n"
        "    if (p->i2t_motor < 0) p->i2t_motor = 0;\n"
        "    if (p->i2t_device < 0) p->i2t_device = 0;\n"
        "    if (p->i2t_device > %.6ff) { p->fault |= 0x02; }\n" % (I_rated**2 * t_thermal_dev) +
        "\n"
        "    // 过压/欠压\n"
        "    if (vbus > V_OV_TRIP) { p->fault |= 0x04; }\n"
        "    if (vbus < V_UV_TRIP) { p->fault |= 0x08; }\n"
        "\n"
        "    // 过温\n"
        "    if (temp_c > TEMP_TRIP) { p->fault |= 0x10; }\n"
        "\n"
        "    // 堵转检测\n"
        "    if (speed_rpm < STALL_SPEED_RPM && i_max > I_RATED * 0.8f) {\n"
        "        p->stall_timer++;\n"
        "        if (p->stall_timer > (uint32_t)(STALL_DURATION_MS / (Ts * 1000))) {\n"
        "            p->fault |= 0x20;\n"
        "        }\n"
        "    } else {\n"
        "        p->stall_timer = 0;\n"
        "    }\n"
        "}\n"
    )

    return {
        "overcurrent": overcurrent,
        "overvoltage": overvoltage,
        "overtemperature": temp,
        "stall_detection": stall,
        "i2t_protection": i2t,
        "c_code": c_code,
        "fault_codes": {
            "0x01": "过流 (Overcurrent)",
            "0x02": "I2t器件保护 (Device thermal)",
            "0x04": "过压 (Overvoltage)",
            "0x08": "欠压 (Undervoltage)",
            "0x10": "过温 (Overtemperature)",
            "0x20": "堵转 (Stall)"
        }
    }


# ============================================================
# 7. 温度补偿 (Temperature Compensation)
# ============================================================

def calculate_tempcomp(Rs, Ls, psi_f, bw_hz, pole_pairs,
                       temp_min=25, temp_max=125, temp_points=5,
                       magnet_type="NdFeB"):
    """
    温度对电机参数和PI增益的影响分析
    """
    # 温度系数
    alpha_cu = 0.00393  # 铜: 0.393%/°C
    if magnet_type.upper() == "NDFEB":
        alpha_mag = -0.0012   # NdFeB: -0.12%/°C
    elif magnet_type.upper() == "SMCO":
        alpha_mag = -0.0003   # SmCo: -0.03%/°C
    elif magnet_type.upper() == "FERRITE":
        alpha_mag = -0.002    # Ferrite: -0.20%/°C
    else:
        alpha_mag = -0.0012   # 默认NdFeB

    T_ref = 25.0  # 参考温度
    omega_c = 2 * math.pi * bw_hz

    # 生成温度点
    temps = []
    for i in range(temp_points):
        if temp_points > 1:
            t = temp_min + (temp_max - temp_min) * i / (temp_points - 1)
        else:
            t = temp_min
        temps.append(round(t, 1))

    # 计算每个温度点的参数
    table = []
    for T in temps:
        Rs_T = Rs * (1 + alpha_cu * (T - T_ref))
        psi_f_T = psi_f * (1 + alpha_mag * (T - T_ref))
        Kt_T = 1.5 * psi_f_T * pole_pairs

        # 电流环PI (Kp不变因为Ls不变, Ki随Rs变化)
        Kp_cur = Ls * omega_c
        Ki_cur = Rs_T * omega_c

        # 速度环PI (Kp和Ki都随Kt变化)
        # 使用零极点配置法 (zeta=0.707)
        zeta = 0.707
        omega_c_speed = omega_c / 10
        J = 1e-5  # 默认惯量, 速度环参数仅供趋势参考
        Kp_spd = (2 * zeta * omega_c_speed * J) / Kt_T if Kt_T > 0 else 0
        Ki_spd = (omega_c_speed ** 2 * J) / Kt_T if Kt_T > 0 else 0

        table.append({
            "temp_C": T,
            "Rs": round(Rs_T, 6),
            "psi_f": round(psi_f_T, 8),
            "Kt": round(Kt_T, 6),
            "Rs_change_pct": round((Rs_T / Rs - 1) * 100, 2),
            "psi_f_change_pct": round((psi_f_T / psi_f - 1) * 100, 2),
            "Kp_current": round(Kp_cur, 6),
            "Ki_current": round(Ki_cur, 6),
            "Kp_speed": round(Kp_spd, 6),
            "Ki_speed": round(Ki_spd, 6)
        })

    # 影响分析
    Rs_change_total = (table[-1]["Rs"] / table[0]["Rs"] - 1) * 100 if len(table) > 1 else 0
    psi_f_change_total = (table[-1]["psi_f"] / table[0]["psi_f"] - 1) * 100 if len(table) > 1 else 0
    Ki_cur_change = (table[-1]["Ki_current"] / table[0]["Ki_current"] - 1) * 100 if len(table) > 1 and table[0]["Ki_current"] > 0 else 0

    # 补偿策略
    c_code = (
        "// Temperature Compensation\n"
        "// Rs补偿: Rs(T) = Rs_25 * (1 + alpha_Cu * (T - 25))\n"
        "// psi_f补偿: psi_f(T) = psi_f_25 * (1 + alpha_mag * (T - 25))\n"
        "#define ALPHA_CU 0.00393f\n"
        "#define ALPHA_MAG %.6ff\n" % alpha_mag +
        "#define RS_25 %.6ff\n" % Rs +
        "#define PSI_F_25 %.8ff\n" % psi_f +
        "#define OMEGA_C %.2ff\n" % omega_c +
        "#define LS %.8ff\n" % Ls +
        "\n"
        "void temp_compensate(float temp_C, float *Kp_cur, float *Ki_cur,\n"
        "                      float *psi_f_comp) {\n"
        "    float dT = temp_C - 25.0f;\n"
        "    float Rs_T = RS_25 * (1.0f + ALPHA_CU * dT);\n"
        "    *psi_f_comp = PSI_F_25 * (1.0f + ALPHA_MAG * dT);\n"
        "    // 电流环: Kp不变(Ls不变), Ki随Rs变化\n"
        "    *Kp_cur = LS * OMEGA_C;\n"
        "    *Ki_cur = Rs_T * OMEGA_C;\n"
        "}\n"
    )

    return {
        "magnet_type": magnet_type,
        "temperature_coefficients": {
            "alpha_Cu_per_C": alpha_cu,
            "alpha_mag_per_C": alpha_mag,
            "description": "铜电阻: +0.393%%/°C, %s磁链: %+.3f%%/°C" % (magnet_type, alpha_mag * 100)
        },
        "compensation_table": table,
        "impact_analysis": {
            "Rs_total_change_pct": round(Rs_change_total, 2),
            "psi_f_total_change_pct": round(psi_f_change_total, 2),
            "Ki_current_change_pct": round(Ki_cur_change, 2),
            "summary": (
                "温度 %.0f→%.0f°C: Rs变化 %+.1f%%, psi_f变化 %+.1f%%\n" % (
                    temps[0], temps[-1], Rs_change_total, psi_f_change_total) +
                "电流环Ki变化 %+.1f%% (Kp不变), 速度环Kp/Ki均受Kt影响\n" % Ki_cur_change +
                "建议: Rs补偿必须做, psi_f补偿影响弱磁和速度环增益"
            )
        },
        "c_code": c_code,
        "recommendations": (
            "1. Rs补偿: 用NTC或PTC读取温度, 实时更新Ki_current\n"
            "2. psi_f补偿: 影响反电动势和弱磁, 高速时更重要\n"
            "3. 查表法比实时计算更快, 建议预计算5-10个温度点存LUT\n"
            "4. 温度传感器应贴近绕组或功率模块, 滞后<5°C"
        )
    }


# ============================================================
# 8. 无感启动策略 (Sensorless Startup)
# ============================================================

def calculate_startup(Rs, Ls, psi_f, pole_pairs, J=None, Kt=None,
                      vbus=24.0, rated_speed_rpm=3000, pwm_freq_khz=20.0,
                      method="all", transition_speed_rpm=None,
                      rated_current=None):
    """
    无感启动策略：I/F开环启动 + HF高频注入
    """
    result = {"method": method}

    # 默认转换速度: 5%额定转速
    if transition_speed_rpm is None:
        transition_speed_rpm = rated_speed_rpm * 0.05
    n_trans = transition_speed_rpm

    # 转换速度对应电气频率
    f_elec_trans = pole_pairs * n_trans / 60.0  # Hz
    omega_elec_trans = 2 * math.pi * f_elec_trans

    # 默认额定电流
    if rated_current is None:
        rated_current = 5.0  # 默认5A

    methods_list = ["if", "hfi"] if method == "all" else [method]

    # === I/F 开环启动 ===
    if "if" in methods_list:
        I_if = 0.7 * rated_current  # I/F电流幅值
        T_ramp = 2.0  # 频率爬坡时间2s
        ramp_rate = f_elec_trans / T_ramp  # Hz/s

        # I/F模式电流环PI (带宽降低, 平滑启动)
        bw_if = min(500, 2 * math.pi * f_elec_trans / (2 * math.pi))  # 限制带宽
        omega_c_if = 2 * math.pi * 500  # 固定500Hz
        Kp_if = Ls * omega_c_if
        Ki_if = Rs * omega_c_if

        # 电压限制
        V_max = vbus / math.sqrt(3) * 0.9  # 90%线性调制区

        # 转换判据
        speed_error_threshold = n_trans * 0.15  # 15%转换速度
        stable_duration_ms = 100

        result["if_method"] = {
            "description": (
                "I/F开环启动: 施加固定幅值电流, 频率从0线性爬升到转换频率,\n"
                "然后切换到闭环观测器控制。适用于中高速启动。"
            ),
            "parameters": {
                "current_amplitude_A": round(I_if, 3),
                "current_ratio": "70%% of rated (%.1fA)" % rated_current,
                "start_freq_hz": 0,
                "transition_freq_hz": round(f_elec_trans, 2),
                "transition_speed_rpm": round(n_trans, 1),
                "ramp_time_s": T_ramp,
                "ramp_rate_hz_per_s": round(ramp_rate, 2),
                "voltage_limit_V": round(V_max, 2),
                "current_loop_bw_hz": 500,
                "Kp_if": round(Kp_if, 6),
                "Ki_if": round(Ki_if, 6)
            },
            "transition_criteria": {
                "speed_error_threshold_rpm": round(speed_error_threshold, 1),
                "stable_duration_ms": stable_duration_ms,
                "conditions": [
                    "观测器速度估计与I/F指令速度差 < %.1f rpm" % speed_error_threshold,
                    "上述条件持续 %d ms" % stable_duration_ms,
                    "电流误差 < 10%% 额定电流"
                ]
            },
            "c_code": (
                "// I/F Startup Code\n"
                "typedef struct {\n"
                "    float I_amplitude;\n"
                "    float freq_hz;\n"
                "    float freq_target;\n"
                "    float ramp_rate;\n"
                "    float theta_elec;\n"
                "    float transition_speed;\n"
                "    uint8_t state; // 0=idle, 1=ramping, 2=transition, 3=closed_loop\n"
                "} IF_Startup_t;\n"
                "\n"
                "void IF_Startup_Update(IF_Startup_t *ifs, float Ts, float speed_est) {\n"
                "    switch (ifs->state) {\n"
                "    case 0: // idle\n"
                "        ifs->freq_hz = 0;\n"
                "        ifs->theta_elec = 0;\n"
                "        ifs->state = 1;\n"
                "        break;\n"
                "    case 1: // ramping\n"
                "        ifs->freq_hz += ifs->ramp_rate * Ts;\n"
                "        if (ifs->freq_hz >= ifs->freq_target) {\n"
                "            ifs->freq_hz = ifs->freq_target;\n"
                "            ifs->state = 2;\n"
                "        }\n"
                "        break;\n"
                "    case 2: // transition\n"
                "        // 检查观测器速度是否收敛\n"
                "        float speed_cmd = ifs->freq_hz * 60 / %d;\n" % pole_pairs +
                "        if (fabsf(speed_est - speed_cmd) < %.1f) {\n" % speed_error_threshold +
                "            ifs->state = 3; // 切换到闭环\n"
                "        }\n"
                "        break;\n"
                "    case 3: // closed loop\n"
                "        break;\n"
                "    }\n"
                "    // 更新电角度\n"
                "    ifs->theta_elec += 2 * 3.14159f * ifs->freq_hz * Ts;\n"
                "    if (ifs->theta_elec > 2 * 3.14159f) ifs->theta_elec -= 2 * 3.14159f;\n"
                "    // I/F: d轴施加电流幅值, q轴电流=0\n"
                "    Id_ref = ifs->I_amplitude;\n"
                "    Iq_ref = 0;\n"
                "}\n"
            ),
            "notes": (
                "1. I/F电流幅值取70%%额定, 太小带不动负载, 太大易失步\n"
                "2. 爬坡速率需根据负载惯量调整, 惯量大则慢\n"
                "3. 转换速度通常5-10%%额定, 太低观测器不可靠\n"
                "4. 转换瞬间会有转矩波动, 可用斜坡过渡(50%%权重→100%%)"
            )
        }

    # === HF 高频注入 ===
    if "hfi" in methods_list:
        f_pwm = pwm_freq_khz * 1000
        # 注入频率: 5-10倍电流环带宽, 且 < f_pwm/4
        f_inj = min(1000, f_pwm / 10)  # 默认1kHz或PWM/10
        omega_inj = 2 * math.pi * f_inj

        # 注入电压幅值: 5-15% Vdc
        V_inj = vbus * 0.1

        # 高频电感 (近似等于Ls)
        Ls_hf = Ls

        # 位置误差信号增益
        K_pemf = V_inj / (omega_inj * Ls_hf) if omega_inj > 0 and Ls_hf > 0 else 0

        # 解调滤波器参数
        f_lpf = f_inj / 5  # 低通截止
        f_bpf_center = f_inj
        f_bpf_bw = f_inj / 2  # 带宽

        # PLL参数 (跟踪转子位置)
        f_pll = 100  # PLL带宽100Hz
        omega_pll = 2 * math.pi * f_pll
        zeta_pll = 0.707
        Kp_pll = 2 * zeta_pll * omega_pll
        Ki_pll = omega_pll ** 2

        result["hfi_method"] = {
            "description": (
                "高频注入法: 注入高频电压到d轴, 利用凸极效应(saliency)\n"
                "从高频电流响应中提取转子位置。适用于零低速启动。"
            ),
            "parameters": {
                "injection_freq_hz": round(f_inj, 1),
                "injection_voltage_V": round(V_inj, 3),
                "voltage_ratio": "10%% of Vdc (%.1fV)" % vbus,
                "high_freq_inductance_H": round(Ls_hf, 8),
                "position_error_gain": round(K_pemf, 8),
                "requires_saliency": "Ld != Lq (内置式PMSM, IPMSM)",
                "not_suitable": "表贴式PMSM (SPMSM) 无凸极效应"
            },
            "demodulation": {
                "description": "注入V_inj*sin(w_inj*t)到d轴, 提取iq高频分量解调",
                "steps": [
                    "1. 注入: Vd_inj = V_inj * sin(w_inj * t)",
                    "2. 采集iq, 带通滤波提取w_inj频率分量",
                    "3. 乘以sin(w_inj * t)解调",
                    "4. 低通滤波得到位置误差信号 epsilon",
                    "5. PLL跟踪: epsilon -> 锁相环 -> 转子位置估计"
                ],
                "bpf_center_hz": round(f_bpf_center, 1),
                "bpf_bandwidth_hz": round(f_bpf_bw, 1),
                "lpf_cutoff_hz": round(f_lpf, 1)
            },
            "pll_parameters": {
                "bandwidth_hz": f_pll,
                "damping_ratio": zeta_pll,
                "Kp_pll": round(Kp_pll, 4),
                "Ki_pll": round(Ki_pll, 4),
                "formula": "Kp = 2*zeta*w_pll, Ki = w_pll^2"
            },
            "c_code": (
                "// HF Injection Sensorless Code\n"
                "#define F_INJ %.1ff\n" % f_inj +
                "#define OMEGA_INJ %.2ff\n" % omega_inj +
                "#define V_INJ %.3ff\n" % V_inj +
                "#define Kp_PLL %.4ff\n" % Kp_pll +
                "#define Ki_PLL %.4ff\n" % Ki_pll +
                "\n"
                "typedef struct {\n"
                "    float theta_inj;   // 注入角度\n"
                "    float theta_est;   // 估计转子角度\n"
                "    float speed_est;   // 估计转速\n"
                "    float pll_integral;\n"
                "} HFI_t;\n"
                "\n"
                "void HFI_Update(HFI_t *hfi, float id, float iq, float Ts) {\n"
                "    // 1. 更新注入角度\n"
                "    hfi->theta_inj += OMEGA_INJ * Ts;\n"
                "    if (hfi->theta_inj > 2*3.14159f) hfi->theta_inj -= 2*3.14159f;\n"
                "    // 2. 注入高频电压 (在d轴)\n"
                "    float Vd_inj = V_INJ * sinf(hfi->theta_inj);\n"
                "    // 3. 解调: iq * sin(theta_inj)\n"
                "    float demod = iq * sinf(hfi->theta_inj);\n"
                "    // 4. 低通滤波 (一阶IIR)\n"
                "    static float epsilon = 0;\n"
                "    float alpha = 0.05f; // LPF系数\n"
                "    epsilon = alpha * demod + (1-alpha) * epsilon;\n"
                "    // 5. PLL: 从epsilon提取位置\n"
                "    hfi->pll_integral += Ki_PLL * epsilon * Ts;\n"
                "    hfi->speed_est = Kp_PLL * epsilon + hfi->pll_integral;\n"
                "    hfi->theta_est += hfi->speed_est * Ts;\n"
                "    if (hfi->theta_est > 2*3.14159f) hfi->theta_est -= 2*3.14159f;\n"
                "    if (hfi->theta_est < 0) hfi->theta_est += 2*3.14159f;\n"
                "    // Vd_inj叠加到d轴电压命令\n"
                "    Vd_ref += Vd_inj;\n"
                "}\n"
            ),
            "notes": (
                "1. 仅适用于IPMSM(内置式), SPMSM(表贴式)无凸极效应不能用\n"
                "2. 注入频率选PWM/10, 避免与PWM谐波干扰\n"
                "3. 注入电压5-15%% Vdc, 太大噪声大太小信噪比差\n"
                "4. LPF系数alpha需根据注入频率调整: alpha ~ f_lpf/f_inj\n"
                "5. HF和I/F可组合: 零低速用HF, 中高速切I/F, 再切闭环"
            )
        }

    # 组合策略
    if method == "all":
        result["combined_strategy"] = {
            "description": "HF注入→I/F→闭环 三段式启动",
            "stage_1": "零低速: HF高频注入 (0 ~ %.0f rpm)" % (n_trans * 0.3),
            "stage_2": "低速: I/F开环爬升 (%.0f ~ %.0f rpm)" % (n_trans * 0.3, n_trans),
            "stage_3": "中高速: 闭环观测器 (> %.0f rpm)" % n_trans,
            "transition_notes": "每段切换需平滑过渡, 建议用权重融合(50/50→100/0)"
        }

    return result
# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="电机PID调参器 1.0.0 - 29种模式")
    parser.add_argument("--mode", required=True,
                        choices=["current", "speed", "position", "zn", "diagnose", "code", "all", "qformat", "feedforward",
                                 "simulate", "sensitivity", "discretize", "fieldweak", "observer", "preset",
                                 "suggest-bw", "export", "svpwm", "svpmw", "platform", "interactive", "reverse",
                                 "antiwindup", "deadtime-comp", "multirate", "stability", "validate",
                                 "protection", "tempcomp", "startup"],
                        help="计算模式")
    
    # 电流环参数
    parser.add_argument("--rs", type=float, help="定子电阻 (Ω)")
    parser.add_argument("--ls", type=float, help="定子电感 (H)")
    
    # 速度环/位置环参数
    parser.add_argument("--j", type=float, help="转动惯量 (kg·m²)")
    parser.add_argument("--b", type=float, default=0, help="摩擦系数 (N·m·s/rad)")
    parser.add_argument("--kt", type=float, help="转矩常数 (N·m/A)")
    
    # 通用参数
    parser.add_argument("--bw", type=float, help="期望带宽 (Hz)")
    parser.add_argument("--zeta", type=float, default=0.707, help="阻尼比 (默认0.707)")
    parser.add_argument("--ts", type=float, default=50e-6, help="采样周期 (s, 默认50μs)")
    
    # ZN法参数
    parser.add_argument("--kc", type=float, help="临界增益")
    parser.add_argument("--tc", type=float, help="临界振荡周期")
    parser.add_argument("--controller-type", default="PI", choices=["P", "PI", "PID"], help="控制器类型")
    
    # 诊断参数
    parser.add_argument("--symptom", type=str, help="症状描述")
    
    # 代码生成参数
    parser.add_argument("--loop", choices=["current", "speed", "position"], help="代码生成的环路")
    parser.add_argument("--output-limit", type=float, help="输出限幅")
    parser.add_argument("--kp", type=float, help="Kp值")
    parser.add_argument("--ki", type=float, help="Ki值")
    parser.add_argument("--kd", type=float, default=0, help="Kd值(默认0)")
    
    # 位置环
    parser.add_argument("--no-speed-loop", action="store_true", help="位置环单环模式(无速度环)")

    # Q格式参数
    parser.add_argument("--vbus", type=float, default=24.0, help="母线电压 (V, 默认24)")
    parser.add_argument("--imax", type=float, help="最大电流 (A, 用于标幺化)")
    parser.add_argument("--rshunt", type=float, help="采样电阻 (Ω)")
    parser.add_argument("--aop", type=float, help="运放增益")
    parser.add_argument("--vref", type=float, default=3.3, help="ADC参考电压 (V, 默认3.3)")
    parser.add_argument("--q-format", type=int, default=15, help="Q格式位数 (默认15)")

    # 前馈参数
    # 默认改为None以区分"未提供"与"显式传0"；validate模式未提供时跳过Kt一致性检查
    parser.add_argument("--psi-f", type=float, default=None, help="永磁体磁链 (Wb)")
    parser.add_argument("--pole-pairs", type=int, default=1, help="极对数 (默认1)")

    # 完整代码生成
    parser.add_argument("--full", action="store_true", help="生成完整控制器代码(.h+.c)")
    
    # === v4 新增参数 ===
    # 仿真参数
    parser.add_argument("--steps", type=int, default=2000, help="仿真步数 (默认2000)")
    parser.add_argument("--ref", type=float, default=1.0, help="阶跃参考值 (默认1.0)")
    
    # 灵敏度分析参数
    parser.add_argument("--variation", type=float, default=30, help="灵敏度分析变化百分比 (默认30)")
    
    # 离散化方法参数
    parser.add_argument("--method", type=str, default="forward", help="离散化方法(forward/backward/tustin/all)")
    
    # 弱磁控制参数
    parser.add_argument("--rated-speed", type=float, help="额定转速rpm")
    parser.add_argument("--max-speed", type=float, help="最大转速rpm")
    
    # 观测器参数
    parser.add_argument("--observer-type", type=str, default="smo", help="观测器类型(smo/luenberger/all)")
    
    # 电机预设参数
    parser.add_argument("--preset-name", type=str, help="电机预设名称")
    
    # 带宽建议参数
    parser.add_argument("--pwm-freq", type=float, help="PWM频率kHz")
    
    # 导出格式参数
    parser.add_argument("--format", type=str, default="matlab", help="导出格式(默认matlab)")
    
    # SVPWM参数
    parser.add_argument("--deadtime", type=int, default=500, help="死区时间ns (默认500)")
    
    # 多平台参数
    parser.add_argument("--platform-choice", type=str, default="stm32", help="平台选择(stm32/gd32/c2000)")
    
    # 交互式引导参数
    parser.add_argument("--target", type=str, help="交互式引导目标(current/speed/position/all)")

    # === v5 新增参数 ===
    # 抗饱和参数
    parser.add_argument("--aw-method", type=str, default="all", help="抗饱和方法(clamping/backcalc/trackback/all)")

    # 多采样率参数
    parser.add_argument("--speed-ratio", type=int, default=10, help="速度环降采样比(默认10)")
    parser.add_argument("--pos-ratio", type=int, default=10, help="位置环降采样比(默认10)")

    # 保护参数
    parser.add_argument("--device-type", type=str, default="MOSFET", help="功率器件类型(IGBT/MOSFET)")
    parser.add_argument("--rated-current", type=float, help="额定电流A")

    # 温度补偿参数
    parser.add_argument("--temp-min", type=float, default=25, help="最低温度°C(默认25)")
    parser.add_argument("--temp-max", type=float, default=125, help="最高温度°C(默认125)")
    parser.add_argument("--temp-points", type=int, default=5, help="温度点数(默认5)")
    parser.add_argument("--magnet-type", type=str, default="NdFeB", help="磁钢类型(NdFeB/SmCo/Ferrite)")

    # 无感启动参数
    parser.add_argument("--startup-method", type=str, default="all", help="启动方法(if/hfi/all)")
    parser.add_argument("--transition-speed", type=float, help="转换速度rpm(默认5%%额定)")

    args = parser.parse_args()

    # --psi-f 未提供时为None。validate模式用None区分"未提供"与"显式传0"；
    # 其余模式保持原有行为（未提供视为0.0），不影响任何计算逻辑
    if args.mode != "validate" and args.psi_f is None:
        args.psi_f = 0.0

    result = {}
    
    # ========== 旧模式 (v1-v3) ==========
    if args.mode == "current":
        if args.rs is None or args.ls is None or args.bw is None:
            print(json.dumps({"error": "电流环计算需要 --rs, --ls, --bw"}, ensure_ascii=False))
            sys.exit(1)
        result["current_loop"] = calculate_current_loop_pi(args.rs, args.ls, args.bw)
        result["discretized"] = discretize_params(
            result["current_loop"]["Kp"],
            result["current_loop"]["Ki"],
            0, args.ts
        )
    
    elif args.mode == "speed":
        if args.j is None or args.kt is None or args.bw is None:
            print(json.dumps({"error": "速度环计算需要 --j, --kt, --bw"}, ensure_ascii=False))
            sys.exit(1)
        result["speed_loop"] = calculate_speed_loop_pi(args.j, args.b, args.kt, args.bw, args.zeta)
        result["discretized"] = discretize_params(
            result["speed_loop"]["Kp"],
            result["speed_loop"]["Ki"],
            0, args.ts
        )
    
    elif args.mode == "position":
        if args.j is None or args.kt is None or args.bw is None:
            print(json.dumps({"error": "位置环计算需要 --j, --kt, --bw"}, ensure_ascii=False))
            sys.exit(1)
        result["position_loop"] = calculate_position_loop_pid(
            args.j, args.kt, args.bw, args.zeta,
            has_speed_loop=not args.no_speed_loop, B=args.b
        )
        result["discretized"] = discretize_params(
            result["position_loop"]["Kp"],
            result["position_loop"]["Ki"],
            result["position_loop"]["Kd"], args.ts
        )
        # 数字域Kd提示（定点化/Q格式实现场景）
        result["position_loop"]["kd_digital_note"] = KD_DIGITAL_NOTE
    
    elif args.mode == "zn":
        if args.kc is None or args.tc is None:
            print(json.dumps({"error": "ZN法需要 --kc, --tc"}, ensure_ascii=False))
            sys.exit(1)
        result["zn_tuning"] = ziegler_nichols_tuning(args.kc, args.tc, args.controller_type)
    
    elif args.mode == "diagnose":
        if not args.symptom:
            print(json.dumps({"error": "诊断需要 --symptom 参数"}, ensure_ascii=False))
            sys.exit(1)
        result["diagnosis"] = diagnose_symptoms(args.symptom)
    
    elif args.mode == "code":
        if args.full:
            if args.rs is None or args.ls is None or args.j is None or args.kt is None:
                print(json.dumps({"error": "完整代码生成需要 --rs, --ls, --j, --kt"}, ensure_ascii=False))
                sys.exit(1)
            bw_current = args.bw or 1000
            bw_speed = bw_current / 10
            bw_position = bw_speed / 10

            curr_res = calculate_current_loop_pi(args.rs, args.ls, bw_current)
            spd_res = calculate_speed_loop_pi(args.j, args.b, args.kt, bw_speed, args.zeta)
            pos_res = calculate_position_loop_pid(args.j, args.kt, bw_position, args.zeta, True, args.b) if not args.no_speed_loop else None

            ff_res = None
            if args.psi_f > 0:
                ff_res = calculate_feedforward(args.rs, args.ls, args.psi_f, args.pole_pairs)

            q_res = None
            imax = args.imax
            if imax is None and args.rshunt and args.aop:
                imax = args.vref / (args.rshunt * args.aop)
            if imax is None:
                imax = 10.0
            q_res = calculate_q_format(curr_res["Kp"], curr_res["Ki"], 0, args.ts, args.vbus, imax, args.q_format)

            full_code = generate_full_code(curr_res, spd_res, pos_res, ff_res, q_res, args.ts, args.vbus)
            result["full_code"] = full_code
        else:
            if not args.loop or args.kp is None or args.ki is None:
                print(json.dumps({"error": "代码生成需要 --loop, --kp, --ki (或用 --full 生成完整控制器)"}, ensure_ascii=False))
                sys.exit(1)
            code = generate_c_code(args.loop, args.kp, args.ki, args.kd, args.ts, args.output_limit)
            result["code"] = code
    
    elif args.mode == "qformat":
        if args.kp is not None and args.ki is not None:
            kp = args.kp
            ki = args.ki
        elif args.rs and args.ls and args.bw:
            curr = calculate_current_loop_pi(args.rs, args.ls, args.bw)
            kp = curr["Kp"]
            ki = curr["Ki"]
        else:
            print(json.dumps({"error": "Q格式计算需要 --kp, --ki 或 --rs, --ls, --bw"}, ensure_ascii=False))
            sys.exit(1)

        imax = args.imax
        if imax is None and args.rshunt and args.aop:
            imax = args.vref / (args.rshunt * args.aop)
        if imax is None:
            imax = 10.0

        result["q_format"] = calculate_q_format(kp, ki, args.kd, args.ts, args.vbus, imax, args.q_format)

    elif args.mode == "feedforward":
        if not args.rs or not args.ls:
            print(json.dumps({"error": "前馈计算需要 --rs, --ls, 可选 --psi-f, --pole-pairs"}, ensure_ascii=False))
            sys.exit(1)
        result["feedforward"] = calculate_feedforward(args.rs, args.ls, args.psi_f, args.pole_pairs)
    
    elif args.mode == "all":
        if args.rs is None or args.ls is None or args.j is None or args.kt is None:
            print(json.dumps({"error": "三环完整计算需要 --rs, --ls, --j, --kt"}, ensure_ascii=False))
            sys.exit(1)
        
        bw_current = args.bw or 1000
        bw_speed = bw_current / 10
        bw_position = bw_speed / 10
        
        result["current_loop"] = calculate_current_loop_pi(args.rs, args.ls, bw_current)
        result["speed_loop"] = calculate_speed_loop_pi(args.j, args.b, args.kt, bw_speed, args.zeta)
        result["position_loop"] = calculate_position_loop_pid(
            args.j, args.kt, bw_position, args.zeta,
            has_speed_loop=True, B=args.b
        )
        # 数字域Kd提示（定点化/Q格式实现场景）
        result["position_loop"]["kd_digital_note"] = KD_DIGITAL_NOTE
        result["bandwidth_check"] = check_bandwidth_ratio(bw_current, bw_speed, bw_position)
        
        result["current_loop_digital"] = discretize_params(
            result["current_loop"]["Kp"], result["current_loop"]["Ki"], 0, args.ts)
        result["speed_loop_digital"] = discretize_params(
            result["speed_loop"]["Kp"], result["speed_loop"]["Ki"], 0, args.ts)
        result["position_loop_digital"] = discretize_params(
            result["position_loop"]["Kp"], result["position_loop"]["Ki"],
            result["position_loop"]["Kd"], args.ts)

        imax = args.imax
        if imax is None and args.rshunt and args.aop:
            imax = args.vref / (args.rshunt * args.aop)
        if imax is None:
            imax = 10.0
        result["q_format"] = calculate_q_format(
            result["current_loop"]["Kp"], result["current_loop"]["Ki"],
            0, args.ts, args.vbus, imax, args.q_format)

        if args.psi_f > 0:
            result["feedforward"] = calculate_feedforward(
                args.rs, args.ls, args.psi_f, args.pole_pairs)
    
    # ========== v4 新增模式 ==========
    elif args.mode == "simulate":
        if not args.loop or args.kp is None or args.ki is None:
            print(json.dumps({"error": "仿真需要 --loop, --kp, --ki, --ts"}, ensure_ascii=False))
            sys.exit(1)
        if args.loop == "current":
            if not args.rs or not args.ls:
                print(json.dumps({"error": "电流环仿真需要 --rs, --ls"}, ensure_ascii=False))
                sys.exit(1)
            plant_params = {"Rs": args.rs, "Ls": args.ls}
        elif args.loop == "speed":
            if not args.j or not args.kt:
                print(json.dumps({"error": "速度环仿真需要 --j, --kt"}, ensure_ascii=False))
                sys.exit(1)
            plant_params = {"J": args.j, "B": args.b, "Kt": args.kt}
        else:
            plant_params = {}
        
        result["simulation"] = simulate_step_response(
            args.loop, args.kp, args.ki, args.kd, args.ts, plant_params,
            steps=args.steps, ref=args.ref, output_limit=args.output_limit
        )
    
    elif args.mode == "sensitivity":
        if not args.bw:
            print(json.dumps({"error": "灵敏度分析需要 --bw"}, ensure_ascii=False))
            sys.exit(1)
        if args.loop == "current":
            if not args.rs or not args.ls:
                print(json.dumps({"error": "电流环灵敏度分析需要 --rs, --ls"}, ensure_ascii=False))
                sys.exit(1)
            base_params = {"Rs": args.rs, "Ls": args.ls, "bw": args.bw, "zeta": args.zeta}
        elif args.loop == "speed":
            if not args.j or not args.kt:
                print(json.dumps({"error": "速度环灵敏度分析需要 --j, --kt"}, ensure_ascii=False))
                sys.exit(1)
            base_params = {"J": args.j, "B": args.b, "Kt": args.kt, "bw": args.bw, "zeta": args.zeta}
        else:
            base_params = {"bw": args.bw, "zeta": args.zeta}
        
        result["sensitivity"] = sensitivity_analysis(base_params, args.loop, args.variation)
    
    elif args.mode == "discretize":
        if args.kp is None or args.ki is None:
            print(json.dumps({"error": "离散化对比需要 --kp, --ki, --ts"}, ensure_ascii=False))
            sys.exit(1)
        result["discretization"] = discretize_params_advanced(
            args.kp, args.ki, args.kd, args.ts, args.method
        )
    
    elif args.mode == "fieldweak":
        if args.psi_f is None or args.ls is None or args.vbus is None:
            print(json.dumps({"error": "弱磁计算需要 --psi-f, --ls, --vbus"}, ensure_ascii=False))
            sys.exit(1)
        if not args.rated_speed or not args.max_speed:
            print(json.dumps({"error": "弱磁计算需要 --rated-speed, --max-speed"}, ensure_ascii=False))
            sys.exit(1)
        result["field_weakening"] = calculate_field_weakening(
            args.psi_f, args.ls, args.vbus, args.pole_pairs,
            args.rated_speed, args.max_speed
        )
    
    elif args.mode == "observer":
        if args.rs is None or args.ls is None or args.psi_f is None:
            print(json.dumps({"error": "观测器计算需要 --rs, --ls, --psi-f"}, ensure_ascii=False))
            sys.exit(1)
        if not args.bw:
            print(json.dumps({"error": "观测器计算需要 --bw (电流环带宽)"}, ensure_ascii=False))
            sys.exit(1)
        max_spd = args.max_speed or 3000
        result["observer"] = calculate_observer_gains(
            args.rs, args.ls, args.psi_f, args.pole_pairs,
            args.bw, args.observer_type, max_spd
        )
    
    elif args.mode == "preset":
        result["preset"] = get_motor_preset(args.preset_name)
    
    elif args.mode == "suggest-bw":
        if not args.pwm_freq:
            print(json.dumps({"error": "带宽建议需要 --pwm-freq (kHz)"}, ensure_ascii=False))
            sys.exit(1)
        motor_params = None
        if args.rs and args.ls:
            motor_params = {"Rs": args.rs, "Ls": args.ls}
        result["bandwidth_suggestion"] = suggest_bandwidth(args.pwm_freq, motor_params)
    
    elif args.mode == "export":
        if not args.loop or args.kp is None or args.ki is None:
            print(json.dumps({"error": "导出需要 --loop, --kp, --ki"}, ensure_ascii=False))
            sys.exit(1)
        params = {"Kp": args.kp, "Ki": args.ki, "Kd": args.kd}
        if args.rs: params["Rs"] = args.rs
        if args.ls: params["Ls"] = args.ls
        if args.j: params["J"] = args.j
        if args.kt: params["Kt"] = args.kt
        params["B"] = args.b
        result["export"] = export_matlab(params, args.loop)
    
    elif args.mode in ("svpwm", "svpmw"):   # svpmw 为历史拼写，保留兼容
        result["svpwm"] = generate_svpwm_code(args.vbus, args.deadtime)
    
    elif args.mode == "platform":
        params = {
            "pwm_freq_khz": args.pwm_freq or 20,
            "vbus": args.vbus,
            "imax": args.imax or 10,
        }
        result["platform_code"] = generate_platform_code(args.platform_choice, params)
    
    elif args.mode == "interactive":
        target = args.target or "all"
        result["interactive_guide"] = interactive_guide(target)
    
    elif args.mode == "reverse":
        if args.kp is None or args.ki is None:
            print(json.dumps({"error": "反算需要 --kp, --ki, --loop"}, ensure_ascii=False))
            sys.exit(1)
        if args.loop == "current":
            if not args.rs or not args.ls:
                print(json.dumps({"error": "电流环反算需要 --rs, --ls"}, ensure_ascii=False))
                sys.exit(1)
            motor_params = {"Rs": args.rs, "Ls": args.ls}
        elif args.loop == "speed":
            if not args.j or not args.kt:
                print(json.dumps({"error": "速度环反算需要 --j, --kt"}, ensure_ascii=False))
                sys.exit(1)
            motor_params = {"J": args.j, "B": args.b, "Kt": args.kt}
        elif args.loop == "position":
            motor_params = {"no_speed_loop": args.no_speed_loop}
            if not args.no_speed_loop:
                motor_params["no_speed_loop"] = False
            if args.j: motor_params["J"] = args.j
            if args.kt: motor_params["Kt"] = args.kt
        else:
            print(json.dumps({"error": "反算需要 --loop (current/speed/position)"}, ensure_ascii=False))
            sys.exit(1)
        
        result["reverse"] = reverse_calculate(args.kp, args.ki, args.kd, args.loop, motor_params)

    # ========== v5 新增模式 ==========
    elif args.mode == "antiwindup":
        if not args.loop or args.kp is None or args.ki is None:
            print(json.dumps({"error": "抗饱和需要 --loop, --kp, --ki, --output-limit"}, ensure_ascii=False))
            sys.exit(1)
        out_limit = args.output_limit or 10.0
        result["antiwindup"] = calculate_antiwindup(
            args.loop, args.kp, args.ki, out_limit, args.ts, args.aw_method
        )

    elif args.mode == "deadtime-comp":
        if not args.vbus or not args.pwm_freq:
            print(json.dumps({"error": "死区补偿需要 --vbus, --pwm-freq, --deadtime"}, ensure_ascii=False))
            sys.exit(1)
        result["deadtime_comp"] = calculate_deadtime_comp(
            args.vbus, args.pwm_freq, args.deadtime, args.rated_current
        )

    elif args.mode == "multirate":
        if not args.pwm_freq or not args.bw:
            print(json.dumps({"error": "多采样率需要 --pwm-freq, --bw"}, ensure_ascii=False))
            sys.exit(1)
        result["multirate"] = calculate_multirate(
            args.pwm_freq, args.bw, args.speed_ratio, args.pos_ratio
        )

    elif args.mode == "stability":
        if not args.loop or args.kp is None or args.ki is None:
            print(json.dumps({"error": "稳定性分析需要 --loop, --kp, --ki"}, ensure_ascii=False))
            sys.exit(1)
        if args.loop == "current":
            if not args.rs or not args.ls:
                print(json.dumps({"error": "电流环稳定性需要 --rs, --ls"}, ensure_ascii=False))
                sys.exit(1)
            motor_params = {"Rs": args.rs, "Ls": args.ls}
        elif args.loop == "speed":
            if not args.j or not args.kt:
                print(json.dumps({"error": "速度环稳定性需要 --j, --kt"}, ensure_ascii=False))
                sys.exit(1)
            motor_params = {"J": args.j, "B": args.b, "Kt": args.kt}
        elif args.loop == "position":
            if not args.j or not args.kt:
                print(json.dumps({"error": "位置环稳定性需要 --j, --kt"}, ensure_ascii=False))
                sys.exit(1)
            motor_params = {"J": args.j, "B": args.b, "Kt": args.kt, "no_speed_loop": args.no_speed_loop}
            if not args.no_speed_loop:
                motor_params["bw_speed"] = (args.bw or 1000) / 10
        else:
            print(json.dumps({"error": "稳定性分析需要 --loop (current/speed/position)"}, ensure_ascii=False))
            sys.exit(1)
        result["stability"] = calculate_stability(
            args.loop, args.kp, args.ki, args.kd, args.ts, motor_params, args.no_speed_loop
        )

    elif args.mode == "validate":
        # psi_f未提供时按0参与范围检查（保留"psi_f=0超出典型范围"error），
        # 但跳过Kt与1.5*psi_f*极对数一致性检查，避免误导性warning；
        # psi_f显式传0时行为不变（psi_f_provided=True，全部照旧）
        result["validation"] = validate_params(
            args.rs, args.ls, args.psi_f if args.psi_f is not None else 0.0,
            args.j, args.kt, args.b,
            args.pole_pairs, args.ts, args.bw, args.pwm_freq,
            psi_f_provided=(args.psi_f is not None)
        )

    elif args.mode == "protection":
        if not args.rated_current:
            print(json.dumps({"error": "保护计算需要 --rated-current, --vbus"}, ensure_ascii=False))
            sys.exit(1)
        result["protection"] = calculate_protection(
            args.rated_current, args.vbus, args.device_type, args.imax
        )

    elif args.mode == "tempcomp":
        if args.rs is None or args.ls is None or args.psi_f is None or args.bw is None:
            print(json.dumps({"error": "温度补偿需要 --rs, --ls, --psi-f, --bw"}, ensure_ascii=False))
            sys.exit(1)
        result["tempcomp"] = calculate_tempcomp(
            args.rs, args.ls, args.psi_f, args.bw, args.pole_pairs,
            args.temp_min, args.temp_max, args.temp_points, args.magnet_type
        )

    elif args.mode == "startup":
        if args.rs is None or args.ls is None or args.psi_f is None:
            print(json.dumps({"error": "无感启动需要 --rs, --ls, --psi-f, --pole-pairs"}, ensure_ascii=False))
            sys.exit(1)
        rated_spd = args.rated_speed or 3000
        result["startup"] = calculate_startup(
            args.rs, args.ls, args.psi_f, args.pole_pairs,
            args.j, args.kt, args.vbus, rated_spd, args.pwm_freq or 20.0,
            args.startup_method, args.transition_speed, args.rated_current
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


def _safe_main():
    """包装main()，将参数校验/计算异常转为JSON错误输出，避免traceback崩溃"""
    usage_hint = (
        "运行 python main.py --help 查看全部模式；"
        "运行 python main.py <模式名> --help 查看该模式的必需参数与默认值"
    )
    try:
        main()
    except (ValueError, ZeroDivisionError, ArithmeticError) as e:
        print(json.dumps(
            {"error": f"参数校验未通过: {e}", "hint": usage_hint},
            ensure_ascii=False))
        sys.exit(1)
    except TypeError as e:
        # 通常由缺少必需数值参数（None参与运算）引起
        msg = str(e)
        # 常见 TypeError 形态中文化（未覆盖的保持原文，保真优先）
        type_cn = {
            "unsupported operand type": "参数缺失或类型不匹配（某必需数值参数未提供，None 参与了运算）",
            "object is not subscriptable": "参数类型错误（期望数组/对象，收到标量或 None）",
            "object is not iterable": "参数类型错误（期望列表参数，收到单个值或 None）",
            "missing": "必需参数缺失",
            "argument": "参数数量或类型不匹配",
        }
        zh = next((v for k, v in type_cn.items() if k in msg), None)
        error = f"参数类型错误：{zh}。原始信息: {msg}" if zh else f"参数类型错误: {msg}"
        print(json.dumps(
            {"error": error, "hint": usage_hint},
            ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    _safe_main()
