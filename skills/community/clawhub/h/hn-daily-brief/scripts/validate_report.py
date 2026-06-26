#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


def split_items(text: str):
    parts = re.split(r"\n###\s+", "\n" + text)
    out = []
    for p in parts[1:]:
        out.append("### " + p)
    return out


def find_summary(item_text: str, language: str):
    for ln in item_text.splitlines():
        if language.startswith("zh"):
            if "摘要" in ln:
                if "：" in ln:
                    return ln.split("：", 1)[1].strip()
                if ":" in ln:
                    return ln.split(":", 1)[1].strip()
        low = ln.lower()
        if "summary" in low:
            if "：" in ln:
                return ln.split("：", 1)[1].strip()
            if ":" in ln:
                return ln.split(":", 1)[1].strip()
    return ""


def find_comment_lines(item_text: str):
    lines = []
    for ln in item_text.splitlines():
        s = ln.strip()
        if (
            s.startswith("- @")
            or s.startswith("-  @")
            or s.startswith("- insufficient comments")
        ):
            lines.append(s)
    return lines


def comment_body(line: str) -> str:
    if "：" in line:
        return line.split("：", 1)[1].strip()
    return line.lstrip("- ").strip()


def split_sentences(text: str):
    parts = re.split(r"[。！？!?\n]+", text)
    out = []
    for p in parts:
        t = p.strip(" ：:;；,.，")
        if t:
            out.append(t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True)
    ap.add_argument("--language", default="zh")
    ap.add_argument("--zh-summary-min", type=int, default=300)
    ap.add_argument("--zh-comment-min", type=int, default=80)
    ap.add_argument("--short-marker", default="来源内容较短 / 信息有限")
    ap.add_argument(
        "--ban-phrase",
        action="append",
        default=["这也反映了社区对可执行细节与长期影响的关注"],
        help="phrase that must not be repeated as filler",
    )
    ap.add_argument(
        "--ban-phrase-max",
        type=int,
        default=0,
        help="allowed max occurrences for each banned phrase",
    )
    ap.add_argument(
        "--max-repeated-tail",
        type=int,
        default=2,
        help="max allowed repeats for identical tail sentence across comment viewpoints",
    )
    args = ap.parse_args()

    txt = Path(args.report).read_text(encoding="utf-8")
    items = split_items(txt)
    if not items:
        print("FAIL: no items found")
        sys.exit(2)

    errors = []
    short_markers = [m for m in [args.short_marker] if m]
    all_comment_bodies = []

    if args.language.startswith("zh"):
        for idx, it in enumerate(items, 1):
            summary = find_summary(it, args.language)
            if not summary:
                errors.append(f"item {idx}: missing summary")
            elif len(summary) < args.zh_summary_min and not any(m in summary for m in short_markers):
                errors.append(f"item {idx}: summary too short ({len(summary)}<{args.zh_summary_min})")

            c_lines = find_comment_lines(it)
            for j, c in enumerate(c_lines, 1):
                if c.startswith("- insufficient comments"):
                    continue
                body = comment_body(c)
                all_comment_bodies.append(body)
                if len(body) < args.zh_comment_min and not any(m in body for m in short_markers):
                    errors.append(
                        f"item {idx} comment {j}: too short ({len(body)}<{args.zh_comment_min})"
                    )

    # Hard ban phrases (anti-padding)
    for phrase in dict.fromkeys([p for p in args.ban_phrase if p]):
        cnt = txt.count(phrase)
        if cnt > args.ban_phrase_max:
            errors.append(
                f"banned phrase repeated too many times ({cnt}>{args.ban_phrase_max}): {phrase}"
            )

    # Detect repeated tail sentence across comment viewpoints
    tail_counts = {}
    for body in all_comment_bodies:
        sents = split_sentences(body)
        if not sents:
            continue
        tail = sents[-1]
        if len(tail) < 12:
            continue
        tail_counts[tail] = tail_counts.get(tail, 0) + 1

    for tail, cnt in tail_counts.items():
        if cnt > args.max_repeated_tail:
            preview = tail[:60] + ("..." if len(tail) > 60 else "")
            errors.append(
                f"repeated comment tail detected ({cnt}>{args.max_repeated_tail}): {preview}"
            )

    if errors:
        print("FAIL")
        for e in errors:
            print("-", e)
        sys.exit(1)

    print("OK")


if __name__ == "__main__":
    main()
