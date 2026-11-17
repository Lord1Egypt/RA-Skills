#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_batch_report.py — 批量检测 HTML 汇总报告（v5.1.0 新增）

`ai_detector.py --batch DIR --csv scores.csv` 的产物是逐文件 CSV——论文级批量
自查时缺一个「一眼看全局」的汇总面。本脚本把该 CSV 渲染成单文件 HTML：

  - 顶部：文件总数 / 均分 / 高·中·低风险计数 / 降级档占比
  - 分布直方图（纯内联 CSS 柱条，零外部资源）
  - 风险分档表 + 逐文件明细（按分数降序，ERROR/unknown 行置顶提示）
  - 页脚带学术诚信声明

零依赖（标准库读 CSV + 字符串拼 HTML）；不重跑引擎（只渲染既有结果）。
用法:
  python3 pp_batch_report.py scores.csv -o report.html
  python3 pp_batch_report.py scores.csv            # 默认同目录 .html
"""
import argparse
import csv
import html
import json
import sys
from collections import Counter
from pathlib import Path

_INTEGRITY = ("学术诚信：本报告由 Paper Polisher Pro 生成，供作者自查与改进写作质量，"
              "不用于规避机构 AIGC 检测；分数为引擎口径的相对参考，不与任何机构检测器互换。")


def read_csv(path):
    """读 batch CSV（utf-8-sig 兼容），返回行 dict 列表。"""
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            rows.append({k: (v or "").strip() for k, v in r.items()})
    return rows


def summarize(rows):
    scored = []
    errors, unknown = [], []
    for r in rows:
        v = r.get("ai_score", "")
        if r.get("risk") == "ERROR" or v == "ERROR":
            errors.append(r)
        elif r.get("risk") == "unknown":
            unknown.append(r)
        else:
            try:
                scored.append({**r, "_score": float(v)})
            except ValueError:
                unknown.append(r)
    n = len(scored)
    scores = [r["_score"] for r in scored]
    bands = Counter(r.get("risk", "") for r in scored)
    return {
        "total": len(rows), "scored": n, "scored_rows": scored,
        "errors": errors, "unknown": unknown,
        "mean": round(sum(scores) / n, 1) if n else None,
        "max": max(scores) if scores else None,
        "min": min(scores) if scores else None,
        "bands": {"high": bands.get("high", 0), "medium": bands.get("medium", 0),
                  "low": bands.get("low", 0)},
        "degraded": sum(1 for r in scored if r.get("degraded_mode", "").lower() == "true"),
    }


def _histogram(scores, width=50):
    """10 分一桶的频次柱条（内联 div 宽度百分比）。"""
    buckets = Counter(int(s // 10) * 10 for s in scores)
    peak = max(buckets.values()) if buckets else 1
    out = []
    for lo in range(0, 100, 10):
        c = buckets.get(lo, 0)
        pct = round(c / peak * 100)
        color = "#c0392b" if lo >= 60 else ("#e67e22" if lo >= 35 else "#27ae60")
        out.append(f'<div class="hrow"><span class="hlab">{lo:02d}-{lo + 9:02d}</span>'
                   f'<div class="hbar" style="width:{max(pct, 1 if c else 0)}%;background:{color}"></div>'
                   f'<span class="hnum">{c}</span></div>')
    return "\n".join(out)


def _risk_badge(risk):
    color = {"high": "#c0392b", "medium": "#e67e22", "low": "#27ae60",
             "unknown": "#7f8c8d", "ERROR": "#8e44ad"}.get(risk, "#7f8c8d")
    return (f'<span style="background:{color};color:#fff;border-radius:3px;'
            f'padding:1px 7px;font-size:12px">{html.escape(risk or "?")}</span>')


def render(rows, src_csv):
    s = summarize(rows)

    def _score_of(r):
        try:
            return float(r.get("ai_score", ""))
        except (TypeError, ValueError):
            return -1.0

    scored = sorted(s["scored_rows"], key=_score_of, reverse=True)
    title = f"批量检测汇总 · {Path(src_csv).stem}"
    parts = [f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>{html.escape(title)}</title><style>
body{{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;margin:24px;color:#222}}
h1{{font-size:20px}} table{{border-collapse:collapse;width:100%;font-size:13px;margin-top:12px}}
th,td{{border:1px solid #ddd;padding:5px 8px;text-align:left}}
th{{background:#f5f5f5}} .cards{{display:flex;gap:12px;margin:14px 0;flex-wrap:wrap}}
.card{{border:1px solid #e3e3e3;border-radius:6px;padding:10px 16px;min-width:110px}}
.card b{{font-size:22px;display:block}} .hrow{{display:flex;align-items:center;gap:8px;margin:3px 0}}
.hlab{{width:52px;font-size:12px;color:#555}} .hbar{{height:14px;border-radius:2px}}
.hnum{{font-size:12px;color:#555}} .note{{color:#777;font-size:12px;margin-top:16px}}
</style></head><body><h1>{html.escape(title)}</h1>"""]

    parts.append(f'<div class="cards">'
                 f'<div class="card"><b>{s["total"]}</b>文件总数</div>'
                 f'<div class="card"><b>{s["mean"] if s["mean"] is not None else "—"}</b>均分'
                 + (f'<div class="note" style="margin:2px 0 0">{s["min"]}–{s["max"]}</div>' if s["mean"] is not None else '')
                 + '</div>'
                 f'<div class="card"><b style="color:#c0392b">{s["bands"]["high"]}</b>high</div>'
                 f'<div class="card"><b style="color:#e67e22">{s["bands"]["medium"]}</b>medium</div>'
                 f'<div class="card"><b style="color:#27ae60">{s["bands"]["low"]}</b>low</div>'
                 f'<div class="card"><b>{s["degraded"]}</b>降级档</div></div>')

    if s["scored_rows"]:
        parts.append("<h3>分数分布（10 分一桶）</h3>"
                     + _histogram([r["_score"] for r in s["scored_rows"]]))

    parts.append("<h3>逐文件明细（分数降序）</h3><table><tr><th>文件</th><th>分数</th>"
                 "<th>风险</th><th>语言</th><th>降级</th></tr>")
    for r in scored:
        dm = "是" if r.get("degraded_mode", "").lower() == "true" else ""
        parts.append(f"<tr><td>{html.escape(r.get('file',''))}</td>"
                     f"<td>{html.escape(r.get('ai_score',''))}</td>"
                     f"<td>{_risk_badge(r.get('risk',''))}</td>"
                     f"<td>{html.escape(r.get('language',''))}</td><td>{dm}</td></tr>")
    for r in s["unknown"]:
        parts.append(f"<tr><td>{html.escape(r.get('file',''))}</td><td>—</td>"
                     f"<td>{_risk_badge('unknown')}</td>"
                     f"<td colspan='2'>{html.escape((r.get('degraded_mode') or r.get('note') or '')[:80])}</td></tr>")
    for r in s["errors"]:
        # CSV 中 ERROR 行: ai_score=ERROR, degraded_mode 列=错误信息
        parts.append(f"<tr><td>{html.escape(r.get('file',''))}</td><td>ERROR</td>"
                     f"<td>{_risk_badge('ERROR')}</td>"
                     f"<td colspan='2'>{html.escape((r.get('degraded_mode') or '')[:80])}</td></tr>")
    parts.append("</table>")

    if s["degraded"]:
        parts.append(f'<p class="note">⚠️ {s["degraded"]} 个文件在降级档（未装监督层或语言门控跳过）：'
                     '降级档对医学语域系统性高估，请结合 scripts/pp_doctor.py 与能力边界矩阵解读。</p>')
    parts.append(f'<p class="note">{_INTEGRITY}<br>数据源：{html.escape(str(src_csv))} ｜ '
                 '重新批量检测：python3 scripts/ai_detector.py --batch DIR --csv scores.csv</p>')
    parts.append("</body></html>")
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser(description="批量检测 CSV → HTML 汇总报告（零依赖，不重跑引擎）")
    ap.add_argument("csv_file", help="ai_detector --batch --csv 的产物路径")
    ap.add_argument("-o", "--output", default=None, help="输出 HTML 路径（默认同目录 <stem>.html）")
    args = ap.parse_args()
    src = Path(args.csv_file)
    if not src.exists():
        print(f"ERROR: 文件不存在: {src}", file=sys.stderr)
        return 2
    rows = read_csv(src)
    if not rows:
        print("ERROR: CSV 无数据行（先跑 ai_detector --batch DIR --csv）", file=sys.stderr)
        return 2
    out = Path(args.output) if args.output else src.with_suffix(".html")
    out.write_text(render(rows, src), encoding="utf-8")
    s = summarize(rows)
    print(f"报告: {out}")
    print(f"汇总: {s['total']} 文件｜均分 {s['mean']}｜high {s['bands']['high']} / "
          f"medium {s['bands']['medium']} / low {s['bands']['low']}"
          f"｜ERROR {len(s['errors'])}｜unknown {len(s['unknown'])}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
