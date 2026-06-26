#!/usr/bin/env python3
"""
电机设计参数计算器
快速计算极槽配合、绕组参数、磁密、反电动势、转矩等核心设计数据

用法：
  python param_calculator.py --poles 8 --Q 36 --L 60 --Di 54 --delta 0.5 --Bg 0.75
  python param_calculator.py --mode interactive
  python param_calculator.py --sweep_slots --poles 8 --L 60 --Di 54
"""

import argparse
import math
import sys

try:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False


def calc_pole_slot(poles, Q, m=3):
    """极槽配合计算"""
    p = poles // 2
    q = Q / (poles * m)  # 每极每相槽数
    tau = Q / poles  # 每极槽数
    return {
        'p': p,
        'q': q,
        'tau_slots': tau,
        'is_fractional': q != int(q) if q else False,
    }


def calc_winding_factor(poles, Q, m=3, coil_pitch=None):
    """绕组系数计算"""
    p = poles // 2
    q_raw = Q / (poles * m)
    q_int = int(q_raw) if q_raw == int(q_raw) else int(q_raw)

    # 每槽电气角度
    alpha_s = 2 * math.pi / Q  # 机械角度 rad
    alpha_e = alpha_s * p  # 电气角度 rad

    # 分布系数
    if q_int > 1:
        kd = math.sin(q_int * alpha_e / 2) / (q_int * math.sin(alpha_e / 2))
    else:
        kd = 1.0

    # 短距系数
    if coil_pitch is None:
        # 默认 5/6 节距 (coil_pitch_y = 5/6 * tau_slots)
        tau_slots = Q / poles
        coil_pitch = round(5 * tau_slots / 6)
    y = coil_pitch  # 节距
    tau_slots = Q / poles  # 极距（槽数）
    kp = math.sin(math.pi * y / (2 * tau_slots))  # 简化：sin(πy/2τ)

    kw = kd * kp
    return {
        'kd': kd,
        'kp': kp,
        'kw': kw,
        'coil_pitch': coil_pitch,
        'pitch_ratio': coil_pitch / tau_slots if tau_slots else 0,
    }


def calc_magnetic(poles, Q, L, Di, delta, Bg, sigma=1.2):
    """磁路计算（简化）"""
    tau = math.pi * Di / poles  # 极距 mm
    Ae = tau * L  # 气隙截面积 mm²
    Phi_g = Bg * Ae * 1e-6  # 每极气隙磁通 Wb

    return {
        'tau_mm': tau,
        'Ae_mm2': Ae,
        'Phi_g_mWb': Phi_g * 1000,
    }


def calc_ke_kt(poles, Q, m, Nph, kw, L, Di, Bg, freq=None, speed=None):
    """反电动势和转矩常数"""
    p = poles // 2
    tau = math.pi * Di / poles
    Ae = tau * L
    Phi_g = Bg * Ae * 1e-6

    # Ke (V/(rad/s))
    if freq:
        Ke = 2.22 * freq * Nph * kw * Phi_g  # 线间有效值近似
    else:
        Ke = 2 * math.pi * Nph * kw * Phi_g / 60  # 简化

    # Kt (Nm/A)
    Kt = 1.5 * p * kw * Nph * Phi_g

    # 线间反电动势（rms）
    if freq and speed:
        n_rpm = speed
        f_elec = n_rpm * p / 60
        E_line_rms = 4.44 * f_elec * Nph * kw * Phi_g
    else:
        E_line_rms = None

    return {
        'Ke_V_rad_s': Ke,
        'Kt_Nm_A': Kt,
        'E_line_rms_V': E_line_rms,
    }


def calc_performance(poles, Q, m, Nph, kw, L, Di, Bg, J, R, Imax):
    """性能估算"""
    p = poles // 2
    tau = math.pi * Di / poles
    Ae = tau * L
    Phi_g = Bg * Ae * 1e-6

    Kt = 1.5 * p * kw * Nph * Phi_g
    Ke_mech = 2 * math.pi * Nph * kw * Phi_g / 60

    # 额定转矩
    T_rated = Kt * Imax

    # 额定功率（近似机械同步功率）
    omega_sync = 2 * math.pi * 50  # 假设 50Hz
    P_sync = 2 * math.pi * p * 50 * T_rated / p  # 简化

    # 机械时间常数
    Tm = J * R / (3 * (Nph * kw * Phi_g * p)**2 + 1e-12)

    # 电气时间常数
    Te = L * 1e-3 / R  # L in mH -> H

    return {
        'Kt_Nm_A': Kt,
        'Ke_V_krpm': Ke_mech * 1000 / (2 * math.pi),
        'T_rated_Nm': T_rated,
        'Tm_s': Tm,
        'Te_s': Te,
    }


