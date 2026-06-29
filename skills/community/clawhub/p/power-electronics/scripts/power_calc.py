#!/usr/bin/env python3
"""
电力电子技术 Skill - 四大变换统一计算
零依赖，Python 标准库。输出 JSON。

transform: ac-dc | dc-ac | dc-dc | ac-ac
"""

import argparse
import json
import math
import sys

SQRT2 = math.sqrt(2)
SQRT3 = math.sqrt(3)
PI = math.pi


# ── 通用工具 ──────────────────────────────────────────────

def e12_round(value: float) -> float:
    if value <= 0:
        return value
    e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    exp = math.floor(math.log10(value))
    mant = value / (10 ** exp)
    best = min(e12, key=lambda x: abs(x - mant))
    return round(best * (10 ** exp), 2)


def cap_standard(value_f: float) -> dict:
    v = value_f * 1e6
    if v < 1:
        return {"calc_uF": round(v, 4), "recommend_uF": round(max(v * 1.5, 0.1), 2)}
    std = [1, 2.2, 4.7, 10, 22, 47, 100, 220, 470, 1000, 2200, 4700]
    target = v * 1.5
    rec = next((s for s in std if s >= target * 0.85), std[-1])
    return {"calc_uF": round(v, 2), "recommend_uF": rec}


# ── AC-DC 整流 ────────────────────────────────────────────

def acdc_rectifier(topology: str, u2: float, alpha_deg: float = 0,
                   io: float = None, ripple_pct: float = 5.0, freq: float = 50):
    """
    u2: 相电压有效值 (V)；三相时 U2 为相电压。
    alpha_deg: 触发角 (°)，不可控整流忽略。
    """
    alpha = math.radians(alpha_deg)
    vm = SQRT2 * u2
    result = {"transform": "ac-dc", "topology": topology, "U2_rms_V": u2, "alpha_deg": alpha_deg}

    if topology == "single-half-uncontrolled":
        vd = vm / PI
        vrms = vm / 2
        ripple_f = freq
        result.update({
            "Vd_avg_V": round(vd, 2),
            "Vd_coeff": round(vd / u2, 3),
            "Vrms_out_V": round(vrms, 2),
            "ripple_freq_Hz": ripple_f,
            "note": "单相半波，输出脉动大，仅小功率",
        })
    elif topology == "single-full-uncontrolled":
        vd = 2 * vm / PI
        vrms = vm / SQRT2
        ripple_f = 2 * freq
        result.update({
            "Vd_avg_V": round(vd, 2),
            "Vd_coeff": round(vd / u2, 3),
            "Vrms_out_V": round(vrms, 2),
            "ripple_freq_Hz": ripple_f,
            "note": "单相桥式/全波，Vd ≈ 0.9·U2",
        })
    elif topology == "single-bridge-controlled":
        vd = (2 * vm / PI) * math.cos(alpha)
        vrms = vm * math.sqrt((PI - alpha + math.sin(2 * alpha) / 2) / PI) if alpha <= PI else 0
        ripple_f = 2 * freq
        result.update({
            "Vd_avg_V": round(vd, 2),
            "Vd_coeff": round(0.9 * math.cos(alpha), 4),
            "Vrms_out_V": round(vrms, 2),
            "ripple_freq_Hz": ripple_f,
            "alpha_range_deg": "0~180（阻感负载）",
            "inversion": alpha > 90,
            "note": "单相全控桥，Vd = 0.9·U2·cosα",
        })
    elif topology == "three-half-controlled":
        vd = (3 * math.sqrt(6) / (2 * PI)) * u2 * math.cos(alpha)  # 1.17·U2·cosα
        coeff = round(1.17 * math.cos(alpha), 4)
        ripple_f = 3 * freq
        result.update({
            "Vd_avg_V": round(vd, 2),
            "Vd_coeff": coeff,
            "ripple_freq_Hz": ripple_f,
            "note": "三相半波，Vd = 1.17·U2·cosα",
        })
    elif topology == "three-bridge-controlled":
        vd = (3 * math.sqrt(6) / PI) * u2 * math.cos(alpha)  # 2.34·U2·cosα
        coeff = round(2.34 * math.cos(alpha), 4)
        ripple_f = 6 * freq
        result.update({
            "Vd_avg_V": round(vd, 2),
            "Vd_coeff": coeff,
            "ripple_freq_Hz": ripple_f,
            "UL_rms_V": round(SQRT3 * u2, 2),
            "note": "三相全控桥，Vd = 2.34·U2·cosα；线电压 UL=√3·U2",
        })
    else:
        return {"error": f"未知 AC-DC 拓扑: {topology}"}

    if io is not None and vd > 0:
        pd = vd * io
        delta_v = ripple_pct / 100 * vd
        c_min = io / (ripple_f * delta_v) if ripple_f > 0 and delta_v > 0 else None
        result["load"] = {
            "Io_A": io,
            "Pd_W": round(pd, 2),
            "filter_ripple_pct": ripple_pct,
        }
        if c_min:
            result["filter"] = cap_standard(c_min)
            result["filter"]["delta_V_V"] = round(delta_v, 3)
        # 平波电感估算（阻感负载，电流连续）
        if topology in ("single-bridge-controlled", "three-bridge-controlled"):
            result["filter"]["L_min_hint_mH"] = round(2.5 * u2 / (1.414 * io * freq), 2)
            result["filter"]["L_note"] = "经验式 L( H )≥2.5·U2/(1.414·Id)，保证连续"

    return result


