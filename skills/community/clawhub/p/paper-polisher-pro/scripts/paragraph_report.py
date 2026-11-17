#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
paragraph_report — 段落级归因报告（v3 新增，应对人机协作写作的现实）。

文档级平均分在混合人机文本上天然失效（实测混合攻击 AUROC 0.38），
本工具输出逐段判定 HTML：每段独立打分+着色+命中模式，人机分工一目了然。

用法:
  python paragraph_report.py <文本文件> --output report.html [--profile journal]
"""
from pathlib import Path
import os, sys, json, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ai_detector

_TPL_HEAD = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<title>段落级归因报告</title><style>
body{font-family:"Microsoft YaHei",sans-serif;max-width:900px;margin:24px auto;color:#222;line-height:1.7}
.sum{display:flex;gap:10px;margin:14px 0;flex-wrap:wrap}
.b{padding:8px 16px;border-radius:8px;font-size:14px}
.p{margin:10px 0;padding:10px 12px;border-left:4px solid #999;border-radius:4px;white-space:pre-wrap}
.hi{background:#fdecea;border-color:#c0392b}.med{background:#fff6e0;border-color:#c9862b}
.lo{background:#f2f8f2;border-color:#7a9b76}
.tag{font-size:12px;color:#666}
h1{font-size:19px}
</style></head><body>"""
_TPL_FOOT = """<p style="color:#888;font-size:12px">判定阈值来自 fusion_config.json（评测语料人类分布 p95/p99 校准）。
段落判定用于人机协作写作的分工定位；文档级分数不适用于拼接文本（混合攻击实测 AUROC 0.38）。</p><footer style='margin-top:24px;padding-top:12px;border-top:1px solid #eee;color:#9aa0a6;font-size:12px;text-align:center;'>本文档由 Paper Polisher Pro 生成 · <a href='https://github.com/docsor1212/paper-polisher-pro' style='color:#9aa0a6;'>GitHub</a> · <a href='https://skillhub.cn/skills/indiv-sorsor/paper-polisher-pro' style='color:#9aa0a6;'>SkillHub</a> · 觉得有用欢迎 Star / 收藏</footer></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--output", default="paragraph_report.html")
    a = ap.parse_args()

    if not Path(a.file).exists():
        print(f"Error: File not found: {a.file}", file=sys.stderr)
        sys.exit(2)
    text = open(a.file, encoding="utf-8", errors="replace").read()
    rep = ai_detector.detect(text, lang="auto")
    fc = ai_detector._load_fusion_config() or {}
    thr = fc.get("thresholds", {"medium": 0.35, "high": 0.60})
    tm = float(thr["medium"]) * 100
    th = float(thr["high"]) * 100

    paras = ai_detector.split_paragraphs(text)
    blend = ai_detector.blended_paragraph_scores(text, rep)
    rows = []
    n_hi = n_med = 0
    for j, p in enumerate(rep.paragraph_scores):
        idx = min(p.get("index", 0), len(paras) - 1)
        raw = paras[idx] if idx < len(paras) else p.get("text", "")
        s = blend[j] if j < len(blend) else p.get("ai_score", 0)
        cls = "hi" if s >= th else ("med" if s >= tm else "lo")
        n_hi += cls == "hi"
        n_med += cls == "med"
        pats = "、".join(m["pattern"][:14] for m in p.get("matched_patterns", [])[:4]) or "-"
        rows.append('<div class="p %s"><span class="tag">段落%d · 融合%.0f分 · %s · 命中: %s</span><br>%s</div>' %
                    (cls, p.get("index", 0) + 1, s,
                     {"hi": "疑似AI", "med": "存疑", "lo": "倾向人类"}[cls], pats,
                     raw[:600]))
    total = max(len(rep.paragraph_scores), 1)
    html = (_TPL_HEAD +
            "<h1>段落级归因报告 <small style='color:#888'>paper-polisher v3</small></h1>" +
            '<div class="sum">'
            '<div class="b" style="background:#fdecea">疑似AI段落 %d (%.0f%%)</div>'
            '<div class="b" style="background:#fff6e0">存疑段落 %d (%.0f%%)</div>'
            '<div class="b" style="background:#f2f8f2">倾向人类 %d (%.0f%%)</div></div>'
            "<p>文档级分数: <b>%.1f</b>（%s）%s</p>"
            "<p style='color:#666'>学术诚信提示：本报告供作者自查与改进写作质量，不用于规避机构的 AIGC 检测；"
            "请遵循所在机构的 AI 使用与披露政策。</p>" %
            (n_hi, 100 * n_hi / total, n_med, 100 * n_med / total,
             total - n_hi - n_med, 100 * (total - n_hi - n_med) / total,
             rep.overall_ai_score, rep.overall_risk,
             ("｜指纹归因: " + ", ".join("%s(%.0f%%)" % (h["family"], h["confidence"] * 100)
                                        for h in rep.model_hints)) if rep.model_hints else "") +
            "".join(rows) + _TPL_FOOT)
    # v4.1: 与 JSON 报告一致的披露行（诚信/混写/平滑度——有信号才显示）
    _disc = []
    if getattr(rep, "mixed_signal", False):
        _disc.append("⚠️ 混写预警：" + (rep.mixed_notice or "")[:80])
    if getattr(rep, "register_hint", ""):
        _disc.append("ℹ️ " + rep.register_hint[:80])
    if getattr(rep, "encoding_warning", ""):
        _disc.append("⚠️ " + rep.encoding_warning[:80])
    if _disc:
        html = html.replace("学术诚信提示", " ".join(_disc) + "<br>学术诚信提示", 1)
    with open(a.output, "w", encoding="utf-8") as f:
        f.write(html)
    print("段落: %d | 疑似AI %d | 存疑 %d | 倾向人类 %d | 文档分 %.1f" %
          (total, n_hi, n_med, total - n_hi - n_med, rep.overall_ai_score))
    if rep.model_hints:
        print("指纹归因:", ", ".join("%s(%.0f%%)" % (h["family"], h["confidence"] * 100)
                                     for h in rep.model_hints))
    print("报告: %s" % a.output)


if __name__ == "__main__":
    import sys as _sys
    try:  # v3.5: 中文 Windows 默认 GBK 控制台会因 emoji/警示符崩溃 stdout——统一 UTF-8
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
