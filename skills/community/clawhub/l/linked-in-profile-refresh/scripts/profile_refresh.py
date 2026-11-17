#!/usr/bin/env python3
"""LinkedIn profile refresh: section audit, headline rewriter,
duty->outcome bullet converter, stealth-sequence checklist,
message scripts. Pure stdlib; no LinkedIn API calls, no data
leaves the machine.

Commands:
  audit --headline H [--about-first A] [--bullets-file F]
  rewrite-headline --role R --domain D --keywords k1,k2
         [--scope S] [--pivot-from P]
  bullets --file F
  stealth          ordered checklist for employed job seekers
  scripts-list     connection / recruiter message templates
"""
import argparse
import math
import re
import sys

DUTY_PATTERNS = [
    ("responsible for", "Owned [what], [scale] — [result with number]"),
    ("worked on", "Shipped [what] — [metric]"),
    ("helped with", "Led [what] — [metric]"),
    ("assisted with", "Drove [what] — [metric]"),
    ("involved in", "Owned [piece] of [what] — [metric]"),
    ("managed the", "Grew/cut [what] — [before]->[after]"),
    ("participated in", "Delivered [what] across [scope] — [metric]"),
    ("duties included", "Led [top duty] — [metric]"),
]

OWNERSHIP_VERBS = ["Led", "Built", "Shipped", "Grew", "Cut",
                   "Automated", "Owned", "Drove", "Scaled",
                   "Delivered", "Reduced", "Launched"]

METRIC_MARKERS = re.compile(
    r"(\d+\s?%|\$\s?\d|\d+\s?(k|m|bn|million|billion|x|hrs?|hours|"
    r"days|weeks|people|person|clients?|markets?|users?|accounts|"
    r"engineers|reports|Q[1-4])\b|\b\d{2,}\b)", re.I)


def has_metric(text):
    return bool(METRIC_MARKERS.search(text))


def cmd_audit(a):
    print("PROFILE AUDIT")
    print("=" * 70)
    score = 0
    # headline
    h = a.headline or ""
    kw = len(re.findall(r"[|,]", h)) + 1
    issues = []
    if not h:
        issues.append("no headline given")
    else:
        if len(h) < 40:
            issues.append("too short (<40 chars) - loads no keywords")
        if len(h) > 220:
            issues.append(f"too long ({len(h)}/220) - silent truncation")
        if len(re.findall(r"[|·]", h)) < 2 and len(h.split()) < 8:
            issues.append("no keyword structure - add role | domain | "
                          "strengths | scope")
        if not re.search(r"\d", h) and "manager" not in h.lower():
            issues.append("no scope number - add team size / scale")
    if issues:
        print(f"HEADLINE: {'; '.join(issues)}")
    else:
        score += 1
        print("HEADLINE: ok — keyword structure present")

    # about first lines
    ab = a.about_first or ""
    if ab:
        if re.match(r"^(i am|i'm)?\s*(a\s+)?(results-driven|"
                    r"hard-working|motivated|detail-oriented|passionate)",
                    ab.strip(), re.I):
            print("ABOUT HOOK: cliche opener ('results-driven' etc) - "
                  "replace with what you do + a number")
        elif not has_metric(ab.split("\n")[0]):
            print("ABOUT HOOK: first line has no number - add one "
                  "(activation %, team size, revenue)")
        else:
            score += 1
            print("ABOUT HOOK: ok")

    # bullets
    if a.bullets_file:
        try:
            lines = [l.strip() for l in
                     open(a.bullets_file, encoding="utf-8")
                     if l.strip()]
        except OSError as e:
            sys.exit(f"cannot read bullets file: {e}")
        duty = 0
        no_metric = 0
        for l in lines:
            low = l.lower()
            if any(p in low for p, _ in DUTY_PATTERNS):
                duty += 1
            if not has_metric(l):
                no_metric += 1
        print(f"BULLETS: {len(lines)} checked - {duty} duty-phrased, "
              f"{no_metric} without a metric/scale marker")
        if duty == 0 and no_metric == 0:
            score += 1

    print("-" * 70)
    print(f"Sections passing: {score}/3 "
          + ("(solid — proceed to scripts/stealth)"
             if score >= 2 else "(rewrite before applying anywhere)"))


def cmd_headline(a):
    parts = [a.role.strip(), a.domain.strip()]
    kws = [k.strip() for k in a.keywords.split(",") if k.strip()]
    if kws:
        parts.append(", ".join(kws[:4]))
    if a.pivot_from:
        parts.insert(1, f"ex-{a.pivot_from.strip()}")
    if a.scope:
        parts.append(a.scope.strip())
    h = " | ".join(p for p in parts if p)
    if len(h) > 220:
        h = h[:217] + "..."
    print(f"HEADLINE ({len(h)}/220 chars):")
    print(f'  {h}')
    print("\nWhy: role token first (indexes for title search), then "
          "domain, then exact skill tokens, then scope proof.")


