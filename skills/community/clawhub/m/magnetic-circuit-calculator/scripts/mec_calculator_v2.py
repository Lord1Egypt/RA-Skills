#!/usr/bin/env python3
"""
电机磁路计算器 v2 (Magnetic Circuit Calculator v2)
基于等效磁路法计算气隙磁通、磁密、永磁体工作点
支持交互模式和命令行模式

用法：
  python mec_calculator_v2.py                           # 交互模式
  python mec_calculator_v2.py --poles 8 --Q 36        # 命令行模式
  python mec_calculator_v2.py --sweep_hm              # hm 扫描分析
"""

import argparse
import math
import sys
from pathlib import Path

try:
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False


# ============================================================
# 永磁材料库
# ============================================================
PM_MATERIALS = {
    'N35':    {'Br': 1.17, 'Hc': 868,  'alpha': -0.12, 'T_max': 80},
    'N42':    {'Br': 1.25, 'Hc': 923,  'alpha': -0.12, 'T_max': 80},
    'N42SH':  {'Br': 1.25, 'Hc': 955,  'alpha': -0.11, 'T_max': 150},
    'N35UH':  {'Br': 1.17, 'Hc': 868,  'alpha': -0.08, 'T_max': 180},
    '35EH':   {'Br': 1.14, 'Hc': 836,  'alpha': -0.04, 'T_max': 200},
    '38UH':   {'Br': 1.18, 'Hc': 860,  'alpha': -0.06, 'T_max': 200},
    '38SH':   {'Br': 1.23, 'Hc': 923,  'alpha': -0.11, 'T_max': 150},
}

# 硅钢片库
STEEL_MATERIALS = {
    '35YT310': {'thickness_mm': 0.35, 'Bf_50Hz_1T': 2.1, 'Bp_max': 1.9},
    'DW310-35': {'thickness_mm': 0.35, 'Bf_50Hz_1T': 2.1, 'Bp_max': 1.9},
    'M19_29Gauss': {'thickness_mm': 0.35, 'Bf_50Hz_1T': 1.85, 'Bp_max': 2.0},
    'B20AT150': {'thickness_mm': 0.20, 'Bf_50Hz_1T': 1.5, 'Bp_max': 1.9},
}


# ============================================================
# 磁路计算核心
# ============================================================

