#!/usr/bin/env python3
"""sawdust_scan.py — 中文锯末词扫描器（hekouwang-writer-skill）

"锯末词"指 AI 高频产出、读起来有木屑感的中文措辞：连接词、空洞程度词、
营销形容词、模糊量化、口头禅。本脚本只报告，不修改。

判定密度上限：3 处/千字（按 CJK 字符计）。

用法：
    sawdust_scan.py FILE [FILE ...]
    echo "文本" | sawdust_scan.py
    sawdust_scan.py --json FILE      # JSON 输出
    sawdust_scan.py --threshold 5 FILE
    sawdust_scan.py --json --check-contrast FILE   # 假靶心候选标记（opt-in）

退出码：恒为 0（advisory，只报告不阻断）。

--check-contrast 只在显式传入时于 JSON 增加 contrast_candidates 字段；
默认调用（含下游 --json + stdin）输出结构与旧版完全一致。
"""

import argparse
import json
import re
import sys

# 锯末词分类表。词表为本 skill 自建，可按需增补。
CATEGORIES = {
    "ai连接词": [
        "值得注意的是", "值得注意", "综上所述", "不难发现", "换言之", "由此可见",
        "毋庸置疑", "不仅如此", "与此同时", "总的来说",
        "众所周知",
    ],
    "空洞程度词": [
        "非常", "十分", "极其", "极为", "相当", "尤为", "分外", "格外",
    ],
    "营销形容词": [
        "强大", "高效", "卓越", "领先", "一站式", "全方位", "无缝",
        "极致", "顶尖", "顶级", "专业级",
    ],
    "模糊量化": [
        "很多", "大量", "些许", "某些情况下", "某种程度上", "不少",
        "诸多", "各种各样",
    ],
    "口头禅": [
        "其实", "说白了", "老实说", "不得不说", "坦白讲",
    ],
}

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
DEFAULT_THRESHOLD = 3.0  # 处/千字

# 假靶心（Contrast Check）候选模式：只标候选 + 风险提示，不判定。
# 字符类排除分号与换行，避免跨句、跨段误报。group(1) 是被否定的 A。
CONTRAST_PATTERNS = [
    ("不是A，而是B", re.compile(r"不是\s*([^，。；\n]+)[，,]\s*而是")),
    ("并非A，而是B", re.compile(r"并非\s*([^，。；\n]+)[，,]\s*而是")),
    ("A已过时，B才是", re.compile(r"([^。；\n]+)已过时[，,]\s*([^。；\n]+)才是")),
]
# A 含这些无主体泛指词时，提示 agent 优先核对来源。
GENERIC_REFERENTS = ("传统", "过去", "其他产品", "别人", "以前", "别家", "其他工具", "其他厂商")
CONTRAST_NOTE = "候选标记，非判定；是否有据由 agent 按证据纪律核对"


def check_contrast(text):
    """返回假靶心候选列表。只标候选 + risk_hints，绝不判定「A 是否被主张过」。"""
    candidates = []
    for label, pattern in CONTRAST_PATTERNS:
        for m in pattern.finditer(text):
            negated = m.group(1).strip()
            hints = [f"A 含无主体泛指词「{w}」" for w in GENERIC_REFERENTS if w in negated]
            candidates.append({
                "line": text.count("\n", 0, m.start()) + 1,
                "pattern": label,
                "negated": negated,
                "risk_hints": hints,
                "note": CONTRAST_NOTE,
            })
    candidates.sort(key=lambda c: c["line"])
    return candidates


def scan(text):
    """返回 {category: {word: count}} 及命中总数。"""
    findings = {}
    total = 0
    for cat, words in CATEGORIES.items():
        hits = {}
        for w in words:
            n = text.count(w)
            if n:
                hits[w] = n
                total += n
        if hits:
            findings[cat] = hits
    return findings, total


def cjk_len(text):
    return len(CJK_RE.findall(text))


