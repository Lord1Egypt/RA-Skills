#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Life Money Skill — 报告渲染器

analysis.json（Contract 2，+ 可选 profile.json）→ report.html
单文件输出：CSS 内嵌、无 JS 依赖、离线可打开。

用法:
    python render_report.py <analysis.json> [--profile <profile.json>] [--out <report.html>]

退出码：0 = 成功；1 = 校验失败或渲染错误。
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSS_PATH = REPO_ROOT / "assets" / "templates" / "report.css"
PROMPTS_PATH = REPO_ROOT / "references" / "seven-prompts.md"

# ── tokens（与 references/report-design.md 同步；SVG 内联用） ──
INK = "#141413"
MUTED = "#6c6a64"
HAIRLINE = "#e6dfd8"
PRIMARY = "#cc785c"
ON_DARK = "#faf9f5"
ON_DARK_SOFT = "#a09d96"
TEAL = "#5db8a6"

CURRENCY_SYMBOL = {"CNY": "¥", "USD": "$", "EUR": "€", "HKD": "HK$", "JPY": "JP¥", "GBP": "£"}

REQUIRED_TOP = [
    "summary", "hidden_skills", "income_opportunities", "monetization_paths",
    "leverage", "higher_pay_roles", "ai_services", "plan_90d",
]


# ════════════════════════ 基础工具 ════════════════════════

def esc(x) -> str:
    return html.escape("" if x is None else str(x), quote=True)


def fmt_money(v, cur: str = "CNY") -> str:
    n = float(v)
    sym = CURRENCY_SYMBOL.get((cur or "CNY").upper(), "")
    if n >= 10000:
        s = f"{n / 10000:.4g}万"
    elif abs(n - round(n)) < 0.5:
        s = f"{int(round(n)):,}"
    else:
        s = f"{n:,.0f}"
    return f"{sym}{s}" if sym else f"{s} {cur}"


def money_span(lo, hi, cur="CNY") -> str:
    a = fmt_money(lo, cur)
    if hi and float(hi) != float(lo):
        return f"{a}–{fmt_money(hi, cur)}"
    return a


def fmt_date(s: str) -> str:
    if not s:
        return dt.date.today().isoformat()
    try:
        return dt.datetime.fromisoformat(str(s).replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        return str(s)


def spike_svg(size: int = 40, color: str = INK, cls: str = "spike") -> str:
    cx = cy = size / 2
    r1, r2 = size * 0.12, size * 0.48
    lines = []
    for i in range(8):
        a = math.pi * i / 4
        x1, y1 = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
        x2, y2 = cx + r2 * math.cos(a), cy + r2 * math.sin(a)
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>'
        )
    c = f' class="{cls}"' if cls else ""
    return (
        f'<svg{c} width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
        f'fill="none" aria-hidden="true">{"".join(lines)}</svg>'
    )


# ════════════════════════ 校验 ════════════════════════