def cmd_bullets(a):
    try:
        lines = [l.strip() for l in open(a.file, encoding="utf-8")
                 if l.strip()]
    except OSError as e:
        sys.exit(f"cannot read file: {e}")
    if not lines:
        sys.exit("file empty")
    for i, l in enumerate(lines, 1):
        low = l.lower()
        scaffold = None
        for pat, fix in DUTY_PATTERNS:
            if pat in low:
                scaffold = fix
                break
        metric = "METRIC" if has_metric(l) else "NO METRIC"
        print(f"{i}. {l}")
        if scaffold:
            print(f"   -> duty phrase detected; rewrite scaffold: "
                  f"{scaffold}")
        elif metric == "NO METRIC":
            print("   -> add a scale marker (%, $, count, time, "
                  "team size, markets) — no metric reads as padding")
        else:
            print("   -> ok: outcome phrasing with metric")
        print()


def cmd_stealth(_a=None):
    steps = [
        ("BEFORE any edit: Settings -> Visibility -> turn OFF "
         "'Share profile changes with network'", "first — order "
         "matters, later is too late"),
        ("Open to Work: set 'Recruiters only' — NEVER the green "
         "banner while employed", "banner is public; recruiter-only "
         "is not (residual risk: your recruiters on LinkedIn "
         "Recruiter can see it)"),
        ("Spread edits over 3-5 days (headline day 1, About day 2, "
         "bullets day 3-4, skills day 5)", "change bursts leak into "
         "feeds even with notifications off"),
        ("No job-post likes / company-page follow bursts during "
         "stealth mode", "recommendation engine tells more than "
         "the profile"),
        ("Photo/banner refresh: fine anytime — profile views are "
         "normal", "credibility hygiene, not a job-seeker tell"),
    ]
    print("STEALTH REFRESH SEQUENCE (employed job seekers)")
    print("=" * 70)
    for i, (step, why) in enumerate(steps, 1):
        print(f"{i}. {step}")
        print(f"   why: {why}")
    print("=" * 70)
    print("Unemployed/public search: skip stealth, add "
          "'| Open to [role] roles' to headline + green banner "
          "(it measurably raises recruiter contacts).")


SCRIPTS = [
    ("Connection request (300-char cap)",
     "Hi {name} — saw your {shared thing, e.g. talk on X / post "
     "about Y}. The {specific detail} framing stuck with me. "
     "Good to connect here."),
    ("Recruiter reply — interested",
     "Hi {name}, thanks for reaching out. {Role} sounds relevant — "
     "{one-line fit}. Could you share the salary band and team "
     "size? Happy to set up a call this week."),
    ("Recruiter reply — not looking, staying warm",
     "Flattered — not exploring moves right now, but {role type} "
     "is squarely my lane for the future; keep me posted on "
     "senior versions."),
    ("Post-call follow-up (same day)",
     "Thanks for the time today, {name} — especially the "
     "{specific topic} discussion. Attached is the {asked-for "
     "item}. Looking forward to next steps."),
    ("Reconnect after a gap",
     "Hi {name} — it's been a while since {context}. I'm now "
     "{1-line now}. Would love to catch up for 15 minutes "
     "sometime this month."),
]


def cmd_scripts(_a=None):
    print("MESSAGE SCRIPTS (fill braces, keep under stated caps)")
    print("=" * 70)
    for name, body in SCRIPTS:
        print(f"-- {name}")
        print(f"   {body}\n")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.
                                 RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    au = sub.add_parser("audit")
    au.add_argument("--headline", default=None)
    au.add_argument("--about-first", default=None)
    au.add_argument("--bullets-file", default=None)
    au.set_defaults(func=cmd_audit)
    rh = sub.add_parser("rewrite-headline")
    rh.add_argument("--role", required=True)
    rh.add_argument("--domain", required=True)
    rh.add_argument("--keywords", required=True,
                    help="comma-separated exact skill tokens")
    rh.add_argument("--scope", default=None)
    rh.add_argument("--pivot-from", default=None)
    rh.set_defaults(func=cmd_headline)
    bu = sub.add_parser("bullets")
    bu.add_argument("--file", required=True)
    bu.set_defaults(func=cmd_bullets)
    st = sub.add_parser("stealth")
    st.set_defaults(func=cmd_stealth)
    sc = sub.add_parser("scripts-list")
    sc.set_defaults(func=cmd_scripts)
    a = p.parse_args()
    try:
        a.func(a)
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
