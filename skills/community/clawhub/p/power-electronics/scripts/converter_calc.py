#!/usr/bin/env python3
"""
电力电子技术 Skill - DC-DC 变换器设计/分析计算
零依赖，仅 Python 标准库。输出 JSON。
"""

import argparse
import json
import math
import sys


def e12_round(value: float, unit: str = "") -> float:
    """将数值取整到 E12 系列（简化版，适用于 μH 量级）。"""
    if value <= 0:
        return value
    e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
    exp = math.floor(math.log10(value))
    mant = value / (10 ** exp)
    best = min(e12, key=lambda x: abs(x - mant))
    return round(best * (10 ** exp), 2)


def cap_standard(value_f: float) -> dict:
    """电容推荐：取计算值 ×1.5 后选常用档。"""
    v = value_f * 1e6  # μF
    if v < 1:
        rec = max(v * 1.5, 0.1)
        return {"calc_uF": round(v, 4), "recommend_uF": round(rec, 2), "note": "小电容建议 MLCC"}
    std = [1, 2.2, 4.7, 10, 22, 47, 100, 220, 470, 1000]
    target = v * 1.5
    rec = min(std, key=lambda x: abs(x - target) if x >= target * 0.8 else float("inf"))
    if rec < target * 0.5:
        rec = next((s for s in std if s >= target), std[-1])
    return {"calc_uF": round(v, 2), "recommend_uF": rec}


def buck_design(vin, vo, io, fsw, k=0.3, cap_ripple=0.01):
    d = vo / vin
    f = fsw * 1e3
    delta_v = cap_ripple * vo
    l = (vin - vo) * d / (k * io * f)
    c = io * d / (f * delta_v)
    delta_il = (vin - vo) * d / (l * f)
    l_crit = (vin - vo) * vo / (2 * io * vin * f)
    mode = "CCM" if l >= l_crit else "DCM"
    return {
        "topology": "buck",
        "mode": mode,
        "duty_ratio": round(d, 4),
        "inductance": {
            "calc_H": round(l, 6),
            "calc_uH": round(l * 1e6, 2),
            "recommend_uH": e12_round(l * 1e6),
            "Lcrit_uH": round(l_crit * 1e6, 2),
        },
        "capacitance": cap_standard(c),
        "ripple": {"delta_IL_A": round(delta_il, 4), "k": k},
        "stress": {
            "switch_Vds_V": round(vin, 2),
            "switch_Id_peak_A": round(io + delta_il / 2, 4),
            "switch_Id_rms_A": round(math.sqrt(io ** 2 + delta_il ** 2 / 12), 4),
            "diode_Vr_V": round(vin, 2),
            "diode_Id_avg_A": round(io, 4),
        },
    }


def buck_analyze(vin, vo, l_uh, fsw, io=None):
    l = l_uh * 1e-6
    f = fsw * 1e3
    d = vo / vin
    delta_il = (vin - vo) * d / (l * f)
    l_crit = (vin - vo) * vo / (2 * (io or 1) * vin * f) if io else None
    result = {
        "topology": "buck",
        "duty_ratio": round(d, 4),
        "delta_IL_A": round(delta_il, 4),
        "inductance_uH": l_uh,
    }
    if io:
        mode = "CCM" if l >= l_crit else "DCM"
        result["mode"] = mode
        result["Lcrit_uH"] = round(l_crit * 1e6, 2)
        result["IL_min_A"] = round(io - delta_il / 2, 4)
        result["stress"] = {
            "switch_Id_peak_A": round(io + delta_il / 2, 4),
        }
    return result


def boost_design(vin, vo, io, fsw, k=0.3, cap_ripple=0.01):
    d = 1 - vin / vo
    iin = io / (1 - d)
    f = fsw * 1e3
    delta_v = cap_ripple * vo
    l = vin * d / (k * iin * f)
    c = io * d / ((1 - d) * f * delta_v)
    delta_il = vin * d / (l * f)
    l_crit = vin * d / (2 * iin * f)
    mode = "CCM" if l >= l_crit else "DCM"
    return {
        "topology": "boost",
        "mode": mode,
        "duty_ratio": round(d, 4),
        "input_current_A": round(iin, 4),
        "inductance": {
            "calc_H": round(l, 6),
            "calc_uH": round(l * 1e6, 2),
            "recommend_uH": e12_round(l * 1e6),
            "Lcrit_uH": round(l_crit * 1e6, 2),
        },
        "capacitance": cap_standard(c),
        "ripple": {"delta_IL_A": round(delta_il, 4), "k": k},
        "stress": {
            "switch_Vds_V": round(vo, 2),
            "switch_Id_peak_A": round(iin + delta_il / 2, 4),
            "diode_Vr_V": round(vo, 2),
            "diode_Id_avg_A": round(io, 4),
        },
    }


def boost_analyze(vin, vo, l_uh, fsw, io=None):
    l = l_uh * 1e-6
    f = fsw * 1e3
    d = 1 - vin / vo
    delta_il = vin * d / (l * f)
    iin = io / (1 - d) if io else None
    result = {
        "topology": "boost",
        "duty_ratio": round(d, 4),
        "delta_IL_A": round(delta_il, 4),
        "inductance_uH": l_uh,
    }
    if io and iin:
        l_crit = vin * d / (2 * iin * f)
        result["mode"] = "CCM" if l >= l_crit else "DCM"
        result["input_current_A"] = round(iin, 4)
        result["Lcrit_uH"] = round(l_crit * 1e6, 2)
        result["stress"] = {
            "switch_Vds_V": round(vo, 2),
            "switch_Id_peak_A": round(iin + delta_il / 2, 4),
        }
    return result


