#!/usr/bin/env python3
"""
report_gen.py - 电机PID调参报告生成器

整合三环参数计算、Q格式、前馈、校验、保护、稳定性分析，
输出可交付的Markdown/HTML调参报告。
"""

import sys
import os
import json
import datetime
import argparse

# 导入main.py中的计算函数
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import (
    calculate_current_loop_pi,
    calculate_speed_loop_pi,
    calculate_position_loop_pid,
    calculate_q_format,
    calculate_feedforward,
    check_bandwidth_ratio,
    discretize_params,
    validate_params,
    calculate_protection,
    calculate_stability,
    suggest_bandwidth,
    KD_DIGITAL_NOTE,
)


def generate_report(motor_params, tuning_options, output_format="markdown"):
    """
    生成完整调参报告。

    Args:
        motor_params: dict with keys Rs, Ls, J, B, Kt, psi_f, pole_pairs,
                      vbus, imax, pwm_freq, rated_current, rated_speed
        tuning_options: dict with keys bw_current, zeta, ts,
                        include_position, include_protection, include_stability,
                        platform, motor_model
        output_format: markdown / html / json
    """
    p = motor_params
    o = tuning_options

    Rs = p.get("Rs")
    Ls = p.get("Ls")
    J = p.get("J")
    B = p.get("B", 0)
    Kt = p.get("Kt")
    psi_f = p.get("psi_f", 0)
    pole_pairs = p.get("pole_pairs", 1)
    vbus = p.get("vbus", 24.0)
    imax = p.get("imax", 10.0)
    ts = o.get("ts", 50e-6)
    zeta = o.get("zeta", 0.707)
    pwm_freq = p.get("pwm_freq", 20.0)
    rated_current = p.get("rated_current", imax)

    # 带宽设置
    bw_current = o.get("bw_current")
    if not bw_current:
        if Rs and Ls:
            suggestion = suggest_bandwidth(pwm_freq, {"Rs": Rs, "Ls": Ls})
            bw_current = suggestion.get("recommended_bw_current_hz", 1000)
        else:
            bw_current = 1000.0
    bw_speed = bw_current / 10
    bw_position = bw_speed / 10

    report = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "motor_model": p.get("motor_model", "未指定"),
        "platform": o.get("platform", "STM32"),
        "motor_params": p,
        "tuning_options": o,
    }

    # 1. 电流环
    if Rs and Ls:
        curr = calculate_current_loop_pi(Rs, Ls, bw_current)
        curr_d = discretize_params(curr["Kp"], curr["Ki"], 0, ts)
        report["current_loop"] = {
            "continuous": curr,
            "digital": curr_d,
            "bandwidth_hz": bw_current,
        }

    # 2. 速度环
    if J and Kt:
        spd = calculate_speed_loop_pi(J, B, Kt, bw_speed, zeta)
        spd_d = discretize_params(spd["Kp"], spd["Ki"], 0, ts)
        report["speed_loop"] = {
            "continuous": spd,
            "digital": spd_d,
            "bandwidth_hz": bw_speed,
            "zeta": zeta,
        }

    # 3. 位置环
    if o.get("include_position", True) and J and Kt:
        pos = calculate_position_loop_pid(J, Kt, bw_position, zeta,
                                          has_speed_loop=True, B=B)
        pos_d = discretize_params(pos["Kp"], pos["Ki"], pos["Kd"], ts)
        report["position_loop"] = {
            "continuous": pos,
            "digital": pos_d,
            "bandwidth_hz": bw_position,
            # 数字域Kd提示
            "kd_digital_note": KD_DIGITAL_NOTE,
        }

    # 4. 带宽检查
    if "current_loop" in report and "speed_loop" in report:
        pos_bw = bw_position if "position_loop" in report else None
        bw_check = check_bandwidth_ratio(bw_current, bw_speed, pos_bw)
        report["bandwidth_check"] = {
            "current_bw": bw_current,
            "speed_bw": bw_speed,
            "position_bw": pos_bw,
            "valid": len(bw_check.get("warnings", [])) == 0,
            "info": bw_check.get("info", []),
            "warnings": bw_check.get("warnings", []),
        }

    # 5. Q格式定点化
    if "current_loop" in report and vbus and imax:
        q = calculate_q_format(
            report["current_loop"]["continuous"]["Kp"],
            report["current_loop"]["continuous"]["Ki"],
            0, ts, vbus, imax
        )
        report["q_format"] = q

    # 6. 前馈补偿 (交叉耦合始终存在，反电动势取决于psi_f)
    if Rs and Ls:
        ff = calculate_feedforward(Rs, Ls, psi_f, pole_pairs)
        report["feedforward"] = ff

    # 7. 参数校验
    report["validation"] = validate_params(
        Rs, Ls, psi_f, J, Kt, B, pole_pairs, ts, bw_current, pwm_freq
    )

    # 8. 保护阈值
    if o.get("include_protection", True) and rated_current:
        report["protection"] = calculate_protection(rated_current, vbus)

    # 9. 稳定性分析（电流环）
    if o.get("include_stability", False) and "current_loop" in report and Rs and Ls:
        try:
            stab = calculate_stability(
                "current",
                report["current_loop"]["continuous"]["Kp"],
                report["current_loop"]["continuous"]["Ki"],
                0, ts,
                {"Rs": Rs, "Ls": Ls}
            )
            report["stability_current"] = stab
        except Exception:
            pass

    if output_format == "json":
        return json.dumps(report, ensure_ascii=False, indent=2)
    if output_format == "html":
        return _format_html(report)

    return _format_markdown(report)