def validate(analysis: dict, profile: dict | None):
    errs, warns = [], []

    for key in REQUIRED_TOP:
        v = analysis.get(key)
        if v in (None, [], {}):
            errs.append(f"缺少必填章节或为空：{key}")
    if errs:
        return errs, warns

    def count(key, lo, hi):
        n = len(analysis.get(key) or [])
        if not (lo <= n <= hi):
            errs.append(f"{key} 数量 {n} 不在 {lo}-{hi} 范围")

    count("hidden_skills", 5, 10)
    count("income_opportunities", 5, 10)
    count("monetization_paths", 3, 99)
    count("higher_pay_roles", 3, 99)
    count("ai_services", 3, 5)

    focuses = (analysis.get("leverage") or {}).get("focuses") or []
    if not (1 <= len(focuses) <= 3):
        errs.append(f"leverage.focuses 数量 {len(focuses)} 不在 1-3")

    phases = (analysis.get("plan_90d") or {}).get("phases") or []
    if len(phases) != 3:
        errs.append(f"plan_90d.phases 数量 {len(phases)}，应为 3")

    hl = (analysis.get("summary") or {}).get("highlights") or []
    if not (3 <= len(hl) <= 6):
        warns.append(f"summary.highlights 数量 {len(hl)}，建议 3-6")

    launch = None
    if profile:
        launch = (profile.get("time_budget") or {}).get("launch_hours_per_week")
    if launch:
        for s in analysis.get("ai_services") or []:
            h = s.get("weekly_hours")
            if isinstance(h, (int, float)) and h > launch:
                errs.append(f"ai_services「{s.get('name')}」weekly_hours={h:g} 超过门禁值 {launch:g}")
    else:
        warns.append("profile 未提供 launch_hours_per_week（门禁 3）——时间预算图不画上限线")

    rated = [o for o in analysis.get("income_opportunities") or []
             if isinstance(o.get("potential_level"), int)]
    if len(rated) < 4:
        warns.append(f"带 potential_level 的收入机会仅 {len(rated)} 条（<4）——机会矩阵图将省略")

    payed = [r for r in analysis.get("higher_pay_roles") or []
             if r.get("pay_monthly_low") and r.get("pay_monthly_high")]
    if not payed:
        warns.append("higher_pay_roles 无薪酬数字——薪酬阶梯图将省略")

    return errs, warns


# ════════════════════════ 组件 ════════════════════════

def sec_head(num: str, title: str, lead: str = "") -> str:
    lead_html = f'<p class="sec-head__lead">{esc(lead)}</p>' if lead else ""
    head_num = f'<div class="sec-head__num">{esc(num)}</div>' if num else ""
    return f'<header class="sec-head">{head_num}<h2>{esc(title)}</h2>{lead_html}</header>'


def band(inner: str, kind: str = "canvas") -> str:
    cls = {"canvas": "band", "soft": "band band--soft", "dark": "band band--dark"}[kind]
    return f'<div class="{cls}"><div class="band__inner"><section class="block">{inner}</section></div></div>'


def dot_for(level: str) -> str:
    cls = {"低": "low", "中": "mid", "高": "high"}.get(level, "mid")
    return f'<span class="dot dot--{cls}"></span>'


def skill_card(s: dict) -> str:
    parts = [f'<div class="skill__name">{esc(s.get("name"))}</div>']
    for label, key in (("价值", "why_valuable"), ("谁付费", "who_pays"), ("AI 货币化", "ai_monetization")):
        if s.get(key):
            parts.append(f'<div class="skill__row"><b>{label}</b>{esc(s[key])}</div>')
    if s.get("evidence"):
        parts.append(f'<div class="skill__ev">依据：{esc(s["evidence"])}</div>')
    return f'<div class="card skill">{"".join(parts)}</div>'


def opp_card(i: int, o: dict) -> str:
    d = o.get("difficulty") or "中"
    attrs = [
        ("启动成本", esc(o.get("startup_cost"))),
        ("时间投入", esc(o.get("time_investment"))),
        ("难度", dot_for(d) + esc(d)),
        ("收入潜力", esc(o.get("income_potential"))),
    ]
    attr_html = "".join(
        f'<div class="attr"><span class="attr__k">{k}</span><span class="attr__v">{v}</span></div>'
        for k, v in attrs
    )
    step = ""
    if o.get("first_step"):
        step = f'<div class="opp__step"><b>第一步</b>{esc(o["first_step"])}</div>'
    return (
        f'<article class="card opp"><div class="opp__head"><h3 class="opp__title">{esc(o.get("title"))}</h3>'
        f'<span class="opp__no">{i:02d}</span></div>'
        f'<p class="opp__desc">{esc(o.get("description"))}</p>'
        f'<div class="opp__attrs">{attr_html}</div>{step}</article>'
    )


