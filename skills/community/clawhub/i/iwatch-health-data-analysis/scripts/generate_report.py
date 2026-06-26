#!/usr/bin/env python3
"""
Apple Health 报告生成器 v2.0
基于用户画像动态校准参考范围，生成个性化 HTML 报告。

用法:
    python3 generate_report.py chart_data.json output.html [options]

Options:
    --gender     male / female / other  (default: other)
    --age        整数年龄               (default: 30)
    --height     身高cm                 (default: 170)
    --weight-unit lb / kg              (default: lb)
    --conditions 病史，逗号分隔         (default: "")
    --activity   sedentary/light/active/athlete (default: light)
    --verdict    一句话结论（可选）
"""

import json
import sys
import argparse
import statistics
from pathlib import Path
from collections import defaultdict


# ═══════════════════════════════════════════════════════════════
# 动态参考范围引擎
# ═══════════════════════════════════════════════════════════════

def build_reference(gender: str, age: int, height_cm: float,
                    activity_level: str, conditions: list) -> dict:
    """
    根据性别/年龄/身高/活动水平，返回个性化参考区间。
    所有范围均基于 ACSM / AHA / WHO 指南。
    """
    g = gender.lower()
    is_female = g in ('female', 'f', '女')
    is_male   = g in ('male', 'm', '男')

    # ── 静息心率 RHR ──────────────────────────────────────────
    if is_female:
        if age <= 25:   rhr_bands = (54, 60, 73, 82)
        elif age <= 35: rhr_bands = (55, 61, 74, 83)
        elif age <= 45: rhr_bands = (56, 62, 75, 84)
        elif age <= 55: rhr_bands = (57, 63, 76, 85)
        else:           rhr_bands = (58, 64, 77, 86)
    elif is_male:
        if age <= 25:   rhr_bands = (49, 55, 68, 77)
        elif age <= 35: rhr_bands = (50, 56, 69, 78)
        elif age <= 45: rhr_bands = (51, 57, 70, 79)
        elif age <= 55: rhr_bands = (52, 58, 71, 80)
        else:           rhr_bands = (53, 59, 72, 81)
    else:               rhr_bands = (52, 58, 71, 80)
    # (优秀上限, 良好上限, 正常上限, 偏高上限)

    # ── VO₂Max 分级 ───────────────────────────────────────────
    if is_female:
        if age <= 29:   vo2_bands = (29, 34, 43, 48)
        elif age <= 39: vo2_bands = (28, 33, 41, 46)
        elif age <= 49: vo2_bands = (24, 30, 37, 41)
        else:           vo2_bands = (20, 24, 30, 35)
    elif is_male:
        if age <= 29:   vo2_bands = (38, 43, 51, 56)
        elif age <= 39: vo2_bands = (35, 41, 49, 53)
        elif age <= 49: vo2_bands = (32, 37, 45, 49)
        else:           vo2_bands = (28, 33, 41, 45)
    else:               vo2_bands = (30, 36, 45, 50)
    vo2_good = vo2_bands[1]   # 良好下限

    # ── HRV SDNN（Apple Watch 连续监测）─────────────────────
    # 迷走神经性晕厥病史 → 不追求过高
    has_vasovagal = any('vaso' in c.lower() or 'syncope' in c.lower() or '晕厥' in c for c in conditions)
    if age <= 30:   hrv_low, hrv_mid, hrv_high = 25, 40, 55
    elif age <= 40: hrv_low, hrv_mid, hrv_high = 20, 35, 50
    elif age <= 50: hrv_low, hrv_mid, hrv_high = 15, 30, 45
    else:           hrv_low, hrv_mid, hrv_high = 12, 25, 40
    if has_vasovagal:
        hrv_high = min(hrv_high, hrv_mid + 8)  # 上限收窄

    # ── BMI 区间（基于身高）──────────────────────────────────
    h = height_cm / 100
    bmi_low   = round(18.5 * h * h, 1)  # 偏瘦下限对应体重 kg
    bmi_norm  = round(24.9 * h * h, 1)  # 正常上限对应体重 kg

    # ── 体脂率 ────────────────────────────────────────────────
    if is_female:
        if age <= 30:   bf_low, bf_high = 21, 32
        elif age <= 40: bf_low, bf_high = 23, 34
        else:           bf_low, bf_high = 24, 36
    elif is_male:
        if age <= 30:   bf_low, bf_high = 8, 20
        elif age <= 40: bf_low, bf_high = 11, 22
        else:           bf_low, bf_high = 13, 25
    else:               bf_low, bf_high = 15, 28

    # ── 步数目标 ──────────────────────────────────────────────
    steps_targets = {
        'sedentary': 6000,
        'light':     8000,
        'active':    10000,
        'athlete':   12000,
    }
    steps_target = steps_targets.get(activity_level, 8000)

    # ── 病史调整标注 ──────────────────────────────────────────
    condition_notes = []
    cond_lower = [c.lower() for c in conditions]
    if any('thyroid' in c or 'hyperthyroid' in c or '甲亢' in c or '甲减' in c for c in cond_lower):
        condition_notes.append("甲状腺病史：RHR/HRV/VO₂Max异常优先排查甲状腺因素")
    if any('hypertension' in c or '高血压' in c for c in cond_lower):
        condition_notes.append("高血压：RHR目标更严格（<70），关注血压数据")
    if any('arrhythmia' in c or '早搏' in c or '心律' in c for c in cond_lower):
        condition_notes.append("心律失常：HRV数据可能失真；RHR偏高有代偿解释")
    if any('low blood pressure' in c or '低血压' in c for c in cond_lower):
        condition_notes.append("低血压：RHR轻度代偿（75-85bpm）为正常生理反应")
    if has_vasovagal:
        condition_notes.append("迷走性晕厥：HRV不追求过高；避免过强迷走张力")
    if any('anemia' in c or '贫血' in c for c in cond_lower):
        condition_notes.append("贫血：RHR偏高/VO₂Max偏低时先排除贫血因素")

    return {
        'rhr_bands':        rhr_bands,      # (优秀上限, 良好上限, 正常上限, 偏高上限)
        'vo2_bands':        vo2_bands,      # (差上限, 一般上限, 良好上限, 优秀上限)
        'vo2_good':         vo2_good,
        'hrv_low':          hrv_low,
        'hrv_mid':          hrv_mid,
        'hrv_high':         hrv_high,
        'bmi_weight_low':   bmi_low,
        'bmi_weight_high':  bmi_norm,
        'bf_low':           bf_low,
        'bf_high':          bf_high,
        'steps_target':     steps_target,
        'condition_notes':  condition_notes,
        'has_vasovagal':    has_vasovagal,
    }


