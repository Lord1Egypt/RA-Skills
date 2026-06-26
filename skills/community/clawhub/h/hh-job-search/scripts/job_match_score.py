#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def overlap(a, b):
    sa = {x.strip().lower() for x in a if str(x).strip()}
    sb = {x.strip().lower() for x in b if str(x).strip()}
    return sorted(sa & sb)


def main():
    if len(sys.argv) != 3:
        print("Usage: job_match_score.py <profile.json> <vacancy.json>", file=sys.stderr)
        sys.exit(2)

    profile = load_json(sys.argv[1])
    vacancy = load_json(sys.argv[2])

    score = 0
    reasons = []
    penalties = []

    profile_stack = profile.get("stack", [])
    vacancy_stack = vacancy.get("stack", [])
    shared_stack = overlap(profile_stack, vacancy_stack)
    score += min(len(shared_stack) * 12, 48)
    if shared_stack:
        reasons.append(f"shared stack: {', '.join(shared_stack)}")

    target_roles = [x.lower() for x in profile.get("target_roles", [])]
    title = str(vacancy.get("title", "")).lower()
    if any(role in title for role in target_roles):
        score += 20
        reasons.append("title matches target roles")

    profile_remote = str(profile.get("remote_mode", "")).lower()
    vacancy_remote = str(vacancy.get("remote_mode", "")).lower()
    if profile_remote and vacancy_remote and profile_remote == vacancy_remote:
        score += 10
        reasons.append("remote mode matches")

    salary_floor = profile.get("salary_floor")
    salary_max = vacancy.get("salary_max") or vacancy.get("salary_min")
    if salary_floor and salary_max:
        if salary_max >= salary_floor:
            score += 15
            reasons.append("salary meets floor")
        else:
            score -= 15
            penalties.append("salary below floor")

    exclude = [x.lower() for x in profile.get("exclude_keywords", [])]
    if any(word in title for word in exclude):
        score -= 30
        penalties.append("excluded keyword in title")

    fit = "skip"
    if score >= 60:
        fit = "strong-match"
    elif score >= 35:
        fit = "possible-match"

    print(json.dumps({
        "fit_label": fit,
        "fit_score": score,
        "fit_reasons": reasons,
        "reasons": reasons,
        "penalties": penalties,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