# ── DC-AC 逆变 ────────────────────────────────────────────

def svpwm_sector(valpha: float, vbeta: float) -> dict:
    """根据 Vα、Vβ 判断 SVPWM 扇区 (1~6)。"""
    if vbeta >= 0:
        if valpha >= 0:
            return 1 if vbeta <= SQRT3 * valpha else 2
        return 2 if vbeta <= -SQRT3 * valpha else 3
    if valpha >= 0:
        return 6 if -vbeta <= SQRT3 * valpha else 5
    return 4 if -vbeta <= -SQRT3 * valpha else 5


def svpwm_times(vdc: float, m: float, theta_deg: float, fsw_khz: float) -> dict:
    """三相 SVPWM 七段式：扇区、T1/T2/T0（μs）。"""
    theta = math.radians(theta_deg % 360)
    t = 1.0 / (fsw_khz * 1e3)
    valpha = m * (vdc / 2) * math.cos(theta)
    vbeta = m * (vdc / 2) * math.sin(theta)
    sector = svpwm_sector(valpha, vbeta)
    theta_s = (theta_deg % 360) - (sector - 1) * 60
    theta_r = math.radians(theta_s)
    t1 = m * t * math.sin(math.radians(60) - theta_r) / math.sin(math.radians(60))
    t2 = m * t * math.sin(theta_r) / math.sin(math.radians(60))
    t0 = max(t - t1 - t2, 0)
    return {
        "sector": sector,
        "theta_deg": round(theta_deg % 360, 2),
        "T1_us": round(t1 * 1e6, 2),
        "T2_us": round(t2 * 1e6, 2),
        "T0_us": round(t0 * 1e6, 2),
        "Tsw_us": round(t * 1e6, 2),
    }


def dcac_inverter(topology: str, vdc: float, m: float = 0.8,
                  fo: float = 50, fsw_khz: float = 10, theta_deg: float = 30):
    result = {"transform": "dc-ac", "topology": topology, "Vdc_V": vdc, "M": m}

    if topology == "single-h-bridge-spwm":
        vo_peak = m * vdc / 2
        vo_rms = vo_peak / SQRT2
        result.update({
            "Vo_fundamental_peak_V": round(vo_peak, 2),
            "Vo_fundamental_rms_V": round(vo_rms, 2),
            "fo_Hz": fo,
            "modulation": "SPWM/CPWM",
            "note": "单相 H 桥，基波峰值 Vo1 = M·Vdc/2",
            "overmodulation": m > 1,
        })
    elif topology == "three-phase-spwm":
        vl_peak = m * vdc / 2
        vl_rms = vl_peak / SQRT2
        vph_rms = vl_rms / SQRT3
        result.update({
            "Vl_fundamental_peak_V": round(vl_peak, 2),
            "Vl_fundamental_rms_V": round(vl_rms, 2),
            "Vph_fundamental_rms_V": round(vph_rms, 2),
            "note": "三相 SPWM，电压利用率较低",
        })
    elif topology == "three-phase-svpwm":
        vl_peak = (SQRT3 / 3) * vdc * m
        vl_rms = vl_peak / SQRT2
        vph_rms = vl_rms / SQRT3
        result.update({
            "Vl_fundamental_peak_V": round(vl_peak, 2),
            "Vl_fundamental_rms_V": round(vl_rms, 2),
            "Vph_fundamental_rms_V": round(vph_rms, 2),
            "max_linear_M": 1.0,
            "six_step_peak_V": round(SQRT3 / 3 * vdc, 2),
            "note": "三相 SVPWM 线性区 M≤1，比 SPWM 电压利用率高约 15.5%",
        })
        if theta_deg is not None:
            result["svpwm_timing"] = svpwm_times(vdc, m, theta_deg, fsw_khz)
            result["fsw_kHz"] = fsw_khz
    elif topology == "three-phase-npc":
        result.update(dcac_npc(vdc, m, fo))
    else:
        return {"error": f"未知 DC-AC 拓扑: {topology}"}

    result["fo_Hz"] = fo
    return result