def _format_markdown(r):
    """格式化为Markdown报告"""
    lines = []
    lines.append(f"# 电机FOC三环PI参数调参报告")
    lines.append("")
    lines.append(f"**电机型号**：{r.get('motor_model', '未指定')}")
    lines.append(f"**目标平台**：{r.get('platform', 'STM32')}")
    lines.append(f"**生成时间**：{r['generated_at']}")
    lines.append("")

    # 电机参数
    sec = [0]
    def _sec(title):
        sec[0] += 1
        return f"## {sec[0]}. {title}"
    lines.append(_sec("电机参数"))
    lines.append("")
    p = r["motor_params"]
    lines.append("| 参数 | 值 | 单位 |")
    lines.append("|------|-----|------|")
    if p.get("Rs") is not None:
        lines.append(f"| 定子电阻 Rs | {p['Rs']} | Ω |")
    if p.get("Ls") is not None:
        lines.append(f"| 定子电感 Ls | {p['Ls']*1000:.2f} | mH |")
    if p.get("J") is not None:
        lines.append(f"| 转动惯量 J | {p['J']:.2e} | kg·m² |")
    if p.get("Kt") is not None:
        lines.append(f"| 转矩常数 Kt | {p['Kt']} | N·m/A |")
    if p.get("psi_f"):
        lines.append(f"| 磁链 ψf | {p['psi_f']} | Wb |")
    if p.get("pole_pairs"):
        lines.append(f"| 极对数 | {p['pole_pairs']} | - |")
    lines.append(f"| 母线电压 Vbus | {p.get('vbus', 24)} | V |")
    lines.append(f"| 最大电流 Imax | {p.get('imax', 10)} | A |")
    lines.append(f"| PWM频率 | {p.get('pwm_freq', 20)} | kHz |")
    lines.append(f"| 采样周期 Ts | {r['tuning_options'].get('ts', 50e-6)*1e6:.0f} | μs |")
    lines.append("")

    # 电流环
    if "current_loop" in r:
        c = r["current_loop"]
        lines.append(_sec("电流环PI参数"))
        lines.append("")
        lines.append(f"**期望带宽**：{c['bandwidth_hz']:.0f} Hz (ωc = {c['bandwidth_hz']*6.283:.0f} rad/s)")
        lines.append("")
        lines.append("| 参数 | 连续域 | 数字域(Ts={:.0f}μs) | 单位 |".format(
            r['tuning_options'].get('ts', 50e-6)*1e6))
        lines.append("|------|--------|---------------------|------|")
        lines.append(f"| Kp | {c['continuous']['Kp']:.4f} | {c['digital']['Kp_digital']:.4f} | V/A |")
        lines.append(f"| Ki | {c['continuous']['Ki']:.2f} | {c['digital']['Ki_digital']:.6f} | V/(A·s) |")
        lines.append("")
        lines.append("**计算公式**：")
        lines.append(f"- Kp = Ls × ωc = {p.get('Ls', 0)*1000:.2f}mH × {c['bandwidth_hz']*6.283:.0f} = {c['continuous']['Kp']:.4f}")
        lines.append(f"- Ki = Rs × ωc = {p.get('Rs', 0)} × {c['bandwidth_hz']*6.283:.0f} = {c['continuous']['Ki']:.2f}")
        lines.append("")

    # 速度环
    if "speed_loop" in r:
        s = r["speed_loop"]
        lines.append(_sec("速度环PI参数"))
        lines.append("")
        lines.append(f"**期望带宽**：{s['bandwidth_hz']:.1f} Hz | **阻尼比**：{s['zeta']}")
        lines.append("")
        lines.append("| 参数 | 连续域 | 数字域 | 单位 |")
        lines.append("|------|--------|--------|------|")
        lines.append(f"| Kp | {s['continuous']['Kp']:.4f} | {s['digital']['Kp_digital']:.4f} | A/(rad/s) |")
        lines.append(f"| Ki | {s['continuous']['Ki']:.2f} | {s['digital']['Ki_digital']:.6f} | A/rad |")
        lines.append("")

    # 位置环
    if "position_loop" in r:
        pos = r["position_loop"]
        lines.append(_sec("位置环PD参数"))
        lines.append("")
        lines.append(f"**期望带宽**：{pos['bandwidth_hz']:.1f} Hz")
        lines.append("")
        lines.append("| 参数 | 连续域 | 数字域 | 单位 |")
        lines.append("|------|--------|--------|------|")
        lines.append(f"| Kp | {pos['continuous']['Kp']:.4f} | {pos['digital']['Kp_digital']:.4f} | 1/s² (级联) |")
        lines.append(f"| Kd | {pos['continuous']['Kd']:.4f} | {pos['digital']['Kd_digital']:.4f} | 1/s (级联) |")
        lines.append("")
        # 数字域Kd提示（定点化/Q格式实现场景）
        lines.append(f"> 💡 {KD_DIGITAL_NOTE}")
        lines.append("")

    # 带宽比
    if "bandwidth_check" in r:
        bc = r["bandwidth_check"]
        lines.append(_sec("带宽比检查"))
        lines.append("")
        lines.append(f"- 电流环：{bc.get('current_bw', 0):.0f} Hz")
        lines.append(f"- 速度环：{bc.get('speed_bw', 0):.1f} Hz (电流环的 1/{bc.get('current_bw',1)/max(bc.get('speed_bw',1),0.01):.0f})")
        if bc.get("position_bw"):
            lines.append(f"- 位置环：{bc['position_bw']:.1f} Hz (速度环的 1/{bc.get('speed_bw',1)/max(bc['position_bw'],0.01):.0f})")
        if bc.get("valid"):
            lines.append("- 检查结果：✅ 带宽比合理（5-10倍级联）")
        else:
            for w in bc.get("warnings", []):
                lines.append(f"- ⚠️ {w}")
        lines.append("")

    # Q格式
    if "q_format" in r:
        q = r["q_format"]
        qf = q.get("q_format", {})
        ver = q.get("verification", {})
        lines.append(_sec("Q格式定点化（对标MCSDK）"))
        lines.append("")
        lines.append(f"**Vbus**：{p.get('vbus', 24)}V | **Imax**：{p.get('imax', 10)}A")
        lines.append("")
        lines.append("```c")
        lines.append(q.get("c_macros", ""))
        lines.append("```")
        lines.append("")
        lines.append(f"- Kp量化误差：{ver.get('Kp_quantization_error_pct', 0):.4f}%")
        lines.append(f"- Ki量化误差：{ver.get('Ki_quantization_error_pct', 0):.4f}%")
        lines.append("")

    # 前馈
    if "feedforward" in r:
        ff = r["feedforward"]
        cc = ff.get("cross_coupling", {})
        bemf = ff.get("back_emf", {})
        lines.append(_sec("前馈补偿系数"))
        lines.append("")
        lines.append("| 补偿项 | 系数 | 公式 |")
        lines.append("|--------|------|------|")
        if cc.get("K_cross_d") is not None:
            lines.append(f"| d轴交叉耦合 | {cc['K_cross_d']:.6f} | {cc.get('Vd_ff_formula', '-ωe·Ls·Iq')} |")
        if cc.get("K_cross_q") is not None:
            lines.append(f"| q轴交叉耦合 | {cc['K_cross_q']:.6f} | {cc.get('Vq_ff_formula', '+ωe·Ls·Id')} |")
        if bemf.get("K_emf") is not None:
            lines.append(f"| 反电动势 | {bemf['K_emf']:.6f} | {bemf.get('Vq_emf_formula', 'ωe·ψf')} |")
        lines.append("")

    # 校验
    if "validation" in r:
        v = r["validation"]
        lines.append(_sec("参数合理性校验"))
        lines.append("")
        if v.get("warnings"):
            for w in v["warnings"]:
                lines.append(f"- ⚠️ {w}")
        if v.get("errors"):
            for e in v["errors"]:
                lines.append(f"- 🔴 {e}")
        if not v.get("warnings") and not v.get("errors"):
            lines.append("✅ 所有参数通过合理性校验")
        lines.append("")

    # 保护
    if "protection" in r:
        pr = r["protection"]
        lines.append(_sec("故障保护阈值建议"))
        lines.append("")
        oc = pr.get("overcurrent", {})
        ov = pr.get("overvoltage", {})
        ot = pr.get("overtemperature", {})
        stall = pr.get("stall_detection", {})
        lines.append("| 保护类型 | 阈值 | 说明 |")
        lines.append("|---------|------|------|")
        if oc.get("hardware_trip_A"):
            lines.append(f"| 硬件过流 | {oc['hardware_trip_A']:.1f} A | 比较器立即关断 |")
        if oc.get("trip_A"):
            lines.append(f"| 软件过流 | {oc['trip_A']:.1f} A | ISR中逐周期检测 |")
        if oc.get("warning_A"):
            lines.append(f"| 过流预警 | {oc['warning_A']:.1f} A | 降额运行 |")
        if ov.get("ov_trip_V"):
            lines.append(f"| 过压保护 | {ov['ov_trip_V']:.1f} V | 母线电压上限 |")
        if ov.get("uv_trip_V"):
            lines.append(f"| 欠压保护 | {ov['uv_trip_V']:.1f} V | 母线电压下限 |")
        if ot.get("trip_temp_C"):
            lines.append(f"| 过温保护 | {ot['trip_temp_C']}°C | {ot.get('device', 'MOSFET')}结温 |")
        if stall.get("current_threshold_A"):
            lines.append(f"| 堵转检测 | {stall['current_threshold_A']:.1f}A × {stall.get('duration_ms', 200)}ms | 速度<{stall.get('speed_threshold_rpm', 30)}rpm且电流超限 |")
        lines.append("")

    # 调参建议
    lines.append(_sec("调参建议"))
    lines.append("")
    lines.append("1. **从理论值的70%开始**：温升导致Rs增大30-50%，实际Kp可略低于理论值")
    lines.append("2. **先调电流环**：给d轴阶跃，观察电流响应无超调后再调速度环")
    lines.append("3. **速度环调参**：加载/卸载测试，Kp太大会震荡，Ki太小有稳态误差")
    lines.append("4. **位置环最后**：确保速度环稳定后再闭合位置环")
    lines.append("5. **加入抗积分饱和**：输出限幅时必须启用clamping或back-calculation")
    lines.append("6. **温升补偿**：如果电机发热严重，用tempcomp模式检查Rs漂移影响")
    lines.append("")
    lines.append("---")
    lines.append("*本报告由电机PID调参器自动生成，参数为理论计算值，实际调试需结合电机响应微调。*")

    return "\n".join(lines)


