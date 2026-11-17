# -*- coding: utf-8 -*-
"""extract_terms.py — 术语候选自动抽取（v1.3.0 新增）。

从原稿抽取术语候选，生成 terms.txt 草稿（人工确认后供 verify.py --terms 使用）。
候选来源：连续大写缩写（按频次）、书名号/引号内专业词。零网络、零依赖。

用法:
    python scripts/extract_terms.py 原稿.txt -o terms.txt
    python scripts/extract_terms.py 原稿.txt --min-count 3 --json
退出码: 0 成功 | 2 用法/文件错误
"""

import argparse
import json
import re
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core

# 英文高频虚词/普通词白名单（不当术语）
_EN_STOP = {"THE", "AND", "WITH", "FOR", "FROM", "NOT", "BUT", "ALL", "ARE", "WAS",
            "WERE", "HAS", "HAD", "ITS", "OUR", "OUT", "NEW", "TWO", "THREE", "ONE",
            "THIS", "THAT", "THESE", "THOSE", "THERE", "WHEN", "THEN", "THAN",
            "ALSO", "BETWEEN", "AFTER", "BEFORE", "UNDER", "OVER", "INTO", "PER"}
_EN_TITLE_STOP = {"The", "This", "That", "These", "Those", "There", "When", "Then",
                  "While", "Where", "Which", "With", "From", "However", "Although",
                  "Because", "Results", "Methods", "Conclusion", "Background",
                  "Table", "Figure", "Equation", "Chapter", "Section", "Patient",
                  "Patients", "Study", "Group", "Treatment", "Data"}


def extract(orig, min_count=2, cap=40):
    """返回 [(term, count, kind)]，按频次降序。kind: abbr/quoted/title。"""
    cands = Counter()
    kinds = {}
    # 连续大写缩写：允许内嵌数字（BRCA1/TP53/H1N1），但整体不得与连字符/数字
    # 相邻（防 PD-L1→PD、IL-6→IL 截断形进候选）
    for m in re.finditer(r"(?<![A-Za-z0-9\-])([A-Z][A-Z0-9]{1,7})(?![A-Za-z0-9\-])", orig):
        w = m.group(1)
        if w in _EN_STOP or not re.match(r"^[A-Z]{2,8}$", w):
            continue
        cands[w] += 1
        kinds.setdefault(w, "abbr")
    # 书名号/直角引号内术语（首字符放宽到拉丁字母：覆盖《PD-L1抑制剂》）
    for m in re.finditer(r"[《「]([A-Za-z\u4e00-\u9fff][\u4e00-\u9fffA-Za-z0-9·－\-]{1,15})[》」]", orig):
        w = m.group(1)
        cands[w] += 1
        kinds.setdefault(w, "quoted")
    # 英文 Title-case 词（≥4 字母，非句首白名单）——仅统计句中出现
    for m in re.finditer(r"(?<![.!?]\s)\b([A-Z][a-z]{3,11})\b", orig):
        w = m.group(0)
        if w in _EN_TITLE_STOP:
            continue
        cands[w] += 1
        kinds.setdefault(w, "title")
    rows = [(w, n, kinds[w]) for w, n in cands.most_common() if n >= min_count]
    return rows[:cap]


def main():
    ap = argparse.ArgumentParser(description="术语候选自动抽取（生成 verify.py --terms 草稿）")
    ap.add_argument("file", help="原稿（.txt/.md/.docx）")
    ap.add_argument("-o", "--output", help="terms.txt 草稿输出路径（建议必填）")
    ap.add_argument("--min-count", type=int, default=2, help="最低出现次数（默认 2）")
    ap.add_argument("--cap", type=int, default=40, help="最多输出候选数（默认 40）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--version", action="version", version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    try:
        orig = hxt_core.read_text(args.file)
    except OSError as e:
        print("错误: 无法读取 %s（%s）" % (args.file, e), file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)
    if not orig.strip():
        print("错误: 输入为空", file=sys.stderr)
        sys.exit(2)

    rows = extract(orig, args.min_count, cap=args.cap)
    if args.json:
        print(json.dumps({"candidates": [{"term": w, "count": n, "kind": k} for w, n, k in rows],
                          "note": "草稿需人工确认（删除非术语项）后再供 verify.py --terms 使用"},
                         ensure_ascii=False, indent=2))
    else:
        print("术语候选 %d 个（≥%d 次）：" % (len(rows), args.min_count))
        for w, n, k in rows:
            print("  %-24s ×%-3d (%s)" % (w, n, k))
        if not rows:
            print("  （无候选——可降低 --min-count 或手工整理）")
    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write("# 术语表草稿（extract_terms.py 自动生成，请人工确认：删除非术语行）\n")
                for w, n, k in rows:
                    f.write("%s\n" % w)
        except OSError as e:
            print("错误: 无法写入 %s（%s）" % (args.output, e), file=sys.stderr)
            sys.exit(2)
        if not args.json:
            print("草稿已写入 %s（人工确认后：verify.py 原稿 改稿 --terms %s）" % (args.output, args.output))
    sys.exit(0)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
