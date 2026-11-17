#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_evidence_report.py — 检测证据报告（v6.6.0 新增；pp.py evidence）

真实场景：作者被质疑「是不是 AI 写的」时，需要一份**如实呈现判定与证据**的
可交付文档——给自己存档，或向导师/编辑/机构说明。本工具把一次检测的完整证据
链渲染成自包含 HTML + Markdown 双形态报告：

  结论卡（分数/风险带/引擎档位/模型指纹/时间）
  → 特征证据明细（逐个命中特征：出现次数 + 定位摘录）
  → 段落分级表（每段分数与风险带）
  → 指纹归因与监督层分布（若在位）
  → 阈值与校准口径（risk_bands 原样呈现）
  → 局限声明（固定：医学高估/人机混写/英文参考/短文本铁律）
  → 学术诚信声明（固定）+ 复现信息（版本/指纹/命令行）

诚实边界（写在报告头与页脚，不可关闭）：本报告如实呈现引擎判定与证据，
供作者自查与说明用途；**不构成「未使用 AI」的任何证明**；分数为引擎口径
相对参考，不与任何机构检测器等价。零依赖（标准库）；引擎与 CLI 完全同源。
用法:
  python3 scripts/pp_evidence_report.py draft.txt --outdir evidence/
  python3 scripts/pp_evidence_report.py draft.docx --html only.html
  python3 scripts/pp.py evidence draft.txt