def calculate_mec(
    poles=8, Q=36, m=3, L=60.0, delta=0.5, Di=54.0,
    hm=3.0, Br=1.25, Hc=955.0, bm=17.0,
    lc=10.0, Jc=None, Ns=28, a=2,
    steel='35YT310', pm_grade='N42SH',
    sigma=None, include_iron=True, T=20,
    plot=False
):
    """
    完整磁路计算

    参数:
        poles:      极数
        Q:          槽数
        m:          相数
        L:          铁心长度 mm
        delta:      气隙长度 mm
        Di:         定子内径 mm
        hm:         永磁体厚度 mm
        Br:         永磁体剩磁 T（20℃）
        Hc:         永磁体矫顽力 kA/m（20℃）
        bm:         永磁体弧向宽度 mm
        lc:         轭部磁路长度 mm（估算）
        Jc:         绕组电流密度 A/mm²（估算，默认4）
        Ns:         每槽导体数
        a:          并联支路数
        sigma:      漏磁系数（None=自动估算）
        include_iron: 是否考虑铁心压降
        T:          工作温度 ℃
        plot:       是否绘图

    返回:
        dict: 所有计算结果
    """
    p = poles // 2  # 极对数
    mu0 = 4 * math.pi * 1e-7

    # ===== 1. 温度修正 =====
    alpha = -0.0008  # N42SH 温度系数约 -0.11%/℃ → -0.0011/℃
    Br_T = Br * (1 + alpha * (T - 20))
    Hc_T = Hc * (1 + alpha * (T - 20))  # 简化，Hc 同样温漂

    # ===== 2. 基本几何 =====
    tau = math.pi * Di / poles       # 极距 mm
    q = Q / (poles * m)             # 每极每相槽数

    # ===== 3. 截面积 =====
    Ae = tau * L                     # 气隙截面积 mm²
    Am = bm * L                      # 永磁体截面积 mm²
    Ac = max(tau * 0.3 * L, 10)     # 轭部截面积 mm²（估算轭高30%极距）

    # ===== 4. 气隙磁动势和磁密 =====
    # 永磁体磁动势
    F_pm = Hc_T * 1000 * hm * 1e-3  # A

    # 气隙截面积比
    kappa = Ae / Am  # 永磁体→气隙放大系数

    # 漏磁系数（估算）
    if sigma is None:
        # 经验公式：与极弧系数和气隙/极距比相关
        alpha_p = bm / tau  # 极弧系数
        sigma = 1.15 + 0.15 * alpha_p  # 简化估算
        sigma = max(1.10, min(sigma, 1.40))

    # ===== 5. 气隙磁密（迭代求解）=====
    def solve_Bg(Bg_guess, tol=1e-5, max_iter=100):
        """迭代求解气隙磁密"""
        for _ in range(max_iter):
            # 气隙所需磁动势
            F_gap = Bg_guess / mu0 * delta * 1e-3

            # 轭部磁动势（简化，线性估算）
            if include_iron:
                Bc = Bg_guess * Ae / Ac  # 轭部磁密
                # BH 线性化估算 Hc_core（铁心在0.5~1.5T区间）
                Hc_core = 200 + 300 * Bc  # A/m（经验）
                F_core = Hc_core * lc * 1e-3
            else:
                F_core = 0

            # 永磁体工作点场
            Hm = (F_pm - F_gap - F_core) / hm  # A/m
            Hm_kA = Hm / 1000

            # 永磁体工作点磁密
            # B = mu0*(H+Hc) for hard magnet (退磁曲线线性段)
            # 更精确：Bm = Br + mu0 * Hm（考虑退磁）
            Bm_new = mu0 * (Hm_T * 1000 + Hc_T * 1000) * 1e-3  # 简化
            # 或者用退磁曲线：Bm = Br - (Hm/Hc)*Br
            Bm_new = Br_T * (1 - Hm / (Hc_T * 1000))
            Bm_new = max(0, Bm_new)  # 不允许负值

            # 反算气隙磁密
            Bg_new = Bm_new / (sigma * kappa)
            Bg_new = max(0, min(Bg_new, 1.5))  # 物理限制

            if abs(Bg_new - Bg_guess) < tol:
                return Bg_new, Bm_new, Hm_kA, F_gap, F_core

            Bg_guess = 0.7 * Bg_guess + 0.3 * Bg_new  # 阻尼迭代

        return Bg_guess, Bm_new, Hm_kA, F_gap, F_core

    Bg, Bm, Hm_kA, F_gap, F_core = solve_Bg(0.8)

    # 每极气隙磁通
    Phi_g = Bg * Ae * 1e-6  # Wb

    # ===== 6. 每相串联匝数 =====
    Nph = Q * Ns / (2 * a)

    # ===== 7. 绕组系数 =====
    alpha_e = 2 * math.pi / Q * poles  # 每槽电气角度 rad
    if q > 1:
        kd = math.sin(q * alpha_e / 2) / (q * math.sin(alpha_e / 2))
    else:
        kd = 1.0
    kp = 0.95  # 短距系数（默认 5/6 节距）
    kw = kd * kp

    # ===== 8. 反电动势常数 Ke =====
    freq = 50  # Hz
    omega_e = 2 * math.pi * freq
    Ke_line = 4.44 * freq * Nph * kw * Phi_g * 1000  # V（线间有效值）
    Ke = 2 * math.pi * Nph * kw * Phi_g / 60 * 60 / (2 * math.pi)  # V/(rad/s) 简化

    # ===== 9. 转矩常数 =====
    Kt = 1.5 * p * kw * Nph * Phi_g  # Nm/A（估算）

    # ===== 10. 同步电抗（估算）=====
    delta_rel = delta / 1000  # m
    tau_m = tau / 1000        # m
    Xd = 2 * omega_e * mu0 * (Nph ** 2) * tau_m * L / 1000 / (delta_rel * math.pi * p)
    Xd = max(Xd, 0.1)  # 防零

    # ===== 11. 诊断 =====
    Bm_ratio = Bm / Br_T * 100
    if Bm_ratio < 50:
        diagnosis = "⚠️ 退磁风险高，建议增加 hm 或换高矫顽力牌号"
        status = "WARN"
    elif Bm_ratio < 60:
        diagnosis = "⚠️ 工作点偏低，建议适当增加 hm"
        status = "LOW"
    elif Bg > 1.1:
        diagnosis = "⚠️ 气隙磁密偏高，铁心可能饱和"
        status = "HIGH"
    else:
        diagnosis = "✅ 工作点正常"
        status = "OK"

    if Jc is None:
        Jc = 4.0  # 默认电流密度 A/mm²

    return {
        # 基本几何
        'p': p, 'tau_mm': tau, 'q': q,
        'Ae_mm2': Ae, 'Am_mm2': Am, 'Ac_mm2': Ac,
        # 磁场
        'Bg_T': Bg, 'Bm_T': Bm, 'Bm_ratio_pct': Bm_ratio,
        'Hm_kA_m': Hm_kA,
        'Phi_g_mWb': Phi_g * 1000,
        # 漏磁
        'sigma': sigma,
        # 绕组
        'Nph': Nph, 'kw': kw, 'kd': kd, 'kp': kp,
        # 性能
        'Ke_V_rms': Ke_line, 'Kt_Nm_A': Kt,
        # 电抗
        'Xd_ohm': Xd,
        # 磁动势
        'F_pm_A': F_pm, 'F_gap_A': F_gap, 'F_core_A': F_core,
        # 诊断
        'diagnosis': diagnosis,
        'status': status,
        # 温度
        'Br_T': Br_T, 'Hc_T_kA_m': Hc_T,
    }


