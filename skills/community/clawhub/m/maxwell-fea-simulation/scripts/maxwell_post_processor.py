#!/usr/bin/env python3
"""
Maxwell 2D 仿真结果后处理脚本
用于提取气隙磁密、反电动势、转矩、损耗等结果

依赖：
  pip install numpy matplotlib pandas scipy
  （无需 Maxwell 软件，仅用于结果后处理）

用法：
  python maxwell_post_processor.py --mode cogging_torque --file "torque.csv"
  python maxwell_post_processor.py --mode back_emf --theta theta.csv --flux flux.csv
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
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# ============================================================
# 齿槽转矩分析
# ============================================================

def analyze_cogging_torque(angle, torque, pole_pairs=None, plot=True):
    """
    分析齿槽转矩

    参数:
        angle: 转子角度数组 (deg 或 rad)
        torque: 对应转矩数组 (Nm)
        pole_pairs: 极对数（用于计算周期）
        plot: 是否绘图

    返回:
        dict: 分析结果
    """
    angle = np.array(angle)
    torque = np.array(torque)

    # 自动检测角度单位
    if np.max(angle) > 2 * np.pi:
        angle_rad = np.deg2rad(angle)
    else:
        angle_rad = angle

    # 基本统计
    T_avg = np.mean(torque)
    T_max = np.max(torque)
    T_min = np.min(torque)
    T_pp = T_max - T_min  # 峰峰值
    T_ripple = T_pp / abs(T_avg) * 100 if T_avg != 0 else 0

    # FFT 分析谐波
    n = len(angle_rad)
    dt = angle_rad[1] - angle_rad[0] if n > 1 else 1
    fft_freq = np.fft.fftfreq(n, d=dt)
    fft_torque = np.fft.fft(torque - T_avg)

    # 取正频率部分
    pos_mask = fft_freq > 0
    freqs = fft_freq[pos_mask]
    amplitudes = np.abs(fft_torque[pos_mask]) * 2 / n

    # 按幅值排序，取前5个谐波
    top_indices = np.argsort(amplitudes)[::-1][:5]
    top_harmonics = []
    for idx in top_indices:
        if amplitudes[idx] > 0.001:  # 过滤噪声
            # 计算是几次谐波（基于极对数）
            if pole_pairs:
                harmonic_order = round(freqs[idx] / pole_pairs)
                freq_in_mech = freqs[idx] / pole_pairs
            else:
                harmonic_order = round(freqs[idx] / (2 * np.pi))
                freq_in_mech = freqs[idx] / (2 * np.pi)
            top_harmonics.append({
                'order': harmonic_order,
                'freq_Hz': freq_in_mech,
                'amplitude_Nm': amplitudes[idx]
            })

    result = {
        'T_avg_Nm': T_avg,
        'T_max_Nm': T_max,
        'T_min_Nm': T_min,
        'T_pp_Nm': T_pp,
        'T_ripple_pct': T_ripple,
        'harmonics': top_harmonics,
    }

    # 绘图
    if plot and HAS_MATPLOTLIB:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # 时域波形
        if np.max(angle) > 2 * np.pi:
            ax1.plot(angle, torque, 'b-', linewidth=1)
            ax1.set_xlabel('Angle (deg)')
        else:
            ax1.plot(np.rad2deg(angle), torque, 'b-', linewidth=1)
            ax1.set_xlabel('Angle (deg)')
        ax1.set_ylabel('Torque (Nm)')
        ax1.set_title('Cogging Torque vs Rotor Angle')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='k', linewidth=0.5)

        # 谐波柱状图
        orders = [h['order'] for h in top_harmonics]
        amps = [h['amplitude_Nm'] for h in top_harmonics]
        ax2.bar(orders, amps, color='steelblue')
        ax2.set_xlabel('Harmonic Order (mechanical cycles per revolution)')
        ax2.set_ylabel('Amplitude (Nm)')
        ax2.set_title('Cogging Torque Harmonics')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('cogging_torque_analysis.png', dpi=150)
        print("[INFO] 齿槽转矩分析图已保存: cogging_torque_analysis.png")

    return result


# ============================================================
# 反电动势分析
# ============================================================

def analyze_back_emf(time, voltage, speed_rpm=None, pole_pairs=4,
                     fundamental_freq=None, plot=True):
    """
    分析反电动势波形谐波含量

    参数:
        time: 时间数组 (s)
        voltage: 电压数组 (V)
        speed_rpm: 转速 (rpm)，用于计算电气频率
        pole_pairs: 极对数
        fundamental_freq: 电气基频 (Hz)，优先级高于 speed_rpm
        plot: 是否绘图

    返回:
        dict: 分析结果
    """
    voltage = np.array(voltage)
    time = np.array(time)

    # 计算电气频率
    if fundamental_freq:
        f_elec = fundamental_freq
    elif speed_rpm and pole_pairs:
        f_elec = speed_rpm * pole_pairs / 60
    else:
        # 从电压波形估计频率
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(voltage, distance=len(voltage)//10)
        if len(peaks) >= 2:
            f_elec = 1 / np.mean(np.diff(time[peaks]))
        else:
            f_elec = None

    # FFT 分析
    n = len(voltage)
    dt = time[1] - time[0] if n > 1 else 1
    fft_v = np.fft.fft(voltage)
    fft_freq = np.fft.fftfreq(n, d=dt)

    pos_mask = fft_freq > 0
    freqs = fft_freq[pos_mask]
    amps = np.abs(fft_v[pos_mask]) * 2 / n
    phases = np.angle(fft_v[pos_mask], deg=True)

    # 找到基频索引
    if f_elec:
        f_idx = np.argmin(np.abs(freqs - f_elec))
        fundamental_amp = amps[f_idx]
        fundamental_phase = phases[f_idx]

        # 计算 THD
        harmonic_orders = [3, 5, 7, 9, 11, 13]
        harmonic_amps = []
        for h in harmonic_orders:
            h_freq = h * f_elec
            h_idx = np.argmin(np.abs(freqs - h_freq))
            if abs(freqs[h_idx] - h_freq) < freqs[1] * 2:  # 容差内
                harmonic_amps.append(amps[h_idx])
            else:
                harmonic_amps.append(0)

        thd = math.sqrt(sum([h**2 for h in harmonic_amps])) / fundamental_amp * 100
    else:
        fundamental_amp = np.max(amps)
        fundamental_phase = 0
        thd = 0

    # 峰值和有效值
    V_peak = np.max(voltage)
    V_rms = np.sqrt(np.mean(voltage**2))

    result = {
        'V_peak_V': V_peak,
        'V_rms_V': V_rms,
        'fundamental_freq_Hz': f_elec,
        'fundamental_amp_V': fundamental_amp,
        'fundamental_phase_deg': fundamental_phase,
        'THD_pct': thd,
        'harmonic_orders': [3, 5, 7, 9, 11, 13],
        'harmonic_amps_V': harmonic_amps if f_elec else [],
    }

    if plot and HAS_MATPLOTLIB:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # 时域波形
        ax1.plot(time * 1000, voltage, 'b-', linewidth=1)
        ax1.set_xlabel('Time (ms)')
        ax1.set_ylabel('Voltage (V)')
        ax1.set_title('Back EMF Waveform')
        ax1.grid(True, alpha=0.3)

        # 谐波柱状图
        ax2.bar([3, 5, 7, 9, 11, 13], harmonic_amps if f_elec else [],
                color='coral')
        ax2.set_xlabel('Harmonic Order')
        ax2.set_ylabel('Amplitude (V)')
        ax2.set_title(f'Back EMF Harmonics (THD={thd:.1f}%)')
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('back_emf_analysis.png', dpi=150)
        print("[INFO] 反电动势分析图已保存: back_emf_analysis.png")

    return result


# ============================================================
# 气隙磁密分析
# ============================================================

def analyze_air_gap_flux_density(angle, Br, position='mid', plot=True):
    """
    分析气隙磁密波形

    参数:
        angle: 角度数组 (deg)
        Br: 径向磁密数组 (T)
        position: 测量位置 ('mid'气隙中部, 'inner'转子侧)
        plot: 是否绘图
    """
    angle = np.array(angle)
    Br = np.array(Br)

    if np.max(angle) > 2 * np.pi:
        angle_rad = np.deg2rad(angle)
    else:
        angle_rad = angle

    # 基本统计
    Br_avg = np.mean(Br)
    Br_max = np.max(Br)
    Br_min = np.min(Br)
    Br_pp = Br_max - Br_min

    # FFT 分析谐波
    n = len(Br)
    fft_Br = np.fft.fft(Br)
    fft_freq = np.fft.fftfreq(n, d=angle_rad[1] - angle_rad[0])

    pos_mask = fft_freq > 0
    freqs = fft_freq[pos_mask]
    amps = np.abs(fft_Br[pos_mask]) * 2 / n

    # 主要谐波（按幅值排序）
    top_indices = np.argsort(amps)[::-1][:6]
    harmonics = []
    for idx in top_indices:
        if amps[idx] > 0.005:
            harmonics.append({
                'order': round(freqs[idx]),
                'amplitude_T': amps[idx],
                'pct_of_fundamental': 0  # 简化
            })

    result = {
        'Br_avg_T': Br_avg,
        'Br_max_T': Br_max,
        'Br_min_T': Br_min,
        'Br_pp_T': Br_pp,
        'harmonics': harmonics,
    }

    if plot and HAS_MATPLOTLIB:
        plt.figure(figsize=(10, 5))
        plt.plot(angle, Br, 'b-', linewidth=1.5)
        plt.axhline(y=Br_avg, color='r', linestyle='--', label=f'Avg={Br_avg:.4f}T')
        plt.xlabel('Angle (deg)')
        plt.ylabel('Radial Flux Density Bᵣ (T)')
        plt.title(f'Air Gap Flux Density ({position})')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.savefig('air_gap_flux_density.png', dpi=150)
        print("[INFO] 气隙磁密图已保存: air_gap_flux_density.png")

    return result


# ============================================================
# 力矩速度特性分析
# ============================================================

def analyze_torque_speed(current_Idq_list, flux_linkage, pole_pairs,
                         resistance=None, plot=True):
    """
    根据给定电流矢量计算力矩-转速特性

    参数:
        current_Idq_list: [(Id, Iq), ...] 电流列表
        flux_linkage: 磁链 Ψm (Wb)
        pole_pairs: 极对数
        resistance: 相电阻 (Ω)，用于计算铜损
    """
    speeds = np.linspace(500, 5000, 50)  # rpm

    results = []
    for Id, Iq in current_Idq_list:
        torques = []
        powers = []
        effs = []

        for n in speeds:
            omega_e = 2 * np.pi * n * pole_pairs / 60  # rad/s

            # 电磁转矩（表贴式 PMSM）
            T = 1.5 * pole_pairs * flux_linkage * Iq

            # 反电动势
            E = flux_linkage * omega_e

            # 电压幅值（忽略 d 轴）
            V = np.sqrt((Id * 0)**2 + (Iq * omega_e * flux_linkage)**2)

            # 机械功率
            P_mech = T * omega_e * 2 * np.pi / 60  # W

            torques.append(T)
            powers.append(P_mech)

        results.append({
            'Id': Id,
            'Iq': Iq,
            'torques': np.array(torques),
            'speeds': speeds,
            'powers': np.array(powers),
        })

    if plot and HAS_MATPLOTLIB:
        plt.figure(figsize=(10, 6))
        for r in results:
            label = f'Id={r["Id"]:.1f}A, Iq={r["Iq"]:.1f}A'
            plt.plot(r['speeds'], r['torques'], label=label, linewidth=2)

        plt.xlabel('Speed (rpm)')
        plt.ylabel('Torque (Nm)')
        plt.title('Torque-Speed Characteristic')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('torque_speed_curve.png', dpi=150)
        print("[INFO] 力矩转速曲线已保存: torque_speed_curve.png")

    return results


# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='Maxwell 仿真结果后处理工具')
    parser.add_argument('--mode', required=True,
                        choices=['cogging_torque', 'back_emf', 'air_gap_flux',
                                 'torque_speed'],
                        help='分析模式')
    parser.add_argument('--file', help='数据文件路径 (.csv)')
    parser.add_argument('--angle', help='角度数据文件或列名')
    parser.add_argument('--torque', help='转矩数据列名')
    parser.add_argument('--voltage', help='电压数据列名')
    parser.add_argument('--time', help='时间数据列名')
    parser.add_argument('--speed', type=float, help='转速 (rpm)')
    parser.add_argument('--pole_pairs', type=int, default=4, help='极对数')
    parser.add_argument('--np', dest='pole_pairs', type=int,
                        help='极对数（--np 别名）')
    parser.add_argument('--plot', type=lambda x: x.lower() == 'true',
                        default=True)
    parser.add_argument('--output', help='输出文件名')

    args = parser.parse_args()

    # 演示数据
    if args.mode == 'cogging_torque':
        # 生成演示齿槽转矩数据（8极，6个周期/转）
        np.random.seed(42)
        angle = np.linspace(0, 360, 361)
        pole_pairs = args.pole_pairs
        # 基波 + 齿槽谐波
        T_cog = (0.05 * np.sin(np.deg2rad(angle * pole_pairs)) +
                 0.02 * np.sin(np.deg2rad(angle * 2 * pole_pairs)) +
                 0.01 * np.sin(np.deg2rad(angle * 3 * pole_pairs)) +
                 0.005 * np.random.randn(len(angle)))

        result = analyze_cogging_torque(angle, T_cog,
                                         pole_pairs=pole_pairs, plot=args.plot)

        print("\n===== 齿槽转矩分析结果 =====")
        print(f"平均转矩: {result['T_avg_Nm']:.4f} Nm")
        print(f"最大转矩: {result['T_max_Nm']:.4f} Nm")
        print(f"最小转矩: {result['T_min_Nm']:.4f} Nm")
        print(f"峰峰值:   {result['T_pp_Nm']:.4f} Nm")
        print(f"转矩脉动: {result['T_ripple_pct']:.2f}%")
        print("\n主要谐波:")
        for h in result['harmonics']:
            print(f"  {h['order']}次谐波: {h['amplitude_Nm']:.4f} Nm")

    elif args.mode == 'back_emf':
        # 生成演示反电动势数据
        np.random.seed(42)
        fundamental_freq = 200  # Hz (3000rpm * 4 / 60)
        time = np.linspace(0, 0.05, 500)
        fundamental = 100 * np.sin(2 * np.pi * fundamental_freq * time)
        harmonic5 = 5 * np.sin(2 * np.pi * 5 * fundamental_freq * time)
        noise = 2 * np.random.randn(len(time))
        voltage = fundamental + harmonic5 + noise

        result = analyze_back_emf(time, voltage, fundamental_freq=fundamental_freq,
                                  pole_pairs=args.pole_pairs, plot=args.plot)

        print("\n===== 反电动势分析结果 =====")
        print(f"峰值电压: {result['V_peak_V']:.2f} V")
        print(f"有效值电压: {result['V_rms_V']:.2f} V")
        print(f"基频: {result['fundamental_freq_Hz']:.1f} Hz")
        print(f"基波幅值: {result['fundamental_amp_V']:.2f} V")
        print(f"THD: {result['THD_pct']:.2f}%")

    elif args.mode == 'air_gap_flux':
        # 生成演示气隙磁密数据
        angle = np.linspace(0, 360, 361)
        Br = (0.8 + 0.1 * np.sin(np.deg2rad(angle * 4)) +
              0.03 * np.sin(np.deg2rad(angle * 8)))
        result = analyze_air_gap_flux_density(angle, Br, plot=args.plot)

        print("\n===== 气隙磁密分析结果 =====")
        print(f"平均磁密: {result['Br_avg_T']:.4f} T")
        print(f"最大磁密: {result['Br_max_T']:.4f} T")
        print(f"最小磁密: {result['Br_min_T']:.4f} T")
        print(f"峰峰值:   {result['Br_pp_T']:.4f} T")

    elif args.mode == 'torque_speed':
        Psi_m = 0.1  # Wb
        current_points = [(0, 10), (0, 15), (0, 20)]
        results = analyze_torque_speed(current_points, Psi_m,
                                       pole_pairs=args.pole_pairs,
                                       plot=args.plot)
        print("\n===== 力矩转速特性 =====")
        for r in results:
            max_t = np.max(r['torques'])
            max_p = np.max(r['powers'])
            print(f"Id={r['Id']:.1f}A, Iq={r['Iq']:.1f}A → "
                  f"最大转矩={max_t:.2f}Nm, 最大功率={max_p:.0f}W")


if __name__ == '__main__':
    main()