def format_output(pole_slot, winding, mag, perf, poles, Q, L, Di, delta, Bg, Nph, m):
    p = poles // 2
    out = f"""
{'='*60}
       电机设计参数计算结果
{'='*60}
【基本参数】
  极数 2p      = {poles} (极对数 p = {p})
  槽数 Q        = {Q}
  相数 m        = {m}
  定子内径 Di   = {Di} mm
  铁心长度 L    = {L} mm
  气隙长度 δ    = {delta} mm
  气隙磁密 Bg   = {Bg} T
  每相串联匝数 Nph = {Nph:.0f}

【极槽配合】
  极距 τ        = {pole_slot['tau_mm']:.2f} mm
  每极槽数      = {pole_slot['tau_slots']:.1f}
  每极每相槽数 q = {pole_slot['q']:.3f}
  分数槽？      = {'是' if pole_slot['is_fractional'] else '否'}

【绕组系数】
  分布系数 Kd   = {winding['kd']:.4f}
  短距系数 Kp   = {winding['kp']:.4f}
  总绕组系数 Kw = {winding['kw']:.4f}
  节距 y        = {winding['coil_pitch']:.0f} 槽
  节距比         = {winding['pitch_ratio']:.3f}

【磁路参数】
  极距 τ        = {mag['tau_mm']:.2f} mm
  气隙截面积 Ae = {mag['Ae_mm2']:.1f} mm²
  每极气隙磁通 Φg = {mag['Phi_g_mWb']:.3f} mWb

【性能估算】
  转矩常数 Kt   = {perf['Kt_Nm_A']:.4f} Nm/A
  反电动势常数 Ke = {perf['Ke_V_krpm']:.3f} V/krpm
  额定转矩（@{Nph:.0f}匝，{m}相，{Bg}T）= {perf['T_rated_Nm']:.3f} Nm (@ Imax)
  机械时间常数 Tm = {perf['Tm_s']:.4f} s
  电气时间常数 Te = {perf['Te_s']:.4f} s
{'='*60}
"""
    return out


def sweep_slots(poles, L, Di, delta, Bg, Nph=100):
    """槽数扫描分析"""
    # 常见槽数选项
    q_options = {1, 1.5, 2, 2.5, 3}
    p = poles // 2

    print(f"\n===== 槽数扫描分析 (2p={poles}, L={L}mm, Di={Di}mm) =====")
    print(f"{'Q':>4} {'q':>6} {'Kw':>8} {'τ/mm':>8} {'Bg/T':>8} {'Kt':>8}")
    print("-" * 50)

    for q in sorted(q_options):
        Q = int(q * poles * 3)
        if Q < 6:
            continue
        ws = calc_winding_factor(poles, Q)
        mag = calc_magnetic(poles, Q, L, Di, delta, Bg)
        perf = calc_performance(poles, Q, 3, Nph, ws['kw'], L, Di, Bg, 1e-3, 1.0, 10)
        print(f"{Q:4d} {q:6.1f} {ws['kw']:8.4f} {mag['tau_mm']:8.2f} "
              f"{Bg:8.3f} {perf['Kt_Nm_A']:8.4f}")


def interactive():
    print("\n" + "="*60)
    print("      电机设计参数计算器（交互模式）")
    print("="*60)

    try:
        poles = int(input("极数 (8): ") or 8)
        Q = int(input("槽数 (36): ") or 36)
        L = float(input("铁心长度 mm (60): ") or 60)
        Di = float(input("定子内径 mm (54): ") or 54)
        delta = float(input("气隙长度 mm (0.5): ") or 0.5)
        Bg = float(input("气隙磁密 T (0.75): ") or 0.75)
        Nph = float(input("每相串联匝数 (100): ") or 100)
        Imax = float(input("额定相电流峰值 A (10): ") or 10)
        R = float(input("相电阻 Ω (1.0): ") or 1.0)
        J = float(input("转动惯量 kg·m² (0.001): ") or 0.001)

        pole_slot = calc_pole_slot(poles, Q)
        winding = calc_winding_factor(poles, Q)
        mag = calc_magnetic(poles, Q, L, Di, delta, Bg)
        perf = calc_performance(poles, Q, 3, Nph, winding['kw'], L, Di, Bg, J, R, Imax)

        print(format_output(pole_slot, winding, mag, perf, poles, Q, L, Di, delta, Bg, Nph, 3))

        # 可选槽数扫描
        ans = input("\n是否进行槽数扫描分析？(y/N): ").strip().upper()
        if ans == 'Y':
            sweep_slots(poles, L, Di, delta, Bg, Nph)

    except KeyboardInterrupt:
        print("\n已退出")


def main():
    parser = argparse.ArgumentParser(description='电机设计参数计算器')
    parser.add_argument('--poles', type=int, default=8, help='极数')
    parser.add_argument('--Q', type=int, default=36, help='槽数')
    parser.add_argument('--L', type=float, default=60, help='铁心长度 mm')
    parser.add_argument('--Di', type=float, default=54, help='定子内径 mm')
    parser.add_argument('--delta', type=float, default=0.5, help='气隙长度 mm')
    parser.add_argument('--Bg', type=float, default=0.75, help='气隙磁密 T')
    parser.add_argument('--Nph', type=float, default=100, help='每相串联匝数')
    parser.add_argument('--Imax', type=float, default=10, help='额定相电流峰值 A')
    parser.add_argument('--R', type=float, default=1.0, help='相电阻 Ω')
    parser.add_argument('--J', type=float, default=1e-3, help='转动惯量 kg·m²')
    parser.add_argument('--sweep_slots', action='store_true', help='槽数扫描分析')
    parser.add_argument('--mode', default='calc', choices=['calc', 'interactive'])

    args = parser.parse_args()

    if args.mode == 'interactive' or (not args.sweep_slots and args.Q == 36 and args.poles == 8):
        if args.mode == 'interactive' or len(sys.argv) == 1:
            interactive()
            return

    if args.sweep_slots:
        sweep_slots(args.poles, args.L, args.Di, args.delta, args.Bg, args.Nph)
        return

    pole_slot = calc_pole_slot(args.poles, args.Q)
    winding = calc_winding_factor(args.poles, args.Q)
    mag = calc_magnetic(args.poles, args.Q, args.L, args.Di, args.delta, args.Bg)
    perf = calc_performance(args.poles, args.Q, 3, args.Nph, winding['kw'],
                           args.L, args.Di, args.Bg, args.J, args.R, args.Imax)

    print(format_output(pole_slot, winding, mag, perf, args.poles, args.Q,
                       args.L, args.Di, args.delta, args.Bg, args.Nph, 3))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        interactive()
    else:
        main()
