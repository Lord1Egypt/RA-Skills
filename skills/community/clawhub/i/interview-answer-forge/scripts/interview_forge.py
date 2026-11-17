#!/usr/bin/env python3
"""
interview_forge.py — STAR story bank, JD question prediction, answer scoring, mock chains.

Subcommands:
  bank init|add|list|export   manage the story bank (~/.interview_bank.json)
  predict <jd.txt>            map JD phrases -> predicted questions -> bank coverage
  score <story.json>          check STAR budgets + rules on a draft
  mock --theme X              print a question + follow-up chain for practice

Stdlib only.
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

BANK_FILE = os.path.join(os.path.expanduser("~"), ".interview_bank.json")

THEMES = ["conflict", "failure", "leadership", "ambiguity", "achievement"]

# JD phrase -> (predicted question, theme)
JD_SIGNALS = [
    (r"fast[- ]paced|rapidly changing|dynamic", "Tell me about competing deadlines. How do you prioritize?", "ambiguity"),
    (r"cross[- ]functional|partner with", "Tell me about influencing a team you don't manage.", "ambiguity"),
    (r"many hats|scrappy|startup mentality|wears multiple", "Describe learning something fast with no help.", "achievement"),
    (r"detail[- ]oriented|attention to detail", "Tell me about catching an error others missed.", "achievement"),
    (r"stakeholder", "Difficult stakeholder: how did you turn them around?", "conflict"),
    (r"mentor|coach|develop (junior|others)", "Tell me about someone you leveled up.", "leadership"),
    (r"data[- ]driven|metrics|analytics", "Tell me about a decision where data overrode intuition.", "achievement"),
    (r"customer[- ]obsessed|customer first|voice of the customer", "Tell me about an angry customer you turned around.", "conflict"),
    (r"scale|hyper[- ]?growth|10x", "Tell me about something you built that broke at scale — and the fix.", "failure"),
    (r"process improvement|efficiency|optimize", "Describe a process you killed or rebuilt.", "achievement"),
    (r"remote|async|distributed", "Tell me about a communication failure and how you fixed it.", "conflict"),
    (r"ambigu(ity|ous)|self[- ]starter|autonom", "Tell me about a project with no clear direction.", "ambiguity"),
    (r"lead|ownership|own the", "Tell me about leading a team through something hard.", "leadership"),
    (r"collaborat|team player", "Tell me about a conflict within a team you resolved.", "conflict"),
    (r"deadline|time[- ]sensitive|under pressure", "Tell me about delivering under an impossible deadline.", "achievement"),
    (r"innovat|experiment|creative", "Tell me about an experiment that failed.", "failure"),
    (r"quality|excellence|high bar", "Tell me about a time quality and speed conflicted.", "ambiguity"),
]

MINING_PROMPTS = [
    "What did you build/fix/ship that outlived you?",
    "What did you refuse to do, and why?",
    "Which number did you move? (time, money, risk, quality, count)",
    "Who did you convince of something they didn't want to hear?",
    "What did you take over that was on fire?",
    "What are you proudest of that never made a slide deck?",
    "What did you do that your manager never learned about?",
    "What mistake do you still think about?",
    "The worst handoff you ever received — what did you do in week one?",
    "The rule you broke for the right reason",
    "The scope you cut to hit a date",
    "The user/customer you personally turned around",
]

FOLLOWUPS = {
    "conflict": ["How did the other person see it?", "What would they say about you now?",
                 "Why didn't you escalate earlier/later?", "What did you learn about yourself?"],
    "failure": ["What exactly was your mistake vs. circumstance?", "How did you surface it?",
                "What changed in your process afterward?", "Have you made a version of it since?"],
    "leadership": ["What did you do when someone underperformed?", "How did you split the work?",
                   "What would your team say was your biggest miss?", "How did you keep momentum?"],
    "ambiguity": ["How did you decide what mattered first?", "What did you deliberately NOT do?",
                  "Who did you have to convince?", "What would you do differently?"],
    "achievement": ["What was YOUR specific contribution?", "How was it measured?",
                    "What almost derailed it?", "What happened to it after you left?"],
}

WEAK_SPOTS = ["unverified number", "team result, personal part unclear", "no negative consequence stated",
              "action taken late", "no timeframe on result", "result is a claim, not a measurement"]


def load_bank():
    if os.path.exists(BANK_FILE):
        try:
            return json.load(open(BANK_FILE))
        except Exception:
            pass
    return {"stories": []}


def save_bank(bank):
    json.dump(bank, open(BANK_FILE, "w"), indent=2)


def cmd_bank(args):
    bank = load_bank()
    if args.action == "init":
        if bank["stories"]:
            print(f"  Bank exists with {len(bank['stories'])} stories (kept).")
        else:
            print("  Fresh bank initialized.")
        save_bank(bank)
        print("  Mining prompts to fill it (20 min, no judging while mining):")
        for p in MINING_PROMPTS:
            print(f"   - {p}")
        return 0
    if args.action == "list":
        if not bank["stories"]:
            print("  Bank empty. Run `bank init` then `bank add`.")
            return 0
        for i, s in enumerate(bank["stories"]):
            print(f"  [{i}] {s['theme']:<11} {s.get('one_liner','?')[:60]}")
            print(f"       result: {s.get('result','?')[:70]}")
        return 0
    if args.action == "add":
        s = {"theme": "", "one_liner": "", "situation": "", "task": "", "action": "", "result": "", "weak_spot": ""}
        print("\n  NEW STORY (Ctrl-C aborts)\n")
        while s["theme"] not in THEMES:
            t = input(f"  theme {THEMES}: ").strip().lower()
            s["theme"] = t
        s["one_liner"] = input("  one-liner (for your own index): ").strip()
        print("\n  STAR with budgets: S<=30w, T<=20w, A<=100w (I-voice!), R<=50w (number+timeframe)")
        s["situation"] = input("\n  S: ").strip()
        s["task"] = input("  T: ").strip()
        s["action"] = input("  A: ").strip()
        s["result"] = input("  R: ").strip()
        ws = input(f"  weak-spot flag {WEAK_SPOTS} (or own words): ").strip()
        s["weak_spot"] = ws
        s["added"] = datetime.now().strftime("%Y-%m-%d")
        bank["stories"].append(s)
        save_bank(bank)
        print(f"\n  Saved. Bank: {len(bank['stories'])} stories. Score it:")
        print(f"  python3 interview_forge.py score <(python3 -c \"import json;print(json.dumps({json.dumps(s)})[:0] or '')\") ")
        print("  (or: bank export N > story.json && score story.json)")
        return 0
    if args.action == "export":
        idx = int(args.index)
        try:
            s = bank["stories"][idx]
        except (IndexError, ValueError):
            print("  bad index"); return 1
        json.dump(s, sys.stdout, indent=2); print()
        return 0
    print("  usage: bank init|add|list|export N")
    return 1


def cmd_predict(args):
    try:
        jd = open(args.jd).read()
    except OSError as e:
        print(f"  can't read JD: {e}"); return 1
    bank = load_bank()
    by_theme = {}
    for s in bank["stories"]:
        by_theme.setdefault(s["theme"], []).append(s["one_liner"])

    text = jd.lower()
    print("\n  PREDICTED QUESTIONS from JD\n" + "  " + "=" * 50)
    seen, gaps = [], []
    for pat, q, theme in JD_SIGNALS:
        if re.search(pat, text):
            if q in seen:
                continue
            seen.append(q)
            cover = by_theme.get(theme, [])
            mark = "READY" if cover else "GAP"
            print(f"\n  [{mark}] {q}")
            print(f"         (theme: {theme}; JD signal: /{pat}/)")
            if cover:
                for c in cover[:2]:
                    print(f"         story: {c[:64]}")
            else:
                gaps.append((q, theme))
    print("\n  ALWAYS-ASK CLASSICS (JD-independent):")
    for q in ["Tell me about yourself (60-90s, present->past->future)",
              "Why us? (3 sentences: what role lets you do / what you bring / why now)",
              "Tell me about a failure (real cost + changed behavior)",
              "Tell me about a conflict (include what the other side wanted)",
              "Weakness (real, with the compensation system)",
              "Questions for them: day-90 success / last person's struggle / team's biggest challenge"]:
        print(f"   - {q}")
    if gaps:
        print(f"\n  GAPS ({len(gaps)}): no bank story for:")
        for q, theme in gaps:
            print(f"   - [{theme}] {q}")
        print("  Mining prompts to close them:")
        for p in MINING_PROMPTS[:6]:
            print(f"   ? {p}")
    else:
        print("\n  All JD-derived probes map to bank stories.")
    return 0


def wc(s):
    return len(s.split())


def cmd_score(args):
    try:
        s = json.load(open(args.story))
    except Exception as e:
        print(f"  can't read story: {e}"); return 1
    total = sum(wc(s.get(k, "")) for k in ("situation", "task", "action", "result"))
    if total == 0:
        print("  empty story"); return 1
    print(f"\n  SCORING '{s.get('one_liner','?')[:50]}'  ({total} words total)\n" + "  " + "=" * 50)
    issues = []
    for k, budget in (("situation", .15), ("task", .10), ("action", .50), ("result", .25)):
        w = wc(s.get(k, ""))
        pct = w / total * 100
        ok = abs(pct - budget * 100) <= 20
        print(f"  {k:<10} {w:>3}w  {pct:>5.1f}%  (target {int(budget*100)}%{' ±20' if ok else '  << OFF'})")
        if not ok:
            issues.append(f"{k} off-budget ({pct:.0f}% vs {int(budget*100)}%)")
    a = s.get("action", "").lower()
    if a.count(" i ") + a.count(" i'") + len(re.findall(r"^i |\ni ", a)) < 2:
        issues.append("Action lacks I-voice (need 'I did X' steps)")
    r = s.get("result", "")
    if not re.search(r"\d|roughly|about|~|third|half|quarter", r.lower()):
        issues.append("Result has no number/band")
    if not re.search(r"\b(day|week|month|quarter|year|hour|q[1-4])\b", r.lower()):
        issues.append("Result has no timeframe")
    print()
    if issues:
        print("  FIX LIST:")
        for i in issues:
            print(f"   - {i}")
    else:
        print("  CLEAN: budgets in range, I-voice, number+timeframe present.")
    if s.get("weak_spot"):
        print(f"\n  Weak-spot flag (prepare the bridge): {s['weak_spot']}")
    else:
        print("\n  No weak-spot flag set — add one; every story has a hole.")
    print(f"\n  Expected follow-ups:")
    for f in FOLLOWUPS.get(s.get("theme", "achievement"), [])[:3]:
        print(f"   ? {f}")
    return 0


def cmd_mock(args):
    theme = args.theme
    if theme not in THEMES:
        print(f"  theme must be one of {THEMES}"); return 1
    qs = {
        "conflict": "Tell me about a time you disagreed with a coworker. What happened?",
        "failure": "Tell me about a time you failed. What did it cost?",
        "leadership": "Tell me about leading a team through something hard.",
        "ambiguity": "Tell me about a project where nobody told you what to do.",
        "achievement": "What's your proudest work accomplishment?",
    }
    print(f"\n  INTERVIEWER: {qs[theme]}\n")
    print("  (answer aloud, 90 seconds, STAR budgets. Then take the chain:)\n")
    for i, f in enumerate(FOLLOWUPS[theme], 1):
        print(f"  follow-up {i}: {f}")
    print("\n  Rule: if any follow-up stings, that's your weak-spot flag for this story.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="STAR story bank + JD prediction + scoring")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("bank"); p.add_argument("action", choices=["init", "add", "list", "export"])
    p.add_argument("index", nargs="?"); p.set_defaults(fn=cmd_bank)
    p = sub.add_parser("predict"); p.add_argument("jd"); p.set_defaults(fn=cmd_predict)
    p = sub.add_parser("score"); p.add_argument("story"); p.set_defaults(fn=cmd_score)
    p = sub.add_parser("mock"); p.add_argument("--theme", required=True); p.set_defaults(fn=cmd_mock)
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help(); sys.exit(1)
    sys.exit(args.fn(args) or 0)


if __name__ == "__main__":
    main()