def dcac_npc(vdc: float, m: float, fo: float) -> dict:
    """三相三电平 NPC 逆变器（SVM 线性区近似）。"""
    vcap = vdc / 2
    # 相电压三电平 ±Vdc/2, 0；线电压基波峰值（线性调制近似）
    vl_peak = (SQRT3 / 4) * vdc * m
    vl_rms = vl_peak / SQRT2
    vph_rms = vl_rms / SQRT3
    vph_peak = m * vcap
    return {
        "Vl_fundamental_peak_V": round(vl_peak, 2),
        "Vl_fundamental_rms_V": round(vl_rms, 2),
        "Vph_fundamental_peak_V": round(vph_peak, 2),
        "Vph_fundamental_rms_V": round(vph_rms, 2),
        "Vdc_total_V": vdc,
        "Vcap_each_V": round(vcap, 2),
        "max_linear_M": 1.0,
        "device_voltage_stress_V": round(vcap, 2),
        "topology_devices": "12 开关 + 6 钳位二极管（每桥臂 2 开关 + 1 钳位管）",
        "output_levels_per_phase": 3,
        "output_levels_line": 5,
        "vs_two_level_svpwm": {
            "two_level_Vl_peak_at_M1": round(SQRT3 / 3 * vdc, 2),
            "npc_advantage": "器件耐压 Vdc/2；dv/dt 更低；THD 更好",
        },
        "note": "NPC 中点电位需平衡控制；详见 references/simulink-templates.md",
    }


# ── DC-DC 斩波（复用原有逻辑）────────────────────────────

def buck_design(vin, vo, io, fsw, k=0.3, cap_ripple=0.01):
    d = vo / vin
    f = fsw * 1e3
    delta_v = cap_ripple * vo
    l = (vin - vo) * d / (k * io * f)
    c = io * d / (f * delta_v)
    delta_il = (vin - vo) * d / (l * f)
    l_crit = (vin - vo) * vo / (2 * io * vin * f)
    return {
        "topology": "buck", "mode": "CCM" if l >= l_crit else "DCM",
        "duty_ratio": round(d, 4),
        "inductance": {"calc_uH": round(l * 1e6, 2), "recommend_uH": e12_round(l * 1e6),
                       "Lcrit_uH": round(l_crit * 1e6, 2)},
        "capacitance": cap_standard(c),
        "ripple": {"delta_IL_A": round(delta_il, 4)},
        "stress": {"switch_Vds_V": round(vin, 2), "switch_Id_peak_A": round(io + delta_il / 2, 4),
                   "diode_Vr_V": round(vin, 2)},
    }


def boost_design(vin, vo, io, fsw, k=0.3, cap_ripple=0.01):
    d = 1 - vin / vo
    iin = io / (1 - d)
    f = fsw * 1e3
    delta_v = cap_ripple * vo
    l = vin * d / (k * iin * f)
    c = io * d / ((1 - d) * f * delta_v)
    delta_il = vin * d / (l * f)
    l_crit = vin * d / (2 * iin * f)
    return {
        "topology": "boost", "mode": "CCM" if l >= l_crit else "DCM",
        "duty_ratio": round(d, 4), "input_current_A": round(iin, 4),
        "inductance": {"calc_uH": round(l * 1e6, 2), "recommend_uH": e12_round(l * 1e6),
                       "Lcrit_uH": round(l_crit * 1e6, 2)},
        "capacitance": cap_standard(c),
        "ripple": {"delta_IL_A": round(delta_il, 4)},
        "stress": {"switch_Vds_V": round(vo, 2), "switch_Id_peak_A": round(iin + delta_il / 2, 4),
                   "diode_Vr_V": round(vo, 2)},
    }


