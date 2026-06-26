#!/usr/bin/env python3
"""
电机磁路计算器 (Magnetic Circuit Calculator)
基于等效磁路法计算气隙磁通、磁密、永磁体工作点

用法：python mec_calculator.py [参数]
"""

import math

def calculate_magnetic_circuit(
    poles=8,
    Q=36,
    m=3,
    L=60.0,       # mm
    delta=0.5,    # 气隙长度 mm
    Di=54.0,      # 定子内径 mm
    hm=3.0,       # 永磁体厚度 mm
    Br=1.25,      # 剩磁 T
    Hc=955.0,     # 矫顽力 kA/m
    bm=17.0,      # 永磁体弧向宽度 mm
    lc=10.0,      # 轭部磁路长度 mm（估算值）
    sigma=1.2,    # 漏磁系数（初始估计）
):
    """磁路计算主函数"""
    
    # ===== 1. 基础几何参数 =====
    p = poles // 2  # 极对数
    tau = math.pi * Di / poles  # 极距 mm
    q = Q / (poles * m)  # 每极每相槽数
    
    # ===== 2. 截面积 =====
    Ae = tau * L        # 气隙截面积 mm²
    Am = bm * L          # 永磁体截面积 mm²
    
    # ===== 3. 气隙磁密估算（忽略铁心压降）=====
    # Bg = sigma * Br * Am / (delta * Ae)
    Bg = sigma * Br * Am / (delta * Ae)  # T
    
    # ===== 4. 每极气隙磁通 =====
    Phi_g = Bg * Ae * 1e-6  # Wb (mm² → m²)
    
    # ===== 5. 永磁体工作点 =====
    # Bm = sigma * Bg * (Ae / Am)
    Bm = sigma * Bg * (Ae / Am)
    Bm_ratio = Bm / Br * 100  # 工作点占 Br 的百分比
    
    # 永磁体磁动势
    F_pm = Hc * 1000 * hm * 1e-3  # A（转成A）
    
    # 气隙所需磁动势
    mu0 = 4 * math.pi * 1e-7
    F_gap = Bg / mu0 * delta * 1e-3  # A
    
    # 轭部压降（线性估算）
    Hc_core = 200  # A/m（取 0.5T 时硅钢片刻度）
    F_core = Hc_core * lc * 1e-3  # A
    
    # 永磁体内部场 Hm
    Hm = (F_pm - F_gap - F_core) / hm  # A/m
    Hm_kA = Hm / 1000  # kA/m
    
    # ===== 6. 反电动势常数 Ke =====
    # 估算每相串联匝数（示例：36槽8极，整距）
    Ns_per_slot = 28  # 每槽导体数
    a = 2  # 并联支路数
    Nph = Q * Ns_per_slot / (2 * a)  # 每相串联匝数
    Kw = 0.933  # 绕组系数（估算值）
    
    # Ke = 2 * pi * Nph * Kw * Phi_g / 60  # V/(rad/s) 形式
    # 或用线间反电动势
    freq = 50  # Hz
    Ke_line = 4.44 * freq * Nph * Kw * Phi_g * 1000  # V（线间有效值）@ 50Hz
    
    # ===== 7. 转矩常数 Kt =====
    Kt = 1.5 * Nph * Kw * Phi_g  # Nm/A（估算）
    
    # ===== 8. 诊断 =====
    if Bm_ratio < 50:
        diagnosis = "⚠️ 存在退磁风险，建议增加 hm 或换高矫顽力牌号"
    elif Bm_ratio < 60:
        diagnosis = "⚠️ 工作点偏低，建议适当增加 hm"
    else:
        diagnosis = "✅ 工作点正常"
    
    return {
        'tau_mm': round(tau, 2),
        'q': round(q, 2),
        'Ae_mm2': round(Ae, 1),
        'Am_mm2': round(Am, 1),
        'Bg_T': round(Bg, 4),
        'Phi_g_Wb': round(Phi_g * 1e6, 3),  # 转成 mWb
        'Bm_T': round(Bm, 4),
        'Bm_ratio_pct': round(Bm_ratio, 1),
        'Hm_kA_m': round(Hm_kA, 1),
        'Ke_V_rms': round(Ke_line, 2),
        'Kt_Nm_A': round(Kt, 4),
        'diagnosis': diagnosis,
        'sigma': sigma,
    }


def format_output(results):
    """格式化输出结果"""
    r = results
    return f"""
===== 磁路计算结果 =====
【基本参数】
极距 τ = {r['tau_mm']} mm
每极每相槽数 q = {r['q']}
气隙截面积 Ae = {r['Ae_mm2']} mm²
永磁体截面积 Am = {r['Am_mm2']} mm²

【气隙磁场】
气隙磁密 Bg = {r['Bg_T']} T
每极气隙磁通 Φg = {r['Phi_g_Wb']} mWb

【永磁体工作点】
漏磁系数 σ = {r['sigma']}
工作点 Bm = {r['Bm_T']} T
工作点占比 Bm/Br = {r['Bm_ratio_pct']}%
工作点场 Hm = {r['Hm_kA_m']} kA/m

【性能估算】
每相串联匝数 Nph = {r['Nph']}（需根据实际填入）
绕组系数 Kw = 0.933（估算值）
反电动势常数 Ke = {r['Ke_V_rms']} V（线间有效值 @ 50Hz）
转矩常数 Kt = {r['Kt_Nm_A']} Nm/A

【诊断】
{r['diagnosis']}
"""


if __name__ == "__main__":
    # 示例：8极36槽表贴式 PMSM
    result = calculate_magnetic_circuit(
        poles=8,
        Q=36,
        m=3,
        L=60.0,
        delta=0.5,
        Di=54.0,
        hm=3.0,
        Br=1.25,
        Hc=955.0,
        bm=17.0,
        lc=10.0,
        sigma=1.2,
    )
    # 添加 Nph 用于显示
    result['Nph'] = int(36 * 28 / 4)
    print(format_output(result))