def buck_boost_design(vin, vo_abs, io_abs, fsw, k=0.3, cap_ripple=0.01):
    vo = abs(vo_abs)
    io = abs(io_abs)
    d = vo / (vin + vo)
    iin = d * io / (1 - d)
    f = fsw * 1e3
    delta_v = cap_ripple * vo
    l = vin * d / (k * iin * f)
    c = io * d / (f * delta_v)
    delta_il = vin * d / (l * f)
    v_stress = vin + vo
    return {
        "topology": "buck-boost",
        "mode": "CCM",
        "output_polarity": "inverted",
        "duty_ratio": round(d, 4),
        "input_current_A": round(iin, 4),
        "inductance": {
            "calc_uH": round(l * 1e6, 2),
            "recommend_uH": e12_round(l * 1e6),
        },
        "capacitance": cap_standard(c),
        "ripple": {"delta_IL_A": round(delta_il, 4)},
        "stress": {
            "switch_Vds_V": round(v_stress, 2),
            "switch_Id_peak_A": round(iin + delta_il / 2, 4),
            "diode_Vr_V": round(v_stress, 2),
        },
    }


def boundary(vin, vo, fsw, topology, r_load=None):
    """CCM/DCM 临界参数。"""
    f = fsw * 1e3
    if topology == "buck":
        if r_load is None:
            return {"error": "buck boundary 需要 --r 负载电阻 (Ω)"}
        io = vo / r_load
        l_crit = (vin - vo) * vo / (2 * io * vin * f)
        return {"topology": "buck", "Lcrit_uH": round(l_crit * 1e6, 2), "Io_crit_A": round(io, 4)}
    if topology == "boost":
        if r_load is None:
            return {"error": "boost boundary 需要 --r 负载电阻 (Ω)"}
        io = vo / r_load
        d = 1 - vin / vo
        iin = io / (1 - d)
        l_crit = vin * d / (2 * iin * f)
        return {"topology": "boost", "Lcrit_uH": round(l_crit * 1e6, 2), "Iin_crit_A": round(iin, 4)}
    return {"error": f"boundary 不支持 {topology}"}


def main():
    parser = argparse.ArgumentParser(description="DC-DC 变换器计算 (电力电子 Skill)")
    parser.add_argument("--topology", required=True, choices=["buck", "boost", "buck-boost"])
    parser.add_argument("--mode", default="design", choices=["design", "analyze", "boundary"])
    parser.add_argument("--vin", type=float, required=True, help="输入电压 (V)")
    parser.add_argument("--vo", type=float, help="输出电压 (V)，buck-boost 可负")
    parser.add_argument("--io", type=float, default=1.0, help="输出电流 (A)")
    parser.add_argument("--fsw", type=float, default=100, help="开关频率 (kHz)")
    parser.add_argument("--l", type=float, help="电感 (μH)，analyze 模式")
    parser.add_argument("--k", type=float, default=0.3, help="纹波系数 ΔI/I")
    parser.add_argument("--cap-ripple", type=float, default=0.01, help="输出电压纹波比 ΔV/V")
    parser.add_argument("--r", type=float, help="负载电阻 (Ω)，boundary 模式")
    args = parser.parse_args()

    if args.mode == "boundary":
        if args.vo is None:
            print(json.dumps({"error": "boundary 模式需要 --vo"}, ensure_ascii=False))
            sys.exit(1)
        result = boundary(args.vin, args.vo, args.fsw, args.topology, args.r)
    elif args.mode == "analyze":
        if args.l is None or args.vo is None:
            print(json.dumps({"error": "analyze 模式需要 --l 和 --vo"}, ensure_ascii=False))
            sys.exit(1)
        if args.topology == "buck":
            result = buck_analyze(args.vin, args.vo, args.l, args.fsw, args.io)
        elif args.topology == "boost":
            result = boost_analyze(args.vin, args.vo, args.l, args.fsw, args.io)
        else:
            result = {"error": "buck-boost analyze 暂未实现，请用 design 模式"}
    else:
        if args.vo is None:
            print(json.dumps({"error": "design 模式需要 --vo"}, ensure_ascii=False))
            sys.exit(1)
        if args.topology == "buck":
            if args.vin <= args.vo:
                print(json.dumps({"error": "Buck 要求 Vin > Vo"}, ensure_ascii=False))
                sys.exit(1)
            result = buck_design(args.vin, args.vo, args.io, args.fsw, args.k, args.cap_ripple)
        elif args.topology == "boost":
            if args.vin >= args.vo:
                print(json.dumps({"error": "Boost 要求 Vin < Vo"}, ensure_ascii=False))
                sys.exit(1)
            result = boost_design(args.vin, args.vo, args.io, args.fsw, args.k, args.cap_ripple)
        else:
            result = buck_boost_design(args.vin, args.vo, args.io, args.fsw, args.k, args.cap_ripple)

    result["inputs"] = {
        "vin_V": args.vin,
        "vo_V": args.vo,
        "io_A": args.io,
        "fsw_kHz": args.fsw,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