def buck_boost_design(vin, vo_abs, io_abs, fsw, k=0.3, cap_ripple=0.01):
    vo, io = abs(vo_abs), abs(io_abs)
    d = vo / (vin + vo)
    iin = d * io / (1 - d)
    f = fsw * 1e3
    delta_v = cap_ripple * vo
    l = vin * d / (k * iin * f)
    c = io * d / (f * delta_v)
    delta_il = vin * d / (l * f)
    return {
        "topology": "buck-boost", "output_polarity": "inverted",
        "duty_ratio": round(d, 4), "input_current_A": round(iin, 4),
        "inductance": {"calc_uH": round(l * 1e6, 2), "recommend_uH": e12_round(l * 1e6)},
        "capacitance": cap_standard(c),
        "ripple": {"delta_IL_A": round(delta_il, 4)},
        "stress": {"switch_Vds_V": round(vin + vo, 2), "switch_Id_peak_A": round(iin + delta_il / 2, 4)},
    }


def dcdc_calc(topology, vin, vo, io, fsw, k, cap_ripple, mode="design", l_uh=None,
              n_ratio=0.2, po=None, eta=0.85, lr=None, cr=None, lm=None):
    if mode == "analyze" and l_uh is not None:
        return dcdc_analyze(topology, vin, vo, io, fsw, l_uh)
    if topology == "buck":
        if vin <= vo:
            return {"error": "Buck 要求 Vin > Vo"}
        return buck_design(vin, vo, io, fsw, k, cap_ripple)
    if topology == "boost":
        if vin >= vo:
            return {"error": "Boost 要求 Vin < Vo"}
        return boost_design(vin, vo, io, fsw, k, cap_ripple)
    if topology == "buck-boost":
        return buck_boost_design(vin, vo, io, fsw, k, cap_ripple)
    if topology == "flyback":
        return flyback_design(vin, vo, io, fsw, n_ratio, eta)
    if topology == "flyback-qr":
        return {"error": "flyback-qr 需 --vin-min 和 --vin-max，请用 CLI 直接调用"}
    if topology == "llc":
        return llc_analyze(vin, vo, po or vin * io, fsw, lr, cr, lm, n_ratio)
    return {"error": f"未知 DC-DC 拓扑: {topology}"}


def dcdc_analyze(topology, vin, vo, io, fsw, l_uh):
    l = l_uh * 1e-6
    f = fsw * 1e3
    r = vo / io if io else None
    if topology == "buck":
        d = vo / vin
        delta_il = (vin - vo) * d / (l * f)
        l_crit = (vin - vo) * vo / (2 * io * vin * f)
        if l >= l_crit:
            return {"topology": "buck", "mode": "CCM", "duty_ratio": round(d, 4),
                    "delta_IL_A": round(delta_il, 4), "IL_min_A": round(io - delta_il / 2, 4),
                    "stress": {"Id_peak_A": round(io + delta_il / 2, 4)}}
        if r:
            vo_dcm = vin * d ** 2 * r / (2 * l * f)
            return {"topology": "buck", "mode": "DCM", "duty_ratio": round(d, 4),
                    "Vo_DCM_V": round(vo_dcm, 2), "note": "DCM: Vo = Vin·D²·R/(2Lf)"}
    if topology == "boost":
        d = 1 - vin / vo
        iin = io / (1 - d)
        delta_il = vin * d / (l * f)
        l_crit = vin * d / (2 * iin * f)
        if l >= l_crit:
            return {"topology": "boost", "mode": "CCM", "duty_ratio": round(d, 4),
                    "input_current_A": round(iin, 4), "delta_IL_A": round(delta_il, 4),
                    "stress": {"Vds_V": round(vo, 2), "Id_peak_A": round(iin + delta_il / 2, 4)}}
        if r:
            vo_dcm = vin / (1 - math.sqrt(1 - vin ** 2 * d ** 2 * r / (2 * l * f * vo)))
            return {"topology": "boost", "mode": "DCM", "note": "DCM Boost 负载相关，需迭代验证"}
    return {"error": f"analyze 不支持 {topology}，可用 buck/boost"}


