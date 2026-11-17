#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""report_engine.py — 办公室提效账本报告生成器（office-token-booster / B 线）

读取用户主动提供的「提效账本」JSON（ledger.json），量化「笨办法 vs 本技能」节省的
Token 与耗时，生成 Markdown / HTML / JSON 报告。

设计原则（与 agent-analytics-report 报告引擎一脉相承，但完全解耦）：
- 纯标准库，无第三方依赖、无网络、无硬编码密钥
- 数据源是用户主动提供的文件（ledger.json），不读取任何平台私有目录
- 节省值为参考估计，不是平台计费数据

账本格式（ledger.json）：
{
  "tasks": [
    {
      "date": "2026-08-08",
      "type": "会议纪要",
      "baseline_tokens": 12000,
      "skill_tokens": 3000,
      "baseline_minutes": 25,
      "skill_minutes": 3,
      "note": "可选备注"
    }
  ]
}
"""

# ---------------------------------------------------------------------------
# FORK NOTE (office-token-booster / B 线):
# 本文件从 agent-analytics-report/scripts/generate_report.py fork 而来，作为独立产品线维护。
# 已剥离宿主数据源耦合：移除 collect_usage_data 运行时导入与 main() 实时采集分支，
# 中性化 pricing.json 引用（B 线默认走「用户上传/导出数据」模式，不依赖天禧/宿主用量 API）。
# 下方报告函数已适配 office ledger 数据（消费 token/耗时/任务类型），作为 B 线唯一报告生成器。
# 通用渲染原语（format_number / _pad_label / build_donut_chart 等）沿用 A 引擎。
# ---------------------------------------------------------------------------

import argparse
import json
import math
import sys
import unicodedata
from pathlib import Path
from diagnose import format_number, load_ledger, diagnose, Diagnosis, _safe_div

import html as _html
# P2 安全：所有进 HTML 的用户字段必须经此转义，杜绝 <script> 等注入。
_esc = _html.escape
from skill_recommender import recommend_skills, format_recommendations_md, format_recommendations_html


# ─────────────────────────────────────────────────────────────
# 通用工具（沿用 A 引擎渲染原语）
# ─────────────────────────────────────────────────────────────

# format_number 已移至 diagnose.py（内核与渲染共用），此处从 diagnose 导入。


def _disp_width(s):
    """等宽字体下的显示宽度：CJK / 全角字符计 2，其余计 1。"""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in str(s))


def _pad_label(s, width):
    """按显示宽度右侧补空格，使等宽字体下中文 / 英文混排的标签列对齐。"""
    return str(s) + " " * max(0, width - _disp_width(s))


# _safe_div 已统一从 diagnose 导入（内核与渲染共用），此处不再重复定义。


# 环形图调色板（与表格配色协调）
_DONUT_PALETTE = [
    "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e67e22", "#34495e", "#16a085", "#c0392b",
    "#8e44ad", "#27ae60",
]


def build_donut_chart(stats, title="节省 Token 占比（按任务类型）",
                      center_label="节省 Token", value_key="saved_tokens", unit=""):
    """生成自包含内联 SVG 环形图（currentColor + CSS 变量，浅/深主题兼容）。

    stats: 含 task_type 与各数值字段的列表。value_key 指定扇形取值字段。
    无数据时返回空串；不依赖外部 CDN。
    """
    items = [s for s in stats if s.get(value_key, 0) > 0]
    total = sum(s.get(value_key, 0) for s in items)
    if total <= 0:
        return ""
    items = sorted(items, key=lambda x: x.get(value_key, 0), reverse=True)

    cx, cy, r, sw = 110, 110, 80, 34
    circ = 2 * math.pi * r
    cum = 0.0
    arcs = []
    legend = []
    for i, s in enumerate(items):
        frac = s.get(value_key, 0) / total
        seg_len = frac * circ
        color = _DONUT_PALETTE[i % len(_DONUT_PALETTE)]
        pct = frac * 100
        arcs.append(
            f'        <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" '
            f'stroke-dasharray="{seg_len:.2f} {circ - seg_len:.2f}" '
            f'stroke-dashoffset="{-cum:.2f}" />'
        )
        legend.append(
            f'            <div class="legend-item">'
            f'<span class="swatch" style="background:{color}"></span>'
            f'{_esc(s["task_type"])}：{pct:.1f}%'
            f'<span class="pct">（{format_number(s.get(value_key, 0))}{unit}）</span></div>'
        )
        cum += seg_len

    svg = f"""    <div class="chart-pie">
        <svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="{title}">
            <g transform="rotate(-90 {cx} {cy})">
                <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" style="stroke:var(--table-border)" stroke-width="{sw}" />
{chr(10).join(arcs)}
            </g>
            <text x="{cx}" y="{cy - 4}" text-anchor="middle" font-size="15" font-weight="bold" style="fill:var(--accent-fg)">{format_number(total)}</text>
            <text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="11" style="fill:var(--muted)">{center_label}</text>
        </svg>
        <div class="legend">
{chr(10).join(legend)}
        </div>
    </div>"""
    return svg


def build_saving_chart_md(by_type, value_key="saved_tokens", title="各任务类型 节省 Token 分布"):
    """Markdown 横向条形图（fenced ``` 代码块）：各任务类型节省量分布。"""
    items = [d for d in by_type if d.get(value_key, 0) > 0]
    if not items:
        return ""
    items = sorted(items, key=lambda x: x.get(value_key, 0), reverse=True)[:10]
    total = sum(d.get(value_key, 0) for d in items) or 1
    maxv = max(d.get(value_key, 0) for d in items) or 1
    bar_w = 32
    label_w = 16
    out = [f"**{title}**", ""]
    for d in items:
        v = d.get(value_key, 0)
        pct = v / total * 100
        n = max(int(bar_w * v / maxv), 1)
        bar = "█" * n
        out.append(f"{_pad_label(d['task_type'], label_w)} | {bar} {pct:.1f}% ({format_number(v)})")
    return "```\n" + "\n".join(out) + "\n```"


def build_trend_line_chart(weeks, value_key="saved_tokens", title="按周节省 Token 趋势"):
    """自包含内联 SVG 折线/面积图（浅/深主题兼容，与 donut 同风格）。

    weeks: list[dict]（含 week / value_key）。无数据返回空串；不依赖外部 CDN。
    """
    pts = [(w.get("week", ""), w.get(value_key, 0) or 0) for w in weeks]
    if not pts:
        return ""
    n = len(pts)
    W, H = 480, 200
    pad_l, pad_r, pad_t, pad_b = 44, 18, 18, 30
    plot_w = W - pad_l - pad_r
    plot_h = H - pad_t - pad_b
    maxv = max(v for _, v in pts) or 1
    xs = [pad_l + (plot_w * i / (n - 1)) if n > 1 else pad_l + plot_w / 2 for i in range(n)]
    ys = [pad_t + plot_h * (1 - v / maxv) for _, v in pts]

    grid = []
    for g in range(5):
        gy = pad_t + plot_h * g / 4
        gv = maxv * (1 - g / 4)
        grid.append(
            f'<line x1="{pad_l}" y1="{gy:.1f}" x2="{W - pad_r}" y2="{gy:.1f}" '
            f'stroke="var(--table-border)" stroke-width="1"/>')
        grid.append(
            f'<text x="{pad_l - 6}" y="{gy + 4:.1f}" text-anchor="end" '
            f'font-size="10" style="fill:var(--muted)">{format_number(gv)}</text>')

    line_pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    area_pts = f"{pad_l},{pad_t + plot_h} " + line_pts + f" {xs[-1]:.1f},{pad_t + plot_h}"
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="var(--accent)" '
        f'stroke="var(--bg)" stroke-width="1.5"><title>{_esc(wk)}: {format_number(v)}</title></circle>'
        for (wk, v), x, y in zip(pts, xs, ys))
    xlabels = "".join(
        f'<text x="{x:.1f}" y="{H - 10}" text-anchor="middle" font-size="10" '
        f'style="fill:var(--muted)">{_esc(wk.replace("2026-", "W").replace("2025-", "W"))}</text>'
        for (wk, _), x in zip(pts, xs))

    return f"""    <div class="chart-line">
      <div class="chart-title">{title}</div>
      <svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{title}">
        {''.join(grid)}
        <polygon points="{area_pts}" fill="var(--accent)" opacity="0.12"/>
        <polyline points="{line_pts}" fill="none" stroke="var(--accent)" stroke-width="2.5"
                  stroke-linejoin="round" stroke-linecap="round"/>
        {dots}
        {xlabels}
      </svg>
    </div>"""


def _fmt_pct(p):
    return "—" if p is None else f"{p:+.1f}%"


def build_compare_card(pc):
    """「本期 vs 上期」对比卡片（消费 Diagnosis.period_compare）。无数据返回空串。"""
    if not pc:
        return ""
    arrow = {"up": "▲", "down": "▼", "flat": "▬", "new": "✦"}.get(pc["direction"], "")
    cur, prev = pc["current"], pc["previous"]
    return f"""
    <div class="cmp-card">
      <div class="cmp-title">📈 本期 vs 上期（{_esc(pc['current_week'])} 对比 {_esc(pc['previous_week'])}）</div>
      <div class="cmp-grid">
        <div><span class="cmp-k">省 Token</span><span class="cmp-v">{format_number(cur['saved_tokens'])}</span>
            <span class="cmp-d {pc['direction']}">{arrow} {_fmt_pct(pc['saved_tokens_pct'])}</span></div>
        <div><span class="cmp-k">任务数</span><span class="cmp-v">{cur['count']}</span>
            <span class="cmp-d {pc['direction']}">{arrow} {_fmt_pct(pc['count_pct'])}</span></div>
        <div><span class="cmp-k">省时间</span><span class="cmp-v">{format_number(cur['saved_minutes'])}分</span>
            <span class="cmp-d {pc['direction']}">{arrow} {_fmt_pct(pc['saved_minutes_pct'])}</span></div>
      </div>
      <div class="cmp-note">上期：省 {format_number(prev['saved_tokens'])} Token / {prev['count']} 次任务</div>
    </div>"""


def build_roi_card(roi_targets, top_n=3):
    """「最该自动化（按 ROI 排序）」卡片（消费 Diagnosis.roi_targets）。无数据返回空串。"""
    if not roi_targets:
        return ""
    items = []
    for t in roi_targets[:top_n]:
        items.append(
            f'<li><b>{_esc(t["task_type"])}</b> — ROI≈{t["roi_score"]} '
            f'（预估月省 {format_number(t["monthly_saved_tokens"])} Token，'
            f'接入约 {t["effort_hours"]} 人时）</li>')
    return f"""
    <div class="roi-card">
      <div class="cmp-title">🤖 最该自动化（按 ROI 排序 Top {top_n}）</div>
      <ul>{''.join(items)}</ul>
    </div>"""


# ─────────────────────────────────────────────────────────────
# 办公数据层（消费 ledger.json）
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# 办公数据层（消费 ledger.json）已移至 diagnose.py（诊断内核）：
#   load_ledger / _safe_div / compute_summary / build_insights
# 本文件只保留渲染层，渲染函数统一消费 diagnose.Diagnosis 对象。
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# 核心洞察（办公域）
# ─────────────────────────────────────────────────────────────

# build_insights 已移至 diagnose.py（诊断内核），其产出由 Diagnosis.insights / recommendations 携带。


# ─────────────────────────────────────────────────────────────
# Markdown 报告（九段结构，办公域适配）
# ─────────────────────────────────────────────────────────────

def generate_markdown_report(s):
    L = []
    L.append("# 办公室提效报告")
    L.append("")
    L.append(f"> 生成时间：{s.generated_at} ｜ 共 {s.n} 条任务记录")
    L.append("")

    # 一、概览
    L.append("## 一、概览")
    L.append("")
    L.append(f"- **节省 Token**：{format_number(s.saved_tok)}（基准 {format_number(s.total_base_tok)} → 本技能 {format_number(s.total_skill_tok)}），节省 **{s.token_save_pct:.1f}%**")
    L.append(f"- **节省时间**：{format_number(s.saved_min)} 分钟（基准 {format_number(s.total_base_min)} → 本技能 {format_number(s.total_skill_min)}），节省 **{s.time_save_pct:.1f}%**")
    L.append("")

    # 本期 vs 上期（周期对比洞察）
    if s.period_compare:
        pc = s.period_compare
        arrow = {"up": "▲", "down": "▼", "flat": "▬", "new": "✦"}.get(pc["direction"], "")
        pct = "—" if pc["saved_tokens_pct"] is None else f"{pc['saved_tokens_pct']:+.1f}%"
        L.append(f"- **本期 vs 上期**（{pc['current_week']} 对比 {pc['previous_week']}）："
                 f"省 {format_number(pc['current']['saved_tokens'])} Token（{arrow} {pct}），"
                 f"任务 {pc['current']['count']} 次。")
        L.append("")

    # 二、Token 提效可视化
    L.append("## 二、Token 提效可视化")
    L.append("")
    L.append(build_saving_chart_md(s.by_type))
    L.append("")

    # 三、任务类型统计
    L.append("## 三、任务类型统计")
    L.append("")
    L.append("| 类型 | 任务数 | 基准 Token | 本技能 Token | 省 Token | 省时间(分) | Token节省% | 质量分 |")
    L.append("|------|------|------|------|------|------|------|------|")
    for d in s.by_type:
        q = d.get("quality_score_avg")
        q_disp = "—" if q is None else q
        L.append(f"| {d['task_type']} | {d['count']} | {format_number(d['baseline_tokens'])} | {format_number(d['skill_tokens'])} | "
                 f"{format_number(d['saved_tokens'])} | {format_number(d['saved_minutes'])} | {d['token_save_pct']:.1f}% | {q_disp} |")
    L.append("")

    # 四、任务 Token 消耗统计
    L.append("## 四、任务 Token 消耗统计")
    L.append("")
    L.append("| 类型 | 基准 Token | 本技能 Token | 节省 Token | 节省占比 |")
    L.append("|------|------|------|------|------|")
    for d in s.by_type:
        L.append(f"| {d['task_type']} | {format_number(d['baseline_tokens'])} | {format_number(d['skill_tokens'])} | "
                 f"{format_number(d['saved_tokens'])} | {d['token_save_pct']:.1f}% |")
    L.append("")

    # 五、能力 / 场景使用统计
    L.append("## 五、能力 / 场景使用统计")
    L.append("")
    L.append("> 按调用次数看各办公能力的使用频度，识别高频场景。")
    L.append("")
    L.append("| 能力 / 场景 | 调用次数 | 占总任务比 |")
    L.append("|------|------|------|")
    for d in s.by_type:
        ratio = _safe_div(d["count"], s.n) * 100
        L.append(f"| {d['task_type']} | {d['count']} | {ratio:.1f}% |")
    L.append("")

    # 六、任务执行情况
    L.append("## 六、任务执行情况")
    L.append("")
    L.append("| 日期 | 类型 | 基准(min) | 技能(min) | 省(min) | 基准(tok) | 技能(tok) | 省(tok) |")
    L.append("|------|------|------|------|------|------|------|------|")
    # 这里需要原始 tasks；compute_summary 不保留，改为在 main 注入
    for t in s.tasks:
        bt = t.get("baseline_tokens", 0) or 0
        st = t.get("skill_tokens", 0) or 0
        bm = t.get("baseline_minutes", 0) or 0
        sm = t.get("skill_minutes", 0) or 0
        L.append(f"| {t.get('date','')} | {t.get('type','')} | {bm} | {sm} | {bm-sm} | {format_number(bt)} | {format_number(st)} | {format_number(bt-st)} |")
    L.append("")

    # 七、产出物清单
    L.append("## 七、产出物清单")
    L.append("")
    for i, t in enumerate(s.tasks, 1):
        note = t.get("note") or "（无备注）"
        L.append(f"{i}. `{t.get('date','')}` ｜ {t.get('type','')} ｜ {note}")
    L.append("")

    # 八、核心洞察与建议
    insights, recs = s.insights, s.recommendations
    L.append("## 八、核心洞察与建议")
    L.append("")
    L.append("**洞察**")
    L.append("")
    for x in insights:
        L.append(f"- {x}")
    L.append("")
    L.append("**建议**")
    L.append("")
    for x in recs:
        L.append(f"- {x}")
    L.append("")

    # 推荐 Skill（本地静态规则，无联网）：集中渲染，含「未经实测验证」披露
    # 完整报告的段落有编号，故传入「九、」标题；摘要用默认无编号标题。
    skill_recs = recommend_skills(s.by_type, s.n)
    if skill_recs:
        L.append(format_recommendations_md(skill_recs, heading="## 九、推荐 Skill"))

    # 十一、下周展望
    L.append("## 十一、下周展望")
    L.append("")
    L.append("- 持续记录任务账本，观察节省趋势是否稳定。")
    L.append("- 对高频 / 高基线场景沉淀为可复用提示词模板，进一步压缩技能 Token。")
    L.append("- 若参加「天禧 AI Skills 苍穹共创计划」，本报告的「本地处理、零上传」可作为合规卖点。")
    L.append("")

    # 质量护栏（不降质量）
    L.append("## 十二、质量护栏（不降质量）")
    L.append("")
    L.append(_quality_guard_md(s))
    L.append("")

    # 数据可信度提示（baseline 护栏）
    if s.caveats:
        L.append("## 十三、数据可信度提示")
        L.append("")
        L.append("> 节省值基于你填写的基准估计，以下提示用于校验「提效」声称的可信度：")
        L.append("")
        for c in s.caveats:
            L.append(f"- ⚠️ {c}")
        L.append("")

    L.append("---")
    L.append(f"*{s.methodology}*")
    return "\n".join(L)


# ─────────────────────────────────────────────────────────────
# HTML 报告
# ─────────────────────────────────────────────────────────────

def _bar_html(value, max_value, color="#2ecc71"):
    w = int(_safe_div(value, max_value) * 100)
    w = max(2, min(100, w))
    return (f'<div style="background:#f3f4f6;border-radius:4px;height:14px;width:100%;">'
            f'<div style="background:{color};height:14px;border-radius:4px;width:{w}%;"></div></div>')


def _quality_guard_html(s):
    """不降质量护栏横幅（HTML）：根据整体质量分均值给「节省是否可信」判定。"""
    if not s.has_quality:
        color, icon, msg = "#6b7280", "ℹ️", "本期无质量分记录，节省值仅反映成本对比（交付质量未测）。"
    elif s.quality_ok:
        color, icon, msg = "#16a34a", "✅", f"质量达标（均分 {s.avg_quality}/100 ≥ 门槛 {s.quality_floor}），节省可信。"
    else:
        color, icon, msg = "#dc2626", "⚠️", (f"质量跌破基线（均分 {s.avg_quality}/100 < 门槛 {s.quality_floor}），"
                                       f"本期节省不可信，请先复核交付物结构完整度。")
    return (f'<div style="border-left:4px solid {color};background:#f9fafb;padding:10px 12px;'
            f'border-radius:8px;margin:14px 0;color:#111827;">'
            f'<strong style="color:{color}">{icon} 质量护栏</strong>　{msg}</div>')


def _quality_guard_md(s):
    """不降质量护栏文案（Markdown）。"""
    if not s.has_quality:
        return ("> ⚠️ **质量护栏**：本期无质量分记录，节省值仅反映成本对比"
                "（交付质量未测）。建议在生成交付物后用本技能自带的确定性质量检查。")
    if s.quality_ok:
        return (f"> ✅ **质量护栏**：均分 {s.avg_quality}/100 ≥ 门槛 {s.quality_floor}，"
                f"交付质量达标，节省可信。")
    return (f"> ⚠️ **质量护栏**：均分 {s.avg_quality}/100 < 门槛 {s.quality_floor}，"
            f"**本期节省不可信**——请先复核交付物结构完整度，勿仅凭成本下降下结论。")


def _quality_cell(q, floor):
    """表格内质量分单元格（HTML）。q=None → 灰色「—」。"""
    if q is None:
        return '<td style="color:var(--muted)">—</td>'
    color = "#16a34a" if q >= floor else "#dc2626"
    return f'<td style="color:{color};font-weight:600">{q}</td>'


def generate_html_report(s):
    donut = build_donut_chart(s.by_type, title="各任务类型 节省 Token 占比",
                              center_label="节省 Token", value_key="saved_tokens")
    insights, recs = s.insights, s.recommendations

    type_rows = ""
    max_tok = max((d["baseline_tokens"] for d in s.by_type), default=1) or 1
    for d in s.by_type:
        q = d.get("quality_score_avg")
        q_disp = "—" if q is None else str(q)
        q_color = "var(--muted)" if q is None else ("#16a34a" if q >= s.quality_floor else "#dc2626")
        type_rows += (
            f'<tr><td>{_esc(d["task_type"])}</td><td>{d["count"]}</td>'
            f'<td>{format_number(d["baseline_tokens"])}</td><td>{format_number(d["skill_tokens"])}</td>'
            f'<td>{format_number(d["saved_tokens"])}</td><td>{format_number(d["saved_minutes"])}</td>'
            f'<td>{d["token_save_pct"]:.1f}%</td>'
            f'<td style="color:{q_color};font-weight:600">{q_disp}</td></tr>'
        )

    week_rows = ""
    for w in s.by_week:
        week_rows += (f'<tr><td>{_esc(w["week"])}</td><td>{w["count"]}</td>'
                      f'<td>{format_number(w["baseline_tokens"])}</td><td>{format_number(w["skill_tokens"])}</td>'
                      f'<td>{format_number(w["saved_tokens"])}</td></tr>')

    trend_chart = build_trend_line_chart(s.by_week)
    compare_card = build_compare_card(s.period_compare)
    roi_card = build_roi_card(s.roi_targets)

    insight_html = "".join(f"<li>{_esc(x)}</li>" for x in insights)
    rec_html = "".join(f"<li>{_esc(x)}</li>" for x in recs)
    caveat_html = "".join(f"<li>{_esc(c)}</li>" for c in s.caveats)

    # Skill 推荐板块（本地静态规则，无联网）
    skill_recs = recommend_skills(s.by_type, s.n)
    skill_rec_html = format_recommendations_html(skill_recs)

    task_rows = ""
    for t in s.tasks:
        bt = t.get("baseline_tokens", 0) or 0
        st = t.get("skill_tokens", 0) or 0
        bm = t.get("baseline_minutes", 0) or 0
        sm = t.get("skill_minutes", 0) or 0
        q = t.get("quality_score")
        q_disp = "—" if q is None else str(q)
        task_rows += (f'<tr><td>{_esc(t.get("date",""))}</td><td>{_esc(t.get("type",""))}</td>'
                      f'<td>{bm}</td><td>{sm}</td><td>{bm-sm}</td>'
                      f'<td>{format_number(bt)}</td><td>{format_number(st)}</td>'
                      f'<td>{format_number(bt-st)}</td>'
                      f'<td style="color:var(--muted)">{q_disp}</td></tr>')

    css = """
    :root{--bg:#fff;--fg:#111827;--muted:#6b7280;--table-border:#e5e7eb;
          --accent:#22c55e;--accent-fg:#111827;}
    body{font-family:-apple-system,Segoe UI,Roboto,'Microsoft YaHei',sans-serif;
         max-width:920px;margin:24px auto;padding:0 16px;color:var(--fg);}
    h1{font-size:22px;} h2{font-size:17px;margin-top:28px;border-left:4px solid var(--accent);padding-left:8px;}
    .cards{display:flex;gap:16px;flex-wrap:wrap;margin:16px 0;}
    .card{flex:1;min-width:180px;background:#f9fafb;border:1px solid var(--table-border);
          border-radius:10px;padding:14px;}
    .card .big{font-size:24px;font-weight:700;} .card .sub{color:var(--muted);font-size:13px;}
    .chart-pie{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:12px 0;}
    .legend{font-size:13px;} .legend-item{margin:2px 0;}
    .swatch{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;}
    .chart-line{margin:12px 0 4px;} .chart-title{font-size:14px;font-weight:600;margin-bottom:6px;}
    .cmp-card,.roi-card{background:#f9fafb;border:1px solid var(--table-border);border-radius:10px;
          padding:14px;margin:14px 0;}
    .cmp-title{font-size:14px;font-weight:600;margin-bottom:10px;}
    .cmp-grid{display:flex;gap:18px;flex-wrap:wrap;}
    .cmp-grid>div{display:flex;flex-direction:column;gap:2px;min-width:120px;}
    .cmp-k{font-size:12px;color:var(--muted);} .cmp-v{font-size:20px;font-weight:700;}
    .cmp-d{font-size:13px;font-weight:600;} .cmp-d.up{color:#16a34a;} .cmp-d.down{color:#dc2626;}
    .cmp-d.flat{color:var(--muted);} .cmp-d.new{color:#2563eb;}
    .cmp-note{font-size:12px;color:var(--muted);margin-top:8px;}
    .roi-card ul{margin:0;padding-left:18px;} .roi-card li{margin:3px 0;font-size:13px;}
    table{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px;}
    th,td{border:1px solid var(--table-border);padding:6px 8px;text-align:right;}
    th:first-child,td:first-child{text-align:left;}
    th{background:#f3f4f6;} .note{color:var(--muted);font-size:12px;margin-top:18px;}
    ul{margin:6px 0;}
    """

    caveat_block = ""
    if s.caveats:
        caveat_block = (
            '<h2>五、数据可信度提示</h2>'
            '<p style="color:var(--muted)">节省值基于你填写的基准估计，以下提示用于校验「提效」声称的可信度：</p>'
            f'<ul>{caveat_html}</ul>'
        )

    quality_block = _quality_guard_html(s)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>办公室提效报告</title>
<style>{css}</style></head><body>
<h1>办公室提效报告</h1>
<p style="color:var(--muted)">生成时间：{s.generated_at} ｜ 共 {s.n} 条任务记录</p>
<div class="cards">
  <div class="card"><div class="big">{format_number(s.saved_tok)}</div><div class="sub">节省 Token（基准 {format_number(s.total_base_tok)} → 本技能 {format_number(s.total_skill_tok)}，省 {s.token_save_pct:.1f}%）</div></div>
  <div class="card"><div class="big">{format_number(s.saved_min)} 分</div><div class="sub">节省时间（基准 {format_number(s.total_base_min)} → 本技能 {format_number(s.total_skill_min)}，省 {s.time_save_pct:.1f}%）</div></div>
  <div class="card" style="display:flex;align-items:center;justify-content:center;">{donut}</div>
</div>
{quality_block}
<h2>一、任务类型统计</h2>
<table><thead><tr><th>类型</th><th>任务数</th><th>基准 Token</th><th>本技能 Token</th><th>省 Token</th><th>省时间(分)</th><th>Token节省%</th><th>质量分</th></tr></thead>
<tbody>{type_rows}</tbody></table>

<h2>二、按周趋势</h2>
{trend_chart}
{compare_card}
<table><thead><tr><th>周</th><th>任务数</th><th>基准 Token</th><th>本技能 Token</th><th>省 Token</th></tr></thead>
<tbody>{week_rows}</tbody></table>
{roi_card}

<h2>三、任务执行情况</h2>
<table><thead><tr><th>日期</th><th>类型</th><th>基准(min)</th><th>技能(min)</th><th>省(min)</th><th>基准(tok)</th><th>技能(tok)</th><th>省(tok)</th><th>质量分</th></tr></thead>
<tbody>{task_rows}</tbody></table>

<h2>四、核心洞察与建议</h2>
<p><strong>洞察</strong></p><ul>{insight_html}</ul>
<p><strong>建议</strong></p><ul>{rec_html}</ul>
{skill_rec_html}
{caveat_block}
<p class="note">节省值为基于你填写的基准估计计算的参考值，用于建立提效体感，非平台计费数据。本报告全部本地生成，不含任何外部传输。</p>
</body></html>"""
    return html


# ─────────────────────────────────────────────────────────────
# JSON 报告
# ─────────────────────────────────────────────────────────────

def generate_json_report(s):
    out = s.to_dict()
    out.pop("tasks", None)
    return json.dumps(out, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────
# 一页摘要（对话式诊断首屏）
# 区别于九段完整报告：只给核心数字 + 提效主力 + 一句话结论 + 数据可信度 + 方法论，
# 作为「先出摘要 + 图表，再支持追问」流程的第一屏。
# ─────────────────────────────────────────────────────────────

def _credibility_block_md(s):
    if s.caveats:
        lines = ["## 数据可信度", "", "> 节省值基于你填写的基准估计，以下提示用于校验「提效」声称的可信度：", ""]
        for c in s.caveats:
            lines.append(f"- ⚠️ {c}")
        lines.append("")
        return "\n".join(lines)
    return "\n".join([
        "## 数据可信度", "",
        "- 基线为你的估计参照，非计费实测；当前未发现明显异常。", "",
    ])


def generate_markdown_summary(s):
    top = s.by_type[0] if s.by_type else None
    L = []
    L.append("# 办公室提效 · 一页摘要")
    L.append("")
    L.append(f"> 生成时间：{s.generated_at} ｜ 共 {s.n} 条任务记录")
    L.append("")
    L.append("## 核心数字")
    L.append("")
    L.append(f"- **节省 Token**：{format_number(s.saved_tok)}（基准 {format_number(s.total_base_tok)} → 本技能 {format_number(s.total_skill_tok)}），省 **{s.token_save_pct:.1f}%**")
    L.append(f"- **节省时间**：{format_number(s.saved_min)} 分（基准 {format_number(s.total_base_min)} → 本技能 {format_number(s.total_skill_min)}），省 **{s.time_save_pct:.1f}%**")
    L.append("")
    L.append("## 提效主力")
    L.append("")
    if top:
        L.append(f"- 「{top['task_type']}」：{top['count']} 次共省 {format_number(top['saved_tokens'])} Token（省 {top['token_save_pct']:.1f}%）")
    else:
        L.append("- 暂无任务类型数据")
    L.append("")
    L.append("## 一句话结论")
    L.append("")
    L.append(f"- {s.insights[0] if s.insights else '暂无数据。'}")
    L.append("")
    L.append(_credibility_block_md(s))
    L.append("")
    L.append(_quality_guard_md(s))

    # 推荐 Skill（本地静态规则，无联网）：集中渲染，含「未经实测验证」披露
    skill_recs = recommend_skills(s.by_type, s.n)
    if skill_recs:
        L.append(format_recommendations_md(skill_recs))

    L.append("---")
    L.append(f"*{s.methodology}*")
    L.append("")
    L.append("> 💡 可继续追问（如「哪个类型省最多」「按周趋势」「有啥建议」），或说「生成完整报告」查看完整明细。")
    return "\n".join(L)


def generate_html_summary(s):
    donut = build_donut_chart(s.by_type, title="各任务类型 节省 Token 占比",
                              center_label="节省 Token", value_key="saved_tokens")
    top = s.by_type[0] if s.by_type else None
    top_html = (f"「{_esc(top['task_type'])}」：{top['count']} 次共省 {format_number(top['saved_tokens'])} Token"
                f"（省 {top['token_save_pct']:.1f}%）") if top else "暂无任务类型数据"
    conclusion = _esc(s.insights[0]) if s.insights else "暂无数据。"
    trend_chart = build_trend_line_chart(s.by_week)
    compare_card = build_compare_card(s.period_compare)
    roi_card = build_roi_card(s.roi_targets)
    # Skill 推荐（本地静态规则，无联网）
    skill_recs = recommend_skills(s.by_type, s.n)
    skill_rec_html = format_recommendations_html(skill_recs)

    if s.caveats:
        cred_html = ('<p style="color:var(--muted)">节省值基于你填写的基准估计，以下提示用于校验「提效」声称的可信度：</p>'
                     '<ul>' + "".join(f"<li>⚠️ {_esc(c)}</li>" for c in s.caveats) + "</ul>")
    else:
        cred_html = '<p style="color:var(--muted)">基线为你的估计参照，非计费实测；当前未发现明显异常。</p>'

    cred_html += _quality_guard_html(s)

    css = """
    :root{--bg:#fff;--fg:#111827;--muted:#6b7280;--table-border:#e5e7eb;
          --accent:#22c55e;--accent-fg:#111827;}
    body{font-family:-apple-system,Segoe UI,Roboto,'Microsoft YaHei',sans-serif;
         max-width:720px;margin:24px auto;padding:0 16px;color:var(--fg);}
    h1{font-size:22px;} h2{font-size:17px;margin-top:24px;border-left:4px solid var(--accent);padding-left:8px;}
    .cards{display:flex;gap:16px;flex-wrap:wrap;margin:16px 0;}
    .card{flex:1;min-width:160px;background:#f9fafb;border:1px solid var(--table-border);
          border-radius:10px;padding:14px;}
    .card .big{font-size:24px;font-weight:700;} .card .sub{color:var(--muted);font-size:13px;}
    .chart-pie{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin:12px 0;}
    .legend{font-size:13px;} .legend-item{margin:2px 0;}
    .swatch{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;}
    .chart-line{margin:12px 0 4px;} .chart-title{font-size:14px;font-weight:600;margin-bottom:6px;}
    .cmp-card,.roi-card{background:#f9fafb;border:1px solid var(--table-border);border-radius:10px;
          padding:14px;margin:14px 0;}
    .cmp-title{font-size:14px;font-weight:600;margin-bottom:10px;}
    .cmp-grid{display:flex;gap:18px;flex-wrap:wrap;}
    .cmp-grid>div{display:flex;flex-direction:column;gap:2px;min-width:120px;}
    .cmp-k{font-size:12px;color:var(--muted);} .cmp-v{font-size:20px;font-weight:700;}
    .cmp-d{font-size:13px;font-weight:600;} .cmp-d.up{color:#16a34a;} .cmp-d.down{color:#dc2626;}
    .cmp-d.flat{color:var(--muted);} .cmp-d.new{color:#2563eb;}
    .cmp-note{font-size:12px;color:var(--muted);margin-top:8px;}
    .roi-card ul{margin:0;padding-left:18px;} .roi-card li{margin:3px 0;font-size:13px;}
    ul{margin:6px 0;} .note{color:var(--muted);font-size:12px;margin-top:18px;}
    """
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>办公室提效 · 一页摘要</title>
<style>{css}</style></head><body>
<h1>办公室提效 · 一页摘要</h1>
<p style="color:var(--muted)">生成时间：{s.generated_at} ｜ 共 {s.n} 条任务记录</p>
<div class="cards">
  <div class="card"><div class="big">{format_number(s.saved_tok)}</div><div class="sub">节省 Token（基准 {format_number(s.total_base_tok)} → 本技能 {format_number(s.total_skill_tok)}，省 {s.token_save_pct:.1f}%）</div></div>
  <div class="card"><div class="big">{format_number(s.saved_min)} 分</div><div class="sub">节省时间（基准 {format_number(s.total_base_min)} → 本技能 {format_number(s.total_skill_min)}，省 {s.time_save_pct:.1f}%）</div></div>
  <div class="card" style="display:flex;align-items:center;justify-content:center;">{donut}</div>
</div>
{trend_chart}
{compare_card}
{roi_card}
<h2>提效主力</h2><p>{top_html}</p>
<h2>一句话结论</h2><p>{conclusion}</p>
{skill_rec_html}
<h2>数据可信度</h2>{cred_html}
<p class="note">{s.methodology}</p>
</body></html>"""
    return html


# ─────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="办公室提效账本报告生成器（office-token-booster）")
    parser.add_argument("data_file", nargs="?", help="账本 JSON 路径（未提供则尝试读取当前目录 ledger.json；B 线仅支持用户上传/导出的数据文件）")
    parser.add_argument("--ledger", dest="data_file", help="账本 JSON 路径（同 data_file）")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    parser.add_argument("--format", type=str, default="markdown",
                        choices=["markdown", "html", "json"], help="输出格式")
    parser.add_argument("--summary", action="store_true",
                        help="输出一页摘要（对话式诊断首屏），而非完整报告")
    args = parser.parse_args()

    if not args.data_file:
        _default_ledger = Path("ledger.json")
        if _default_ledger.is_file():
            args.data_file = str(_default_ledger)
    if not args.data_file:
        print("[错误] B 线（office-token-booster）仅支持读取用户上传/导出的数据文件，"
              "不实时采集宿主用量。用法: python report_engine.py <ledger.json> [--format markdown|html|json]",
              file=sys.stderr)
        return 2

    try:
        tasks = load_ledger(args.data_file)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 2

    if not tasks:
        print("[提示] 账本为空，无可统计任务。", file=sys.stderr)
        return 1

    diag = diagnose(tasks)

    if args.summary:
        if args.format == "html":
            report = generate_html_summary(diag)
        else:
            report = generate_markdown_summary(diag)
    elif args.format == "markdown":
        report = generate_markdown_report(diag)
    elif args.format == "html":
        report = generate_html_report(diag)
    else:
        report = generate_json_report(diag)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"[OK] 报告已保存到 {args.output}", file=sys.stderr)
    else:
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
