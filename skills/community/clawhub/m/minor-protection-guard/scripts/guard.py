# -*- coding: utf-8 -*-
"""未成年人保护合规护栏 - 检测引擎。

纯标准库实现，无第三方依赖、无网络请求、无外部进程调用。
用法见 SKILL.md 的「Agent 调用」与「快速开始」章节。
"""
import argparse
import json
import sys
from pathlib import Path

# 规则词表与分类元数据（同一目录受控文件，动态导入）
RULES_PATH = Path(__file__).resolve().parent / "rules" / "terms.py"
import importlib.util
_spec = importlib.util.spec_from_file_location("terms", RULES_PATH)
terms = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(terms)

TERMS = terms.TERMS
CATEGORIES = terms.CATEGORIES
CATEGORY_LABEL = terms.CATEGORY_LABEL

SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1}


def _dedup(findings):
    """重叠去重：保留高 severity / 更长匹配。"""
    findings.sort(key=lambda f: (f["start"], -(SEVERITY_ORDER.get(f["risk"], 0)), -len(f["term"])))
    keep = []
    for f in findings:
        overlap = False
        for k in keep:
            if f["start"] < k["end"] and f["end"] > k["start"]:
                overlap = True
                break
        if not overlap:
            keep.append(f)
    return keep


def detect(text):
    """扫描文本，返回命中列表（已去重）。"""
    results = []
    for t in TERMS:
        start = 0
        while True:
            idx = text.find(t["term"], start)
            if idx == -1:
                break
            results.append({
                "term": t["term"],
                "category": t["category"],
                "category_label": CATEGORY_LABEL.get(t["category"], t["category"]),
                "risk": t.get("risk", CATEGORIES.get(t["category"], {}).get("risk", "medium")),
                "suggestion": t["suggestion"],
                "basis": t.get("basis", ""),
                "start": idx,
                "end": idx + len(t["term"]),
            })
            start = idx + 1
    return _dedup(results)


def evaluate(text):
    """评估文本合规风险，返回结构化结果。"""
    hits = detect(text)
    risk_rank = [SEVERITY_ORDER.get(h["risk"], 0) for h in hits]
    level = "clean" if not hits else ("high" if 3 in risk_rank else ("medium" if 2 in risk_rank else "low"))
    cats = {}
    for h in hits:
        cats[h["category"]] = cats.get(h["category"], 0) + 1
    return {
        "level": level,
        "total": len(hits),
        "by_category": cats,
        "findings": hits,
    }


def _print_text(report):
    if report["level"] == "clean":
        print("✓ clean — 未检测到未成年人保护相关违规表述。")
        return
    icon = {"high": "✗", "medium": "!", "low": "·"}[report["level"]]
    print(f"{icon} {report['level'].upper()} — 检测到 {report['total']} 处风险提示：")
    print("-" * 60)
    for h in report["findings"]:
        print(f"[{h['risk'].upper()}] ({h['category_label']}) 命中「{h['term']}」")
        print(f"    建议：{h['suggestion']}")
        if h.get("basis"):
            print(f"    依据：{h['basis']}")
    print("-" * 60)


def main():
    ap = argparse.ArgumentParser(description="未成年人保护合规护栏检测引擎")
    ap.add_argument("--text", help="待检测文本")
    ap.add_argument("--stdin", action="store_true", help="从标准输入读取文本")
    ap.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    ap.add_argument("--list-categories", action="store_true", help="列出所有检测类别")
    args = ap.parse_args()

    if args.list_categories:
        for k, v in CATEGORIES.items():
            print(f"{k}\t{v['label']}\t{v['risk']}\t{v['desc']}")
        return

    if args.stdin:
        text = sys.stdin.read()
    elif args.text:
        text = args.text
    else:
        ap.error("请通过 --text / --stdin 提供文本，或 --list-categories 查看类别")
        return

    report = evaluate(text)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_text(report)


if __name__ == "__main__":
    main()
