#!/usr/bin/env python3
"""
User Decision Profile Manager
Tracks decision preferences, biases, and patterns across sessions.

Usage:
  python user_profile.py show
  python user_profile.py add-bias --bias "沉没成本" --evidence "多次因已投入时间而不愿放弃"
  python user_profile.py add-preference --key "risk_tolerance" --value "low" --note "多次选择稳妥方案"
  python user_profile.py add-pattern --pattern "在时间压力下倾向于维持现状"
  python user_profile.py add-past --title "选了XX公司" --lesson "选了便宜的但后悔了"
  python user_profile.py summary
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

DATA_DIR = Path.home() / ".decision-advisor" / "data"
PROFILE_FILE = DATA_DIR / "user_profile.json"

DEFAULT_PROFILE = {
    "created": None,
    "updated": None,
    "biases": [],
    "preferences": {},
    "patterns": [],
    "past_lessons": [],
}


def load_profile():
    if PROFILE_FILE.exists():
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {**DEFAULT_PROFILE, "created": datetime.now().isoformat()}


def save_profile(profile):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    profile["updated"] = datetime.now().isoformat()
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)


def cmd_show(args):
    profile = load_profile()
    print(json.dumps(profile, ensure_ascii=False, indent=2))


def cmd_add_bias(args):
    profile = load_profile()
    entry = {
        "bias": args.bias,
        "evidence": args.evidence or "",
        "detected_date": datetime.now().isoformat()[:10],
        "occurrences": 1,
    }
    # Check if bias already exists, increment occurrences
    for existing in profile["biases"]:
        if existing["bias"] == args.bias:
            existing["occurrences"] += 1
            if args.evidence:
                existing["evidence"] += f"; {args.evidence}"
            existing["last_seen"] = datetime.now().isoformat()[:10]
            save_profile(profile)
            print(f"Updated existing bias '{args.bias}' (occurrences: {existing['occurrences']})")
            return
    profile["biases"].append(entry)
    save_profile(profile)
    print(f"Added new bias: {args.bias}")


def cmd_add_preference(args):
    profile = load_profile()
    profile["preferences"][args.key] = {
        "value": args.value,
        "note": args.note or "",
        "updated": datetime.now().isoformat()[:10],
    }
    save_profile(profile)
    print(f"Set preference: {args.key} = {args.value}")


def cmd_add_pattern(args):
    profile = load_profile()
    entry = {
        "pattern": args.pattern,
        "detected_date": datetime.now().isoformat()[:10],
    }
    profile["patterns"].append(entry)
    save_profile(profile)
    print(f"Added pattern: {args.pattern}")


def cmd_add_past(args):
    profile = load_profile()
    entry = {
        "title": args.title,
        "lesson": args.lesson,
        "date": datetime.now().isoformat()[:10],
    }
    profile["past_lessons"].append(entry)
    save_profile(profile)
    print(f"Added past lesson: {args.title}")


def cmd_summary(args):
    profile = load_profile()

    print("=" * 50)
    print("  用户决策画像摘要")
    print("=" * 50)

    # Biases
    if profile["biases"]:
        print("\n⚠️  已识别的决策偏误:")
        for b in sorted(profile["biases"], key=lambda x: -x.get("occurrences", 1)):
            count = b.get("occurrences", 1)
            print(f"  - {b['bias']} (出现 {count} 次)")
            if b.get("evidence"):
                print(f"    证据: {b['evidence']}")
    else:
        print("\n✅ 暂未识别到明显决策偏误")

    # Preferences
    if profile["preferences"]:
        print("\n📊 决策偏好:")
        for k, v in profile["preferences"].items():
            print(f"  - {k}: {v['value']}")
            if v.get("note"):
                print(f"    备注: {v['note']}")

    # Patterns
    if profile["patterns"]:
        print("\n🔄 决策行为模式:")
        for p in profile["patterns"]:
            print(f"  - {p['pattern']}")

    # Past lessons
    if profile["past_lessons"]:
        print("\n📝 历史教训:")
        for l in profile["past_lessons"][-5:]:
            print(f"  - [{l.get('date','')}] {l['title']}: {l['lesson']}")

    print()


def main():
    parser = argparse.ArgumentParser(description="User Decision Profile Manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("show")

    p_bias = sub.add_parser("add-bias")
    p_bias.add_argument("--bias", required=True, help="Name of the cognitive bias")
    p_bias.add_argument("--evidence", default="", help="Evidence or example")

    p_pref = sub.add_parser("add-preference")
    p_pref.add_argument("--key", required=True, help="Preference key (e.g. risk_tolerance)")
    p_pref.add_argument("--value", required=True, help="Preference value")
    p_pref.add_argument("--note", default="", help="Additional note")

    p_pat = sub.add_parser("add-pattern")
    p_pat.add_argument("--pattern", required=True, help="Behavioral pattern description")

    p_past = sub.add_parser("add-past")
    p_past.add_argument("--title", required=True, help="Decision title")
    p_past.add_argument("--lesson", required=True, help="Lesson learned")

    sub.add_parser("summary")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    {
        "show": cmd_show,
        "add-bias": cmd_add_bias,
        "add-preference": cmd_add_preference,
        "add-pattern": cmd_add_pattern,
        "add-past": cmd_add_past,
        "summary": cmd_summary,
    }[args.command](args)


if __name__ == "__main__":
    main()