def flyback_design(vin, vo, io, fsw, n_ratio=0.2, eta=0.85):
    """n_ratio = Ns/Np，DCM Flyback 设计。"""
    po = vo * io
    pin = po / eta
    d = (n_ratio * vo) / (vin + n_ratio * vo)
    t = 1.0 / (fsw * 1e3)
    lm = vin ** 2 * d ** 2 * t / (2 * pin)
    ipk = vin * d * t / lm if lm > 0 else 0
    vds = vin + vo / n_ratio
    id_avg_sec = io / (1 - d)
    lm_uh = lm * 1e6
    lm_disp = {"calc_uH": round(lm_uh, 2)} if lm_uh < 1000 else {"calc_mH": round(lm * 1e3, 3)}
    if lm_uh < 1000:
        lm_disp["recommend_uH"] = e12_round(lm_uh)
    else:
        lm_disp["recommend_mH"] = e12_round(lm * 1e3)
    return {
        "topology": "flyback", "mode": "DCM",
        "turns_ratio_Ns_Np": round(n_ratio, 4),
        "duty_ratio": round(d, 4),
        "magnetizing_inductance": lm_disp,
        "power": {"Po_W": round(po, 2), "Pin_W": round(pin, 2), "eta": eta},
        "stress": {
            "switch_Vds_V": round(vds * 1.2, 1),
            "switch_Vds_note": "加 20% 漏感尖峰裕量",
            "Ipk_pri_A": round(ipk, 3),
            "Id_sec_avg_A": round(id_avg_sec, 3),
        },
        "note": "DCM 反激；多输出需单独核算各绕组能量",
    }


def flyback_qr(vin_min, vin_max, vo, io, fsw_max_khz, n_ratio=0.2, eta=0.85):
    """
    QR/BCM 反激：频率随 Vin 变化。
    设计点：Vin_min + 满载时 fsw = fsw_max → 定 Lm。
    fsw(Vin) ≈ Vin²/(Vin_min²)·fsw_max（恒功率近似）
    """
    po = vo * io
    pin = po / eta
    fsw_max = fsw_max_khz * 1e3

    def d_at(vin):
        return (n_ratio * vo) / (vin + n_ratio * vo)

    lm = vin_min ** 2 / (2 * pin * fsw_max)
    d_min = d_at(vin_min)

    f_min = fsw_max
    f_max = vin_max ** 2 / vin_min ** 2 * fsw_max
    ipk_min = math.sqrt(2 * pin / (lm * f_min)) if lm * f_min > 0 else 0
    ipk_max = math.sqrt(2 * pin / (lm * f_max)) if lm * f_max > 0 else 0
    vds = vin_max + vo / n_ratio

    lm_uh = lm * 1e6
    return {
        "topology": "flyback-qr", "mode": "QR/BCM",
        "turns_ratio_Ns_Np": round(n_ratio, 4),
        "Vin_range_V": {"min": vin_min, "max": vin_max},
        "duty_at_Vin_min": round(d_min, 4),
        "duty_at_Vin_max": round(d_at(vin_max), 4),
        "magnetizing_inductance": {
            "calc_uH": round(lm_uh, 2),
            "recommend_uH": e12_round(lm_uh),
        },
        "switching_frequency_kHz": {
            "at_Vin_min_full_load": round(f_min / 1e3, 1),
            "at_Vin_max_full_load": round(f_max / 1e3, 1),
            "fsw_max_design_kHz": fsw_max_khz,
            "note": "fsw proportional to Vin^2 (constant power); light load freq higher",
        },
        "power": {"Po_W": round(po, 2), "Pin_W": round(pin, 2), "eta": eta},
        "stress": {
            "switch_Vds_V": round(vds * 1.2, 1),
            "Ipk_at_Vin_min_A": round(ipk_min, 3),
            "Ipk_at_Vin_max_A": round(ipk_max, 3),
        },
        "note": "QR 反激适合宽输入适配器；需限制 fsw 上限与 EMI",
    }