# ======================================================================
# HTML 报告（单文件、内联样式、内嵌 SVG 阶跃响应，无外部依赖）
# ======================================================================

def _sim_current_step(Kp, Ki, Rs, Ls, n_points=300):
    """电流环 PI 闭环阶跃响应（前向欧拉）。

    被控对象 1/(Ls·s + Rs)，控制器 Kp + Ki/s，单位阶跃。
    返回 (t_list, y_list)，t 单位 ms。
    """
    if not (Kp and Ki and Rs and Ls) or Ls <= 0:
        return None, None
    tc = Ls / max(Rs, 1e-9)            # 电气时间常数
    dt = tc / 60.0
    n = n_points
    t_ms, y, xi = [], [], []
    yi = 0.0
    integ = 0.0
    for i in range(n):
        t_ms.append(i * dt * 1000.0)
        y.append(yi)
        e = 1.0 - yi
        integ += Ki * e * dt
        u = Kp * e + integ
        yi += ((u - Rs * yi) / Ls) * dt
    return t_ms, y


def _sim_speed_step(Kp, Ki, J, B, Kt, imax, zeta, n_points=300):
    """速度环 PI 阶跃响应（内环理想化，输出限幅 imax）。

    返回 (t_list, y_list)，t 单位 ms，y 归一化到 1.0 = 参考转速。
    """
    if not (Kp and Ki and J and Kt) or J <= 0:
        return None, None
    # 用二阶标准型时间尺度估算仿真窗口（阻尼振荡周期）
    wn = (Kt * Kp / J) ** 0.5 if Kt * Kp > 0 else 10.0
    dt = min(0.4 / (wn * 50.0), 1e-4)
    n = n_points
    t_ms, y = [], []
    omega = 0.0
    integ = 0.0
    for i in range(n):
        t_ms.append(i * dt * 1000.0)
        y.append(omega)
        e = 1.0 - omega                    # 归一化参考
        iq_cmd = Kp * e + integ
        iq = max(-imax, min(imax, iq_cmd))  # 电流限幅
        integ += Ki * e * dt
        omega += ((Kt * iq - B * omega) / J) * dt
    return t_ms, y