def classify_rhr(rhr: float, bands: tuple) -> tuple:
    """返回 (等级文字, CSS颜色类)"""
    if rhr is None:
        return '--', 'neutral'
    e, g, n, h = bands
    if rhr <= e:   return '优秀', 'excellent'
    if rhr <= g:   return '良好', 'good'
    if rhr <= n:   return '正常', 'normal'
    if rhr <= h:   return '偏高', 'warn'
    return '过高', 'danger'


def classify_vo2(vo2: float, bands: tuple) -> tuple:
    if vo2 is None:
        return '--', 'neutral'
    d, avg, g, e = bands
    if vo2 <= d:   return '差', 'danger'
    if vo2 <= avg: return '一般', 'warn'
    if vo2 <= g:   return '良好', 'good'
    if vo2 <= e:   return '优秀', 'excellent'
    return '精英', 'excellent'


def weight_to_kg(raw_val, unit: str) -> float:
    """原始体重值转换为 kg"""
    if raw_val is None:
        return None
    return round(raw_val * 0.4536, 1) if unit == 'lb' else round(raw_val, 1)


def compute_bmi(weight_kg: float, height_cm: float) -> float:
    if not weight_kg or not height_cm:
        return None
    return round(weight_kg / (height_cm / 100) ** 2, 1)


# ═══════════════════════════════════════════════════════════════
# 统计工具
# ═══════════════════════════════════════════════════════════════

def pearson_r(xs, ys) -> float:
    paired = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(paired) < 3:
        return None
    xs2, ys2 = zip(*paired)
    n = len(xs2)
    mx, my = sum(xs2)/n, sum(ys2)/n
    num = sum((x-mx)*(y-my) for x, y in zip(xs2, ys2))
    den = (sum((x-mx)**2 for x in xs2) * sum((y-my)**2 for y in ys2)) ** 0.5
    return round(num/den, 2) if den else None


def month_label(m: str) -> str:
    return m[2:].replace('-', '.')


# ═══════════════════════════════════════════════════════════════
# 分析核心
# ═══════════════════════════════════════════════════════════════

def analyze(data: dict, ref: dict, profile: dict) -> dict:
    """返回分析摘要，用于渲染报告"""
    months = sorted(data.keys())
    if not months:
        return {}

    weight_unit = profile.get('weight_unit', 'lb')
    height_cm   = profile.get('height_cm', 170)

    last = data[months[-1]]
    last_rhr  = last.get('rhr')
    last_hrv  = last.get('hrv')
    last_vo2  = last.get('vo2')
    last_steps = last.get('steps')
    last_spo2 = last.get('spo2')
    last_wt_kg = weight_to_kg(last.get('weight_raw'), weight_unit)

    all_rhr = [data[m].get('rhr') for m in months if data[m].get('rhr')]
    all_hrv = [data[m].get('hrv') for m in months if data[m].get('hrv')]
    all_vo2 = [data[m].get('vo2') for m in months if data[m].get('vo2')]

    rhr_lbl, rhr_cls = classify_rhr(last_rhr, ref['rhr_bands'])
    vo2_lbl, vo2_cls = classify_vo2(last_vo2, ref['vo2_bands'])

    max_rhr = max(all_rhr) if all_rhr else None
    min_hrv = min(all_hrv) if all_hrv else None

    corr = pearson_r(
        [data[m].get('rhr') for m in months],
        [data[m].get('hrv') for m in months]
    )

    bmi = compute_bmi(last_wt_kg, height_cm)
    bf_pct = round(last.get('body_fat_pct', 0) * 100, 1) if last.get('body_fat_pct') else None

    return {
        'last_month':  months[-1],
        'first_month': months[0],
        'num_months':  len(months),
        'last_rhr':    last_rhr,
        'last_hrv':    last_hrv,
        'last_vo2':    last_vo2,
        'last_steps':  last_steps,
        'last_spo2':   last_spo2,
        'last_wt_kg':  last_wt_kg,
        'max_rhr':     max_rhr,
        'min_hrv':     min_hrv,
        'rhr_lbl':     rhr_lbl,
        'rhr_cls':     rhr_cls,
        'vo2_lbl':     vo2_lbl,
        'vo2_cls':     vo2_cls,
        'corr':        corr,
        'bmi':         bmi,
        'bf_pct':      bf_pct,
        'steps_ok':    (last_steps or 0) >= ref['steps_target'],
    }


# ═══════════════════════════════════════════════════════════════
# HTML 模板渲染
# ═══════════════════════════════════════════════════════════════