def llc_analyze(vin, vo, po, fsw_khz, lr_uh, cr_nf, lm_uh, n_ratio=1.0):
    """LLC 谐振参数分析（FHA 近似）。"""
    if not all([lr_uh, cr_nf, lm_uh]):
        return {"error": "LLC 需要 --lr (μH)、--cr (nF)、--lm (μH)"}
    lr = lr_uh * 1e-6
    cr = cr_nf * 1e-9
    lm = lm_uh * 1e-6
    fr = 1.0 / (2 * PI * math.sqrt(lr * cr))
    fn = (fsw_khz * 1e3) / fr
    m = lm / lr
    z0 = math.sqrt(lr / cr)
    rac = (8 / PI ** 2) * n_ratio ** 2 * vo ** 2 / po
    q = z0 / rac if rac > 0 else 0
    denom = math.sqrt((1 + m - m / fn ** 2) ** 2 + (q * (1 / fn ** 2 - 1)) ** 2)
    gain = m / denom if denom > 0 else 0
    vo_est = vin * gain / n_ratio
    zvs = fn < 1.0
    warn = []
    if q > 5:
        warn.append("Q 偏大，增益可能被压低，建议减小 Lr/Cr 或增大 n")
    if q < 0.2:
        warn.append("Q 偏小，环流损耗可能增大")
    if abs(vo_est - vo) / vo > 0.15:
        warn.append("估算 Vo 与目标偏差>15%，需调整 fr/fn 或匝比，并仿真验证")
    return {
        "topology": "llc",
        "resonant_freq_kHz": round(fr / 1e3, 2),
        "switching_freq_kHz": fsw_khz,
        "fn_ratio": round(fn, 3),
        "Lm_Lr_ratio": round(m, 2),
        "quality_factor_Q": round(q, 3),
        "voltage_gain_M": round(gain, 4),
        "Vo_estimated_V": round(vo_est, 2),
        "Vo_target_V": vo,
        "ZVS_region": zvs,
        "ZVS_note": "fn<1 通常原边 ZVS 区；fn>1 升压区，需仿真确认",
        "turns_ratio_Np_Ns": round(1 / n_ratio, 4) if n_ratio else None,
        "warnings": warn if warn else None,
    }


def boost_pfc(vin_rms, vo, po, fsw_min_khz, eta=0.9, freq=50):
    """CRM/边界 Boost PFC 电感估算。"""
    vin_pk = SQRT2 * vin_rms
    if vo <= vin_pk:
        return {"error": f"Vo ({vo}V) 应 > 输入峰值 {round(vin_pk, 1)}V"}
    d_max = 1 - vin_pk / vo
    fsw_min = fsw_min_khz * 1e3
    lm = vin_pk ** 2 / (2 * po * fsw_min)
    ipk_line = SQRT2 * po / (eta * vin_rms) * (1 + math.pi / (4 * math.tan(d_max))) if d_max > 0.01 else po / vin_rms
    ipk_simple = 2 * SQRT2 * po / (eta * vin_rms)
    return {
        "transform": "ac-dc", "topology": "boost-pfc", "mode": "CRM/BCM",
        "Vin_rms_V": vin_rms, "Vin_peak_V": round(vin_pk, 2),
        "Vo_bus_V": vo, "Po_W": po,
        "D_max_at_line_peak": round(d_max, 4),
        "inductance": {
            "calc_mH": round(lm * 1e3, 3),
            "recommend_mH": e12_round(lm * 1e3 * 10) / 10,
        },
        "current": {
            "Ipk_approx_A": round(ipk_simple, 3),
            "note": "峰值电流近似 2√2·Po/(η·Vin_rms)",
        },
        "fsw_min_kHz": fsw_min_khz,
        "line_freq_Hz": freq,
        "note": "CRM PFC；全输入范围需校核最低/最高开关频率",
    }


def acdc_rl_load(u2, alpha_deg, r, l_mh, freq=50):
    """单相全控桥阻感负载：临界角与工况判定。"""
    l = l_mh * 1e-3
    omega = 2 * PI * freq
    alpha_crit = math.degrees(math.atan(omega * l / r))
    alpha = alpha_deg
    continuous = alpha >= alpha_crit
    vm = SQRT2 * u2
    vd = (2 * vm / PI) * math.cos(math.radians(alpha)) if continuous else None
    return {
        "transform": "ac-dc", "topology": "single-bridge-rl",
        "U2_rms_V": u2, "R_ohm": r, "L_mH": l_mh,
        "alpha_critical_deg": round(alpha_crit, 2),
        "alpha_given_deg": alpha,
        "current_mode": "连续" if continuous else "断续/临界",
        "Vd_avg_V": round(vd, 2) if vd else "需分段积分（断续）",
        "note": "连续时 Vd=0.9·U2·cosα；α<α_crit 时电流断续，公式不同",
    }


def rectifier_pf(topology, alpha_deg):
    """相控整流位移功率因数近似。"""
    alpha = math.radians(alpha_deg)
    pf = math.cos(alpha)
    return {
        "transform": "ac-dc", "topology": topology,
        "alpha_deg": alpha_deg,
        "displacement_PF": round(pf, 4),
        "note": "理想连续电流仅位移因子；实际 PF 含谐波，α 越大 PF 越低",
    }


# ── AC-AC 交流变换 ────────────────────────────────────────