def format_output(r):
    """格式化输出"""
    return f"""
{'='*55}
           磁路计算结果
{'='*55}
【基本几何参数】
  极对数 p         = {r['p']}
  极距 τ           = {r['tau_mm']:.2f} mm
  每极每相槽数 q   = {r['q']:.2f}
  气隙截面积 Ae    = {r['Ae_mm2']:.1f} mm²
  永磁体截面积 Am  = {r['Am_mm2']:.1f} mm²
  轭部截面积 Ac    = {r['Ac_mm2']:.1f} mm²

【气隙磁场】
  气隙磁密 Bg      = {r['Bg_T']:.4f} T
  每极气隙磁通 Φg  = {r['Phi_g_mWb']:.3f} mWb

【永磁体工作点】
  漏磁系数 σ       = {r['sigma']:.3f}
  工作点 Bm        = {r['Bm_T']:.4f} T
  工作点占比 Bm/Br = {r['Bm_ratio_pct']:.1f}%
  工作点场 Hm      = {r['Hm_kA_m']:.1f} kA/m

【磁动势分配】
  永磁体 F_pm      = {r['F_pm_A']:.1f} A
  气隙 F_gap       = {r['F_gap_A']:.1f} A
  轭部 F_core      = {r['F_core_A']:.1f} A

【绕组参数】
  每相串联匝数 Nph = {r['Nph']:.0f}
  分布系数 Kd      = {r['kd']:.4f}
  短距系数 Kp      = {r['kp']:.2f}
  总绕组系数 Kw    = {r['kw']:.4f}

【性能估算】
  反电动势常数 Ke = {r['Ke_V_rms']:.2f} V（线间有效值 @ 50Hz）
  转矩常数 Kt     = {r['Kt_Nm_A']:.4f} Nm/A
  同步电抗 Xd      = {r['Xd_ohm']:.3f} Ω

【温度修正 @ 20℃】
  修正后 Br       = {r['Br_T']:.4f} T
  修正后 Hc       = {r['Hc_T_kA_m']:.1f} kA/m

【诊断】
  {r['diagnosis']}
{'='*55}
"""


