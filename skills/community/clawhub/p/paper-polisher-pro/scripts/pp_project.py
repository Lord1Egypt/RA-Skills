#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_project.py — 项目工作台（v6.9.0 新增；pp.py project）

真实场景：学位论文/书稿/课题组报告 = 一个目录里的多个章节文件。此前要自己
编排「逐文件 workflow + 跨文件术语一致性 + 汇总对照」三步；本工具一条命令
完成项目级自查并产出总览：

  1. 逐文件完整自查（引擎与 pp_workflow 同源，进程内调用）——每文件
     workflow.json/.md 照常落盘，单文件失败只损失该文件行（与批量同哲学）
  2. 项目聚合：分数/风险带/段落分级/门禁逐文件对照表 + 项目级统计
  3. 跨文件术语一致性（pp_term_consistency.analyze 同源）——库内概念
     写法矩阵与统一建议内嵌进总览
  4. 项目总览 HTML（自包含）+ JSON（机读）——给作者的全稿驾驶舱

诚实边界（固定）：分数为引擎口径相对参考；项目总览供作者自查与改进写作，
不构成任何「合规证明」或「未使用 AI」的证明；一致性维度只覆盖术语库内概念。
零依赖（标准库）；全部引擎同源，无新打分代码。
用法:
  python3 scripts/pp_project.py 章节目录/ --outdir project_report/
  python3 scripts/pp.py project 章节目录/