def acac_calc(topology: str, u2: float, alpha_deg: float = 0,
              duty: float = 0.5, fin: float = 50, fout: float = 10,
              pulse_ratio: int = 3):
    """
    u2: 输入相/线电压有效值 (V)
    alpha_deg: 相控触发角
    duty: 交流斩波占空比
    pulse_ratio: 交交变频拍数比 (fout = fin / ratio 近似)
    """
    alpha = math.radians(alpha_deg)
    result = {"transform": "ac-ac", "topology": topology, "Uin_rms_V": u2}

    if topology == "single-phase-control":
        # 电阻负载相控调压
        vo_rms = u2 * math.sqrt((PI - alpha + math.sin(2 * alpha) / 2) / PI)
        result.update({
            "alpha_deg": alpha_deg,
            "Vo_rms_V": round(vo_rms, 2),
            "voltage_ratio": round(vo_rms / u2, 4),
            "note": "单相相控调压器（电阻负载），反并联晶闸管",
        })
    elif topology == "three-phase-control":
        vo_rms = u2 * math.sqrt((PI - alpha + math.sin(2 * alpha) / 2) / PI)
        result.update({
            "alpha_deg": alpha_deg,
            "Vo_rms_V": round(vo_rms, 2),
            "voltage_ratio": round(vo_rms / u2, 4),
            "note": "三相相控调压（Y 接，每相独立相控，电阻负载近似）",
        })
    elif topology == "ac-chopper":
        vo_rms = u2 * math.sqrt(duty)
        result.update({
            "duty_ratio": duty,
            "Vo_rms_V": round(vo_rms, 2),
            "voltage_ratio": round(math.sqrt(duty), 4),
            "note": "交流斩波（电阻负载），Vo = Vin·√D",
        })
    elif topology == "cycloconverter":
        fout_calc = fin / pulse_ratio
        result.update({
            "fin_Hz": fin,
            "fout_Hz": round(fout_calc, 2),
            "pulse_ratio": pulse_ratio,
            "max_fout_rule": "fout << fin，通常 fout ≤ fin/3 ~ fin/10",
            "note": f"交交变频（{pulse_ratio} 脉波），输出频率约为 fin/{pulse_ratio}",
        })
    elif topology == "matrix-basic":
        result.update({
            "fin_Hz": fin,
            "fout_max_Hz": round(fin / 3, 2),
            "note": "矩阵变换器：理论 fout < fin/3，四象限运行，无中间 DC 环节",
        })
    else:
        return {"error": f"未知 AC-AC 拓扑: {topology}"}

    if fout and topology == "cycloconverter":
        result["requested_fout_Hz"] = fout
    return result