def path_card(p: dict) -> str:
    metas = []
    if p.get("target_customer"):
        metas.append(f'<b>目标客户</b> {esc(p["target_customer"])}')
    if p.get("pricing_hint"):
        metas.append(f'<b>定价参考</b> {esc(p["pricing_hint"])}')
    meta_html = f'<p class="path__meta">{" ｜ ".join(metas)}</p>' if metas else ""
    return (
        f'<div class="card"><div class="path__name">{esc(p.get("name"))}</div>'
        f'<p class="path__desc">{esc(p.get("description"))}</p>{meta_html}</div>'
    )


def leverage_block(lv: dict) -> str:
    fs = sorted(lv.get("focuses") or [], key=lambda x: x.get("rank") or 9)
    if not fs:
        return ""
    main = fs[0]
    main_html = (
        f'<div class="lev-main"><div class="lev-main__k">最高优先级 · 如果只做一件事</div>'
        f'<h3>{esc(main.get("focus"))}</h3><p>{esc(main.get("rationale"))}</p></div>'
    )
    rest = fs[1:]
    if not rest:
        return main_html
    subs = "".join(
        f'<div class="card"><div class="lev-sub__rank">优先 #{esc(r.get("rank"))}</div>'
        f'<h4>{esc(r.get("focus"))}</h4><p>{esc(r.get("rationale"))}</p></div>'
        for r in rest
    )
    return main_html + f'<div class="lev-sub">{subs}</div>'


def svc_card(s: dict) -> str:
    h = s.get("weekly_hours")
    h_html = f'<span class="pill">{h:g} 小时 / 周</span>' if isinstance(h, (int, float)) else ""
    price = (
        f'<p class="svc__price"><b>定价参考</b>　{esc(s["price_hint"])}</p>'
        if s.get("price_hint") else ""
    )
    return (
        f'<div class="card"><div class="svc__head"><div class="svc__name">{esc(s.get("name"))}</div>{h_html}</div>'
        f'<p class="svc__desc">{esc(s.get("description"))}</p>{price}</div>'
    )


def timeline_html(plan: dict) -> str:
    cols = []
    for i, p in enumerate(plan.get("phases") or []):
        acts = "".join(f'<li>{esc(a)}</li>' for a in (p.get("actions") or []))
        first = " tl--first" if i == 0 else ""
        cols.append(
            f'<div class="tl{first}"><span class="tl__dot"></span>'
            f'<div class="tl__name">{esc(p.get("name"))}</div>'
            f'<p class="tl__focus">{esc(p.get("focus"))}</p>'
            f'<ul class="tl__acts">{acts}</ul>'
            f'<span class="pill pill--coral tl__ms">里程碑 · {esc(p.get("milestone"))}</span></div>'
        )
    return f'<div class="timeline">{"".join(cols)}</div>'


def prompts_html(prompts) -> str:
    cards = "".join(
        f'<div class="prompt"><div class="prompt__hd"><span class="prompt__no">PROMPT {n:02d}</span>'
        f'<span class="prompt__t">{esc(title)}</span></div>'
        f'<p class="prompt__q">“{esc(q)}”</p></div>'
        for n, title, q in prompts
    )
    return cards


# ════════════════════════ SVG 图表 ════════════════════════

