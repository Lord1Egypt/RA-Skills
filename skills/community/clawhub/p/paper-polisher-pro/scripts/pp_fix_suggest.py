#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_fix_suggest.py — 句子级改写建议引擎（v5.0.0 新增）

定位：检测工具告诉你「这篇像 AI / 哪些段像」，本脚本回答下一步的自然问题——
「具体哪几句、因为什么、往哪个方向改」。只指位 + 给策略，不代写、不自动改写
（自动改写既超出规则引擎能力，也不符合学术诚信定位：改写决定权在作者本人）。

逐句扫描七类特征（全部复用引擎既有模式库/统计口径，零新增依赖）：
  1. ai_cliche        AI 套话/陈词滥调（最强信号，换具体表述或删）
  2. filler           AI 高频填充短语（值得注意的是/综上所述…，删或并入前句）
  3. template         模板句式（不仅…而且 / 一方面…另一方面 / 进行了…分析 等，拆分或改主动陈述）
  4. vague            模糊限定（在一定程度上/总体而言…，给出可量化的具体表述方向）
  5. connective       连接词开头密度（此外/然而/同时…，建议变换句首）
  6. punctuation      标点习惯（破折号/冒号强调滥用，改逗号、括号或拆句）
  7. rhythm           节律（本句与邻句长度高度接近=均匀节律，建议长短句交错）

输出：
  - 文本报告：逐句「原句 + 问题清单 + 改写策略」，文末给全篇分布与总体建议
  - --json：结构化 suggestions（下游/程序化使用），含 integrity_notice 学术诚信声明

用法:
  python3 pp_fix_suggest.py <file> [--top N] [--json] [--lang auto]
  python3 pp_fix_suggest.py --demo            # 内置双样例演示
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

_INTEGRITY = ("学术诚信：本建议供作者自查与改进写作质量，改写与否由作者决定；"
              "请按所在机构政策规范披露 AI 使用。")

# 连接词开头（句首 0-2 字符内出现即算"连接词开头"）
_CONNECTIVES = ["此外", "同时", "然而", "与此同时", "因此", "其次", "首先",
                "总之", "综上", "另外", "进一步", "基于此", "由此可见",
                "Moreover", "However", "Furthermore", "In addition", "Therefore"]

# 破折号/冒号强调习惯
_DASH_RE = re.compile(r"——|--|—")
_COLON_EMPH_RE = re.compile(r"：[^，。；]{2,30}(?:——|：)")

# 类别 → 改写策略（用户可直接照做）
ADVICE = {
    "ai_cliche": ("AI 套话（最强特征）。策略：删掉或换成你自己的具体判断——"
                  "写清「谁/对什么/量化如何」，不使用泛化评价词。"),
    "filler": ("AI 高频填充短语。策略：多数可直接删除；需要保留逻辑时并入前句，"
               "用「具体到本研究：…」式实指替代。"),
    "template": ("模板句式。策略：拆成两个短句或改为主动陈述；"
                 "「不仅…而且」只保留信息量更大的一半；「对X进行了Y分析」改为「我们用Y检验X」式实义动词句。"),
    "translationese": ("翻译腔（英文句法直译痕迹）。策略：被动堆叠改主动句、"
                       "「扮演…角色/发挥着…作用」换成实义动词，长定语拆成短句。"),
    "vague": ("模糊限定语。策略：能量化就量化（比例/例数/阈值）；不能量化就删掉，"
              "让结论强度与证据对齐。"),
    "connective": ("AI 偏好连接词开头。策略：变换句首——用主语开头、用数据开头，"
                   "或把逻辑关系藏进句子结构而非靠连词声明。"),
    "punctuation": ("破折号/冒号强调堆叠。策略：改逗号或括号；一段内破折号≤1 处，"
                    "解释性内容用「即/也就是」自然带出。"),
    "rhythm": ("句子长度过于均匀（AI 节律特征）。策略：本句与邻句合并或拆分，"
               "制造长短交错；关键结论用短句收束。"),
}

# 句首连接词命中数占全文句子比例的超阈值（经验值，超过才提示）
CONNECTIVE_RATIO_ALERT = 0.25


# 模式库原始类别 → 规范 type（映射到 ADVICE 键）
_CAT_TO_TYPE = {
    "ai_cliches": "ai_cliche", "filler_phrases": "filler",
    "vague_expressions": "vague", "redundant_expressions": "template",
    "translationese": "translationese",
}