# ── CLI ───────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="四大电力变换计算")
    p.add_argument("--transform", required=True,
                   choices=["ac-dc", "dc-ac", "dc-dc", "ac-ac"])
    p.add_argument("--topology", required=True, help="具体拓扑名称")
    p.add_argument("--mode", default="design", choices=["design", "analyze"])
    p.add_argument("--eta", type=float, default=0.85, help="效率 (Flyback/PFC)")
    p.add_argument("--po", type=float, help="输出功率 (W)")
    p.add_argument("--n-ratio", type=float, default=0.2, help="匝比 Ns/Np (Flyback/LLC)")
    p.add_argument("--r", type=float, help="负载电阻 (Ω)，RL 整流/DCM")
    p.add_argument("--l-mh", type=float, help="电感 (mH)，RL 整流或 LLC 的 Lm")
    p.add_argument("--lr", type=float, help="谐振电感 Lr (μH)")
    p.add_argument("--cr", type=float, help="谐振电容 Cr (nF)")
    p.add_argument("--lm", type=float, help="励磁电感 Lm (μH)，LLC")

    # 通用 / AC
    p.add_argument("--u2", type=float, help="相电压有效值 (V)")
    p.add_argument("--alpha", type=float, default=0, help="触发角 (°)")
    p.add_argument("--freq", type=float, default=50, help="工频 (Hz)")
    p.add_argument("--io", type=float, help="负载电流 (A)")
    p.add_argument("--ripple", type=float, default=5, help="滤波纹波 (%)")

    # DC
    p.add_argument("--vin", type=float, help="输入电压 (V)")
    p.add_argument("--vin-min", type=float, help="QR Flyback 最低输入 (V)")
    p.add_argument("--vin-max", type=float, help="QR Flyback 最高输入 (V)")
    p.add_argument("--fsw-max", type=float, help="QR Flyback 最高开关频率 (kHz)")
    p.add_argument("--vo", type=float, help="输出电压 (V)")
    p.add_argument("--vdc", type=float, help="直流母线 (V)")
    p.add_argument("--fsw", type=float, default=100, help="开关频率 (kHz)")
    p.add_argument("--l", type=float, help="电感 (μH)，DC-DC analyze")
    p.add_argument("--k", type=float, default=0.3, help="电感纹波比")
    p.add_argument("--cap-ripple", type=float, default=0.01, help="电容纹波比 ΔV/V")

    # 逆变 / AC-AC
    p.add_argument("--m", type=float, default=0.8, help="调制比 M")
    p.add_argument("--fo", type=float, default=50, help="输出频率 (Hz)")
    p.add_argument("--theta", type=float, default=30, help="SVPWM 电角度 (°)")
    p.add_argument("--duty", type=float, default=0.5, help="交流斩波占空比")
    p.add_argument("--pulse-ratio", type=int, default=3, help="交交变频拍比")

    args = p.parse_args()
    t = args.transform

    if t == "ac-dc":
        if args.topology == "boost-pfc":
            if args.u2 is None or args.vo is None or args.po is None:
                print(json.dumps({"error": "boost-pfc 需要 --u2 --vo --po"}, ensure_ascii=False))
                sys.exit(1)
            result = boost_pfc(args.u2, args.vo, args.po, args.fsw, args.eta, args.freq)
        elif args.topology == "single-bridge-rl":
            if args.u2 is None or args.r is None or args.l_mh is None:
                print(json.dumps({"error": "single-bridge-rl 需要 --u2 --r --l-mh"}, ensure_ascii=False))
                sys.exit(1)
            result = acdc_rl_load(args.u2, args.alpha, args.r, args.l_mh, args.freq)
        elif args.topology == "rectifier-pf":
            result = rectifier_pf("controlled-bridge", args.alpha)
        elif args.u2 is None:
            print(json.dumps({"error": "AC-DC 需要 --u2 相电压有效值"}, ensure_ascii=False))
            sys.exit(1)
        else:
            result = acdc_rectifier(args.topology, args.u2, args.alpha, args.io, args.ripple, args.freq)

    elif t == "dc-ac":
        vdc = args.vdc or args.vin
        if vdc is None:
            print(json.dumps({"error": "DC-AC 需要 --vdc 或 --vin"}, ensure_ascii=False))
            sys.exit(1)
        result = dcac_inverter(args.topology, vdc, args.m, args.fo, args.fsw, args.theta)

    elif t == "dc-dc":
        if args.topology == "flyback-qr":
            vin_min = args.vin_min or args.vin
            vin_max = args.vin_max or args.vin
            fsw_max = args.fsw_max or args.fsw
            if not all([vin_min, vin_max, args.vo, args.io]):
                print(json.dumps({"error": "flyback-qr 需要 --vin-min --vin-max --vo --io"}, ensure_ascii=False))
                sys.exit(1)
            result = flyback_qr(vin_min, vin_max, args.vo, args.io, fsw_max, args.n_ratio, args.eta)
            result["transform"] = "dc-dc"
        elif args.topology == "llc":
            if args.vin is None or args.vo is None:
                print(json.dumps({"error": "LLC 需要 --vin --vo"}, ensure_ascii=False))
                sys.exit(1)
            po = args.po or (args.io or 1.0) * args.vo
            result = llc_analyze(args.vin, args.vo, po, args.fsw, args.lr, args.cr, args.lm, args.n_ratio)
            result["transform"] = "dc-dc"
        elif args.vin is None or args.vo is None:
            print(json.dumps({"error": "DC-DC 需要 --vin 和 --vo"}, ensure_ascii=False))
            sys.exit(1)
        else:
            io = args.io or 1.0
            result = dcdc_calc(args.topology, args.vin, args.vo, io, args.fsw, args.k,
                               args.cap_ripple, args.mode, args.l, args.n_ratio,
                               args.po, args.eta, args.lr, args.cr, args.lm)
            result["transform"] = "dc-dc"

    elif t == "ac-ac":
        if args.u2 is None:
            print(json.dumps({"error": "AC-AC 需要 --u2 输入电压有效值"}, ensure_ascii=False))
            sys.exit(1)
        result = acac_calc(args.topology, args.u2, args.alpha, args.duty, args.freq, args.fo, args.pulse_ratio)

    else:
        result = {"error": f"未知 transform: {t}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