def svg_matrix(opps):
    rated = [(i + 1, o) for i, o in enumerate(opps)
             if isinstance(o.get("potential_level"), int) and o.get("difficulty") in ("低", "中", "高")]
    if len(rated) < 4:
        return None, None

    W, H = 1000, 420
    L, R, T, B = 96, 40, 30, 56
    x0, x1 = L, W - R
    colw = (x1 - x0) / 3
    step_y = (H - T - B) / 4
    cols = {"低": 0, "中": 1, "高": 2}

    def pos(d, lv):
        return x0 + colw * (cols[d] + 0.5), T + (5 - lv) * step_y

    parts = []
    for lv in range(1, 6):
        y = T + (5 - lv) * step_y
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{HAIRLINE}" stroke-width="1"/>')
        parts.append(f'<text x="{x0 - 16}" y="{y + 4.5:.1f}" text-anchor="end" font-size="13" fill="{MUTED}">{lv}</text>')
    parts.append(f'<text x="{x0 - 16}" y="{T - 12}" text-anchor="end" font-size="12" fill="{MUTED}">潜力量级</text>')
    for ci, d in enumerate(("低", "中", "高")):
        cx = x0 + colw * (ci + 0.5)
        parts.append(f'<text x="{cx:.1f}" y="{H - 22}" text-anchor="middle" font-size="14" fill="{MUTED}">{d}难度</text>')

    cells = defaultdict(list)
    for n, o in rated:
        cells[(o["difficulty"], o["potential_level"])].append((n, o))
    offs = [(0, 0), (34, 0), (-34, 0), (0, 30), (0, -30), (34, 30), (-34, -30), (34, -30), (-34, 30), (0, 58)]
    for (d, lv), items in cells.items():
        bx, by = pos(d, lv)
        for k, (n, o) in enumerate(items):
            ox, oy = offs[k % len(offs)]
            cx, cy = bx + ox, by + oy
            quickwin = (d == "低" and lv >= 4)
            fill = PRIMARY if quickwin else INK
            parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="15" fill="{fill}"/>')
            parts.append(
                f'<text x="{cx:.1f}" y="{cy + 4.5:.1f}" text-anchor="middle" font-size="13" '
                f'fill="#ffffff" font-weight="600">{n}</text>'
            )
    svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="收入机会矩阵">{"".join(parts)}</svg>'

    leg = []
    for n, o in rated:
        lv = o["potential_level"]
        stars = "★" * lv + "☆" * (5 - lv)
        quick = " quick" if (o["difficulty"] == "低" and lv >= 4) else ""
        leg.append(
            f'<span class="mleg__i{quick}"><b>{n:02d}</b>{esc(o.get("title"))}'
            f'<em>ㅤ{esc(o["difficulty"])}难度 · {stars}</em></span>'
        )
    legend = f'<div class="mleg">{"".join(leg)}</div>'
    return svg, legend


def nice_bounds(lo, hi):
    span = hi - lo
    step = 5000
    if span > 40000:
        step = 10000
    if span > 90000:
        step = 20000
    lo_r = int(math.floor((lo - step * 0.2) / step) * step)
    hi_r = int(math.ceil((hi + step * 0.2) / step) * step)
    ticks = list(range(lo_r, hi_r + step, step))
    return lo_r, hi_r, ticks