def _svg_curve(t, y, width=460, height=180, color="#0969da", label=""):
    """把阶跃响应画成内嵌 SVG 折线（0/100% 参考线 + 响应曲线）。"""
    if not t or not y:
        return ""
    t_max = max(t[-1], 1e-9)
    y_all = y + [1.0]
    y_max = max(max(y), 1.0) * 1.15
    y_min = min(min(y), 0.0)
    if y_max - y_min < 1e-9:
        y_max = y_min + 1.0
    pad_l, pad_r, pad_t, pad_b = 34, 8, 10, 20

    def X(tv):
        return pad_l + (tv / t_max) * (width - pad_l - pad_r)

    def Y(v):
        return pad_t + (y_max - v) / (y_max - y_min) * (height - pad_t - pad_b)

    pts = " ".join("%.1f,%.1f" % (X(tv), Y(vv)) for tv, vv in zip(t, y))
    overshoot = (max(y) - 1.0) * 100.0 if y else 0.0
    parts = [
        '<svg viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="%s">' % (width, height, label),
        '<rect width="%d" height="%d" fill="#f6f8fa" rx="6"/>' % (width, height),
        # 0% / 100% 参考线
        '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#d0d7de" stroke-dasharray="4 3" stroke-width="1"/>' % (pad_l, Y(0.0), width - pad_r, Y(0.0)),
        '<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#d0d7de" stroke-dasharray="4 3" stroke-width="1"/>' % (pad_l, Y(1.0), width - pad_r, Y(1.0)),
        '<text x="%d" y="%.1f" font-size="10" fill="#656d76">100%%</text>' % (2, Y(1.0) - 2),
        '<text x="%d" y="%.1f" font-size="10" fill="#656d76">0</text>' % (2, Y(0.0) - 2),
        '<polyline points="%s" fill="none" stroke="%s" stroke-width="2"/>' % (pts, color),
        '<text x="%d" y="%d" font-size="11" fill="#1f2328">%s</text>' % (pad_l, height - 6, label),
        '<text x="%d" y="%d" font-size="10" fill="#656d76" text-anchor="end">t=%.0fms</text>' % (width - pad_r, height - 6, t_max),
    ]
    if overshoot > 0.5:
        parts.append('<text x="%d" y="%d" font-size="10" fill="#d93026">超调 %.1f%%</text>'
                     % (width - pad_r, pad_t + 10, overshoot))
    parts.append("</svg>")
    return "".join(parts)


