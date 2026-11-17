#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_trend.py — 多轮趋势报告（v6.0.0 新增；`pp.py trend`）

单次检测只回答「现在多少分」；作者多轮改稿真正要问的是
「改了这么多版，AI 分数到底有没有在降」。本脚本把同一文稿的
多份 workflow JSON（按文件修改时间排序）渲染成一张自包含 HTML
轨迹仪表盘：

  - 内联 SVG 折线（分数轨迹，风险带着色，降级档轮次标注）
  - 相邻两轮 delta 表：↓改善 / ↑回升（回升轮次醒目标注）
  - 最新一轮结论卡片 + 段落 hi/med/lo 历史
  - 页脚学术诚信声明 + 数据源清单

诚实边界：分数为引擎口径相对参考，改写应以质量为准——分数下降
不等于内容更好；降级档与融合档轮次混排时不可直接比（图表标注）。

零依赖（标准库）；不重跑引擎（只渲染既有 workflow 产物）。
用法:
  python3 pp_trend.py 文稿1.workflow.json 文稿2.workflow.json ...
  python3 pp_trend.py 报告目录/            # 扫描目录下全部 *.workflow.json
  python3 pp_trend.py 目录/ -o trend.html
"""
import argparse
import html
import json
import sys
from datetime import datetime
from pathlib import Path

_INTEGRITY = ("学术诚信：本报告由 Paper Polisher Pro 生成，供作者自查与改进写作质量，"
              "不用于规避机构 AIGC 检测；分数为引擎口径的相对参考，改稿请以内容质量为准。")

_CSS = """
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;margin:24px;color:#222;max-width:1080px}
h1{font-size:20px}h2{font-size:16px;margin-top:24px}
table{border-collapse:collapse;width:100%;font-size:13px;margin-top:10px}
th,td{border:1px solid #ddd;padding:5px 8px;text-align:left}
th{background:#f5f5f5}.up{color:#c0392b;font-weight:bold}.down{color:#27ae60;font-weight:bold}
.badge{color:#fff;border-radius:3px;padding:1px 7px;font-size:12px}
.note{color:#777;font-size:12px;margin-top:16px}.muted{color:#888;font-size:12px}
.cards{display:flex;gap:12px;margin:14px 0;flex-wrap:wrap}
.card{border:1px solid #e3e3e3;border-radius:6px;padding:10px 16px;min-width:130px}
.card b{font-size:22px;display:block}
"""

_RISK_COLOR = {"high": "#c0392b", "medium": "#e67e22", "low": "#27ae60", "unknown": "#7f8c8d"}


def collect(inputs):
    """收集 workflow JSON：文件直取，目录扫 *.workflow.json；按 mtime 升序。"""
    runs = []
    seen = set()
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            files = sorted(p.glob("*.workflow.json"))
        elif p.is_file():
            files = [p]
        else:
            print(f"WARN: 跳过不存在的输入 {inp}", file=sys.stderr)
            continue
        for f in files:
            key = f.resolve()
            if key in seen:
                continue
            seen.add(key)
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                print(f"WARN: 跳过无法解析的 {f}（{e}）", file=sys.stderr)
                continue
            det = d.get("detect") or {}
            score = det.get("overall_ai_score")
            paras = d.get("paragraphs") or {}
            runs.append({
                "file": str(f), "stem": f.stem.replace(".workflow", ""),
                "mtime": f.stat().st_mtime,
                "when": datetime.fromtimestamp(f.stat().st_mtime).strftime("%m-%d %H:%M"),
                "score": score if isinstance(score, (int, float)) else None,
                "risk": det.get("overall_risk", "unknown"),
                "degraded": bool(det.get("degraded_mode")),
                "engine": d.get("engine_version", "?"),
                "hi": paras.get("high"), "med": paras.get("medium"), "total": paras.get("total"),
            })
    runs.sort(key=lambda r: r["mtime"])
    return runs


def _svg_line(runs):
    """分数轨迹折线（内联 SVG；降级轮空心点）。"""
    pts = [(i, r["score"]) for i, r in enumerate(runs) if r["score"] is not None]
    if len(pts) < 2:
        return ""
    W, H, PAD = 760, 240, 40
    n = len(runs)
    xs = lambda i: PAD + i * (W - 2 * PAD) / max(n - 1, 1)
    ys = lambda s: H - PAD - (s / 100.0) * (H - 2 * PAD)
    polylines, dots = [], []
    # 风险带参考线
    for band, yy, color in (("high ≥60", ys(60), "#c0392b"), ("medium ≥35", ys(35), "#e67e22")):
        polylines.append(f'<line x1="{PAD}" y1="{yy:.0f}" x2="{W - PAD}" y2="{yy:.0f}" '
                         f'stroke="{color}" stroke-dasharray="4 4" stroke-width="1" opacity="0.5"/>'
                         f'<text x="{W - PAD + 4}" y="{yy + 4:.0f}" font-size="10" fill="{color}">{band}</text>')
    seq = " ".join(f"{xs(i):.0f},{ys(s):.0f}" for i, s in pts)
    polylines.append(f'<polyline points="{seq}" fill="none" stroke="#2E5E8F" stroke-width="2.5"/>')
    for i, r in enumerate(runs):
        if r["score"] is None:
            continue
        color = _RISK_COLOR.get(r["risk"], "#7f8c8d")
        if r["degraded"]:
            dots.append(f'<circle cx="{xs(i):.0f}" cy="{ys(r["score"]):.0f}" r="6" fill="#fff" '
                        f'stroke="{color}" stroke-width="2.5"/>')
        else:
            dots.append(f'<circle cx="{xs(i):.0f}" cy="{ys(r["score"]):.0f}" r="5" fill="{color}"/>')
        dots.append(f'<text x="{xs(i):.0f}" y="{ys(r["score"]) - 12:.0f}" font-size="11" '
                    f'text-anchor="middle" fill="#333">{r["score"]:.0f}</text>')
        dots.append(f'<text x="{xs(i):.0f}" y="{H - PAD + 16}" font-size="10" text-anchor="middle" '
                    f'fill="#888">{html.escape(r["when"])}</text>')
    return (f'<svg width="{W}" height="{H}" role="img" aria-label="score trend">'
            + "".join(polylines) + "".join(dots) + "</svg>")


def _delta_table(runs):
    rows = []
    prev = None
    for r in runs:
        if prev is None or r["score"] is None or prev["score"] is None:
            delta = "—"
            cls = ""
        else:
            d = r["score"] - prev["score"]
            delta = f"{d:+.1f}"
            if d < -0.05:
                delta += " ↓改善"; cls = "down"
            elif d > 0.05:
                delta += " ↑回升"; cls = "up"
            else:
                cls = ""
        degrade = ' <span class="badge" style="background:#7f8c8d">降级档</span>' if r["degraded"] else ""
        rows.append(f"<tr><td>{html.escape(r['when'])}</td>"
                    f"<td>{html.escape(r['stem'])}</td>"
                    f"<td>{'—' if r['score'] is None else r['score']}</td>"
                    f'<td><span class="badge" style="background:{_RISK_COLOR.get(r["risk"], "#7f8c8d")}">'
                    f'{html.escape(str(r["risk"]))}</span>{degrade}</td>'
                    f'<td>{r.get("hi", "—")}/{r.get("med", "—")}/{r.get("total", "—")}</td>'
                    f'<td class="{cls}">{delta}</td>'
                    f"<td>{html.escape(r['engine'])}</td></tr>")
        prev = r
    return ("<table><tr><th>时间</th><th>文稿</th><th>AI 分</th><th>风险带</th>"
            "<th>段落 hi/med/总</th><th>较上一轮</th><th>引擎</th></tr>"
            + "".join(rows) + "</table>"
            "<p class='muted'>↓改善=分数下降；↑回升=分数上升。分数下降不等于内容更好——"
            "改写请以内容质量为准；降级档与融合档轮次不可直接互比。</p>")


def render(runs, title):
    valid = [r for r in runs if r["score"] is not None]
    first, last = valid[0], valid[-1]
    net = last["score"] - first["score"]
    net_txt = f"{net:+.1f}（{'↓改善' if net < 0 else '↑回升' if net > 0 else '持平'}）"
    parts = [f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>{html.escape(title)}</title><style>{_CSS}</style></head><body>
<h1>{html.escape(title)}</h1>
<div class='cards'>
<div class="card"><b>{len(runs)}</b>轮次</div>
<div class="card"><b>{first["score"]:.0f} → {last["score"]:.0f}</b>首→末</div>
<div class="card"><b class="{'down' if net < 0 else ('up' if net > 0 else '')}">{net_txt.split('（')[0]}</b>净变化</div>
<div class="card"><b style="color:{_RISK_COLOR.get(last['risk'], '#7f8c8d')}">{html.escape(str(last['risk']))}</b>最新风险带</div>
</div>"""]
    svg = _svg_line(runs)
    if svg:
        parts.append("<h2>分数轨迹</h2>" + svg)
    else:
        parts.append("<p class='muted'>有效轮次不足 2，无法画轨迹（仍列出逐轮明细）。</p>")
    parts.append("<h2>逐轮明细</h2>" + _delta_table(runs))
    srcs = "；".join(r["file"] for r in runs)
    parts.append(f'<p class="note">{_INTEGRITY}<br>数据源（{len(runs)} 份，按修改时间排序）：'
                 f'{html.escape(srcs)} ｜ 生成时间 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ｜ '
                 f'零外部资源、零网络</p>')
    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("inputs", nargs="+", help="workflow JSON 文件或含 *.workflow.json 的目录（≥2 份）")
    ap.add_argument("-o", "--output", default=None, help="输出 HTML（默认 trend.report.html）")
    ap.add_argument("--title", default="改稿趋势 · AI 分数轨迹", help="报告标题")
    a = ap.parse_args()

    runs = collect(a.inputs)
    if len(runs) < 2:
        print("ERROR: 趋势报告需要至少 2 份可解析的 workflow JSON"
              "（先对每轮改稿跑 python3 scripts/pp.py workflow 文稿，再汇总到这里）",
              file=sys.stderr)
        return 2
    out = Path(a.output) if a.output else Path("trend.report.html")
    out.write_text(render(runs, a.title), encoding="utf-8")
    valid = [r for r in runs if r["score"] is not None]
    if valid:
        net = valid[-1]["score"] - valid[0]["score"]
        print(f"趋势报告已生成: {out}（{len(runs)} 轮；首→末 "
              f"{valid[0]['score']:.0f}→{valid[-1]['score']:.0f}，净变化 {net:+.1f}）")
    else:
        print(f"趋势报告已生成: {out}（{len(runs)} 轮，均无可评分）")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