def render(path, text, threshold):
    n_cjk = cjk_len(text)
    findings, total = scan(text)
    density = (total / n_cjk * 1000) if n_cjk else 0.0
    out = []
    out.append(f"文件：{path}")
    out.append(f"中文字数：{n_cjk}    命中总数：{total}    密度：{density:.2f} 处/千字（上限 {threshold:.1f}）")
    out.append("-" * 62)
    if not findings:
        out.append("✅ 无锯末词命中。")
    else:
        for cat, hits in findings.items():
            detail = "、".join(f"{w}×{n}" for w, n in sorted(hits.items(), key=lambda x: -x[1]))
            out.append(f"【{cat}】{detail}")
        if density > threshold:
            out.append(f"⚠️ 密度超限（{density:.2f} > {threshold}）。逐词判断：删词、换具体数字，或术语例外（专有名词保留）。")
        else:
            out.append("密度未超限，但建议逐词确认是否命中例外（政策专有名词、引用原文不删）。")
    return "\n".join(out)


def selftest():
    """内置自测：干净文本 0 命中；锯末文本必须命中；模态词不是锯末。"""
    cases = [
        ("干净文本", "这段话没有任何问题，只有一句话。", 0),
        ("锯末文本", "这是一个非常值得注意的事实；它不仅很强大，而且还很高效，"
                  "能够一站式地、全方位地、无缝地解决很多问题。", 7),
        ("模态保留", "月养老金约668元，以核定为准，待核实。", 0),
    ]
    ok = True
    for name, text, min_hits in cases:
        _, total = scan(text)
        good = total >= min_hits if min_hits else total == 0
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}"
              f"（要求命中 {'≥' + str(min_hits) if min_hits else '0'}，实际 {total}）")
    # 假靶心候选：三种模式各命中一次；无触发词/跨行不命中；泛指词给提示。
    contrast_cases = [
        ("不是A而是B", "不是传统工具只管语法，而是我们的产品更全面。", 1, True),
        ("并非A而是B", "并非过去的做法有误，而是场景变了。", 1, True),
        ("已过时才是", "老方案已过时，新架构才是正道。", 1, False),
        ("无触发词不报", "传统工具只管语法，我们的产品更全面。", 0, False),
        ("跨行不报", "不是传统工具只管语法\n而是我们的产品更全面。", 0, False),
    ]
    for name, text, n_expect, hint_expect in contrast_cases:
        got = check_contrast(text)
        good = (len(got) == n_expect and
                (bool(got[0]["risk_hints"]) == hint_expect if got else not hint_expect))
        ok = ok and good
        print(f"  [{'PASS' if good else 'FAIL'}] {name}"
              f"（期望候选 {n_expect}/泛指提示 {hint_expect}，实际 {len(got)}"
              f"/{got[0]['risk_hints'] if got else []}）")

    print("selftest:", "全部通过" if ok else "有失败项")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="中文锯末词扫描（只报告，不修改）")
    ap.add_argument("files", nargs="*", help="待扫描文件；省略时读 stdin")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help=f"密度上限，处/千字（默认 {DEFAULT_THRESHOLD}）")
    ap.add_argument("--check-contrast", action="store_true",
                    help="标记假靶心候选句（只标候选，不判定；仅 --json 时新增字段）")
    ap.add_argument("--selftest", action="store_true", help="运行内置自测")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    texts = []
    if args.files:
        for f in args.files:
            try:
                with open(f, encoding="utf-8") as fh:
                    texts.append((f, fh.read()))
            except OSError as e:
                print(f"读取失败：{f}（{e}）", file=sys.stderr)
                return 2
    else:
        texts.append(("<stdin>", sys.stdin.read()))

    results = []
    for path, text in texts:
        n_cjk = cjk_len(text)
        findings, total = scan(text)
        density = (total / n_cjk * 1000) if n_cjk else 0.0
        results.append({"path": path, "cjk": n_cjk, "hits": total,
                        "density": round(density, 2), "findings": findings,
                        "threshold": args.threshold,
                        "over": density > args.threshold})
        # opt-in：仅在显式 --check-contrast 时追加字段，默认结构逐字节不变。
        if args.check_contrast:
            results[-1]["contrast_candidates"] = check_contrast(text)
        if not args.json:
            print(render(path, text, args.threshold))
            print()

    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0],
                         ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
