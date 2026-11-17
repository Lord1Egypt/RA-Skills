#!/usr/bin/env python3
"""Audit a minimal edit by comparing before/after text.

Recommended, keeps document text out of process arguments:

    python audit_edit.py --stdin <<'JSON'
    {"before": "...", "after": "...", "must_remove": ["综上所述"]}
    JSON

    # original from file, revised text piped in
    python audit_edit.py --before before.txt --after-stdin < revised.txt

Also supported:

    python audit_edit.py --before before.txt --after after.txt
    python audit_edit.py --before before.txt --after after.txt --must-remove-file removed.txt
    python audit_edit.py --before before.txt --after after.txt --must-remove "综上所述"

Discouraged: --before-text and --after-text put document text on the command
line, where it can be retained in shell history, process listings, and
orchestration logs. Use them only for short, non-confidential snippets; the
script prints a warning when they are used.

This script reads only the files named on the command line, plus stdin when
asked. It does not walk the working directory, read environment variables, or
touch the network.

The marker lists cover Chinese and English only. Other languages get no useful
signal here and need manual review. Marker lists are heuristic and incomplete;
they cannot replace manual judgment.
"""

import argparse
import difflib
import json
import re
import sys

CN_MARKERS = [
    "综上所述",
    "综上可见",
    "总体来看",
    "总体而言",
    "值得注意的是",
    "需要注意的是",
    "需要指出的是",
    "换言之",
    "换句话说",
    "更准确地说",
    "更具体地说",
    "需要说明的是",
    "不难发现",
    "毋庸置疑",
    "显而易见",
    "毫无疑问",
    "从某种意义上说",
    "改动如下",
    "修改如下",
    "赋能",
    "抓手",
    "闭环",
    "颗粒度",
    "场景化",
    "生态化",
    "平台化",
    "底层逻辑",
    "战略协同",
    "深度绑定",
    "价值最大化",
    "一站式",
    "全方位",
    "多维度",
    "系统性",
    "组合拳",
    "矩阵",
    "拉通",
    "对齐",
    "沉淀",
    "方法论",
    "打法",
    "降本增效",
    "提质增效",
    "共建",
    "打通",
    "深耕",
    "聚焦",
    "打造",
    "构建",
    "助力",
    "驱动",
    "撬动",
    "释放",
]

EN_MARKERS = [
    "in conclusion",
    "to summarize",
    "to sum up",
    "all in all",
    "it is worth noting",
    "it should be noted",
    "it is important to note",
    "needless to say",
    "moreover",
    "furthermore",
    "in other words",
    "to put it another way",
    "more precisely",
    "that is to say",
    "leverage",
    "synergy",
    "holistic",
    "ecosystem",
    "end-to-end",
    "seamless",
    "cutting-edge",
    "game-changer",
    "paradigm shift",
    "actionable insights",
    "key takeaways",
    "next steps",
    "empower",
    "unlock",
    "streamline",
    "robust",
    "granular",
    "landscape",
    "pivotal",
    "underscore",
    "delve",
]


def normalize(text):
    return re.sub(r"\s+", "", text)


def find_new_markers(before, after):
    lowered_before = before.lower()
    lowered_after = after.lower()
    found = []
    for marker in CN_MARKERS:
        if marker in after and marker not in before:
            found.append(marker)
    for marker in EN_MARKERS:
        if marker in lowered_after and marker not in lowered_before:
            found.append(marker)
    return found


def read_text_file(path, label):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError as exc:
        sys.exit(f"cannot read {label} file {path!r}: {exc}")


def read_phrases(path):
    phrases = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            phrase = line.strip()
            if phrase:
                phrases.append(phrase)
    return phrases


def read_stdin_text():
    if sys.stdin.isatty():
        sys.exit("--stdin was given but stdin is a terminal; pipe or redirect the payload in")
    return sys.stdin.buffer.read().decode("utf-8", errors="replace")