"""
import argparse
import html
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

_INTEGRITY = ("学术诚信：项目总览由 Paper Polisher Pro 生成，供作者自查与改进写作质量；"
              "分数为引擎口径相对参考，不构成任何合规证明或「未使用 AI」的证明；"
              "一致性维度只覆盖术语库内概念。请遵循所在机构的 AI 使用与披露政策。")


def _iter_files(d, recursive=False):
    it = d.rglob("*") if recursive else d.iterdir()
    return sorted(f for f in it
                  if f.is_file() and f.suffix.lower() in (".txt", ".md", ".docx")
                  and f.stat().st_size < 5 * 1024 * 1024)


def run_project(dir_path, outdir, recursive=False, lang="auto"):
    from docx_text import read_text_any, DocxError
    from pp_workflow import workflow
    import pp_term_consistency as ptc

    d = Path(dir_path)
    files = _iter_files(d, recursive)
    if len(files) < 2:
        print("项目模式需要目录内至少 2 份文稿（txt/md/docx）——单文件直接跑 "
              "python3 scripts/pp.py workflow <文件>", file=sys.stderr)
        sys.exit(2)  # 退出码契约：输入错误=2
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    per_file = []
    for f in files:
        row = {"file": f.name}
        try:
            text = read_text_any(f)
            if len(text.strip()) < 100:
                row.update(note="insufficient text (<100 chars)", risk="unknown")
            else:
                r = workflow(text, lang=lang)
                jf = outdir / (f.stem + ".workflow.json")
                mf = outdir / (f.stem + ".workflow.md")
                jf.write_text(json.dumps(r, ensure_ascii=False, indent=2),
                              encoding="utf-8")
                from pp_workflow import to_markdown
                mf.write_text(to_markdown(r), encoding="utf-8")
                det = r["detect"]
                row.update(score=det.get("overall_ai_score"),
                           risk=det.get("overall_risk"),
                           hi=r["paragraphs"]["high"], med=r["paragraphs"]["medium"],
                           total=r["paragraphs"]["total"],
                           gate_verdict=r["gate"].get("verdict"),
                           gate_score=r["gate"].get("composite_ai_risk"),
                           report=str(mf.name))
        except DocxError as e:
            from pp_errors import render
            title, _ = render(e)
            row.update(error=title)
        except Exception as e:
            # 单文件失败不炸项目（与批量同哲学）；错误经人话化
            try:
                from pp_errors import render
                title, _ = render(e)
            except Exception:
                title = f"{type(e).__name__}: {e}"[:120]
            row.update(error=title)
        per_file.append(row)

    # 跨文件术语一致性（同源复用：直接对源目录分析）
    try:
        tc = ptc.analyze(str(d), recursive=recursive)
        tc_matrix = tc["matrix"]
        tc_inconsistent = [m for m in tc_matrix if m["inconsistent"]]
    except SystemExit:
        tc_matrix, tc_inconsistent = [], []

    scored = [r for r in per_file if isinstance(r.get("score"), (int, float))]
    agg = {
        "files": len(files),
        "scored": len(scored),
        "failed": sum(1 for r in per_file if "error" in r),
        "short": sum(1 for r in per_file if r.get("note")),
        "mean_score": round(sum(r["score"] for r in scored) / len(scored), 1) if scored else None,
        "max_score": max((r["score"] for r in scored), default=None),
        "high_risk_files": sum(1 for r in scored if r.get("risk") == "high"),
        "inconsistent_concepts": len(tc_inconsistent),
    }
    return {"directory": str(d), "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "aggregate": agg, "per_file": per_file,
            "term_matrix": tc_matrix,
            "integrity_notice": _INTEGRITY}


_CSS = """body{font-family:-apple-system,'PingFang SC',sans-serif;margin:24px;color:#222;max-width:1060px}
h1{font-size:20px}h2{font-size:16px;margin-top:26px;border-left:4px solid #2E5E8F;padding-left:8px}
table{border-collapse:collapse;width:100%;font-size:13px;margin-top:10px}
th,td{border:1px solid #ddd;padding:5px 8px;text-align:left;vertical-align:top}
th{background:#f5f5f5}.badge{color:#fff;border-radius:3px;padding:1px 8px;font-size:12px}
.bad{background:#fdecea}.ok{background:#eef7ee}
.cards{display:flex;gap:12px;margin:14px 0;flex-wrap:wrap}
.card{border:1px solid #e3e3e3;border-radius:6px;padding:10px 16px;min-width:120px}
.card b{font-size:22px;display:block}
.note{color:#777;font-size:12px;margin-top:14px}
.decl{border:1px solid #e8d9a0;background:#fdf9ec;border-radius:6px;padding:10px 14px;font-size:13px}"""


def render_html(r, out_path):
    agg = r["aggregate"]
    color = {"high": "#c0392b", "medium": "#e67e22", "low": "#27ae60",
             "unknown": "#7f8c8d"}
    rows = []
    for p in r["per_file"]:
        if "error" in p:
            rows.append(f"<tr class='bad'><td>{html.escape(p['file'])}</td>"
                        f"<td colspan=5>❌ {html.escape(p['error'])}</td></tr>")
            continue
        if p.get("note"):
            rows.append(f"<tr><td>{html.escape(p['file'])}</td><td colspan=5>⚪ 过短不判定</td></tr>")
            continue
        c = color.get(p["risk"], "#7f8c8d")
        rows.append(f"<tr class='{'bad' if p['risk']=='high' else 'ok'}'>"
                    f"<td>{html.escape(p['file'])}</td>"
                    f"<td><b>{p['score']}</b></td>"
                    f"<td><span class='badge' style='background:{c}'>{p['risk']}</span></td>"
                    f"<td>{p['hi']}/{p['med']}/{p['total']}</td>"
                    f"<td>{html.escape(str(p['gate_verdict']))}（{p['gate_score']}）</td>"
                    f"<td><span class=muted>{html.escape(str(p['report']))}</span></td></tr>")
    inc_rows = []
    for m in r["term_matrix"]:
        if not m["inconsistent"]:
            continue
        vs = "；".join(f"「{html.escape(s)}」@ {html.escape(','.join(fs))}"
                       for s, fs in m["variants"].items())
        inc_rows.append(f"<tr class='bad'><td><b>{html.escape(m['concept'])}</b></td>"
                        f"<td>{vs}</td><td>统一为「{html.escape(m['recommend'])}」"
                        f"<br><span class=note>{html.escape(m['basis'])}</span></td></tr>")
    ok_terms = [m for m in r["term_matrix"] if not m["inconsistent"]]
    out_path.write_text(f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>项目自查总览</title><style>{_CSS}</style></head><body>
<h1>项目自查总览</h1>
<p class=note>生成于 {r['generated_at']} ｜ 目录 {html.escape(r['directory'])}</p>
<div class="cards">
<div class="card"><b>{agg['files']}</b><span class=note>文稿</span></div>
<div class="card"><b style="color:{color.get('high')}">{agg['high_risk_files']}</b><span class=note>高风险文件</span></div>
<div class="card"><b>{agg['mean_score'] if agg['mean_score'] is not None else '—'}</b><span class=note>均分</span></div>
<div class="card"><b style="color:{'#c0392b' if agg['inconsistent_concepts'] else '#27ae60'}">{agg['inconsistent_concepts']}</b><span class=note>术语跨文件不一致</span></div>
<div class="card"><b>{agg['failed']}</b><span class=note>失败/跳过</span></div>
</div>
<h2>逐文件总览</h2>
<table><tr><th>文件</th><th>分</th><th>风险带</th><th>段落 高/中/全</th><th>门禁</th><th>详细报告</th></tr>
{''.join(rows)}</table>
<h2>跨文件术语不一致（{agg['inconsistent_concepts']}）</h2>
<table><tr><th>概念</th><th>写法 @ 文件</th><th>统一建议</th></tr>
{''.join(inc_rows) or '<tr><td colspan=3>✓ 未发现</td></tr>'}</table>
""" + (f"<h2>一致概念（{len(ok_terms)}）</h2><p class=note>{html.escape('、'.join(m['concept'] for m in ok_terms[:30]))}"
       f"{'…' if len(ok_terms) > 30 else ''}</p>" if ok_terms else "") + f"""
<div class="decl" style="margin-top:18px">{_INTEGRITY}</div>
<p class=note>每文件的完整自查报告（workflow.md/.json）在同目录；单文件深读用 pp.py explain。</p>
<p class=note>Paper Polisher Pro · 项目自查总览 · 诚信声明为报告组成部分</p>
</body></html>""", encoding="utf-8")


def print_text(r):
    agg = r["aggregate"]
    print(f"项目自查: {agg['files']} 份文稿（可评 {agg['scored']}，失败 {agg['failed']}，过短 {agg['short']}）")
    print(f"均分 {agg['mean_score']} ｜ 最高 {agg['max_score']} ｜ 高风险文件 {agg['high_risk_files']}"
          f" ｜ 术语跨文件不一致 {agg['inconsistent_concepts']}")
    print("─" * 60)
    for p in r["per_file"]:
        if "error" in p:
            print(f"  [错误] {p['file']}: {p['error'][:50]}")
        elif p.get("note"):
            print(f"  [过短] {p['file']}: 不判定")
        else:
            mark = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(p["risk"], "·")
            print(f"  {mark} {p['score']:5.1f} {p['risk']:7s} {p['file']}")
    for m in r["term_matrix"]:
        if m["inconsistent"]:
            vs = "；".join(f"「{s}」@ {','.join(fs)}" for s, fs in m["variants"].items())
            print(f"◆ 术语不一致 {m['concept']}：{vs} → 建议统一「{m['recommend']}」")
    print("─" * 60)
    print(_INTEGRITY)


def main():
    ap = argparse.ArgumentParser(description="项目工作台：目录级全套自查+术语一致性+总览报告")
    ap.add_argument("directory", help="章节目录（≥2 份 txt/md/docx）")
    ap.add_argument("--outdir", default=None, help="产物目录（默认 <目录>/_project/）")
    ap.add_argument("--recursive", action="store_true", help="递归子目录")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    ap.add_argument("--json", action="store_true", help="输出 JSON 摘要（stdout）")
    a = ap.parse_args()
    d = Path(a.directory)
    if not d.is_dir():
        print(f"Error: not a directory: {a.directory}", file=sys.stderr)
        sys.exit(2)
    outdir = Path(a.outdir) if a.outdir else d / "_project"
    r = run_project(d, outdir, recursive=a.recursive, lang=a.lang)
    sj = outdir / "project_summary.json"
    sj.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    oh = outdir / "project_overview.html"
    render_html(r, oh)
    print(f"项目总览: {oh}", file=sys.stderr)
    print(f"项目摘要: {sj}", file=sys.stderr)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print_text(r)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
