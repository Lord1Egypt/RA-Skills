# -*- coding: utf-8 -*-
"""stylecheck.py — 风格画像（v2.6.0）：style_guide 七步法的量化验收放大镜。

回答「深改还剩哪里没改干净」：段落级黑话定位 + 句长节奏 + 开场词多样性 +
逐项档位（自然/观察/偏机器，阈值用 dev 仓库四语料校准）+ 指南锚点。
--compare 给改前改后两份画像的差值——深改验收从「凭感觉」变成「看指标」。

口径与诚实声明：
- 画像只做验收提示，不改评分（评分归 scan，档位只标注不拦截）；
- 阈值出自本地语料校准，非任何外部检测口径；短文本（<8 句）的多样性
  指标不判档。

用法:
    python scripts/stylecheck.py draft.txt
    python scripts/stylecheck.py draft.txt --json
    python scripts/stylecheck.py 原稿.txt 改稿.txt --compare
退出码: 0 完成 | 2 用法/文件错误
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core

_BAND_ORDER = {"自然": 0, "观察": 1, "偏机器": 2}
_METRIC_NAMES = {"jargon_1k": "黑话密度（每千字）", "sent_cv": "句长变异系数",
                 "band_conc": "句长带集中度（规整文体也会偏高）",
                 "opener_top": "最高频句首占比", "opener_streak": "最长连续同开场"}


def _read(path):
    try:
        return hxt_core.read_text(path)
    except OSError as e:
        hxt_core.fail("无法读取 %s" % path, hint="检查文件路径与权限；%s" % e)
    except ValueError as e:
        hxt_core.fail(str(e))


def render(profile, source=""):
    m = _METRIC_NAMES
    lines = ["# 风格画像：%s" % (source or "(stdin)"), ""]
    lines.append("> style_guide 七步法的量化验收；档位出自本地语料校准，"
                 "非任何外部检测口径。")
    lines.append("")
    lines.append("## 总览")
    lines.append("")
    lines.append("- %d 段 / %d 句" % (profile["n_paras"], profile["n_sents"]))
    lines.append("")
    lines.append("| 指标 | 值 | 档位 |")
    lines.append("|---|---|---|")
    for k in ("jargon_1k", "sent_cv", "band_conc", "opener_top", "opener_streak"):
        g = profile["global"][k]
        lines.append("| %s | %s | %s |" % (m[k], g["value"], g["band"]))
    lines.append("")
    if profile["worst_paras"]:
        lines.append("## 重点段落（黑话命中降序）")
        lines.append("")
        for p in profile["paras"]:
            if p["idx"] in profile["worst_paras"]:
                lines.append("- 第 %d 段（%d 字/%d 句，命中 %d）：%s"
                             % (p["idx"], p["chars"], p["sents"],
                                p["jargon_hits"], p["worst_sample"]))
        lines.append("")
    lines.append("## 指南锚点")
    lines.append("")
    for a in profile["advice"]:
        lines.append("- %s" % a)
    lines.append("")
    return "\n".join(lines)


def render_compare(pa, pb, sa, sb):
    m = _METRIC_NAMES
    lines = ["# 风格画像对比：%s → %s" % (sa, sb), ""]
    lines.append("| 指标 | 改前 | 改后 | 档位变化 |")
    lines.append("|---|---|---|---|")
    for k in ("jargon_1k", "sent_cv", "band_conc", "opener_top", "opener_streak"):
        a, b = pa["global"][k], pb["global"][k]
        delta = ""
        if a["band"] != b["band"]:
            delta = "%s → %s" % (a["band"], b["band"])
        elif _BAND_ORDER.get(a["band"], 0) == 0:
            delta = "维持自然"
        lines.append("| %s | %s | %s | %s |" % (m[k], a["value"], b["value"], delta))
    lines.append("")
    hit_a = sum(p["jargon_hits"] for p in pa["paras"])
    hit_b = sum(p["jargon_hits"] for p in pb["paras"])
    lines.append("黑话命中合计：%d → %d（%s%d）"
                 % (hit_a, hit_b, "+" if hit_b >= hit_a else "", hit_b - hit_a))
    sa_, sb_ = pa.get("stats") or {}, pb.get("stats") or {}
    if sa_ and sb_:
        lines.append("")
        lines.append("**统计面板（信息性，看趋势不判档）**")
        lines.append("")
        lines.append("| 统计量 | 改前 | 改后 |")
        lines.append("|---|---|---|")
        for k, label in (("ttr_zh", "TTR（中）"), ("ttr_en", "TTR（英）"),
                         ("func_ratio_zh", "虚词比例（中）"),
                         ("func_ratio_en", "虚词比例（英）")):
            va, vb = sa_.get(k), sb_.get(k)
            if va is not None or vb is not None:
                lines.append("| %s | %s | %s |" % (label, va, vb))
        qa, qb = sa_.get("sent_len_quantiles") or {}, sb_.get("sent_len_quantiles") or {}
        if qa and qb:
            lines.append("| 句长分位 P25/50/75/90 | %s/%s/%s/%s | %s/%s/%s/%s |" % (
                qa.get("p25"), qa.get("p50"), qa.get("p75"), qa.get("p90"),
                qb.get("p25"), qb.get("p50"), qb.get("p75"), qb.get("p90")))
    lines.append("")
    lines.append("> 档位只做验收提示；改稿完整性以 verify.py 为准（exit 0 才算过）。")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="风格画像：style_guide 量化验收（段落级黑话定位+节奏+开场多样性）")
    ap.add_argument("file", nargs="?", help="输入文件（.txt/.md/.docx）；--compare 时传两份")
    ap.add_argument("file2", nargs="?", help="改稿文件（仅 --compare 模式）")
    ap.add_argument("--compare", action="store_true",
                    help="对比模式：file=改前，file2=改后，输出画像差值")
    ap.add_argument("--json", action="store_true", help="JSON 输出（单文件画像）")
    ap.add_argument("--raw-markdown", action="store_true",
                    help="对 .md 输入保留 markdown 标记扫描（缺省 v3.6.0 起自动剥离；"
                         "--compare 恒为原文口径）")
    ap.add_argument("--html", help="生成单文件 HTML 画像报告到此路径（单文件与 --compare 均可用）")
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    if args.compare:
        if args.json:
            hxt_core.fail("--json 仅支持单文件画像模式",
                          hint="去掉 --compare，或去掉 --json")
        if not args.file or not args.file2:
            hxt_core.fail("--compare 需要两份文件：原稿 改稿",
                          hint="python scripts/stylecheck.py 原稿.txt 改稿.txt --compare")
        ta, tb = _read(args.file), _read(args.file2)
        if not ta.strip() or not tb.strip():
            hxt_core.fail("输入为空（原稿或改稿）",
                          hint="--compare 的两份文件都必须是非空文本")
        pa, pb = hxt_core.style_profile(ta), hxt_core.style_profile(tb)
        if args.html:
            import reporter
            try:
                with open(args.html, "w", encoding="utf-8") as hf:
                    hf.write(reporter.render_style_compare(pa, pb, args.file, args.file2))
            except OSError as e:
                hxt_core.fail("无法写入 %s" % args.html, hint="检查路径与权限：%s" % e)
            print("HTML 对比报告已写入 %s" % args.html, file=sys.stderr)
        print(render_compare(pa, pb, args.file, args.file2))
        return
    if not args.file:
        t = sys.stdin.read()
        src = "(stdin)"
    else:
        t = _read(args.file)
        src = args.file
    if not t.strip():
        hxt_core.fail("输入为空", hint="请传入 .txt/.md/.docx 文件或通过管道给文本")
    md_struct = None
    if (not getattr(args, "raw_markdown", False)
            and (args.file or "").lower().endswith((".md", ".markdown"))):
        t, md_struct = hxt_core.strip_markdown(t)
        if not t.strip():
            hxt_core.fail("剥离 markdown 结构后正文为空（纯结构文档）",
                          hint="--raw-markdown 可保留原样扫描")
        profile = hxt_core.style_profile(t)
        profile["md_struct"] = md_struct
    if "profile" not in dir():
        profile = hxt_core.style_profile(t)
    if args.html:
        import reporter
        try:
            with open(args.html, "w", encoding="utf-8") as hf:
                hf.write(reporter.render_style_profile(profile, src))
        except OSError as e:
            hxt_core.fail("无法写入 %s" % args.html, hint="检查路径与权限：%s" % e)
        print("HTML 画像报告已写入 %s" % args.html, file=sys.stderr)
    if args.json:
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        print(render(profile, src))


if __name__ == "__main__":
    hxt_core.cli_entry(main)
