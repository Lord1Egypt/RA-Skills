#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把一份申诉跑成可直接回帖的裁决。

用法：
    python scripts/handle_appeal.py <包目录> <申诉.json> [--run] [--out 回复.md]

产出是一段 Markdown：表格 + 结论 + 下一步。可以直接贴到 Issue 回复里。
裁决规则与 review.py --appeal 完全一致——这里只是换了个便于受理的输出形态。
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review as R  # noqa: E402

MARKS = {"OVERTURNED": "推翻", "UPHELD": "维持",
         "UNKNOWN_ID": "无效 ID", "REJECTED": "拒收"}


def build_md(root, r, ar):
    d = r["data"]
    lines = []
    lines.append("### 申诉裁决 · %s v%s" % (d.get("name"), d.get("version")))
    lines.append("")
    lines.append("评测结论：结构制 **%d/%d（%.0f%%）%s**" %
                 (d["total"], d["max"], d["pct"], d["verdict"]))
    lines.append("")
    if not ar.get("ok"):
        lines.append("申诉文件无法解析：%s" % ar.get("error"))
        return "\n".join(lines)
    lines.append("| 申诉项 | 裁决 | 理由 |")
    lines.append("|---|---|---|")
    over = 0
    for rid, claim, verdict, why in ar["items"]:
        if verdict == "OVERTURNED":
            over += 1
        lines.append("| `%s` | **%s** | %s |" % (rid, MARKS.get(verdict, verdict), why))
    lines.append("")
    lines.append("**小结**：%d 条申诉中 %d 条推翻原判定。" % (len(ar["items"]), over))
    lines.append("")
    if over:
        lines.append("推翻的项，原判定依据不成立。请复测确认该维度是否真的变化——"
                     "规则可能还有别的依据在支撑同一个扣分，所以复测前不建议直接认为分数会回升。")
        lines.append("")
    lines.append("裁决已写入 `appeal_log.json`，可公开查阅。")
    lines.append("")
    lines.append("> 说明：裁决只核验「原判定依据是否成立」，不修改已给出的分数。"
                 "会因申诉自动加分的评测器，它的分数就没有意义了。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="把申诉跑成可回帖的裁决")
    ap.add_argument("package", help="被评测的包目录")
    ap.add_argument("appeal", help="申诉 JSON")
    ap.add_argument("--run", action="store_true", help="复评时实跑测试执行器")
    ap.add_argument("--out", default=None, help="把裁决写到这个文件")
    a = ap.parse_args()

    root = os.path.abspath(a.package)
    if not os.path.isdir(root):
        sys.exit("包目录不存在：%s" % root)

    r = R.review(root, a.run, None)
    if not r.get("ok"):
        sys.exit("评测失败：%s" % r.get("msg"))

    ar = R.appeal_check(root, r["data"], a.appeal)
    md = build_md(root, r, ar)

    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(md + "\n")
        print("已写出 %s" % a.out)
    else:
        print(md)


if __name__ == "__main__":
    main()