def _format_html(r):
    """格式化为单文件 HTML 报告（内嵌阶跃响应 SVG，可直接分享/存档）。"""
    import html as _html

    def esc(s):
        return _html.escape(str(s), quote=True)

    p = r["motor_params"]
    o = r["tuning_options"]

    # --- SVG 曲线（有参数才画） ---
    cur_svg = ""
    if "current_loop" in r:
        c = r["current_loop"]
        t, y = _sim_current_step(c["continuous"]["Kp"], c["continuous"]["Ki"],
                                 p.get("Rs"), p.get("Ls"))
        cur_svg = _svg_curve(t, y, label="电流环阶跃响应（仿真）")

    spd_svg = ""
    if "speed_loop" in r:
        s = r["speed_loop"]
        t, y = _sim_speed_step(s["continuous"]["Kp"], s["continuous"]["Ki"],
                               p.get("J"), p.get("B", 0), p.get("Kt"),
                               p.get("imax", 10), s.get("zeta", 0.707))
        spd_svg = _svg_curve(t, y, color="#8250df", label="速度环阶跃响应（仿真，输出限幅）")

    # --- 参数卡 ---
    cards = []
    if "current_loop" in r:
        c = r["current_loop"]
        cards.append(("电流环 PI", c["bandwidth_hz"],
                      [("Kp", c["digital"]["Kp_digital"], "V/A"),
                       ("Ki", c["digital"]["Ki_digital"], "V/(A·s)")]))
    if "speed_loop" in r:
        s = r["speed_loop"]
        cards.append(("速度环 PI", s["bandwidth_hz"],
                      [("Kp", s["digital"]["Kp_digital"], "A/(rad/s)"),
                       ("Ki", s["digital"]["Ki_digital"], "A/rad")]))
    if "position_loop" in r:
        pos = r["position_loop"]
        cards.append(("位置环 PD", pos["bandwidth_hz"],
                      [("Kp", pos["digital"]["Kp_digital"], "1/s²"),
                       ("Kd", pos["digital"]["Kd_digital"], "1/s")]))
    cards_html = "".join(
        '<div class="card"><div class="ttl">%s <span class="bw">BW %s Hz</span></div>'
        '<div class="kv">%s</div></div>' % (
            esc(name), esc("%.0f" % bw),
            "".join('<div class="row"><span>%s</span><b>%.4f</b><i>%s</i></div>' % (k, v, esc(u))
                    for k, v, u in kvs))
        for name, bw, kvs in cards)

    # --- 带宽比 / 校验 ---
    check_rows = []
    if "bandwidth_check" in r:
        bc = r["bandwidth_check"]
        if bc.get("valid"):
            check_rows.append('<div class="okline">✅ 带宽比合理（5-10 倍级联）</div>')
        else:
            for w in bc.get("warnings", []):
                check_rows.append('<div class="warnline">⚠️ %s</div>' % esc(w))
    if "validation" in r:
        v = r["validation"]
        for w in v.get("warnings", []):
            check_rows.append('<div class="warnline">⚠️ %s</div>' % esc(w))
        for e in v.get("errors", []):
            check_rows.append('<div class="errline">🔴 %s</div>' % esc(e))
        if not v.get("warnings") and not v.get("errors"):
            check_rows.append('<div class="okline">✅ 所有参数通过合理性校验</div>')
    checks_html = "".join(check_rows) if check_rows else ""

    # --- 保护阈值表 ---
    prot_rows = []
    if "protection" in r:
        pr = r["protection"]
        oc = pr.get("overcurrent", {})
        ov = pr.get("overvoltage", {})
        ot = pr.get("overtemperature", {})
        stall = pr.get("stall_detection", {})
        rows = []
        if oc.get("hardware_trip_A"):
            rows.append(("硬件过流", "%.1f A" % oc["hardware_trip_A"], "比较器立即关断"))
        if oc.get("trip_A"):
            rows.append(("软件过流", "%.1f A" % oc["trip_A"], "ISR 逐周期检测"))
        if oc.get("warning_A"):
            rows.append(("过流预警", "%.1f A" % oc["warning_A"], "降额运行"))
        if ov.get("ov_trip_V"):
            rows.append(("过压保护", "%.1f V" % ov["ov_trip_V"], "母线电压上限"))
        if ov.get("uv_trip_V"):
            rows.append(("欠压保护", "%.1f V" % ov["uv_trip_V"], "母线电压下限"))
        if ot.get("trip_temp_C"):
            rows.append(("过温保护", "%s°C" % ot["trip_temp_C"], ot.get("device", "MOSFET") + "结温"))
        if stall.get("current_threshold_A"):
            rows.append(("堵转检测", "%.1f A × %sms" % (stall["current_threshold_A"], stall.get("duration_ms", 200)),
                         "速度<%srpm" % stall.get("speed_threshold_rpm", 30)))
        prot_rows = "".join(
            "<tr><td>%s</td><td><b>%s</b></td><td>%s</td></tr>" % (esc(a), esc(b), esc(c))
            for a, b, c in rows)

    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>电机FOC调参报告 - {model}</title>