def render_html(chart_data_full: dict, profile: dict, ref: dict,
                analysis: dict, verdict: str) -> str:
    """将所有数据渲染为完整 HTML 字符串"""

    data = chart_data_full.get('data', chart_data_full)
    months = sorted(data.keys())
    labels_js = json.dumps([month_label(m) for m in months])

    def series(key):
        return json.dumps([data[m].get(key) for m in months])

    def weight_series():
        unit = profile.get('weight_unit', 'lb')
        h = profile.get('height_cm', 170)
        vals = []
        for m in months:
            raw = data[m].get('weight_raw')
            vals.append(weight_to_kg(raw, unit))
        return json.dumps(vals)

    # 睡眠新格式
    sleep_new_months = [m for m in months if data[m].get('sleep_deep', 0) + data[m].get('sleep_rem', 0) > 0]
    sleep_labels = json.dumps([month_label(m) for m in sleep_new_months])
    def sleep_pct(key):
        result = []
        for m in sleep_new_months:
            d = data[m]
            total = d.get('sleep_deep',0)+d.get('sleep_rem',0)+d.get('sleep_core',0)+d.get('sleep_awake',0)
            result.append(round(d.get(key,0)/total*100) if total else 0)
        return json.dumps(result)

    # SpO2
    spo2_months = [m for m in months if data[m].get('spo2') is not None]
    spo2_labels = json.dumps([month_label(m) for m in spo2_months])
    spo2_vals   = json.dumps([data[m]['spo2'] for m in spo2_months])

    # 散点（RHR × HRV）
    scatter_pts = [{'x': data[m].get('rhr'), 'y': data[m].get('hrv'), 'm': m}
                   for m in months if data[m].get('rhr') and data[m].get('hrv')]
    scatter_js = json.dumps(scatter_pts)

    # 事件检测：自动找 RHR 最高月份
    rhr_vals = [(m, data[m]['rhr']) for m in months if data[m].get('rhr')]
    peak_month = max(rhr_vals, key=lambda x: x[1])[0] if rhr_vals else None
    # 恢复点：peak 之后 RHR 首次回到正常
    normal_thresh = ref['rhr_bands'][2]  # 正常上限
    recover_month = None
    if peak_month:
        post_peak = [(m, data[m]['rhr']) for m in months if m > peak_month and data[m].get('rhr')]
        for m, v in post_peak:
            if v <= normal_thresh:
                recover_month = m
                break

    # 用户信息字符串
    gender_map = {'male': '男', 'female': '女', 'm': '男', 'f': '女', '男': '男', '女': '女'}
    gender_display = gender_map.get(profile.get('gender', '').lower(), profile.get('gender', '--'))
    age_display = profile.get('age', '--')
    height_display = profile.get('height_cm', '--')
    weight_unit_display = 'lb' if profile.get('weight_unit') == 'lb' else 'kg'
    last_wt = analysis.get('last_wt_kg')
    last_wt_str = f"{last_wt}kg" if last_wt else '--'

    conditions_list = profile.get('conditions', [])
    conditions_display = '、'.join(conditions_list) if conditions_list else '无已知病史'

    activity_map = {'sedentary': '久坐', 'light': '轻度活动', 'active': '规律运动', 'athlete': '专业训练'}
    activity_display = activity_map.get(profile.get('activity_level', 'light'), '--')

    ref_notes = '\n'.join(f'<li>{n}</li>' for n in ref.get('condition_notes', []))

    # VO₂Max 参考线
    vo2_good = ref['vo2_good']

    # 步数目标
    steps_target = ref['steps_target']

    bmi_str = str(analysis.get('bmi', '--'))
    corr_str = str(analysis.get('corr', '--'))
    last_rhr_str = str(analysis.get('last_rhr', '--'))
    last_hrv_str = str(analysis.get('last_hrv', '--'))
    last_vo2_str = str(analysis.get('last_vo2', '--'))
    last_spo2_str = f"{analysis.get('last_spo2', '--')}%" if analysis.get('last_spo2') else '--'
    last_steps_str = f"{int(analysis['last_steps']/1000)}k" if analysis.get('last_steps') else '--'
    max_rhr_str = str(analysis.get('max_rhr', '--'))

    steps_badge = '✓ 达标' if analysis.get('steps_ok') else '⚠ 偏低'
    steps_color = '#3fb950' if analysis.get('steps_ok') else '#d29922'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Apple Health 健康分析报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Helvetica Neue',sans-serif;background:#0d1117;color:#e6edf3;min-height:100vh}}
