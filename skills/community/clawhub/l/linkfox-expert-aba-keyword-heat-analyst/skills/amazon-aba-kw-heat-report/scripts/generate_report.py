#!/usr/bin/env python3
"""amazon-aba-kw-heat-report — generate HTML/JSON dashboard for keyword heat analysis.

Usage:
  # from keyword list (will call amazon-aba-kw-heat / L3 ABA)
  python generate_report.py '{"keywords":["yoga mat","exercise mat"],"region":"US","weeks":104}'

  # from existing ABA / shell_a JSON response
  python generate_report.py --input /path/to/aba_result.json --out-dir ./out

  # help
  python generate_report.py --help

Requires LINKFOXAGENT_API_KEY when fetching live data.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import secrets
import statistics
import subprocess
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


def _resolve_session_dir() -> Path:
    """Resolve session output directory: <cwd>/linkfox/<YYYY-MM-DD>/<session>/reports/"""
    acpx = os.environ.get("ACPX_WORKSPACES", "").strip()
    candidates = []
    if acpx:
        candidates.append(Path(acpx) / "linkfox")
    candidates.append(Path.cwd() / "linkfox")
    candidates.append(Path.home() / "linkfox")
    root = candidates[0]
    for c in candidates:
        try:
            c.mkdir(parents=True, exist_ok=True)
            (c / ".write_probe").write_text("")
            (c / ".write_probe").unlink()
            root = c
            break
        except OSError:
            continue
    today = datetime.now().strftime("%Y-%m-%d")
    sid = (os.environ.get("SESSION_ID") or "").strip()
    if not sid:
        sid = datetime.now().strftime("%H%M%S") + "-" + secrets.token_hex(3)
    session_dir = root / today / sid / "reports"
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir

SKILL_DIR = Path(__file__).resolve().parents[1]
REFERENCES = SKILL_DIR / "references"
DEFAULT_LAYOUT = REFERENCES / "layout.json"

PALETTE = [
    "#ff6b2c",
    "#7dc4ff",
    "#3dd68c",
    "#f0c14a",
    "#c792ea",
    "#f07178",
    "#89ddff",
]


def find_heat_shell() -> Path | None:
    candidates = [
        SKILL_DIR.parent / "amazon-aba-kw-heat/scripts/shell_a.py",
        Path("/root/.linkfox/workspaces/.claude/skills/amazon-aba-kw-heat/scripts/shell_a.py"),
        Path.home() / ".hermes/skills/amazon-aba-kw-heat/scripts/shell_a.py",
        Path("/root/.hermes/skills/amazon-aba-kw-heat/scripts/shell_a.py"),
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


def slope_label(sfrs):
    if len(sfrs) < 4:
        return "数据不足", None
    mid = len(sfrs) // 2
    a = statistics.mean(sfrs[:mid])
    b = statistics.mean(sfrs[mid:])
    if a <= 0:
        return "数据不足", None
    chg = (b - a) / a
    if chg <= -0.15:
        lab = "明显升温"
    elif chg <= -0.05:
        lab = "升温"
    elif chg < 0.05:
        lab = "平稳"
    elif chg < 0.15:
        lab = "掉热"
    else:
        lab = "明显掉热"
    return lab, round(chg * 100, 1)


def corr_consistency(a, b):
    n = min(len(a), len(b))
    if n < 5:
        return "数据不足", None
    a, b = a[:n], b[:n]
    ma, mb = statistics.mean(a), statistics.mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    da = math.sqrt(sum((x - ma) ** 2 for x in a))
    db = math.sqrt(sum((y - mb) ** 2 for y in b))
    if da == 0 or db == 0:
        return "无法判断", None
    r = num / (da * db)
    if r >= 0.7:
        lab = "高一致"
    elif r >= 0.4:
        lab = "较一致"
    elif r >= 0.15:
        lab = "弱一致"
    elif r >= -0.15:
        lab = "不一致"
    else:
        lab = "反向"
    return lab, round(r, 2)


def week_num_in_year(dt: datetime) -> int:
    return dt.isocalendar()[1]


def tier_of(sfr: int | None) -> str:
    if sfr is None:
        return "unknown"
    if sfr < 50000:
        return "hot"
    if sfr < 200000:
        return "mid"
    return "tail"


def fetch_aba(keywords: list[str], region: str = "US", weeks: int = 104) -> dict:
    shell = find_heat_shell()
    params = {
        "region": region,
        "keywords": keywords,
        "weeks": weeks,
        "top_k_asin": 0,
    }
    if shell:
        proc = subprocess.run(
            [sys.executable, str(shell), json.dumps(params, ensure_ascii=False)],
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            timeout=180,
        )
        if proc.returncode != 0:
            raise RuntimeError(
                f"heat shell failed rc={proc.returncode}: {proc.stderr or proc.stdout}"
            )
        return json.loads(proc.stdout)

    # fallback: local aba_common from heat skill sibling
    sys.path.insert(0, str((shell.parent if shell else Path("."))))
    # direct L3 via common if vendored next to us
    common = SKILL_DIR / "scripts" / "aba_common.py"
    if not common.exists():
        heat_common = Path.home() / ".hermes/skills/amazon-aba-kw-heat/scripts/aba_common.py"
        if heat_common.exists():
            sys.path.insert(0, str(heat_common.parent))
            from aba_common import run_shell  # type: ignore

            return run_shell("A", params)
        raise RuntimeError(
            "amazon-aba-kw-heat not installed; provide --input ABA JSON or install the heat skill"
        )
    return {}


def rows_from_aba(raw: dict) -> list[dict]:
    tables = raw.get("tables") or []
    if not tables:
        return []
    return tables[0].get("data") or []


def build_series(rows: list[dict], keywords: list[str] | None):
    series = defaultdict(list)
    for r in rows:
        rl = {str(k).lower(): v for k, v in r.items()}
        kw = rl.get("searchterm") or rl.get("search_term")
        d = rl.get("reportstartdate") or rl.get("report_start_date")
        sfr = rl.get("searchfrequencyrank") or rl.get("search_frequency_rank")
        if not kw or not d or sfr is None:
            continue
        try:
            sfr = int(float(sfr))
        except Exception:
            continue
        dt = datetime.strptime(str(d)[:10], "%Y-%m-%d")
        series[kw].append((dt, sfr))

    for kw, pts in list(series.items()):
        by_day = {}
        for dt, sfr in pts:
            day = dt.strftime("%Y-%m-%d")
            if day not in by_day or sfr < by_day[day][1]:
                by_day[day] = (dt, sfr)
        series[kw] = sorted(by_day.values(), key=lambda x: x[0])

    if keywords:
        # preserve user order; append extras
        ordered = list(keywords)
        for k in series:
            if k not in ordered:
                ordered.append(k)
    else:
        ordered = sorted(series.keys(), key=lambda k: (series[k][-1][1] if series[k] else 10**12))
    return series, ordered


def compute_payload(raw: dict, keywords: list[str] | None, region: str = "US") -> dict:
    rows = rows_from_aba(raw)
    series, ordered = build_series(rows, keywords)
    if not series:
        raise RuntimeError("no SFR series in ABA response")

    all_dates = [dt for kw in series for dt, _ in series[kw]]
    max_dt = max(all_dates)
    this_year = max_dt.year
    last_year = this_year - 1

    metrics = []
    chart_series = []
    yoy_pairs = []

    for i, kw in enumerate(ordered):
        pts = series.get(kw) or []
        if not pts:
            continue
        ly = [(dt, s) for dt, s in pts if dt.year == last_year]
        ty = [(dt, s) for dt, s in pts if dt.year == this_year]
        ly_sfr = [s for _, s in sorted(ly)]
        ty_sfr = [s for _, s in sorted(ty)]
        ly_by_w = {week_num_in_year(dt): (dt, s) for dt, s in ly}
        ty_by_w = {week_num_in_year(dt): (dt, s) for dt, s in ty}
        common = sorted(set(ly_by_w) & set(ty_by_w))

        ly_lab, ly_chg = slope_label(ly_sfr) if ly_sfr else ("无数据", None)
        ty_lab, ty_chg = slope_label(ty_sfr) if ty_sfr else ("无数据", None)
        a = [ly_by_w[w][1] for w in common]
        b = [ty_by_w[w][1] for w in common]
        cons_lab, cons_r = corr_consistency(a, b) if common else ("数据不足", None)

        def peak(pts_year):
            if not pts_year:
                return None, None
            dt, s = min(pts_year, key=lambda x: x[1])
            return f"{dt.isocalendar()[1]:02d}周({dt.strftime('%m-%d')})", dt

        ly_peak, ly_peak_dt = peak(ly)
        ty_peak, ty_peak_dt = peak(ty)
        peak_offset = None
        if ly_peak_dt and ty_peak_dt:
            peak_offset = ty_peak_dt.isocalendar()[1] - ly_peak_dt.isocalendar()[1]

        yoy_list = []
        for w in common:
            sl, st = ly_by_w[w][1], ty_by_w[w][1]
            if sl > 0:
                yoy_list.append((st - sl) / sl * 100)
        avg_yoy = round(statistics.mean(yoy_list), 1) if yoy_list else None
        latest = pts[-1][1]
        color = PALETTE[i % len(PALETTE)]

        metrics.append(
            {
                "keyword": kw,
                "color": color,
                "tier": tier_of(latest),
                "last_year_trend": ly_lab,
                "this_year_trend": ty_lab,
                "last_year_trend_pct": ly_chg,
                "this_year_trend_pct": ty_chg,
                "consistency": cons_lab,
                "consistency_r": cons_r,
                "last_year_peak_week": ly_peak or "—",
                "this_year_peak_week": ty_peak or "—",
                "peak_week_offset": peak_offset if peak_offset is not None else "—",
                "avg_yoy_change_pct": avg_yoy if avg_yoy is not None else "—",
                "last_year_valid_weeks": len(ly),
                "this_year_valid_weeks": len(ty),
                "latest_sfr": latest,
                "latest_date": pts[-1][0].strftime("%Y-%m-%d"),
                "best_sfr": min(s for _, s in pts),
                "points": len(pts),
            }
        )
        chart_series.append(
            {
                "name": kw,
                "color": color,
                "tier": tier_of(latest),
                "data": [
                    {
                        "date": dt.strftime("%Y-%m-%d"),
                        "week": week_num_in_year(dt),
                        "year": dt.year,
                        "sfr": s,
                    }
                    for dt, s in pts
                ],
            }
        )
        yoy_pairs.append(
            {
                "keyword": kw,
                "weeks": common,
                "last_year": [ly_by_w[w][1] for w in common],
                "this_year": [ty_by_w[w][1] for w in common],
            }
        )

    with_sfr = [m for m in metrics if m["latest_sfr"] is not None]
    hottest = min(with_sfr, key=lambda m: m["latest_sfr"]) if with_sfr else None
    heat_up = [m for m in metrics if isinstance(m["avg_yoy_change_pct"], (int, float))]
    max_up = min(heat_up, key=lambda m: m["avg_yoy_change_pct"]) if heat_up else None
    max_down = max(heat_up, key=lambda m: m["avg_yoy_change_pct"]) if heat_up else None
    all_x = sorted({p["date"] for s in chart_series for p in s["data"]})

    return {
        "title": "ABA 关键词热度分析报告",
        "subtitle": "批量词 · small multiples 默认 · 点选高亮",
        "region": region,
        "generated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "data_window": {
            "min": min(all_dates).strftime("%Y-%m-%d"),
            "max": max(all_dates).strftime("%Y-%m-%d"),
            "this_year": this_year,
            "last_year": last_year,
            "source": "amazon-aba-kw-heat-report ← amazon-aba-kw-heat / ABA",
        },
        "summary": {
            "keyword_count": len(ordered),
            "hit_count": len(metrics),
            "hottest_keyword": hottest["keyword"] if hottest else None,
            "hottest_latest_sfr": hottest["latest_sfr"] if hottest else None,
            "max_heat_up_keyword": max_up["keyword"] if max_up else None,
            "max_heat_up_yoy_pct": max_up["avg_yoy_change_pct"] if max_up else None,
            "max_heat_down_keyword": max_down["keyword"] if max_down else None,
            "max_heat_down_yoy_pct": max_down["avg_yoy_change_pct"] if max_down else None,
            "note_sfr": "SFR 数值越小越热；同比变化%为 SFR 变化，负值=同比更热",
        },
        "metrics_table": metrics,
        "chart_series": chart_series,
        "yoy_pairs": yoy_pairs,
        "all_dates": all_x,
        "default_focus": hottest["keyword"] if hottest else (ordered[0] if ordered else None),
        "field_schema": [
            {"key": "keyword", "label": "关键词"},
            {"key": "last_year_trend", "label": "去年趋势"},
            {"key": "this_year_trend", "label": "今年趋势"},
            {"key": "consistency", "label": "一致性"},
            {"key": "last_year_peak_week", "label": "去年峰值周"},
            {"key": "this_year_peak_week", "label": "今年峰值周"},
            {"key": "peak_week_offset", "label": "峰值周偏移"},
            {"key": "avg_yoy_change_pct", "label": "平均同比变化"},
            {"key": "last_year_valid_weeks", "label": "去年有效周数"},
        ],
    }


def load_layout() -> dict:
    if DEFAULT_LAYOUT.exists():
        return json.loads(DEFAULT_LAYOUT.read_text(encoding="utf-8"))
    return {
        "reportType": "aba-kw-heat-dashboard",
        "version": "1.1",
        "expert": "关键词热度分析专家",
    }


def render_html(payload: dict) -> str:
    """v1.1 dashboard: small multiples default, focus highlight, optional overlay."""
    heat_rows = []
    for s in payload["chart_series"]:
        prev = None
        for p in s["data"]:
            delta = None if prev is None else p["sfr"] - prev
            heat_rows.append(
                {"keyword": s["name"], "date": p["date"], "sfr": p["sfr"], "wow": delta}
            )
            prev = p["sfr"]

    data_js = json.dumps(payload, ensure_ascii=False)
    heat_js = json.dumps(heat_rows, ensure_ascii=False)
    dw = payload["data_window"]
    gen = payload["generated_at"]

    # HTML template kept as one string; JS avoids nested f-expression issues via concatenation
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>ABA 关键词热度分析报告 v1.1</title>
<script src="https://agent-files.linkfox.com/example/public/echarts.min.js"></script>
<style>
  :root {{
    --bg:#0b0f17; --panel:#121a27; --border:#1e2a3c; --text:#e7eef9; --muted:#8b9bb4;
    --accent:#ff6b2c; --good:#3dd68c; --bad:#f07178; --card:#161f2e;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0;
    font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
    background:var(--bg); color:var(--text);
  }}
  header {{ padding:28px 32px 12px; border-bottom:1px solid var(--border); }}
  header h1 {{ margin:0 0 6px; font-size:22px; font-weight:700; }}
  header p {{ margin:0; color:var(--muted); font-size:13px; }}
  .wrap {{ padding:20px 32px 48px; max-width:1280px; margin:0 auto; }}
  .cards {{ display:grid; grid-template-columns:repeat(5,1fr); gap:12px; margin-bottom:18px; }}
  @media (max-width:1000px) {{ .cards {{ grid-template-columns:repeat(2,1fr); }} }}
  .card {{ background:var(--card); border:1px solid var(--border); border-radius:12px; padding:14px 16px; }}
  .card .label {{ color:var(--muted); font-size:12px; margin-bottom:6px; }}
  .card .value {{ font-size:18px; font-weight:700; word-break:break-all; }}
  .card .sub {{ color:var(--accent); font-size:12px; margin-top:4px; }}
  .panel {{ background:var(--panel); border:1px solid var(--border); border-radius:14px; padding:14px 16px 12px; margin-bottom:16px; }}
  .panel h2 {{ margin:0 0 8px; font-size:15px; font-weight:600; }}
  .panel .hint {{ color:var(--muted); font-size:12px; margin:-2px 0 10px; }}
  .toolbar {{ display:flex; flex-wrap:wrap; gap:10px 16px; align-items:center; margin-bottom:10px; font-size:13px; color:var(--muted); }}
  .toolbar label {{ display:inline-flex; align-items:center; gap:6px; cursor:pointer; user-select:none; }}
  .focus-pill {{ display:inline-flex; align-items:center; gap:8px; padding:4px 10px; border-radius:999px; border:1px solid var(--border); background:#0b0f17; color:var(--text); font-size:12px; }}
  .focus-pill b {{ color:var(--accent); }}
  .sm-grid {{ display:grid; grid-template-columns:repeat(3, 1fr); gap:12px; }}
  @media (max-width:1000px) {{ .sm-grid {{ grid-template-columns:repeat(2, 1fr); }} }}
  @media (max-width:640px) {{ .sm-grid {{ grid-template-columns:1fr; }} }}
  .sm-tile {{
    background:#0e1520; border:1px solid var(--border); border-radius:12px; padding:8px 8px 4px;
    cursor:pointer; transition: border-color .15s, box-shadow .15s;
  }}
  .sm-tile:hover {{ border-color:#3a4d6a; }}
  .sm-tile.active {{ border-color:var(--accent); box-shadow:0 0 0 1px rgba(255,107,44,.35); }}
  .sm-tile .ttl {{ display:flex; justify-content:space-between; gap:8px; align-items:center; font-size:12px; margin:0 4px 2px; }}
  .sm-tile .ttl .name {{ font-weight:600; color:var(--text); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
  .sm-tile .ttl .meta {{ color:var(--muted); font-variant-numeric:tabular-nums; }}
  .sm-chart {{ width:100%; height:150px; }}
  .chart {{ width:100%; height:360px; }}
  .chart.sm {{ height:300px; }}
  .chart.overlay {{ height:340px; }}
  #overlayPanel {{ display:none; }}
  #overlayPanel.show {{ display:block; }}
  table {{ width:100%; border-collapse:collapse; font-size:13px; }}
  th, td {{ padding:10px 8px; border-bottom:1px solid var(--border); text-align:left; }}
  th {{ color:var(--muted); font-weight:600; position:sticky; top:0; background:var(--panel); }}
  tr {{ cursor:pointer; }}
  tr:hover td {{ background:rgba(255,107,44,.06); }}
  tr.focus-row td {{ background:rgba(255,107,44,.12); }}
  .tag {{ display:inline-block; padding:2px 8px; border-radius:999px; font-size:11px; border:1px solid var(--border); }}
  .tag.up {{ color:var(--good); border-color:rgba(61,214,140,.35); background:rgba(61,214,140,.08); }}
  .tag.down {{ color:var(--bad); border-color:rgba(240,113,120,.35); background:rgba(240,113,120,.08); }}
  .tag.flat {{ color:var(--muted); }}
  .tag.hi {{ color:#7dc4ff; border-color:rgba(125,196,255,.35); background:rgba(125,196,255,.08); }}
  .tag.tier-hot {{ color:#ffb086; border-color:rgba(255,107,44,.4); }}
  .tag.tier-mid {{ color:#9ec9ff; border-color:rgba(125,196,255,.35); }}
  .tag.tier-tail {{ color:#8b9bb4; }}
  footer {{ color:var(--muted); font-size:12px; padding:8px 2px; }}
  .grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; }}
  @media (max-width:900px) {{ .grid2 {{ grid-template-columns:1fr; }} }}
  select {{ background:#0b0f17; color:#e7eef9; border:1px solid #1e2a3c; border-radius:8px; padding:6px 10px; }}
</style>
</head>
<body>
<header>
  <h1>ABA 关键词热度分析报告 <span style="color:var(--muted);font-size:14px;font-weight:500">v1.1</span></h1>
  <p>专家：关键词热度分析师 · 站点 {payload.get('region','US')} · 窗口 {dw['min']} → {dw['max']} · 生成 {gen}</p>
</header>
<div class="wrap">
  <div class="cards" id="cards"></div>
  <div class="panel">
    <h2>1. SFR 多周趋势 · 一词一图（默认）</h2>
    <p class="hint">共用时间轴，纵轴对数且倒置（越靠上越热）。点击瓷砖选焦点；全量叠线默认关闭。</p>
    <div class="toolbar">
      <span class="focus-pill">当前焦点：<b id="focusLabel">—</b></span>
      <label><input type="checkbox" id="chkOverlay"/> 显示全量叠线（高级，默认关）</label>
    </div>
    <div id="smGrid" class="sm-grid"></div>
  </div>
  <div class="panel">
    <h2>2. 焦点趋势（点选高亮）</h2>
    <p class="hint">焦点词实线加粗；其余半透明灰线作背景。</p>
    <div id="chartFocus" class="chart"></div>
  </div>
  <div class="panel" id="overlayPanel">
    <h2>2b. 全量叠线（可选）</h2>
    <p class="hint">硬对比时再开。跨数量级时可读性会下降。</p>
    <div id="chartOverlay" class="chart overlay"></div>
  </div>
  <div class="grid2">
    <div class="panel">
      <h2>3. 最新周热度条形</h2>
      <p class="hint">SFR 升序。点击切换焦点。</p>
      <div id="chartBars" class="chart sm"></div>
    </div>
    <div class="panel">
      <h2>4. 同比周对齐</h2>
      <p class="hint">实线=今年，虚线=去年。默认跟随焦点。</p>
      <select id="yoySelect"></select>
      <div id="chartYoy" class="chart sm"></div>
    </div>
  </div>
  <div class="panel">
    <h2>5. 升降温热力图（近16周 ΔSFR）</h2>
    <p class="hint">绿=升温（SFR变小），红=掉热（SFR变大）。</p>
    <div id="chartHeat" class="chart" style="height:420px"></div>
  </div>
  <div class="panel">
    <h2>6. 同比与趋势指标表</h2>
    <p class="hint">点击行切换焦点。同比%负值=更热。</p>
    <div style="overflow:auto;max-height:480px">
      <table id="metricsTable">
        <thead>
          <tr>
            <th>关键词</th><th>分层</th><th>去年趋势</th><th>今年趋势</th><th>一致性</th>
            <th>去年峰值周</th><th>今年峰值周</th><th>峰值周偏移</th>
            <th>平均同比变化</th><th>去年有效周数</th><th>最新SFR</th>
          </tr>
        </thead>
        <tbody></tbody>
      </table>
    </div>
  </div>
  <footer>
    amazon-aba-kw-heat-report v1.1 · 配对技能 amazon-aba-kw-heat · SFR 非绝对搜索量
  </footer>
</div>
<script>
const DATA = {data_js};
const HEAT = {heat_js};
let focusKw = DATA.default_focus || (DATA.chart_series[0] && DATA.chart_series[0].name);
const charts = {{}};

function tagClass(label) {{
  if (!label) return 'flat';
  if (String(label).indexOf('升温') >= 0) return 'up';
  if (String(label).indexOf('掉热') >= 0) return 'down';
  if (String(label).indexOf('一致') >= 0) return 'hi';
  return 'flat';
}}
function tierLabel(t) {{
  if (t === 'hot') return '热门<5万';
  if (t === 'mid') return '中腰<20万';
  if (t === 'tail') return '长尾';
  return t || '—';
}}
function tierClass(t) {{ return 'tier-' + (t || 'tail'); }}
function seriesByName(name) {{
  for (let i = 0; i < DATA.chart_series.length; i++) if (DATA.chart_series[i].name === name) return DATA.chart_series[i];
  return null;
}}
function metricByName(name) {{
  for (let i = 0; i < DATA.metrics_table.length; i++) if (DATA.metrics_table[i].keyword === name) return DATA.metrics_table[i];
  return null;
}}
function yoyIndex(name) {{
  for (let i = 0; i < DATA.yoy_pairs.length; i++) if (DATA.yoy_pairs[i].keyword === name) return i;
  return 0;
}}
const axisSfr = {{
  type:'log', inverse:true, name:'SFR', nameTextStyle:{{color:'#8b9bb4', fontSize:10}},
  axisLabel:{{color:'#8b9bb4', fontSize:10}}, splitLine:{{lineStyle:{{color:'#1e2a3c'}}}}
}};
function alignSeries(s) {{
  const map = {{}};
  (s.data || []).forEach(function(p) {{ map[p.date] = p.sfr; }});
  return (DATA.all_dates || []).map(function(d) {{ return map[d] == null ? null : map[d]; }});
}}

(function() {{
  const s = DATA.summary;
  const items = [
    {{label:'查询词数', value:s.keyword_count}},
    {{label:'命中数', value:s.hit_count}},
    {{label:'最热词（最新SFR）', value:s.hottest_keyword, sub:'SFR ' + s.hottest_latest_sfr}},
    {{label:'最大升温（同比）', value:s.max_heat_up_keyword, sub: (s.max_heat_up_yoy_pct!=null?s.max_heat_up_yoy_pct+'%':'—') + '（负=更热）'}},
    {{label:'最大掉热（同比）', value:s.max_heat_down_keyword, sub: (s.max_heat_down_yoy_pct!=null?s.max_heat_down_yoy_pct+'%':'—')}}
  ];
  document.getElementById('cards').innerHTML = items.map(function(i) {{
    return '<div class="card"><div class="label">' + i.label + '</div><div class="value">' +
      (i.value == null ? '—' : i.value) + '</div>' + (i.sub ? '<div class="sub">' + i.sub + '</div>' : '') + '</div>';
  }}).join('');
}})();

function buildSmallMultiples() {{
  const grid = document.getElementById('smGrid');
  grid.innerHTML = '';
  const x = DATA.all_dates || [];
  DATA.chart_series.forEach(function(s, idx) {{
    const m = metricByName(s.name) || {{}};
    const tile = document.createElement('div');
    tile.className = 'sm-tile' + (s.name === focusKw ? ' active' : '');
    tile.dataset.kw = s.name;
    tile.innerHTML = '<div class="ttl"><span class="name" style="color:' + (s.color||'#fff') + '">' + s.name +
      '</span><span class="meta">SFR ' + (m.latest_sfr == null ? '—' : m.latest_sfr) +
      '</span></div><div class="sm-chart" id="sm_' + idx + '"></div>';
    tile.addEventListener('click', function() {{ setFocus(s.name); }});
    grid.appendChild(tile);
    const ch = echarts.init(document.getElementById('sm_' + idx));
    charts['sm_' + idx] = ch;
    ch.setOption({{
      animation:false, backgroundColor:'transparent',
      grid:{{left:36,right:8,top:8,bottom:18}},
      tooltip:{{ trigger:'axis', formatter:function(params) {{
        const p = params[0]; if (!p || p.value == null) return s.name;
        return s.name + '<br/>' + p.axisValue + '<br/>SFR ' + p.value;
      }}}},
      xAxis:{{ type:'category', data:x, axisLabel:{{show:false}}, axisTick:{{show:false}}, axisLine:{{lineStyle:{{color:'#1e2a3c'}}}} }},
      yAxis:{{ type:'log', inverse:true, axisLabel:{{color:'#5c6b84', fontSize:9, formatter:function(v){{
        if (v>=1e6) return (v/1e6)+'M'; if (v>=1e3) return (v/1e3)+'k'; return v;
      }}}}, splitLine:{{lineStyle:{{color:'#182233'}}}}, axisLine:{{show:false}}, axisTick:{{show:false}} }},
      series:[{{ type:'line', data:alignSeries(s), showSymbol:false, connectNulls:true, smooth:0.15,
        lineStyle:{{width:2, color:s.color || '#7dc4ff'}}, areaStyle:{{color:(s.color||'#7dc4ff'), opacity:0.08}} }}]
    }});
  }});
}}

function renderFocus() {{
  if (!charts.focus) charts.focus = echarts.init(document.getElementById('chartFocus'));
  const ch = charts.focus;
  const x = DATA.all_dates || [];
  const series = DATA.chart_series.map(function(s) {{
    const isFocus = s.name === focusKw;
    return {{
      name:s.name, type:'line', data:alignSeries(s), showSymbol:false, connectNulls:true, smooth:0.15,
      z: isFocus ? 10 : 1,
      lineStyle: {{ width: isFocus ? 3.2 : 1.5, color: s.color || '#7dc4ff', opacity: isFocus ? 1 : 0.6 }}
    }};
  }});
  series.sort(function(a,b) {{ if (a.name===focusKw) return 1; if (b.name===focusKw) return -1; return 0; }});
  ch.setOption({{
    backgroundColor:'transparent', tooltip:{{trigger:'axis'}}, legend:{{show:false}},
    grid:{{left:58,right:20,top:24,bottom:40}},
    xAxis:{{type:'category', data:x, axisLabel:{{color:'#8b9bb4', hideOverlap:true}}, axisLine:{{lineStyle:{{color:'#1e2a3c'}}}}}},
    yAxis: Object.assign({{}}, axisSfr, {{ name:'SFR（上=热）' }}),
    series: series
  }}, true);
}}

function renderOverlay() {{
  if (!charts.overlay) charts.overlay = echarts.init(document.getElementById('chartOverlay'));
  const x = DATA.all_dates || [];
  charts.overlay.setOption({{
    backgroundColor:'transparent', tooltip:{{trigger:'axis'}},
    legend:{{type:'scroll', textStyle:{{color:'#8b9bb4'}}, top:0}},
    grid:{{left:58,right:20,top:40,bottom:40}},
    xAxis:{{type:'category', data:x, axisLabel:{{color:'#8b9bb4', hideOverlap:true}}, axisLine:{{lineStyle:{{color:'#1e2a3c'}}}}}},
    yAxis: Object.assign({{}}, axisSfr, {{ name:'SFR（上=热）' }}),
    series: DATA.chart_series.map(function(s) {{
      return {{ name:s.name, type:'line', showSymbol:false, connectNulls:true, smooth:0.15, data:alignSeries(s), lineStyle:{{width:1.8, color:s.color}} }};
    }})
  }}, true);
}}

function renderBars() {{
  if (!charts.bars) charts.bars = echarts.init(document.getElementById('chartBars'));
  const ch = charts.bars;
  const rows = DATA.metrics_table.filter(function(m){{return m.latest_sfr!=null;}}).sort(function(a,b){{return a.latest_sfr-b.latest_sfr;}});
  ch.setOption({{
    backgroundColor:'transparent', tooltip:{{trigger:'axis', axisPointer:{{type:'shadow'}}}},
    grid:{{left:140,right:24,top:16,bottom:24}},
    xAxis:{{type:'log', axisLabel:{{color:'#8b9bb4'}}, splitLine:{{lineStyle:{{color:'#1e2a3c'}}}}, name:'SFR'}},
    yAxis:{{type:'category', data:rows.map(function(r){{return r.keyword;}}), axisLabel:{{color:'#e7eef9'}}}},
    series:[{{ type:'bar', data: rows.map(function(r) {{
      const active = r.keyword === focusKw;
      return {{ value:r.latest_sfr, itemStyle:{{ color: active ? (r.color||'#ff6b2c') : 'rgba(125,196,255,0.35)', borderRadius:[0,4,4,0] }} }};
    }}) }}]
  }}, true);
  ch.off('click');
  ch.on('click', function(p) {{ if (p && p.name) setFocus(p.name); }});
}}

function setupYoy() {{
  const sel = document.getElementById('yoySelect');
  sel.innerHTML = '';
  DATA.yoy_pairs.forEach(function(p, i) {{
    const o = document.createElement('option'); o.value=i; o.textContent=p.keyword; sel.appendChild(o);
  }});
  sel.addEventListener('change', function(e) {{
    const idx = +e.target.value; renderYoy(idx);
    if (DATA.yoy_pairs[idx]) setFocus(DATA.yoy_pairs[idx].keyword, true);
  }});
  charts.yoy = echarts.init(document.getElementById('chartYoy'));
}}
function renderYoy(i) {{
  const ch = charts.yoy; const p = DATA.yoy_pairs[i];
  if (!p || !p.weeks.length) {{
    ch.setOption({{ title:{{text:'该词暂无足够同比对齐周', left:'center', top:'middle', textStyle:{{color:'#8b9bb4', fontSize:13}}}}, series:[] }}, true);
    return;
  }}
  ch.setOption({{
    backgroundColor:'transparent', title:{{show:false}}, tooltip:{{trigger:'axis'}}, legend:{{textStyle:{{color:'#8b9bb4'}}}},
    grid:{{left:60,right:20,top:36,bottom:32}},
    xAxis:{{type:'category', data:p.weeks.map(function(w){{return 'W'+w;}}), axisLabel:{{color:'#8b9bb4'}}}},
    yAxis: Object.assign({{}}, axisSfr, {{ name:'SFR（上=热）' }}),
    series:[
      {{name: DATA.data_window.last_year + '（去年）', type:'line', data:p.last_year, lineStyle:{{type:'dashed'}}, showSymbol:false}},
      {{name: DATA.data_window.this_year + '（今年）', type:'line', data:p.this_year, showSymbol:false, lineStyle:{{color:'#ff6b2c'}}}}
    ]
  }}, true);
}}

function renderHeat() {{
  charts.heat = echarts.init(document.getElementById('chartHeat'));
  const kws = DATA.chart_series.map(function(s){{return s.name;}});
  const dates = Array.from(new Set(HEAT.map(function(h){{return h.date;}}))).sort();
  const useDates = dates.slice(-16);
  const data = []; let maxAbs = 1;
  HEAT.forEach(function(h) {{
    if (useDates.indexOf(h.date) < 0 || h.wow == null) return;
    maxAbs = Math.max(maxAbs, Math.abs(h.wow));
    data.push([useDates.indexOf(h.date), kws.indexOf(h.keyword), h.wow]);
  }});
  charts.heat.setOption({{
    backgroundColor:'transparent',
    tooltip:{{ formatter:function(p){{ return kws[p.value[1]] + '<br/>' + useDates[p.value[0]] + '<br/>ΔSFR: ' + p.value[2]; }} }},
    grid:{{left:140,right:24,top:16,bottom:60}},
    xAxis:{{type:'category', data:useDates, axisLabel:{{color:'#8b9bb4', rotate:40}}}},
    yAxis:{{type:'category', data:kws, axisLabel:{{color:'#e7eef9'}}}},
    visualMap:{{ min:-maxAbs, max:maxAbs, calculable:true, orient:'horizontal', left:'center', bottom:0,
      inRange:{{color:['#3dd68c','#1e2a3c','#f07178']}}, textStyle:{{color:'#8b9bb4'}} }},
    series:[{{type:'heatmap', data:data, emphasis:{{itemStyle:{{shadowBlur:8}}}}}}]
  }});
}}

function renderTable() {{
  const tb = document.querySelector('#metricsTable tbody');
  tb.innerHTML = DATA.metrics_table.map(function(m) {{
    const yoy = m.avg_yoy_change_pct;
    const yoyStr = (typeof yoy === 'number') ? ((yoy>0?'+':'') + yoy + '%') : yoy;
    const trClass = m.keyword === focusKw ? ' class="focus-row"' : '';
    return '<tr data-kw="' + m.keyword + '"' + trClass + '>' +
      '<td><b style="color:' + (m.color||'#fff') + '">' + m.keyword + '</b></td>' +
      '<td><span class="tag ' + tierClass(m.tier) + '">' + tierLabel(m.tier) + '</span></td>' +
      '<td><span class="tag ' + tagClass(m.last_year_trend) + '">' + m.last_year_trend + '</span></td>' +
      '<td><span class="tag ' + tagClass(m.this_year_trend) + '">' + m.this_year_trend + '</span></td>' +
      '<td><span class="tag ' + tagClass(m.consistency) + '">' + m.consistency +
        (m.consistency_r!=null ? ' (' + m.consistency_r + ')' : '') + '</span></td>' +
      '<td>' + m.last_year_peak_week + '</td><td>' + m.this_year_peak_week + '</td><td>' + m.peak_week_offset + '</td>' +
      '<td>' + yoyStr + '</td><td>' + m.last_year_valid_weeks + '</td><td>' +
      (m.latest_sfr == null ? '—' : m.latest_sfr) + '</td></tr>';
  }}).join('');
  Array.prototype.forEach.call(tb.querySelectorAll('tr'), function(tr) {{
    tr.addEventListener('click', function() {{ setFocus(tr.getAttribute('data-kw')); }});
  }});
}}

function setFocus(kw, fromYoy) {{
  if (!kw) return;
  focusKw = kw;
  document.getElementById('focusLabel').textContent = kw;
  Array.prototype.forEach.call(document.querySelectorAll('.sm-tile'), function(t) {{
    if (t.dataset.kw === kw) t.classList.add('active'); else t.classList.remove('active');
  }});
  renderFocus(); renderBars(); renderTable();
  if (!fromYoy) {{
    const sel = document.getElementById('yoySelect');
    const idx = yoyIndex(kw); sel.value = String(idx); renderYoy(idx);
  }}
}}

document.getElementById('chkOverlay').addEventListener('change', function(e) {{
  const panel = document.getElementById('overlayPanel');
  if (e.target.checked) {{
    panel.classList.add('show'); renderOverlay();
    setTimeout(function(){{ if (charts.overlay) charts.overlay.resize(); }}, 50);
  }} else panel.classList.remove('show');
}});

buildSmallMultiples(); setupYoy(); renderHeat(); setFocus(focusKw);
window.addEventListener('resize', function() {{
  Object.keys(charts).forEach(function(k) {{ try {{ charts[k].resize(); }} catch (e) {{}} }});
}});
</script>
</body>
</html>
"""