def _load_categories(lang):
    f = HERE.parent / "references" / f"ai_patterns_{lang}.json"
    if not f.exists():
        return {}
    return json.load(open(f, encoding="utf-8")).get("categories", {})


def _compiled(categories, wanted):
    out = []
    for cat in wanted:
        for p in categories.get(cat, {}).get("patterns", []):
            try:
                out.append((cat, re.compile(p)))
            except re.error:
                continue
    return out


def split_sentences_keep(text):
    """按。！？；(半全角)切句，保留分隔符，过滤纯空白。"""
    parts = re.split(r"(?<=[。！？；!?;])", text)
    return [p for p in (s.strip() for s in parts) if p]


def analyze(text, lang="zh", top=None):
    """返回结构化 suggestions 列表 + 全篇统计。"""
    from ai_detector import detect_lang, split_sentences, sentence_length_stats  # 引擎复用
    if lang == "auto":
        lang = detect_lang(text)
    categories = _load_categories(lang)
    strong = _compiled(categories, ["ai_cliches", "filler_phrases", "vague_expressions",
                                    "redundant_expressions", "translationese"])
    templates = _compiled(categories, ["sentence_structure", "conclusion_patterns",
                                       "medical_templates", "structural_markers"])

    sentences = split_sentences_keep(text) if lang == "zh" else split_sentences(text, lang)
    # 节律参照：邻句长度
    lens = [len(s) for s in sentences]
    results = []
    connective_opens = 0

    for i, sent in enumerate(sentences):
        issues = []
        seen = set()
        for cat, rx in strong:
            m = rx.search(sent)
            if not m or cat in seen:
                continue
            if cat == "redundant_expressions" and re.search(r"[，。；、]", m.group(0)):
                continue  # 「进行了X(Y)」冗余判定只在同一小句内成立；跨小句拼接=模式库已知误报形态
            seen.add(cat)
            issues.append({"type": _CAT_TO_TYPE.get(cat, cat),
                           "evidence": m.group(0)[:40]})
        for cat, rx in templates:
            if "template" in seen:
                break  # 每句只报一个模板句式命中（首个=最强）
            m = rx.search(sent)
            if m:
                seen.add("template")
                seen.add(cat)
                issues.append({"type": "template", "evidence": m.group(0)[:40]})
        # 连接词开头
        head = sent[:6]
        if any(sent.startswith(c) or head.startswith(c) for c in _CONNECTIVES):
            connective_opens += 1
            issues.append({"type": "connective", "evidence": sent[:4]})
        # 标点习惯：破折号每句 ≥1 且全文 ≥2 处才逐句提示；冒号强调同理
        # （局部先记 raw，最后按全文频次过滤）
        if _DASH_RE.search(sent):
            issues.append({"type": "_dash_raw", "evidence": "——"})
        m = _COLON_EMPH_RE.search(sent)
        if m:
            issues.append({"type": "_colon_raw", "evidence": m.group(0)[:20]})
        # 节律：与邻句长度差都 <10% 且三者都 >25 字
        if 0 < i < len(sentences) - 1:
            a, b, c = lens[i - 1], lens[i], lens[i + 1]
            if min(a, b, c) > 25 and abs(a - b) / b < 0.1 and abs(b - c) / c < 0.1:
                issues.append({"type": "rhythm", "evidence": f"{a}/{b}/{c}字"})
        if issues:
            results.append({"index": i, "sentence": sent, "issues": issues})

    # 标点类按全文频次过滤（≥2 处才算习惯）
    n_dash = sum(1 for r in results for x in r["issues"] if x["type"] == "_dash_raw")
    n_colon = sum(1 for r in results for x in r["issues"] if x["type"] == "_colon_raw")
    for r in results:
        keep = []
        for x in r["issues"]:
            t = x["type"]
            if t == "_dash_raw":
                if n_dash >= 2:
                    keep.append({"type": "punctuation", "evidence": "破折号"})
            elif t == "_colon_raw":
                if n_colon >= 2:
                    keep.append({"type": "punctuation", "evidence": x["evidence"]})
            elif t == "connective":
                # 连接词开头按全文占比过滤（低占比不值得逐句打断）
                if connective_opens / max(1, len(sentences)) >= CONNECTIVE_RATIO_ALERT:
                    keep.append(x)
            else:
                keep.append(x)
        r["issues"] = keep
    results = [r for r in results if r["issues"]]

    # 排序：问题多的句子在前（同分按原文顺序）
    results.sort(key=lambda r: (-len(r["issues"]), r["index"]))
    if top:
        results = results[:top]

    stats = {
        "total_sentences": len(sentences),
        "flagged_sentences": len(results),
        "flag_ratio": round(len(results) / max(1, len(sentences)), 3),
        "connective_open_ratio": round(connective_opens / max(1, len(sentences)), 3),
        "type_counts": {},
    }
    for r in results:
        for x in r["issues"]:
            stats["type_counts"][x["type"]] = stats["type_counts"].get(x["type"], 0) + 1
    return results, stats, lang