.hero{{background:linear-gradient(135deg,#0d1117,#161b22,#1c2128);padding:52px 44px 44px;border-bottom:1px solid #30363d;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;top:-20%;right:-5%;width:500px;height:500px;background:radial-gradient(circle,rgba(88,166,255,.07),transparent 70%);border-radius:50%;pointer-events:none}}
.tag{{display:inline-block;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#58a6ff;background:rgba(88,166,255,.1);border:1px solid rgba(88,166,255,.25);padding:3px 11px;border-radius:20px;margin-bottom:14px}}
h1{{font-size:clamp(24px,3.5vw,40px);font-weight:800;line-height:1.15;margin-bottom:8px;letter-spacing:-.5px}}
h1 .ac{{background:linear-gradient(90deg,#58a6ff,#79c0ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.sub{{font-size:13px;color:#8b949e;margin-bottom:22px}}
.verdict{{display:inline-flex;align-items:center;gap:9px;background:rgba(63,185,80,.1);border:1px solid rgba(63,185,80,.3);padding:11px 18px;border-radius:10px;font-size:13px}}
.vdot{{width:7px;height:7px;background:#3fb950;border-radius:50%;box-shadow:0 0 7px #3fb950;animation:p 2s infinite;flex-shrink:0}}
@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}

/* 用户画像栏 */
.profile-bar{{background:#161b22;border-bottom:1px solid #30363d;padding:14px 44px;display:flex;flex-wrap:wrap;gap:24px;align-items:center}}
.pf-item{{display:flex;align-items:center;gap:6px;font-size:12px}}
.pf-label{{color:#8b949e}}
.pf-val{{color:#e6edf3;font-weight:600}}
.pf-note{{font-size:11px;color:#d29922;background:rgba(210,153,34,.1);border:1px solid rgba(210,153,34,.25);padding:2px 8px;border-radius:6px}}

/* 参考范围调整提示 */
.ref-notes{{background:#161b22;border:1px solid #30363d;border-left:3px solid #58a6ff;border-radius:8px;padding:10px 16px;margin:16px 44px;font-size:12px;color:#8b949e}}
.ref-notes ul{{margin-left:14px;}}
.ref-notes li{{margin:2px 0;}}

/* KPI */
.kpi-strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:#21262d;border-top:1px solid #30363d;border-bottom:1px solid #30363d}}
.kpi{{background:#161b22;padding:18px 14px;text-align:center}}
.kpi-icon{{font-size:18px;margin-bottom:5px}}
.kpi-val{{font-size:24px;font-weight:800;line-height:1;margin-bottom:3px}}
.kpi-lbl{{font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.4px}}
.kpi-delta{{font-size:10px;margin-top:4px;font-weight:600}}
.good{{color:#3fb950}}.warn{{color:#d29922}}.bad{{color:#f85149}}.info{{color:#58a6ff}}

/* Layout */
.body{{padding:28px 44px;max-width:1440px;margin:0 auto}}
.charts-2{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-bottom:18px}}
.span2{{grid-column:1/-1}}
.card{{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px}}
.card-hd{{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:16px;gap:10px}}
.card-title{{font-size:13px;font-weight:700;color:#e6edf3;display:flex;align-items:center;gap:6px}}
.cdot{{width:6px;height:6px;border-radius:50%;flex-shrink:0}}
.card-sub{{font-size:11px;color:#8b949e;margin-top:2px}}
.badge{{font-size:10px;font-weight:700;padding:3px 8px;border-radius:16px;white-space:nowrap}}
.bg{{background:rgba(63,185,80,.15);color:#3fb950;border:1px solid rgba(63,185,80,.3)}}
.by{{background:rgba(210,153,34,.15);color:#d29922;border:1px solid rgba(210,153,34,.3)}}
.bb{{background:rgba(88,166,255,.12);color:#58a6ff;border:1px solid rgba(88,166,255,.25)}}
.cw{{height:200px;position:relative}}
.cw-tall{{height:250px;position:relative}}
.cw-sm{{height:165px;position:relative}}
.section-hd{{font-size:12px;font-weight:700;color:#8b949e;text-transform:uppercase;letter-spacing:1px;margin:28px 0 12px;display:flex;align-items:center;gap:8px}}
.section-hd::after{{content:'';flex:1;height:1px;background:#21262d}}

/* 洞察 */
.insights{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-bottom:28px}}
.ins{{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px 16px;display:flex;gap:11px}}
.ins-icon{{font-size:18px;flex-shrink:0;margin-top:1px}}
.ins-lv{{font-size:9px;font-weight:800;letter-spacing:1px;text-transform:uppercase;padding:1px 6px;border-radius:6px;display:inline-block;margin-bottom:4px}}
.lv-hi{{background:rgba(248,81,73,.15);color:#f85149}}
.lv-md{{background:rgba(210,153,34,.15);color:#d29922}}
.lv-lo{{background:rgba(63,185,80,.15);color:#3fb950}}
.ins-name{{font-size:12px;font-weight:700;margin-bottom:3px;color:#e6edf3}}
.ins-desc{{font-size:11px;color:#8b949e;line-height:1.55}}

@media(max-width:800px){{.body,.hero,.profile-bar,.ref-notes{{padding-left:18px;padding-right:18px}}.charts-2{{grid-template-columns:1fr}}}}
footer{{border-top:1px solid #21262d;padding:24px 44px;text-align:center;font-size:11px;color:#6e7681;background:#0d1117}}
</style>
</head>
<body>

<div class="hero">
  <div class="tag">Apple Health · 个性化健康报告 v2.0</div>
  <h1>身体数据<br><span class="ac">全景分析报告</span></h1>
  <p class="sub">数据范围：{analysis['first_month']} → {analysis['last_month']} · 共 {analysis['num_months']} 个月</p>
  <div class="verdict"><div class="vdot"></div><span>{verdict}</span></div>
</div>

<!-- 用户画像栏 -->
<div class="profile-bar">
  <div class="pf-item"><span class="pf-label">性别</span><span class="pf-val">{gender_display}</span></div>
  <div class="pf-item"><span class="pf-label">年龄</span><span class="pf-val">{age_display} 岁</span></div>
  <div class="pf-item"><span class="pf-label">身高</span><span class="pf-val">{height_display} cm</span></div>
  <div class="pf-item"><span class="pf-label">当前体重</span><span class="pf-val">{last_wt_str}（BMI {bmi_str}）</span></div>
  <div class="pf-item"><span class="pf-label">活动水平</span><span class="pf-val">{activity_display}</span></div>
  <div class="pf-item"><span class="pf-label">病史</span><span class="pf-val">{conditions_display}</span></div>
  <div class="pf-note">参考范围已按个人信息动态校准</div>
</div>

{f'<div class="ref-notes"><strong style="color:#58a6ff">📌 病史影响说明：</strong><ul>{ref_notes}</ul></div>' if ref_notes else ''}

<!-- KPI -->
<div class="kpi-strip">
  <div class="kpi"><div class="kpi-icon">❤️</div><div class="kpi-val" style="color:#f85149">{last_rhr_str}</div><div class="kpi-lbl">RHR bpm</div><div class="kpi-delta {'good' if analysis.get('rhr_cls') in ('excellent','good','normal') else 'warn'}">{analysis.get('rhr_lbl','--')}</div></div>
  <div class="kpi"><div class="kpi-icon">💙</div><div class="kpi-val" style="color:#58a6ff">{last_hrv_str}</div><div class="kpi-lbl">HRV ms</div><div class="kpi-delta good">自主神经弹性</div></div>
  <div class="kpi"><div class="kpi-icon">🫁</div><div class="kpi-val" style="color:#3fb950">{last_vo2_str}</div><div class="kpi-lbl">VO₂Max</div><div class="kpi-delta {'good' if analysis.get('vo2_cls') in ('good','excellent') else 'warn'}">{analysis.get('vo2_lbl','--')}</div></div>
  <div class="kpi"><div class="kpi-icon">👟</div><div class="kpi-val" style="color:#d29922">{last_steps_str}</div><div class="kpi-lbl">日均步数</div><div class="kpi-delta" style="color:{steps_color}">{steps_badge}</div></div>
  <div class="kpi"><div class="kpi-icon">🩸</div><div class="kpi-val" style="color:#bc8cff">{last_spo2_str}</div><div class="kpi-lbl">血氧 SpO₂</div><div class="kpi-delta good">✓ 正常</div></div>
  <div class="kpi"><div class="kpi-icon">⚖️</div><div class="kpi-val" style="color:#a5d6ff">{bmi_str}</div><div class="kpi-lbl">BMI</div><div class="kpi-delta info">参考 18.5-24.9</div></div>
</div>

<div class="body">

<div class="section-hd">❤️ 心血管系统</div>
<div class="charts-2">
  <div class="card span2">
    <div class="card-hd">
      <div>
        <div class="card-title"><div class="cdot" style="background:#f85149"></div>静息心率 &amp; HRV 趋势</div>
        <div class="card-sub">RHR 与 HRV 理论呈强负相关（相关系数 r={corr_str}）· 历史峰值 RHR {max_rhr_str} bpm</div>
      </div>
      <div class="badge bg">r = {corr_str}</div>
    </div>
    <div class="cw-tall"><canvas id="cRhrHrv"></canvas></div>
  </div>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="card-title"><div class="cdot" style="background:#3fb950"></div>VO₂Max 心肺适能</div>
        <div class="card-sub">当前：{last_vo2_str} mL/kg/min · 年龄/性别匹配基准：{vo2_good}（良好下限）</div>
      </div>
      <div class="badge {'bg' if analysis.get('vo2_cls') in ('good','excellent') else 'by'}">{analysis.get('vo2_lbl','--')} {'✓' if analysis.get('vo2_cls') in ('good','excellent') else '↑提升中'}</div>
    </div>
    <div class="cw"><canvas id="cVo2"></canvas></div>
  </div>
  <div class="card">
    <div class="card-hd">
      <div>
        <div class="card-title"><div class="cdot" style="background:#d29922"></div>自主神经相关性（RHR × HRV）</div>
        <div class="card-sub">甲亢/压力/疾病期 → 右上角（高RHR+低HRV）；恢复期 → 左下角</div>
      </div>
      <div class="badge bb">散点轨迹</div>
    </div>
    <div class="cw"><canvas id="cScatter"></canvas></div>
  </div>
</div>

<div class="section-hd">👟 活动与代谢</div>
<div class="charts-2">
  <div class="card span2">
    <div class="card-hd">
      <div>
        <div class="card-title"><div class="cdot" style="background:#d29922"></div>日均步数 &amp; 活动卡路里</div>
        <div class="card-sub">目标步数：{steps_target:,} 步/天（基于 {activity_display} 活动水平）</div>
      </div>
      <div class="badge {'bg' if analysis.get('steps_ok') else 'by'}">{steps_badge}</div>
    </div>
    <div class="cw"><canvas id="cSteps"></canvas></div>
  </div>
</div>

<div class="section-hd">🌙 睡眠系统</div>
<div class="charts-2">
  <div class="card span2">
    <div class="card-hd">
      <div>
        <div class="card-title"><div class="cdot" style="background:#76e4f7"></div>睡眠结构（Deep / REM / Core / Awake）</div>
        <div class="card-sub">Deep ≥13%、REM ≥15% 为良好目标 · 仅含支持睡眠分期的设备数据</div>
      </div>
      <div class="badge by">关注 Deep 占比</div>
    </div>
    <div class="cw"><canvas id="cSleep"></canvas></div>
  </div>
</div>

<div class="section-hd">🩸 血氧</div>
<div class="charts-2">
  <div class="card span2">
    <div class="card-hd">
      <div>
        <div class="card-title"><div class="cdot" style="background:#bc8cff"></div>血氧饱和度 SpO₂</div>
        <div class="card-sub">正常 ≥95% · 夜间低于 93% 建议就医 · 月均值偏低需排查睡眠呼吸</div>
      </div>
    </div>
    <div class="cw-sm"><canvas id="cSpo2"></canvas></div>
  </div>
</div>

<div class="section-hd">🔍 关键洞察</div>
<div class="insights" id="insightsGrid"></div>

</div>
<footer>
  Apple Health Export 分析报告 · 参考范围：ACSM / AHA / WHO 指南 · 基于个人信息动态校准<br>
  本报告由 AI 自动生成，仅供健康参考，不替代专业医疗诊断
</footer>

<script>
// ── 数据 ──────────────────────────────────────────────────────
const MONTHS     = {labels_js};
const RHR_DATA   = {series('rhr')};
const HRV_DATA   = {series('hrv')};
const VO2_DATA   = {series('vo2')};
const STEPS_DATA = {series('steps')};
const KCAL_DATA  = {series('active_kcal')};
const WEIGHT_KG  = {weight_series()};
const SLEEP_LABELS = {sleep_labels};
const SLEEP_DEEP = {sleep_pct('sleep_deep')};
const SLEEP_REM  = {sleep_pct('sleep_rem')};
const SLEEP_CORE = {sleep_pct('sleep_core')};
const SLEEP_AWAKE= {sleep_pct('sleep_awake')};
const SPO2_LABELS= {spo2_labels};
const SPO2_VALS  = {spo2_vals};
const SCATTER    = {scatter_js};

const VO2_GOOD   = {vo2_good};
const STEPS_TGT  = {steps_target};
const PEAK_MONTH = {json.dumps(peak_month)};
const RECOVER_MONTH = {json.dumps(recover_month)};

// ── 通用配置 ─────────────────────────────────────────────────
const BF = {{family:"-apple-system,'PingFang SC',sans-serif",size:10}};
const GC = 'rgba(255,255,255,0.05)';
const TC = {{backgroundColor:'#1c2128',titleFont:{{size:11}},bodyFont:{{size:10}},borderColor:'#30363d',borderWidth:1}};

// ── 事件线插件 ───────────────────────────────────────────────
function evPlug(evts) {{
  return {{
    id:'ev',
    afterDraw(chart) {{
      const {{ctx,scales:{{x}},chartArea:ca}} = chart;
      evts.forEach(([m,color,label]) => {{
        const i = MONTHS.indexOf(m);
        if(i<0) return;
        const xp = x.getPixelForValue(i);
        ctx.save();
        ctx.strokeStyle=color; ctx.lineWidth=1.5; ctx.setLineDash([4,3]);
        ctx.beginPath(); ctx.moveTo(xp,ca.top); ctx.lineTo(xp,ca.bottom); ctx.stroke();
        ctx.fillStyle=color; ctx.font=`bold 9px ${{BF.family}}`; ctx.setLineDash([]);
        ctx.fillText(label, xp+3, ca.top+12);
        ctx.restore();
      }});
    }}
  }};
}}

// ── Chart 1: RHR + HRV ───────────────────────────────────────
new Chart(document.getElementById('cRhrHrv'),{{
  type:'line',
  data:{{labels:MONTHS,datasets:[
    {{label:'RHR (bpm)',data:RHR_DATA,yAxisID:'yr',borderColor:'#f85149',backgroundColor:'rgba(248,81,73,.1)',borderWidth:2,pointRadius:2.5,fill:true,tension:0.4,spanGaps:true}},
    {{label:'HRV SDNN (ms)',data:HRV_DATA,yAxisID:'yh',borderColor:'#58a6ff',backgroundColor:'rgba(88,166,255,.1)',borderWidth:2,pointRadius:2.5,fill:true,tension:0.4,spanGaps:true}},
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},
    plugins:{{legend:{{labels:{{color:'#8b949e',font:BF,boxWidth:9,padding:12}}}},tooltip:TC}},
    scales:{{
      x:{{ticks:{{color:'#6e7681',font:BF,maxTicksLimit:14}},grid:{{color:GC}}}},
      yr:{{position:'left',ticks:{{color:'#f85149',font:BF}},grid:{{color:GC}},title:{{display:true,text:'RHR bpm',color:'#f85149',font:{{size:9}}}}}},
      yh:{{position:'right',ticks:{{color:'#58a6ff',font:BF}},grid:{{display:false}},title:{{display:true,text:'HRV ms',color:'#58a6ff',font:{{size:9}}}}}},
    }}}},
  plugins:[evPlug([[PEAK_MONTH,'#f85149','峰值'],[RECOVER_MONTH,'#3fb950','恢复']].filter(e=>e[0]))]
}});

// ── Chart 2: VO2Max ──────────────────────────────────────────
new Chart(document.getElementById('cVo2'),{{
  type:'line',
  data:{{labels:MONTHS,datasets:[{{label:'VO₂Max',data:VO2_DATA,borderColor:'#3fb950',backgroundColor:'rgba(63,185,80,.1)',borderWidth:2,pointRadius:2.5,fill:true,tension:0.4,spanGaps:true}}]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:TC}},
    scales:{{x:{{ticks:{{color:'#6e7681',font:BF,maxTicksLimit:10}},grid:{{color:GC}}}},y:{{ticks:{{color:'#8b949e',font:BF}},grid:{{color:GC}}}}}}}},
  plugins:[{{id:'vref',beforeDraw(chart){{
    const {{ctx,chartArea:ca,scales:{{y}}}}=chart;
    const yg=y.getPixelForValue(VO2_GOOD);
    ctx.save();
    ctx.fillStyle='rgba(63,185,80,.07)'; ctx.fillRect(ca.left,ca.top,ca.width,yg-ca.top);
    ctx.strokeStyle='rgba(63,185,80,.4)'; ctx.lineWidth=1; ctx.setLineDash([3,3]);
    ctx.beginPath(); ctx.moveTo(ca.left,yg); ctx.lineTo(ca.right,yg); ctx.stroke();
    ctx.fillStyle='rgba(63,185,80,.8)'; ctx.font=`bold 9px ${{BF.family}}`; ctx.setLineDash([]);
    ctx.fillText(`良好下限 ${{VO2_GOOD}}`,ca.left+5,yg-4); ctx.restore();
  }}}}]
}});

// ── Chart 3: Scatter ─────────────────────────────────────────
const sc_n = MONTHS.length;
const scColors = SCATTER.map(pt=>{{
  const i = MONTHS.indexOf(pt.m);
  const frac = i/sc_n;
  if(frac<0.33) return '#f85149';
  if(frac<0.66) return '#d29922';
  return '#3fb950';
}});
new Chart(document.getElementById('cScatter'),{{
  type:'scatter',
  data:{{datasets:[{{label:'月度均值',data:SCATTER,backgroundColor:scColors,borderColor:scColors,pointRadius:6,pointHoverRadius:9,borderWidth:1.5}}]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{...TC,callbacks:{{label:c=>` ${{c.raw.m}}  RHR=${{c.raw.x}} HRV=${{c.raw.y}}ms`}}}}}},
    scales:{{
      x:{{title:{{display:true,text:'RHR (bpm)',color:'#8b949e',font:BF}},ticks:{{color:'#6e7681',font:BF}},grid:{{color:GC}}}},
      y:{{title:{{display:true,text:'HRV SDNN (ms)',color:'#8b949e',font:BF}},ticks:{{color:'#6e7681',font:BF}},grid:{{color:GC}}}},
    }}}}
}});

// ── Chart 4: Steps + Kcal ────────────────────────────────────
new Chart(document.getElementById('cSteps'),{{
  type:'bar',
  data:{{labels:MONTHS,datasets:[
    {{label:'日均步数',data:STEPS_DATA,yAxisID:'ys',backgroundColor:'rgba(210,153,34,.6)',borderColor:'#d29922',borderWidth:1,borderRadius:2,type:'bar'}},
    {{label:'活动 kcal',data:KCAL_DATA,yAxisID:'yk',borderColor:'#f85149',backgroundColor:'transparent',borderWidth:1.5,pointRadius:1.5,tension:0.4,type:'line',spanGaps:true}},
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{labels:{{color:'#8b949e',font:BF,boxWidth:9,padding:10}}}},tooltip:TC}},
    scales:{{
      x:{{ticks:{{color:'#6e7681',font:BF,maxTicksLimit:12}},grid:{{display:false}}}},
      ys:{{position:'left',min:0,ticks:{{color:'#d29922',font:BF,callback:v=>(v/1000).toFixed(0)+'k'}},grid:{{color:GC}}}},
      yk:{{position:'right',min:0,ticks:{{color:'#f85149',font:BF}},grid:{{display:false}}}},
    }}}},
  plugins:[{{id:'stgt',beforeDraw(chart){{
    const {{ctx,chartArea:ca,scales:{{ys}}}}=chart;
    const yt=ys.getPixelForValue(STEPS_TGT);
    ctx.save(); ctx.strokeStyle='rgba(63,185,80,.4)'; ctx.lineWidth=1; ctx.setLineDash([3,3]);
    ctx.beginPath(); ctx.moveTo(ca.left,yt); ctx.lineTo(ca.right,yt); ctx.stroke();
    ctx.fillStyle='rgba(63,185,80,.7)'; ctx.font=`9px ${{BF.family}}`; ctx.setLineDash([]);
    ctx.fillText(`目标 ${{(STEPS_TGT/1000).toFixed(0)}}k`,ca.left+4,yt-3); ctx.restore();
  }}}}]
}});

// ── Chart 5: Sleep ───────────────────────────────────────────
new Chart(document.getElementById('cSleep'),{{
  type:'bar',
  data:{{labels:SLEEP_LABELS,datasets:[
    {{label:'Deep %',data:SLEEP_DEEP,backgroundColor:'#58a6ff',borderRadius:2,stack:'s'}},
    {{label:'REM %', data:SLEEP_REM, backgroundColor:'#bc8cff',borderRadius:2,stack:'s'}},
    {{label:'Core %',data:SLEEP_CORE,backgroundColor:'#3fb950', borderRadius:2,stack:'s'}},
    {{label:'Awake%',data:SLEEP_AWAKE,backgroundColor:'#f85149',borderRadius:2,stack:'s'}},
  ]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{labels:{{color:'#8b949e',font:{{size:9}},boxWidth:8,padding:8}}}},tooltip:{{...TC,callbacks:{{label:c=>` ${{c.dataset.label}}: ${{c.parsed.y}}%`}}}}}},
    scales:{{
      x:{{stacked:true,ticks:{{color:'#6e7681',font:{{size:8}},maxTicksLimit:14}},grid:{{display:false}}}},
      y:{{stacked:true,max:100,ticks:{{color:'#8b949e',font:BF,callback:v=>v+'%'}},grid:{{color:GC}}}},
    }}}}
}});

// ── Chart 6: SpO2 ────────────────────────────────────────────
new Chart(document.getElementById('cSpo2'),{{
  type:'line',
  data:{{labels:SPO2_LABELS,datasets:[{{label:'SpO₂ %',data:SPO2_VALS,borderColor:'#bc8cff',backgroundColor:'rgba(188,140,255,.1)',borderWidth:2,pointRadius:2.5,fill:true,tension:0.4}}]}},
  options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{display:false}},tooltip:{{...TC,callbacks:{{label:c=>` ${{c.parsed.y}}%`}}}}}},
    scales:{{x:{{ticks:{{color:'#6e7681',font:BF,maxTicksLimit:10}},grid:{{color:GC}}}},y:{{min:92,max:100,ticks:{{color:'#8b949e',font:BF,callback:v=>v+'%'}},grid:{{color:GC}}}}}}}},
  plugins:[{{id:'s95',beforeDraw(chart){{
    const {{ctx,chartArea:ca,scales:{{y}}}}=chart;
    const y95=y.getPixelForValue(95);
    ctx.save(); ctx.strokeStyle='rgba(248,81,73,.4)'; ctx.lineWidth=1; ctx.setLineDash([3,3]);
    ctx.beginPath(); ctx.moveTo(ca.left,y95); ctx.lineTo(ca.right,y95); ctx.stroke();
    ctx.fillStyle='rgba(248,81,73,.6)'; ctx.font=`9px ${{BF.family}}`; ctx.setLineDash([]);
    ctx.fillText('关注线 95%',ca.left+4,y95-3); ctx.restore();
  }}}}]
}});

// ── 洞察生成（动态）─────────────────────────────────────────
const insights = [];

// RHR 趋势
const rhrValid = RHR_DATA.filter(v=>v!==null);
const rhrMax = rhrValid.length ? Math.max(...rhrValid) : null;
const rhrLast = rhrValid.length ? rhrValid[rhrValid.length-1] : null;
if(rhrMax && rhrLast && rhrMax - rhrLast > 10) {{
  insights.push(['✅','lv-lo','RHR 明显改善',`历史峰值 ${{rhrMax}} bpm，当前 ${{rhrLast}} bpm，下降 ${{(rhrMax-rhrLast).toFixed(0)}} bpm，心血管负担减轻`]);
}} else if(rhrLast && rhrLast > {ref['rhr_bands'][2]}) {{
  insights.push(['⚡','lv-md','RHR 偏高',`当前 ${{rhrLast}} bpm，高于年龄/性别正常上限 {ref['rhr_bands'][2]} bpm，建议增加有氧训练`]);
}}

// HRV
const hrvValid = HRV_DATA.filter(v=>v!==null);
const hrvLast = hrvValid.length ? hrvValid[hrvValid.length-1] : null;
if(hrvLast && hrvLast < {ref['hrv_low']}) {{
  insights.push(['⚡','lv-md','HRV 偏低',`当前 ${{hrvLast}} ms，低于参考下限 {ref['hrv_low']} ms，自主神经调节弹性不足，建议改善睡眠和减压`]);
}} else if(hrvLast) {{
  insights.push(['💙','lv-lo','HRV 自主神经平衡',`当前 ${{hrvLast}} ms，处于正常区间，自主神经调节功能良好`]);
}}

// VO2Max
const vo2Valid = VO2_DATA.filter(v=>v!==null);
const vo2Last = vo2Valid.length ? vo2Valid[vo2Valid.length-1] : null;
if(vo2Last) {{
  if(vo2Last >= VO2_GOOD) {{
    insights.push(['🫁','lv-lo',`VO₂Max 达到良好水平`,`当前 ${{vo2Last}} mL/kg/min，已超过年龄/性别良好基准 ${{VO2_GOOD}}，心肺适能状态优`]);
  }} else {{
    insights.push(['🫁','lv-md',`VO₂Max 仍有提升空间`,`当前 ${{vo2Last}} mL/kg/min，目标 ${{VO2_GOOD}}（良好下限），建议规律有氧训练`]);
  }}
}}

// 步数
const stepsValid = STEPS_DATA.filter(v=>v!==null);
const stepsLast = stepsValid.length ? stepsValid[stepsValid.length-1] : null;
if(stepsLast) {{
  if(stepsLast >= STEPS_TGT) {{
    insights.push(['👟','lv-lo','活动量达标',`日均 ${{Math.round(stepsLast/1000)}}k 步，高于个性化目标 ${{Math.round(STEPS_TGT/1000)}}k，保持`]);
  }} else {{
    insights.push(['👟','lv-md','活动量偏低',`日均 ${{Math.round(stepsLast/1000)}}k 步，低于目标 ${{Math.round(STEPS_TGT/1000)}}k，建议增加日常步行`]);
  }}
}}

// 相关系数
const corrVal = {json.dumps(analysis.get('corr'))};
if(corrVal && Math.abs(corrVal) > 0.7) {{
  insights.push(['📊','lv-lo','RHR-HRV 强负相关',`相关系数 r=${{corrVal}}，数据质量高，趋势分析可信度强`]);
}}

// 睡眠 Deep
const deepVals = SLEEP_DEEP.filter(v=>v>0);
const deepAvg = deepVals.length ? deepVals.reduce((a,b)=>a+b,0)/deepVals.length : null;
if(deepAvg && deepAvg < 12) {{
  insights.push(['🌙','lv-md','Deep Sleep 偏低',`近期 Deep Sleep 平均占比 ${{deepAvg.toFixed(0)}}%，低于理想目标 13%，建议规律作息、侧卧入睡，排查夜间血氧`]);
}}

// SpO2 波动
const spo2Vals = SPO2_VALS.filter(v=>v!==null);
const spo2Avg = spo2Vals.length ? spo2Vals.reduce((a,b)=>a+b,0)/spo2Vals.length : null;
if(spo2Avg && spo2Avg < 96.5) {{
  insights.push(['🩸','lv-md','血氧月均偏低',`平均 ${{spo2Avg.toFixed(1)}}%，建议监测夜间最低值，排查轻度睡眠呼吸问题`]);
}}

// 渲染
const grid = document.getElementById('insightsGrid');
insights.forEach(([icon,lv,name,desc]) => {{
  grid.innerHTML += `<div class="ins">
    <div class="ins-icon">${{icon}}</div>
    <div><div class="ins-lv ${{lv}}">${{lv==='lv-hi'?'高优先':'lv-md'===lv?'中等关注':'良好'}}</div>
    <div class="ins-name">${{name}}</div>
    <div class="ins-desc">${{desc}}</div></div>
  </div>`;
}});
</script>
</body>
</html>"""
    return html


# ═══════════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Apple Health 报告生成器 v2.0')
    parser.add_argument('data_path',  help='chart_data.json 路径')
    parser.add_argument('out_path',   help='输出 HTML 路径')
    parser.add_argument('--gender',      default='other')
    parser.add_argument('--age',         type=int, default=30)
    parser.add_argument('--height',      type=float, default=170)
    parser.add_argument('--weight-unit', default='lb', choices=['lb','kg'])
    parser.add_argument('--conditions',  default='')
    parser.add_argument('--activity',    default='light',
                        choices=['sedentary','light','active','athlete'])
    parser.add_argument('--verdict',     default=None)
    args = parser.parse_args()

    raw = json.loads(Path(args.data_path).read_text())
    # 兼容新旧格式
    if 'data' in raw:
        chart_data_full = raw
        data = raw['data']
    else:
        chart_data_full = {'data': raw}
        data = raw

    conditions = [c.strip() for c in args.conditions.split(',') if c.strip()]

    profile = {
        'gender':         args.gender,
        'age':            args.age,
        'height_cm':      args.height,
        'weight_unit':    args.weight_unit,
        'conditions':     conditions,
        'activity_level': args.activity,
    }

    ref = build_reference(
        gender=args.gender,
        age=args.age,
        height_cm=args.height,
        activity_level=args.activity,
        conditions=conditions,
    )

    analysis = analyze(data, ref, profile)

    if not args.verdict:
        rhr_lbl = analysis.get('rhr_lbl', '--')
        vo2_lbl = analysis.get('vo2_lbl', '--')
        verdict = f'整体判断：RHR {rhr_lbl}（{analysis.get("last_rhr","--")} bpm）· VO₂Max {vo2_lbl}（{analysis.get("last_vo2","--")}）· 基于个人画像动态校准'
    else:
        verdict = args.verdict

    html = render_html(chart_data_full, profile, ref, analysis, verdict)
    Path(args.out_path).write_text(html, encoding='utf-8')
    print(f"[INFO] 报告已生成：{args.out_path}")


if __name__ == '__main__':
    main()