<style>
:root{{--ink:#1f2328;--muted:#656d76;--line:#d8dee4;--bg:#f6f8fa;--blue:#0969da;--purple:#8250df}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Microsoft YaHei","PingFang SC",sans-serif;color:var(--ink);background:#fff;padding:32px 40px;max-width:1000px;margin:0 auto}}
h1{{font-size:22px}} .meta{{color:var(--muted);font-size:13px;margin:6px 0 20px}}
h2{{font-size:16px;margin:26px 0 12px;border-bottom:1px solid var(--line);padding-bottom:6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin-bottom:20px}}
.card{{border:1px solid var(--line);border-radius:8px;padding:14px 16px;background:var(--bg)}}
.card .ttl{{font-weight:700;font-size:14px;margin-bottom:8px}}
.card .bw{{font-weight:400;font-size:12px;color:var(--blue);margin-left:6px}}
.row{{display:flex;align-items:baseline;gap:8px;padding:3px 0;font-size:13px}}
.row span{{color:var(--muted);width:28px}}
.row b{{font-size:16px;font-family:Consolas,monospace}}
.row i{{color:var(--muted);font-style:normal;font-size:11px}}
.curves{{display:grid;grid-template-columns:repeat(auto-fit,minmax(460px,1fr));gap:14px}}
table{{border-collapse:collapse;width:100%%;font-size:13px;margin:8px 0}}
th,td{{border:1px solid var(--line);padding:6px 10px;text-align:left}}
th{{background:var(--bg)}}
.okline{{color:#116329;background:#f0fff4;border-radius:4px;padding:6px 10px;margin:4px 0;font-size:13px}}
.warnline{{color:#9a6700;background:#fff8c5;border-radius:4px;padding:6px 10px;margin:4px 0;font-size:13px}}
.errline{{color:#d93026;background:#fff1f0;border-radius:4px;padding:6px 10px;margin:4px 0;font-size:13px}}
ol{{margin:8px 0 0 20px;font-size:13px;line-height:1.9}}
footer{{margin-top:30px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:12px}}
@media print {{ body{{padding:12px}} }}
</style>
</head>
<body>
<h1>电机 FOC 三环 PI 调参报告</h1>
<div class="meta">电机型号 {model} · 目标平台 {platform} · 生成时间 {ts}</div>
<div class="grid">{cards}</div>
{curves}
<h2>带宽比与参数校验</h2>
{checks}
{prot}
<h2>调参建议</h2>
<ol>
<li><b>从理论值的 70% 开始</b>：温升导致 Rs 增大 30-50%，实际 Kp 可略低于理论值</li>
<li><b>先调电流环</b>：给 d 轴阶跃，观察电流响应无超调后再调速度环</li>
<li><b>速度环调参</b>：加载/卸载测试，Kp 太大会震荡，Ki 太小有稳态误差</li>
<li><b>位置环最后</b>：确保速度环稳定后再闭合位置环</li>
<li><b>加入抗积分饱和</b>：输出限幅时必须启用 clamping 或 back-calculation</li>
<li><b>温升补偿</b>：电机发热严重时用 tempcomp 模式检查 Rs 漂移影响</li>
</ol>
<footer>本报告由 motor-pid-tuner 1.0.0 自动生成 · 阶跃响应为线性模型仿真，实际调试需结合电机响应微调 · 单文件 HTML，可直接分享/存档</footer>
</body>
</html>""".format(
        model=esc(r.get("motor_model", "未指定")),
        platform=esc(r.get("platform", "STM32")),
        ts=esc(r.get("generated_at", "")),
        cards=cards_html,
        curves='<div class="curves">%s</div>' % (cur_svg + spd_svg) if (cur_svg or spd_svg) else "",
        checks=checks_html if checks_html else '<div class="okline">无校验数据（参数不全）</div>',
        prot=('<h2>故障保护阈值建议</h2><table><tr><th>保护类型</th><th>阈值</th><th>说明</th></tr>%s</table>' % prot_rows) if prot_rows else "",
    )


def main():
    parser = argparse.ArgumentParser(description="电机PID调参报告生成器")
    parser.add_argument("--rs", type=float, required=True, help="定子电阻Ω")
    parser.add_argument("--ls", type=float, required=True, help="定子电感mH")
    parser.add_argument("--j", type=float, required=True, help="转动惯量kg·m²")
    parser.add_argument("--kt", type=float, required=True, help="转矩常数N·m/A")
    parser.add_argument("--b", type=float, default=0, help="摩擦系数")
    parser.add_argument("--psi-f", type=float, default=0, help="磁链Wb")
    parser.add_argument("--pole-pairs", type=int, default=1, help="极对数")
    parser.add_argument("--vbus", type=float, default=24, help="母线电压V")
    parser.add_argument("--imax", type=float, default=10, help="最大电流A")
    parser.add_argument("--pwm-freq", type=float, default=20, help="PWM频率kHz")
    parser.add_argument("--rated-current", type=float, help="额定电流A")
    parser.add_argument("--bw-current", type=float, help="电流环带宽Hz")
    parser.add_argument("--zeta", type=float, default=0.707, help="阻尼比")
    parser.add_argument("--ts", type=float, default=50e-6, help="采样周期s")
    parser.add_argument("--motor-model", default="未指定", help="电机型号")
    parser.add_argument("--platform", default="STM32", help="目标平台")
    parser.add_argument("--no-position", action="store_true", help="不包含位置环")
    parser.add_argument("--no-protection", action="store_true", help="不包含保护阈值")
    parser.add_argument("--with-stability", action="store_true", help="包含稳定性分析")
    parser.add_argument("--format", choices=["markdown", "html", "json"], default="markdown",
                       help="输出格式（html=单文件可视化报告，内嵌阶跃响应曲线）")
    parser.add_argument("--output", "-o", help="输出文件路径（html 格式建议 .html 后缀）")

    args = parser.parse_args()

    motor_params = {
        "Rs": args.rs,
        "Ls": args.ls / 1000,  # mH → H
        "J": args.j,
        "B": args.b,
        "Kt": args.kt,
        "psi_f": args.psi_f,
        "pole_pairs": args.pole_pairs,
        "vbus": args.vbus,
        "imax": args.imax,
        "pwm_freq": args.pwm_freq,
        "rated_current": args.rated_current or args.imax,
        "motor_model": args.motor_model,
    }

    tuning_options = {
        "bw_current": args.bw_current,
        "zeta": args.zeta,
        "ts": args.ts,
        "include_position": not args.no_position,
        "include_protection": not args.no_protection,
        "include_stability": args.with_stability,
        "platform": args.platform,
    }

    result = generate_report(motor_params, tuning_options, args.format)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"报告已保存到: {args.output}", file=sys.stderr)
    else:
        print(result)


def _safe_main():
    """包装main()，将参数校验/计算异常转为错误输出，避免traceback崩溃"""
    try:
        main()
    except (ValueError, ZeroDivisionError, ArithmeticError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
    except TypeError as e:
        print(f"参数类型错误或缺少必需数值参数: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    _safe_main()