_TYPE_ZH = {
    "ai_cliche": "AI套话", "filler": "填充短语", "template": "模板句式",
    "vague": "模糊限定", "connective": "连接词开头", "punctuation": "标点习惯",
    "rhythm": "均匀节律", "translationese": "翻译腔",
}


def to_text(results, stats, lang, top):
    lines = []
    if lang == "zh":
        lines.append("── 句子级改写建议 ──")
        if not results:
            lines.append(f"全文 {stats['total_sentences']} 句，未发现可改进特征句"
                         f"（引擎模式库口径）。这不构成「无需润色」的结论——"
                         "通读润稿仍建议由作者本人完成。")
            lines.append(_INTEGRITY)
            return "\n".join(lines)
        lines.append(f"全文 {stats['total_sentences']} 句，其中 {stats['flagged_sentences']} 句"
                     f"存在可改进特征（占比 {stats['flag_ratio']:.0%}）。"
                     f"以下按问题数排序，展示前 {len(results)} 句（--top 可调）。\n")
        for r in results:
            lines.append(f"[句 {r['index'] + 1}] {r['sentence']}")
            for x in r["issues"]:
                name = _TYPE_ZH.get(x["type"], x["type"])
                lines.append(f"  · {name}（{x['evidence']}）")
                lines.append(f"    → {ADVICE[x['type']]}")
            lines.append("")
        tc = stats["type_counts"]
        dist = "、".join(f"{_TYPE_ZH.get(k, k)}×{v}" for k, v in
                         sorted(tc.items(), key=lambda kv: -kv[1]))
        lines.append(f"全篇特征分布：{dist or '无'}")
        lines.append("总体建议：优先处理 AI套话/填充短语（删除成本最低、收益最大）；"
                     "节律与连接词问题在通读润稿时统一处理。")
        lines.append(_INTEGRITY)
    else:
        lines.append("── Sentence-level rewrite suggestions ──")
        if not results:
            lines.append(f"{stats['total_sentences']} sentences scanned; none carried "
                         "improvable features (engine pattern-library criteria). "
                         "This is not a 'no polishing needed' verdict.")
            lines.append(_INTEGRITY)
            return "\n".join(lines)
        lines.append(f"{stats['flagged_sentences']} of {stats['total_sentences']} sentences "
                     f"carry improvable features ({stats['flag_ratio']:.0%}); "
                     f"showing top {len(results)} by issue count.\n")
        for r in results:
            lines.append(f"[#{r['index'] + 1}] {r['sentence']}")
            for x in r["issues"]:
                lines.append(f"  · {x['type']} ({x['evidence']})")
                lines.append(f"    → {ADVICE[x['type']]}")
            lines.append("")
        lines.append(_INTEGRITY)
    return "\n".join(lines)


_DEMO_AI = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
            "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
            "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
            "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
            "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。")
_DEMO_HUMAN = ("我们入组了 2019 到 2021 年间的 47 例患者，其中 6 例随访脱落。"
               "方案提前通过了伦理审查。用药后的头两周最容易出皮疹，"
               "护士站为此专门做了一页交接清单。第三个月复查时，"
               "有位老太太把药掰成了半片——她觉得贵，想省着吃。"
               "这类依从性细节，报表上看不见，只能靠随访时多问一句。")