def sweep_hm(poles=8, Q=36, L=60, delta=0.5, Di=54, bm=17, Br=1.25, Hc=955):
    """扫描永磁体厚度 hm，分析对性能的影响"""
    hm_range = np.linspace(2, 6, 21)  # 2mm ~ 6mm
    results = []
    for hm in hm_range:
        r = calculate_mec(poles=poles, Q=Q, L=L, delta=delta, Di=Di,
                          hm=hm, Br=Br, Hc=Hc, bm=bm,
                          include_iron=True, sigma=1.2)
        results.append(r)

    Bg_list = [r['Bg_T'] for r in results]
    Bm_ratio_list = [r['Bm_ratio_pct'] for r in results]
    Ke_list = [r['Ke_V_rms'] for r in results]

    print("\n===== hm 扫描结果 =====")
    print(f"{'hm/mm':>8} {'Bg/T':>8} {'Bm/Br%':>8} {'Ke/V':>8} {'诊断':>20}")
    print("-" * 58)
    for hm, r in zip(hm_range, results):
        print(f"{hm:8.2f} {r['Bg_T']:8.4f} {r['Bm_ratio_pct']:8.1f} "
              f"{r['Ke_V_rms']:8.2f} {r['diagnosis'][:20]:>20}")

    if HAS_PLOT:
        fig, axes = plt.subplots(1, 3, figsize=(14, 4))

        axes[0].plot(hm_range, Bg_list, 'b-', linewidth=2)
        axes[0].set_xlabel('hm (mm)')
        axes[0].set_ylabel('Bg (T)')
        axes[0].set_title('Air Gap Flux Density')
        axes[0].grid(True, alpha=0.3)
        axes[0].axhline(y=0.8, color='r', linestyle='--', alpha=0.5, label='Target 0.8T')
        axes[0].legend()

        axes[1].plot(hm_range, Bm_ratio_list, 'g-', linewidth=2)
        axes[1].set_xlabel('hm (mm)')
        axes[1].set_ylabel('Bm/Br (%)')
        axes[1].set_title('PM Working Point')
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(y=60, color='r', linestyle='--', alpha=0.5)
        axes[1].axhline(y=50, color='orange', linestyle='--', alpha=0.5)

        axes[2].plot(hm_range, Ke_list, 'r-', linewidth=2)
        axes[2].set_xlabel('hm (mm)')
        axes[2].set_ylabel('Ke (V)')
        axes[2].set_title('Back EMF Constant')
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('hm_sweep_analysis.png', dpi=150)
        print("\n[INFO] 扫描图已保存: hm_sweep_analysis.png")

    # 推荐值
    for r in results:
        if r['status'] == 'OK' and r['Bg_T'] > 0.7 and r['Bm_ratio_pct'] > 55:
            print(f"\n💡 推荐 hm = {hm_range[results.index(r)]:.1f} mm "
                  f"(Bg={r['Bg_T']:.3f}T, Bm/Br={r['Bm_ratio_pct']:.1f}%)")
            break


def compare_slots(poles=8, L=60, delta=0.5, Di=54, hm=3, Br=1.25, Hc=955):
    """对比不同槽数的极槽配合方案"""
    slot_options = [(36, 1.5), (48, 2), (24, 1)]  # (Q, q)
    print("\n===== 极槽配合方案对比 =====")
    print(f"{'Q':>4} {'q':>6} {'Kw':>8} {'Bg/T':>8} {'Bm/Br%':>8} {'Ke/V':>8}")
    print("-" * 50)
    for Q, q in slot_options:
        bm_approx = math.pi * Di / poles * 0.8  # 估算极弧宽度
        r = calculate_mec(poles=poles, Q=Q, L=L, delta=delta, Di=Di,
                          hm=hm, Br=Br, Hc=Hc, bm=bm_approx,
                          include_iron=True, sigma=1.15)
        print(f"{Q:4d} {q:6.2f} {r['kw']:8.4f} {r['Bg_T']:8.4f} "
              f"{r['Bm_ratio_pct']:8.1f} {r['Ke_V_rms']:8.2f}")


# ============================================================
# 交互模式
# ============================================================