def generate(
    *,
    keywords: list[str] | None = None,
    region: str = "US",
    weeks: int = 104,
    input_path: Path | None = None,
    out_dir: Path,
) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if input_path:
        raw = json.loads(Path(input_path).read_text(encoding="utf-8"))
    else:
        if not keywords:
            raise ValueError("keywords required when --input not set")
        raw = fetch_aba(keywords, region=region, weeks=weeks)

    # persist raw
    raw_path = out_dir / "aba_raw.json"
    raw_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8")

    payload = compute_payload(raw, keywords, region=region)
    layout = load_layout()
    layout = dict(layout)
    layout["generated_at"] = payload["generated_at"]
    layout["test_keywords"] = keywords or [m["keyword"] for m in payload["metrics_table"]]

    data_path = out_dir / "kw-heat-data.json"
    layout_path = out_dir / "kw-heat-layout.json"
    html_path = out_dir / "kw-heat-report.html"

    data_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    layout_path.write_text(json.dumps(layout, ensure_ascii=False, indent=2), encoding="utf-8")
    html_path.write_text(render_html(payload), encoding="utf-8")

    return {
        "success": True,
        "html": str(html_path.resolve()),
        "data": str(data_path.resolve()),
        "layout": str(layout_path.resolve()),
        "raw": str(raw_path.resolve()),
        "summary": payload["summary"],
        "default_focus": payload["default_focus"],
        "keyword_count": payload["summary"]["keyword_count"],
    }


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    parser = argparse.ArgumentParser(description="ABA keyword heat report generator")
    parser.add_argument("json_params", nargs="?", help="JSON: keywords|asins|imageUrl/image + region/weeks/out_dir")
    parser.add_argument("--input", dest="input_path", help="Existing ABA JSON path")
    parser.add_argument("--out-dir", dest="out_dir", default=None)
    parser.add_argument("--region", default=None)
    parser.add_argument("--weeks", type=int, default=None)
    args = parser.parse_args()

    params = {}
    if args.json_params:
        try:
            params = json.loads(args.json_params)
        except json.JSONDecodeError as e:
            print(f"Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    keywords = params.get("keywords") or params.get("keyword")
    if isinstance(keywords, str):
        keywords = [keywords]
    region = args.region or params.get("region") or "US"
    weeks = args.weeks or int(params.get("weeks") or 104)
    out_dir = Path(
        args.out_dir
        or params.get("out_dir")
        or params.get("outDir")
        or _resolve_session_dir()
    )
    input_path = args.input_path or params.get("input")

    entry_meta = None
    # Entry expansion: image / ASIN → keywords (unless --input raw ABA provided)
    needs_resolve = (not input_path) and (
        not keywords
        or params.get("asins")
        or params.get("asin")
        or params.get("imageUrl")
        or params.get("image_url")
        or params.get("image")
        or params.get("image_path")
    )
    if needs_resolve and (
        params.get("asins")
        or params.get("asin")
        or params.get("imageUrl")
        or params.get("image_url")
        or params.get("image")
        or params.get("image_path")
        or not keywords
    ):
        resolve_script = Path(__file__).resolve().parent / "resolve_entry.py"
        if not resolve_script.is_file():
            print(json.dumps({"success": False, "error": "resolve_entry.py missing"}, ensure_ascii=False))
            sys.exit(2)
        proc = subprocess.run(
            [sys.executable, str(resolve_script), json.dumps(params, ensure_ascii=False)],
            capture_output=True,
            text=True,
            env=os.environ.copy(),
            timeout=300,
        )
        try:
            entry_meta = json.loads(proc.stdout or "{}")
        except json.JSONDecodeError:
            print(json.dumps({
                "success": False,
                "error": "resolve_entry non-JSON",
                "stdout": (proc.stdout or "")[:500],
                "stderr": (proc.stderr or "")[:500],
            }, ensure_ascii=False, indent=2))
            sys.exit(2)
        if not entry_meta.get("success"):
            print(json.dumps(entry_meta, ensure_ascii=False, indent=2))
            sys.exit(2)
        keywords = entry_meta.get("keywords") or keywords
        region = entry_meta.get("region") or region

    try:
        result = generate(
            keywords=keywords,
            region=region,
            weeks=weeks,
            input_path=Path(input_path) if input_path else None,
            out_dir=out_dir,
        )
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(2)

    if entry_meta:
        result["entry"] = {
            "mode": entry_meta.get("mode"),
            "keywords": entry_meta.get("keywords"),
            "sources": entry_meta.get("sources"),
            "warnings": entry_meta.get("warnings"),
        }
        # persist entry resolution
        try:
            (Path(out_dir) / "entry_resolve.json").write_text(
                json.dumps(entry_meta, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            result["entry_resolve"] = str((Path(out_dir) / "entry_resolve.json").resolve())
        except Exception:
            pass

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