def run_demo():
    print("=" * 30, "样例 A（AI 感文本）", "=" * 30)
    r, s, lang = analyze(_DEMO_AI)
    print(to_text(r, s, lang, top=None))
    print()
    print("=" * 30, "样例 B（人类感文本）", "=" * 30)
    r, s, lang = analyze(_DEMO_HUMAN)
    print(to_text(r, s, lang, top=None))


def main():
    ap = argparse.ArgumentParser(description="句子级改写建议（指位+策略，不代改）")
    ap.add_argument("file", nargs="?", help="待分析文本文件（UTF-8/GBK 自动容错）")
    ap.add_argument("--top", type=int, default=None, help="只展示问题最多的前 N 句")
    ap.add_argument("--json", action="store_true", help="结构化输出")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    ap.add_argument("--demo", action="store_true", help="内置双样例演示")
    ap.add_argument("--worksheet", metavar="PATH",
                    help="v7.0.0: 另存改稿工作单（Markdown 复选框清单：原句/问题/策略/改后留白）——"
                         "把『指位+策略』变成可逐条执行的改稿文档，改完配 rewrite-check 验收")
    args = ap.parse_args()

    if args.demo:
        run_demo()
        return 0
    if not args.file:
        ap.print_help()
        return 2
    p = Path(args.file)
    if not p.exists():
        print(f"文件不存在: {p}", file=sys.stderr)
        return 2
    from docx_text import read_text_any, DocxError
    try:
        text = read_text_any(p)
    except (DocxError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if len(text.strip()) < 100:
        print("文本不足 100 字符：按铁律不输出任何判定类结论（含改写建议）。", file=sys.stderr)
        return 2
    results, stats, lang = analyze(text, args.lang, args.top)
    if args.json:
        print(json.dumps({
            "file": str(p), "language": lang, "stats": stats,
            "suggestions": [{"index": r["index"] + 1, "sentence": r["sentence"],
                             "issues": [{"type": x["type"], "evidence": x["evidence"],
                                         "advice": ADVICE[x["type"]]} for x in r["issues"]]}
                            for r in results],
            "integrity_notice": _INTEGRITY,
            "notice": "改写建议是排序辅助：指位与策略供人工润稿参考，不构成任何合规判定。",
        }, ensure_ascii=False, indent=1))
    else:
        print(to_text(results, stats, lang, args.top))
    if args.worksheet:
        _write_worksheet(results, stats, Path(args.worksheet), p)
        print(f"改稿工作单: {args.worksheet}", file=sys.stderr)
    return 0


def _write_worksheet(results, stats, out_path, src_path):
    """v7.0.0 改稿工作单：Markdown 复选框清单（不代改——改后内容留白由作者填）。"""
    lines = [f"# 改稿工作单 · {src_path.name}",
             "",
             f"> 生成依据 {stats.get('total_sentences', '?')} 句中的 {stats.get('flagged', len(results))} 句带可改进特征。"
             "逐条处理：读懂问题与策略 → 在「改后」处写你的版本 → 全部完成后用 "
             "`pp.py rewrite-check 原稿 改稿` 验收效果。改不改、怎么改由作者决定。",
             "",
             "| # | 原句 | 问题 | 策略 |",
             "|---|---|---|---|"]
    for i, r in enumerate(results, 1):
        issues = "；".join(f"{x['type']}（{x['evidence']}）" for x in r["issues"][:3])
        sentences = " ".join(r["sentence"].split())[:80]
        advice0 = ADVICE[r["issues"][0]["type"]][:40] if r["issues"] else ""
        lines.append(f"| {i} | {sentences} | {issues} | {advice0} |")
    lines.append("")
    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. 原句")
        lines.append("")
        lines.append(f"> {r['sentence']}")
        lines.append("")
        for x in r["issues"]:
            lines.append(f"- **{x['type']}**：{x['evidence']}")
            lines.append(f"  - 策略：{ADVICE.get(x['type'], '（见 to_text 输出的通用策略）')}")
        lines.append("")
        lines.append("- [ ] 改后：")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("改完验收：`python3 scripts/pp.py rewrite-check 原稿.txt 改稿.txt` ｜ "
                 "多轮复盘：`pp.py trend 轮次目录/`")
    lines.append("")
    lines.append("_学术诚信：本工具不代改——工作单供作者自查与改进写作质量，每个字由作者写；"
                 "请按所在机构政策规范披露 AI 使用。_")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