def interactive_mode():
    """交互式输入参数"""
    print("\n" + "="*55)
    print("       电机磁路计算器 v2（交互模式）")
    print("="*55)
    print("\n直接回车使用默认值（括号内显示）")

    try:
        poles = int(input(f"极数 (8): ") or 8)
        Q = int(input(f"槽数 (36): ") or 36)
        L = float(input(f"铁心长度 mm (60): ") or 60)
        delta = float(input(f"气隙长度 mm (0.5): ") or 0.5)
        Di = float(input(f"定子内径 mm (54): ") or 54)
        hm = float(input(f"永磁体厚度 mm (3): ") or 3)
        pm = input("永磁体牌号 (N42SH): ") or "N42SH"
        Ns = int(input(f"每槽导体数 (28): ") or 28)
        a = int(input(f"并联支路数 (2): ") or 2)

        if pm in PM_MATERIALS:
            Br = PM_MATERIALS[pm]['Br']
            Hc = PM_MATERIALS[pm]['Hc']
            print(f"  → Br={Br}T, Hc={Hc}kA/m")
        else:
            Br = float(input(f"永磁体 Br T ({PM_MATERIALS['N42SH']['Br']}): ")
                       or PM_MATERIALS['N42SH']['Br'])
            Hc = float(input(f"永磁体 Hc kA/m ({PM_MATERIALS['N42SH']['Hc']}): ")
                       or PM_MATERIALS['N42SH']['Hc'])

        bm = float(input(f"永磁体弧向宽度 mm (估算): ") or 0)
        if bm == 0:
            bm = math.pi * Di / poles * 0.8

        r = calculate_mec(poles=poles, Q=Q, L=L, delta=delta, Di=Di,
                          hm=hm, Br=Br, Hc=Hc, bm=bm, Ns=Ns, a=a)
        print(format_output(r))

    except KeyboardInterrupt:
        print("\n\n已退出")


# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description='电机磁路计算器 - 基于等效磁路法计算气隙磁密、永磁体工作点等')
    parser.add_argument('--poles', type=int, default=8, help='极数')
    parser.add_argument('--Q', type=int, default=36, help='槽数')
    parser.add_argument('--L', type=float, default=60, help='铁心长度 mm')
    parser.add_argument('--delta', type=float, default=0.5, help='气隙长度 mm')
    parser.add_argument('--Di', type=float, default=54, help='定子内径 mm')
    parser.add_argument('--hm', type=float, default=3, help='永磁体厚度 mm')
    parser.add_argument('--Br', type=float, help='永磁体剩磁 T')
    parser.add_argument('--Hc', type=float, help='永磁体矫顽力 kA/m')
    parser.add_argument('--bm', type=float, help='永磁体弧向宽度 mm')
    parser.add_argument('--Ns', type=int, default=28, help='每槽导体数')
    parser.add_argument('--a', type=int, default=2, help='并联支路数')
    parser.add_argument('--pm', default='N42SH', help='永磁体牌号')
    parser.add_argument('--sigma', type=float, help='漏磁系数（默认自动估算）')
    parser.add_argument('--no_iron', action='store_true', help='忽略铁心压降')
    parser.add_argument('--T', type=float, default=20, help='工作温度 ℃')

    group = parser.add_argument_group('分析模式')
    group.add_argument('--sweep_hm', action='store_true',
                       help='扫描永磁体厚度分析')
    group.add_argument('--compare_slots', action='store_true',
                       help='对比不同槽数方案')

    args = parser.parse_args()

    # 参数来源
    if args.pm in PM_MATERIALS and args.Br is None:
        Br = PM_MATERIALS[args.pm]['Br']
        Hc = PM_MATERIALS[args.pm]['Hc']
    else:
        Br = args.Br or 1.25
        Hc = args.Hc or 955

    bm = args.bm
    if bm is None:
        bm = math.pi * args.Di / args.poles * 0.8

    if args.sweep_hm:
        sweep_hm(poles=args.poles, Q=args.Q, L=args.L, delta=args.delta,
                 Di=args.Di, bm=bm, Br=Br, Hc=Hc)
        return

    if args.compare_slots:
        compare_slots(poles=args.poles, L=args.L, delta=args.delta,
                      Di=args.Di, hm=args.hm, Br=Br, Hc=Hc)
        return

    # 单次计算
    r = calculate_mec(
        poles=args.poles, Q=args.Q, L=args.L, delta=args.delta, Di=args.Di,
        hm=args.hm, Br=Br, Hc=Hc, bm=bm, Ns=args.Ns, a=args.a,
        sigma=args.sigma, include_iron=not args.no_iron, T=args.T
    )
    print(format_output(r))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        interactive_mode()
    else:
        main()