def svg_salary(roles, current, cur="CNY"):
    rows = [(r.get("role_or_industry") or "", float(r["pay_monthly_low"]), float(r["pay_monthly_high"]))
            for r in roles if r.get("pay_monthly_low") and r.get("pay_monthly_high")]
    if not rows:
        return None
    vals = [v for _, lo, hi in rows for v in (lo, hi)]
    if current:
        vals.append(float(current))
    lo_r, hi_r, ticks = nice_bounds(min(vals), max(vals))

    W = 1000
    Lbl, X0, X1 = 236, 236, 912
    T, row_h = 52, 64
    H = T + row_h * len(rows) + 40

    def X(v):
        return X0 + (v - lo_r) / (hi_r - lo_r) * (X1 - X0)

    parts = []
    for tv in ticks:
        x = X(tv)
        parts.append(f'<line x1="{x:.1f}" y1="{T - 18}" x2="{x:.1f}" y2="{H - 36}" stroke="{HAIRLINE}" stroke-width="1"/>')
        parts.append(f'<text x="{x:.1f}" y="{H - 14}" text-anchor="middle" font-size="12" fill="{MUTED}">{fmt_money(tv, cur)}</text>')
    for i, (name, lo, hi) in enumerate(rows):
        y = T + i * row_h
        nm = name if len(name) <= 15 else name[:14] + "…"
        parts.append(f'<text x="{Lbl - 18}" y="{y + 17:.1f}" text-anchor="end" font-size="14" fill="{INK}">{esc(nm)}</text>')
        parts.append(f'<rect x="{X(lo):.1f}" y="{y:.1f}" width="{max(X(hi) - X(lo), 6):.1f}" height="24" rx="6" fill="{INK}" opacity="0.86"/>')
        parts.append(f'<text x="{X(hi) + 10:.1f}" y="{y + 17:.1f}" font-size="12.5" fill="{MUTED}">{fmt_money(lo, cur)}–{fmt_money(hi, cur)}</text>')
    if current:
        x = X(float(current))
        parts.append(f'<line x1="{x:.1f}" y1="{T - 30}" x2="{x:.1f}" y2="{H - 36}" stroke="{PRIMARY}" stroke-width="1.6" stroke-dasharray="5 5"/>')
        parts.append(f'<text x="{min(max(x, 90), W - 90):.1f}" y="{T - 38}" text-anchor="middle" font-size="12.5" fill="{PRIMARY}">你当前 {fmt_money(current, cur)}</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="薪酬阶梯">{"".join(parts)}</svg>'


def svg_budget(services, limit):
    rows = [(s.get("name") or "", float(s["weekly_hours"])) for s in services
            if isinstance(s.get("weekly_hours"), (int, float))]
    if not rows:
        return None
    vmax = max([h for _, h in rows] + ([float(limit)] if limit else [])) * 1.15
    W = 1000
    Lbl, X0, X1 = 316, 316, 880
    T, row_h = 40, 46
    H = T + row_h * len(rows) + 36

    def X(v):
        return X0 + (v / vmax) * (X1 - X0)

    parts = []
    for i, (name, h) in enumerate(rows):
        y = T + i * row_h
        nm = name if len(name) <= 17 else name[:16] + "…"
        parts.append(f'<text x="{Lbl - 18}" y="{y + 17:.1f}" text-anchor="end" font-size="14" fill="{INK}">{esc(nm)}</text>')
        parts.append(f'<rect x="{X0}" y="{y + 2:.1f}" width="{max(X(h) - X0, 4):.1f}" height="20" rx="6" fill="{INK}" opacity="0.86"/>')
        parts.append(f'<text x="{X(h) + 10:.1f}" y="{y + 17:.1f}" font-size="12.5" fill="{MUTED}">{h:g} 小时 / 周</text>')
    if limit:
        x = X(float(limit))
        parts.append(f'<line x1="{x:.1f}" y1="{T - 22}" x2="{x:.1f}" y2="{H - 30}" stroke="{PRIMARY}" stroke-width="1.6" stroke-dasharray="5 5"/>')
        parts.append(f'<text x="{min(max(x, 80), W - 80):.1f}" y="{T - 30}" text-anchor="middle" font-size="12.5" fill="{PRIMARY}">每周可投入 {float(limit):g}h</text>')
    return f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="启动时间预算">{"".join(parts)}</svg>'


# ════════════════════════ 提示词加载（canonical 单一真源） ════════════════════════

def load_prompts():
    text = PROMPTS_PATH.read_text(encoding="utf-8")
    out = []
    for blk in re.split(r"\n## ", text):
        m = re.match(r"(\d)\.\s+([^\n]+)", blk)
        if not m:
            continue
        num = int(m.group(1))
        if num < 1 or num > 7:
            continue
        q = re.search(r'^>\s*"(.+?)"\s*$', blk, flags=re.M)
        if not q:
            continue
        out.append((num, m.group(2).strip(), q.group(1).strip()))
    out.sort()
    return out if len(out) == 7 else None


# ════════════════════════ 组装 ════════════════════════

def build_html(analysis: dict, profile: dict, css: str, prompts) -> tuple[str, dict]:
    profile = profile or {}
    summary = analysis.get("summary") or {}
    meta = analysis.get("meta") or {}
    identity = profile.get("identity") or {}
    name = identity.get("name") or "你"
    role = identity.get("current_role") or ""
    city = identity.get("city") or ""
    date = fmt_date(meta.get("generated_at"))
    cur = (profile.get("salary") or {}).get("currency") or "CNY"

    stats = {"matrix": False, "salary": False, "budget": False}

    # ── 封面 ──
    target_html = ""
    it = (profile.get("goals") or {}).get("income_target")
    if it and it.get("min_amount"):
        period = "月" if (it.get("period") or "monthly") == "monthly" else "年"
        target_html = (
            f'<span class="pill pill--coral">目标 {money_span(it["min_amount"], it.get("max_amount"), it.get("currency") or cur)} / {period}</span>'
        )
    sub_bits = [name] + ([role] if role else []) + ([city] if city else [])
    cover = (
        f'<div class="band"><div class="band__inner"><header class="cover">{spike_svg()}'
        f'<div class="cover__eyebrow">LIFE MONEY REPORT · 职业变现诊断</div>'
        f'<h1>人生搞钱诊断报告</h1>'
        f'<p class="cover__sub">{esc(" · ".join(sub_bits))}</p>'
        f'<div class="cover__rule"></div>'
        f'<div class="cover__meta"><span>{esc(date)}</span>{target_html}'
        f'<span>基于 7 轮职业变现分析生成</span></div>'
        f'</header></div></div>'
    )

    # ── 01 摘要 ──
    hl_items = "".join(
        f'<div class="hl__item"><div class="hl__no">{i:02d}</div><p class="hl__t">{esc(h)}</p></div>'
        for i, h in enumerate(summary.get("highlights") or [], 1)
    )
    note_html = ""
    if summary.get("assumptions"):
        joined = "；".join(esc(a) for a in summary["assumptions"])
        note_html = f'<div class="note"><b>分析假设</b> · {joined}</div>'
    sec_summary = band(
        f'{sec_head("摘要", "关键发现", "跨维度提炼的要点，细节见后文各章。")}'
        f'<div class="hl">{hl_items}</div>{note_html}'
    )

    # ── 02 隐藏技能 ──
    skills = analysis.get("hidden_skills") or []
    sec_skills = band(
        f'{sec_head("01 / 07", "隐藏技能", f"你可能低估、但市场会为之付费的能力——共 {len(skills)} 项。")}'
        f'<div class="grid-2">{"".join(skill_card(s) for s in skills)}</div>',
        "soft",
    )

    # ── 03 收入机会 ──
    opps = analysis.get("income_opportunities") or []
    matrix_svg, matrix_leg = svg_matrix(opps)
    chart_html = ""
    if matrix_svg:
        stats["matrix"] = True
        chart_html = (
            f'<div class="chart">{matrix_svg}'
            f'<p class="chart__cap">横轴：启动难度 · 纵轴：收入潜力量级（1-5，相对你的目标区间）· 珊瑚色标记建议优先启动的低难度高潜力机会</p></div>'
            f'{matrix_leg}'
        )
    target_txt = ""
    if it and it.get("min_amount"):
        target_txt = f'（{money_span(it["min_amount"], it.get("max_amount"), it.get("currency") or cur)} / 月）'
    sec_opps = band(
        f'{sec_head("02 / 07", "收入机会", f"对齐你确认的目标{target_txt}筛选出的现实路径。")}'
        f'{chart_html}<div class="opps">{"".join(opp_card(i, o) for i, o in enumerate(opps, 1))}</div>'
    )

    # ── 04 变现路径 ──
    paths = analysis.get("monetization_paths") or []
    groups = defaultdict(list)
    for p in paths:
        groups[p.get("type") or "其他"].append(p)
    order = ["服务", "咨询产品", "数字产品", "自由职业"]
    ghtml = ""
    for t in order + [k for k in groups if k not in order]:
        items = groups.get(t)
        if not items:
            continue
        cards = "".join(path_card(p) for p in items)
        ghtml += f'<div class="paths__group"><h3>{esc(t)}<span>{len(items)} 项</span></h3><div class="path-row">{cards}</div></div>'
    sec_paths = band(
        f'{sec_head("03 / 07", "变现路径", "把你当作一家「一人企业」来盘点——可打包成服务、产品与自由职业的机会。")}'
        f'<div class="paths">{ghtml}</div>',
        "soft",
    )

    # ── 05 最大杠杆 ──
    sec_leverage = band(
        f'{sec_head("04 / 07", "最大杠杆机会", "如果时间有限，按此优先级行动。")}'
        f'{leverage_block(analysis.get("leverage") or {})}'
    )

    # ── 06 高薪方向 ──
    roles = analysis.get("higher_pay_roles") or []
    current_amount = None
    sal = profile.get("salary") or {}
    if sal.get("current_amount"):
        current_amount = float(sal["current_amount"])
        if sal.get("period") == "annual":
            current_amount = current_amount / 12.0
    sal_svg = svg_salary(roles, current_amount, cur)
    sal_chart = ""
    if sal_svg:
        stats["salary"] = True
        sal_chart = (
            f'<div class="chart">{sal_svg}'
            f'<p class="chart__cap">色条为该方向的月薪参考区间（估算）；虚线为你的当前月薪。数据口径见附录 B。</p></div>'
        )
    role_rows = ""
    for r in roles:
        pay_pill = ""
        if r.get("pay_monthly_low") and r.get("pay_monthly_high"):
            pay_pill = f'<span class="pill pill--outline">{fmt_money(r["pay_monthly_low"], cur)}–{fmt_money(r["pay_monthly_high"], cur)} / 月</span>'
        elif r.get("pay_gap"):
            pay_pill = f'<span class="pill pill--outline">{esc(r["pay_gap"])}</span>'
        qual = f'<p class="role__qual"><b>为什么是你</b>{esc(r.get("qualification"))}</p>' if r.get("qualification") else ""
        role_rows += (
            f'<div class="role"><div class="role__l"><h3>{esc(r.get("role_or_industry"))}</h3>{pay_pill}</div>'
            f'<div class="role__r"><p class="role__why">{esc(r.get("why_higher_pay"))}</p>{qual}</div></div>'
        )
    sec_roles = band(
        f'{sec_head("05 / 07", "什么薪水更高", "你的能力在人才市场的定价不止于此。")}'
        f'{sal_chart}<div class="roles">{role_rows}</div>',
        "soft",
    )

    # ── 07 AI 副业 ──
    svcs = analysis.get("ai_services") or []
    launch = (profile.get("time_budget") or {}).get("launch_hours_per_week")
    bud_svg = svg_budget(svcs, launch)
    bud_chart = ""
    if bud_svg:
        stats["budget"] = True
        bud_chart = (
            f'<div class="chart">{bud_svg}'
            f'<p class="chart__cap">色条为启动该服务预计投入的每周小时数；虚线为你确认的每周可投入时间。</p></div>'
        )
    lead = f"用 AI 放大交付效率的方案——全部控制在你每周 {launch:g} 小时的预算内。" if launch else "用 AI 放大交付效率的方案。"
    sec_services = band(
        f'{sec_head("06 / 07", "AI 副业服务", lead)}'
        f'{bud_chart}<div class="svc">{"".join(svc_card(s) for s in svcs)}</div>'
    )

    # ── 08 90 天计划 ──
    plan = analysis.get("plan_90d") or {}
    goal = plan.get("goal_statement") or ""
    goal_html = f'<p class="note"><b>90 天目标</b> · {esc(goal)}</p>' if goal else ""
    sec_plan = band(
        f'{sec_head("07 / 07", "90 天计划", "分阶段行动与验收里程碑。")}'
        f'{goal_html}<div style="height:24px"></div>{timeline_html(plan)}',
        "soft",
    )

    # ── 附录 A ──
    sec_appendix_a = band(
        f'{sec_head("附录 A", "原始提示词（来源 @Raul_IA_Prod）", "本报告方法论使用的全部原始指令，可复制到任意 AI 助手中复用。")}'
        f'<div class="prompts">{prompts_html(prompts)}'
        f'<p class="prompts__cap">以上为 canonical 原文，未做改写。</p></div>',
        "dark",
    )

    # ── 附录 B ──
    sources = (meta.get("calibration") or {}).get("sources") or []
    src_html = ""
    if sources:
        items = "".join(
            f'<li><b>{esc(s.get("label"))}</b>{("，" + esc(s.get("note"))) if s.get("note") else ""}'
            f'{("（" + esc(s.get("url")) + "）") if s.get("url") else ""}</li>'
            for s in sources
        )
        src_html = f'<p class="path__desc" style="margin-bottom:8px">本报告的估算参考来源：</p><ul class="sources">{items}</ul>'
    cal_note = "（来源见上）" if sources else "（本次未做市场校准）"
    disc = (
        f'<p class="disc">本报告由 AI 基于你提供的个人档案与职业经历生成，仅供个人参考，'
        f'不构成职业、投资或法律建议。「收入潜力」「薪酬参考」等均为估算口径{cal_note}，不构成任何收入承诺。'
        f'生成时间：{esc(date)}。</p>'
    )
    sec_appendix_b = band(
        f'{sec_head("附录 B", "数据来源与免责声明")}{src_html}{disc}'
    )

    # ── 页脚 ──
    footer = (
        f'<div class="footer"><div class="footer__inner">'
        f'<div class="footer__brand">{spike_svg(18, ON_DARK, "")} <span>人生搞钱 · Life Money Skill</span></div>'
        f'<div class="sep"></div>'
        f'<p>7 轮职业变现诊断 · 生成于 {esc(date)} · 报告为个人决策参考，请结合自身实际情况判断。</p>'
        f'</div></div>'
    )

    doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>人生搞钱诊断报告 · {esc(name)}</title>
<style>
{css}
</style>
</head>
<body>
{cover}
{sec_summary}
{sec_skills}
{sec_opps}
{sec_paths}
{sec_leverage}
{sec_roles}
{sec_services}
{sec_plan}
{sec_appendix_a}
{sec_appendix_b}
{footer}
</body>
</html>
"""
    return doc, stats


def main(argv=None):
    ap = argparse.ArgumentParser(description="Life Money Skill 报告渲染器")
    ap.add_argument("analysis", help="analysis.json 路径")
    ap.add_argument("--profile", help="profile.json 路径（可选：目标 / 薪资 / 门禁值）")
    ap.add_argument("--out", help="输出 report.html 路径（默认与 analysis 同目录）")
    args = ap.parse_args(argv)

    apath = Path(args.analysis)
    if not apath.exists():
        print(f"✗ 找不到文件：{apath}")
        return 1
    analysis = json.loads(apath.read_text(encoding="utf-8"))

    profile = None
    if args.profile:
        ppath = Path(args.profile)
        if not ppath.exists():
            print(f"✗ 找不到文件：{ppath}")
            return 1
        profile = json.loads(ppath.read_text(encoding="utf-8"))

    errs, warns = validate(analysis, profile)
    for w in warns:
        print(f"⚠ {w}")
    if errs:
        print("✗ 校验未通过：")
        for e in errs:
            print(f"  - {e}")
        return 1

    if not CSS_PATH.exists():
        print(f"✗ 缺少样式文件：{CSS_PATH}")
        return 1
    css = CSS_PATH.read_text(encoding="utf-8")

    prompts = load_prompts()
    if not prompts:
        print(f"✗ 解析 {PROMPTS_PATH} 失败：未取到 7 条提示词")
        return 1

    doc, stats = build_html(analysis, profile or {}, css, prompts)
    out = Path(args.out) if args.out else apath.with_name("report.html")
    out.write_text(doc, encoding="utf-8")

    kb = out.stat().st_size / 1024
    charts = "、".join(
        name for name, on in (("机会矩阵", stats["matrix"]), ("薪酬阶梯", stats["salary"]), ("时间预算", stats["budget"])) if on
    ) or "无"
    print(f"✔ 已生成 {out}（{kb:.1f} KB）")
    print(f"  结构：封面 + 摘要 + 7 章 + 附录 A/B；提示词 {len(prompts)} 条；图表：{charts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