"""
import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent

_LIMIT = ("局限声明（固定内容，如实呈现）:①降级档（未装监督层）对医学语域系统性高估"
          "（@medium 人类误报约 59%）——医学内容仅采信 @high 档或安装监督层；"
          "②人机混写文档的段落归因仅供人工复核（文档级 AUROC 0.52-0.54，原理性局限）；"
          "③英文文本走纯规则骨架评分，结论仅供参考；④不足 100 字不出判定（短文本铁律）。")
_INTEGRITY = ("学术诚信声明（固定内容）:本报告由 Paper Polisher Pro 生成，供作者自查与"
              "改进写作质量，如实呈现引擎判定与证据；不用于规避机构 AIGC 检测，"
              "不构成「未使用 AI」的任何证明；分数为引擎口径相对参考，不与任何机构"
              "检测器等价。请遵循所在机构的 AI 使用与披露政策。")

_CSS = """
body{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;margin:24px;color:#222;max-width:960px}
h1{font-size:20px}h2{font-size:16px;margin-top:26px;border-left:4px solid #2E5E8F;padding-left:8px}
table{border-collapse:collapse;width:100%;font-size:13px;margin-top:10px}
th,td{border:1px solid #ddd;padding:5px 8px;text-align:left}
th{background:#f5f5f5}.badge{color:#fff;border-radius:3px;padding:1px 8px;font-size:12px}
.card{border:1px solid #e3e3e3;border-radius:6px;padding:12px 18px;margin:12px 0;display:flex;gap:28px;flex-wrap:wrap}
.card b{font-size:26px;display:block}
.muted{color:#888;font-size:12px}.note{color:#555;font-size:13px}
.decl{border:1px solid #e8d9a0;background:#fdf9ec;border-radius:6px;padding:10px 14px;margin:10px 0;font-size:13px}
code{background:#f4f4f4;padding:1px 5px;border-radius:3px;font-size:12px}
.ctx{color:#666}
mark{background:#ffe89c;padding:0 2px}
"""


def _supervised_fp():
    """监督模型指纹（pp_setup 同源逻辑：cache 模型 md5_12 + 注册表版本核对）。"""
    try:
        sys.path.insert(0, str(HERE))
        from pp_setup import md5_12
        cache = Path.home() / ".cache" / "paper-polisher" / "qwen3-detector" / "model.int8.onnx"
        if not cache.is_file():
            return "未安装（降级档）"
        got = md5_12(cache)
        reg = json.loads((HERE.parent / "references" / "supervised_models.json")
                         .read_text(encoding="utf-8"))
        for m in reg.get("models", []):
            if m.get("md5_12") == got:
                return f"{got}（签发版 {m.get('id', '?')}）"
        return f"{got}（未在签发注册表内）"
    except Exception:
        return "获取失败"


def run_detect(path):
    """引擎同源：subprocess 调 ai_detector --format json。"""
    p = subprocess.run([sys.executable, str(HERE / "ai_detector.py"), str(path),
                        "--format", "json"], capture_output=True, timeout=600,
                       text=True, encoding="utf-8", errors="replace")
    if p.returncode not in (0, 1) or not p.stdout.strip():
        raise RuntimeError(f"引擎退出码 {p.returncode}: {p.stderr[-200:]}")
    return json.loads(p.stdout)


def _sentences(text):
    return [s for s in re.split(r"(?<=[。！？!?；;])\s*", text) if s.strip()]


def _locate(pattern, text, limit=3):
    """特征在原文中的定位摘录（最多 limit 句，每句高亮命中）。"""
    hits = []
    for s in _sentences(text):
        if pattern in s and len(hits) < limit:
            frag = html.escape(s.strip())[:160]
            hits.append(frag.replace(html.escape(pattern),
                                     f"<mark>{html.escape(pattern)}</mark>"))
        if len(hits) >= limit:
            break
    return hits


def build_sections(d, src_text, src_name):
    """从 detect JSON 组织报告区块（返回 [(title, html)]）。"""
    secs = []
    # 特征证据明细
    rows = []
    for tp in d.get("top_patterns", []):
        pat = tp.get("pattern", "?")
        cnt = tp.get("count", 0)
        locs = _locate(pat, src_text)
        rows.append(f"<tr><td><b>{html.escape(pat)}</b></td><td>{cnt}</td>"
                    f"<td>{('<br>'.join('…' + x + '…' for x in locs)) or '<span class=muted>（长文本摘录略）</span>'}</td></tr>")
    if rows:
        secs.append(("特征证据明细（逐特征出现次数与原文定位）",
                     "<table><tr><th>特征</th><th>次数</th><th>定位摘录（高亮）</th></tr>"
                     + "".join(rows) + "</table>"))
    else:
        secs.append(("特征证据明细", "<p class=muted>本次判定未命中任何已知特征。</p>"))
    # 段落分级
    paras = d.get("paragraph_scores", [])
    if paras:
        rows = []
        for i, p in enumerate(paras[:20], 1):
            c = {"high": "#c0392b", "medium": "#e67e22", "low": "#27ae60",
                 "unknown": "#7f8c8d"}.get(p.get("class", p.get("risk", "")), "#7f8c8d")
            rows.append(f"<tr><td>第 {i} 段</td>"
                        f"<td><span class='badge' style='background:{c}'>{html.escape(str(p.get('class', p.get('risk', '?'))))}</span></td>"
                        f"<td>{p.get('score', p.get('ai_score', '—'))}</td>"
                        f"<td class='ctx'>{html.escape(str(p.get('excerpt', p.get('text', '')))[:80])}…</td></tr>")
        secs.append(("段落分级（前 20 段）",
                     "<table><tr><th>段</th><th>风险带</th><th>分</th><th>摘录</th></tr>"
                     + "".join(rows) + "</table>"))
    # 指纹归因 + 监督层
    hints = d.get("model_hints") or []
    sup = d.get("supervised") or {}
    bits = []
    if hints:
        bits.append("<p>模型指纹归因（仅提示，不参与分数）：<b>"
                    + "</b>、<b>".join(html.escape(f"{h.get('model', '?')} ({h.get('p', 0):.2f})")
                                       if isinstance(h.get('p'), (int, float))
                                       else html.escape(str(h)) for h in hints[:5])
                    + "</b></p>")
    if sup:
        bits.append(f"<p>监督层分布：p(人类)={sup.get('p_human', '—')}｜p(AI)={sup.get('p_ai', '—')}｜"
                    f"p(AI辅助)={sup.get('p_ai_assisted', '—')}｜层={html.escape(str(sup.get('layer', '—')))}</p>")
    if d.get("degraded_mode"):
        bits.append(f"<p class='note'>⚠️ 当前为降级档（未装监督层）：{html.escape(d.get('degraded_notice', ''))}</p>")
    if bits:
        secs.append(("归因与监督层", "".join(bits)))
    # 阈值与校准
    rb = d.get("risk_bands") or {}
    if rb:
        secs.append(("阈值与校准口径（原样呈现）",
                     f"<p>medium ≥ {rb.get('medium', '—')}｜high ≥ {rb.get('high', '—')}｜"
                     f"校准：{html.escape(str(rb.get('calibration', '—')))}<br>"
                     f"<span class=muted>{html.escape(str(rb.get('note', '')))}</span></p>"))
    return secs


def render_html(d, secs, src_name, out_path):
    score = d.get("overall_ai_score", "—")
    risk = d.get("overall_risk", "unknown")
    color = {"high": "#c0392b", "medium": "#e67e22", "low": "#27ae60",
             "unknown": "#7f8c8d"}.get(risk, "#7f8c8d")
    fp = _supervised_fp()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    parts = [f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>检测证据报告 · {html.escape(src_name)}</title><style>{_CSS}</style></head><body>
<h1>检测证据报告</h1>
<p class=muted>生成时间 {now} ｜ 文稿 {html.escape(src_name)} ｜ 由 Paper Polisher Pro 引擎如实生成</p>
<div class="decl"><b>报告定位</b>：本报告如实呈现引擎判定与证据，供作者自查与说明用途；
不构成「未使用 AI」的任何证明；分数为引擎口径相对参考，不与任何机构检测器等价。</div>
<div class="card"><div><b style="color:{color}">{score}</b><span class=muted>引擎分（0-100）</span></div>
<div><span class="badge" style="background:{color};font-size:14px;padding:3px 12px">{html.escape(str(risk))}</span>
<span class=muted>风险带</span></div>
<div><b style="font-size:16px">{html.escape(str(d.get('language', '—')))}／{"监督档" if not d.get("degraded_mode") else "降级档"}</b>
<span class=muted>语言／档位</span></div>
<div><b style="font-size:14px">{html.escape(str(fp)[:16])}</b><span class=muted>模型指纹</span></div></div>"""]
    for title, body in secs:
        parts.append(f"<h2>{title}</h2>\n{body}")
    parts.append(f"""<h2>局限声明</h2><div class="decl">{_LIMIT.replace('①', '<br>①').replace('②', '<br>②').replace('③', '<br>③').replace('④', '<br>④').split(':', 1)[1]}</div>
<h2>学术诚信声明</h2><div class="decl">{_INTEGRITY.split(':', 1)[1]}</div>
<h2>复现信息</h2><p class=muted>引擎与 CLI 同源。复现命令：<code>python3 scripts/ai_detector.py {html.escape(src_name)} --format json</code>
｜模型指纹 {html.escape(str(fp))}｜环境自检 <code>pp.py doctor</code>。同稿同档同版本应逐位一致——不一致即 bug。</p>
<p class="muted">Paper Polisher Pro · 检测证据报告 · 页脚诚信声明为报告组成部分</p></body></html>""")
    out_path.write_text("\n".join(parts), encoding="utf-8")


def render_md(d, secs, src_name, out_path):
    score = d.get("overall_ai_score", "—")
    risk = d.get("overall_risk", "unknown")
    fp = _supervised_fp()
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# 检测证据报告 · {src_name}",
             "",
             f"> 生成时间 {now}｜引擎如实生成。**报告定位**：如实呈现判定与证据，供作者自查与说明用途；"
             "不构成「未使用 AI」的任何证明；分数为引擎口径相对参考，不与任何机构检测器等价。",
             "",
             f"- **引擎分**：{score}（0-100）｜**风险带**：{risk}｜**语言/档位**：{d.get('language', '—')}"
             f"／{'监督档' if not d.get('degraded_mode') else '降级档'}｜**模型指纹**：`{fp}`",
             ""]
    for title, body in secs:
        # HTML 区块转简明 MD（表格行提取）
        rows = re.findall(r"<tr><td>(.*?)</td>(.*?)</tr>", body, re.S)
        lines.append(f"## {title}")
        lines.append("")
        if rows:
            for first, rest in rows[:20]:
                cells = [re.sub(r"<[^>]+>", " ", c).strip() for c in
                         re.findall(r"<td>(.*?)</td>", "<td>" + first + rest)]
                lines.append("- " + "｜".join(x.replace("\n", " ") for x in cells))
        else:
            txt = re.sub(r"<[^>]+>", "", body).strip()
            lines.append(txt[:600])
        lines.append("")
    lines += ["## 局限声明", "", _LIMIT.replace(':①', '：\n\n①'), "",
              "## 学术诚信声明", "", _INTEGRITY.replace(':本', '：\n\n本'), "",
              "## 复现信息", "",
              f"- 复现命令：`python3 scripts/ai_detector.py {src_name} --format json`",
              f"- 模型指纹：`{fp}`｜环境自检：`pp.py doctor`",
              "- 同稿同档同版本应逐位一致——不一致即 bug。",
              "",
              "---",
              "",
              "Paper Polisher Pro · 检测证据报告 · 诚信声明为报告组成部分"]
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description="检测证据报告（HTML+Markdown，如实呈现判定与证据）")
    ap.add_argument("input", help="文稿（txt/md/docx）")
    ap.add_argument("--outdir", default=None, help="输出目录（默认与输入同目录）")
    ap.add_argument("--html", metavar="PATH", default=None, help="仅输出 HTML 到指定路径")
    ap.add_argument("--md", metavar="PATH", default=None, help="仅输出 MD 到指定路径")
    a = ap.parse_args()

    src = Path(a.input)
    if not src.is_file():
        print(f"Error: file not found: {a.input}", file=sys.stderr)
        sys.exit(2)  # 退出码契约：输入错误=2
    from docx_text import read_text_any
    text = read_text_any(src)
    if len(text.strip()) < 100:
        print("短文本（<100 字）按铁律不出判定，证据报告无意义——请提交 100 字以上文稿。", file=sys.stderr)
        sys.exit(2)
    d = run_detect(src)
    stem = src.stem
    if a.html or a.md:
        outs = []
        if a.html:
            render_html(d, build_sections(d, text, src.name), src.name, Path(a.html))
            outs.append(a.html)
        if a.md:
            render_md(d, build_sections(d, text, src.name), src.name, Path(a.md))
            outs.append(a.md)
    else:
        outdir = Path(a.outdir) if a.outdir else src.parent
        outdir.mkdir(parents=True, exist_ok=True)
        h = outdir / f"{stem}.evidence.html"
        m = outdir / f"{stem}.evidence.md"
        render_html(d, build_sections(d, text, src.name), src.name, h)
        render_md(d, build_sections(d, text, src.name), src.name, m)
        outs = [str(h), str(m)]
    print(f"证据报告已生成（{d.get('overall_ai_score', '—')}/{d.get('overall_risk', '—')}）：")
    for o in outs:
        print(f"  {o}")
    print("定位：如实呈现判定与证据，供自查与说明；不构成「未使用 AI」的证明（详见报告内声明）。")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