def parse_payload(payload):
    """Accept a JSON object with before / after / must_remove, or plain text pairs."""
    text = payload.strip()
    if text.startswith("{"):
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            sys.exit(f"--stdin received invalid JSON: {exc}")
        if not isinstance(data, dict):
            sys.exit("--stdin JSON must be an object")
        before = data.get("before")
        after = data.get("after")
        if before is None or after is None:
            sys.exit('--stdin JSON must contain both "before" and "after"')
        must_remove = data.get("must_remove") or []
        if isinstance(must_remove, str):
            must_remove = [must_remove]
        return before, after, list(must_remove)
    sys.exit(
        "--stdin expects a JSON object with \"before\", \"after\", and optional "
        "\"must_remove\"; plain text is ambiguous here"
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description="Audit a minimal text edit. Prefer --stdin or files over inline text."
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help='Read a JSON payload {"before": ..., "after": ..., "must_remove": [...]} from stdin (recommended)',
    )
    before_group = parser.add_mutually_exclusive_group()
    before_group.add_argument("--before", help="Path to the original text file")
    before_group.add_argument("--before-text", help="Original text as a command-line argument (discouraged)")
    before_group.add_argument("--before-stdin", action="store_true", help="Read the original text from stdin")
    after_group = parser.add_mutually_exclusive_group()
    after_group.add_argument("--after", help="Path to the edited text file")
    after_group.add_argument("--after-text", help="Edited text as a command-line argument (discouraged)")
    after_group.add_argument("--after-stdin", action="store_true", help="Read the edited text from stdin")
    parser.add_argument(
        "--must-remove",
        action="append",
        default=[],
        help="Phrase the user asked to delete; repeat for multiple phrases",
    )
    parser.add_argument(
        "--must-remove-file",
        help="File with one phrase to delete per line, for phrases that contain quotes",
    )
    parser.add_argument("--threshold", type=float, default=1.5, help="Max new/old ratio")
    parser.add_argument("--fail", action="store_true", help="Exit 1 on warnings")
    return parser


def resolve_inputs(args, parser):
    if args.before_stdin and args.after_stdin:
        parser.error("--before-stdin and --after-stdin cannot be combined; use --stdin with JSON")

    inline_flags = [flag for flag, value in (
        ("--before-text", args.before_text),
        ("--after-text", args.after_text),
    ) if value is not None]
    if inline_flags and args.stdin:
        parser.error("--stdin cannot be combined with " + ", ".join(inline_flags))

    must_remove = list(args.must_remove)
    if args.must_remove_file:
        must_remove += read_phrases(args.must_remove_file)

    if args.stdin:
        before, after, payload_phrases = parse_payload(read_stdin_text())
        return before, after, must_remove + payload_phrases

    stdin_text = None
    if args.before_stdin or args.after_stdin:
        stdin_text = read_stdin_text()

    if args.before is not None:
        before = read_text_file(args.before, "original")
    elif args.before_stdin:
        before = stdin_text
    elif args.before_text is not None:
        before = args.before_text
    else:
        parser.error("provide --before, --before-text, --before-stdin, or --stdin")

    if args.after is not None:
        after = read_text_file(args.after, "edited")
    elif args.after_stdin:
        after = stdin_text
    elif args.after_text is not None:
        after = args.after_text
    else:
        parser.error("provide --after, --after-text, --after-stdin, or --stdin")

    return before, after, must_remove


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = build_parser()
    args = parser.parse_args()
    before, after, must_remove = resolve_inputs(args, parser)

    if args.before_text is not None or args.after_text is not None:
        print(
            "WARNING: inline text on the command line can be retained in shell history, "
            "process listings, and orchestration logs. Use --stdin or file paths for "
            "anything confidential.",
            file=sys.stderr,
        )

    nb = normalize(before)
    na = normalize(after)
    matcher = difflib.SequenceMatcher(None, nb, na)

    changed_old = 0
    changed_new = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("replace", "insert"):
            changed_old += i2 - i1
            changed_new += j2 - j1
        elif tag == "delete":
            changed_old += i2 - i1

    warnings = []
    if changed_old > 0:
        ratio = changed_new / changed_old
        if ratio > args.threshold:
            warnings.append(
                f"new changed text is {changed_new} chars vs {changed_old} old chars "
                f"(ratio {ratio:.2f} > {args.threshold})"
            )

    new_markers = find_new_markers(before, after)
    if new_markers:
        warnings.append(
            "new AI-flavor candidates (manual review): " + ", ".join(new_markers)
        )

    if after.count("**") > before.count("**"):
        warnings.append("added bold markers")

    if changed_new > changed_old + 80:
        warnings.append(f"added {changed_new - changed_old} chars beyond the replaced text")

    for phrase in must_remove:
        if phrase in before and phrase in after:
            warnings.append(f"must-remove phrase still present: {phrase}")
        elif phrase not in before:
            warnings.append(f"must-remove phrase not found in original: {phrase}")

    print(f"chars before={len(nb)} after={len(na)} changed_old={changed_old} changed_new={changed_new}")
    for warning in warnings:
        print("WARN:", warning)
    if not warnings:
        print("OK: no expansion, deletion, or AI-flavor warnings.")
    print(
        "NOTE: marker lists cover Chinese and English only and are heuristic; "
        "other languages and every judgment call still need manual review."
    )

    if args.fail and warnings:
        sys.exit(1)


if __name__ == "__main__":
    main()
