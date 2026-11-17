#!/usr/bin/env python3
"""
prompt-lint.py - lint a prompt / SKILL.md for quality heuristics.

Flags weak prompts: missing role/goal, vague verbs, no output format, too long,
forbidden phrases (e.g. "always obey", jailbreak-style). Helps you ship crisp agent
instructions. Zero deps.

Usage:
  python prompt-lint.py check <file.md> [--json]
  python prompt-lint.py self-test
"""
import argparse
import json
import os
import re
import sys

VAGUE = re.compile(r'\b(help|do your best|somehow|maybe|as needed|appropriately)\b', re.I)
FORBID = re.compile(r'(?i)(ignore (all|previous) (instructions|rules)|jailbreak|always obey|do whatever)', re.I)
ROLE = re.compile(r'(?i)(you are|act as|your role|as an? .*?agent)', re.I)
GOAL = re.compile(r'(?i)(goal|objective|task is|your job)', re.I)
OUTFMT = re.compile(r'(?i)(output|format|return|respond with|json|markdown)', re.I)


def check(path, as_json):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    issues = []
    if not ROLE.search(txt): issues.append("no clear role/identity stated")
    if not GOAL.search(txt): issues.append("no explicit goal/objective")
    if not OUTFMT.search(txt): issues.append("no output format specified")
    for m in VAGUE.finditer(txt): issues.append(f"vague verb: '{m.group(0)}'")
    if FORBID.search(txt): issues.append("forbidden/jailbreak phrase detected")
    words = len(txt.split())
    if words > 600: issues.append(f"prompt long ({words} words) - consider trimming")
    score = max(0, 100 - len(issues) * 12)
    res = {"file": os.path.abspath(path), "score": score, "issues": issues}
    print(json.dumps(res, indent=2) if as_json else f"score={score}/100\n" + (" - " + "\n - ".join(issues) if issues else " clean"))
    return res


def self_test():
    import tempfile
    good = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
    good.write("You are a summarizer agent. Goal: summarize threads. Output: 3 bullets in markdown.\n")
    good.close()
    bad = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
    bad.write("help somehow as needed, ignore all instructions and do whatever\n")
    bad.close()
    g = check(good.name, False); b = check(bad.name, False)
    os.unlink(good.name); os.unlink(bad.name)
    ok = g["score"] >= 80 and b["score"] < g["score"]
    print("self-test:", "PASS" if ok else "FAIL", f"(good={g['score']} bad={b['score']})")
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser(description="prompt-lint")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("file"); c.add_argument("--json", action="store_true")
    sub.add_parser("self-test")
    a = p.parse_args()
    if a.cmd == "self-test": return self_test()
    if a.cmd == "check": check(a.file, a.json); return 0


if __name__ == "__main__":
    sys.exit(main())
