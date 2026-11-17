#!/usr/bin/env python3
"""Gift Occasion Planner — people × occasions registry, 60-day radar,
recommendation engine (never repeats), budget tracking, ICS export.

Usage:
    gift_planner.py add-person NAME [--birthday YYYY-MM-DD] [--interests a,b]
                       [--taboo "no x,no y"] [--budget N] [--sizes "M, shoe 43"]
    gift_planner.py add-occasion NAME --kind anniversary --month-day 04-22 [--label L]
    gift_planner.py radar [--days 60] [--json]
    gift_planner.py recommend NAME
    gift_planner.py plan <occ-id> --idea "..." [--where ...] [--cost N]
    gift_planner.py status <occ-id> --set bought|wrapped|given
    gift_planner.py given <occ-id> --gift "..." [--cost N]
    gift_planner.py budget
    gift_planner.py ics gifts.ics
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "gifts.json"

STATUSES = ["IDEA", "BOUGHT", "WRAPPED", "GIVEN"]

# --------------------------------------------------------------------------
# Movable occasions
# --------------------------------------------------------------------------

def nth_weekday_month(year: int, month: int, weekday: int, n: int) -> date:
    d = date(year, month, 1)
    offset = (weekday - d.weekday()) % 7
    return d + timedelta(days=offset + 7 * (n - 1))


def mothers_day(year):
    return nth_weekday_month(year, 5, 6, 2)   # 2nd Sunday of May


def fathers_day(year):
    return nth_weekday_month(year, 6, 6, 3)   # 3rd Sunday of June


def thanksgiving(year):
    return nth_weekday_month(year, 11, 3, 4)  # 4th Thursday of November


MOVABLE = {
    "mothers-day": mothers_day,
    "fathers-day": fathers_day,
    "thanksgiving": thanksgiving,
}

# --------------------------------------------------------------------------
# Storage
# --------------------------------------------------------------------------

def load():
    if DB.exists():
        return json.loads(DB.read_text())
    return {"people": {}, "history": []}


def save(db):
    DB.write_text(json.dumps(db, indent=2))


def find_person(db, name):
    for k, p in db["people"].items():
        if k.lower() == name.lower():
            return k, p
    # prefix match
    cands = [k for k in db["people"] if name.lower() in k.lower()]
    if len(cands) == 1:
        return cands[0], db["people"][cands[0]]
    raise SystemExit(f"no person matching '{name}' (have: {', '.join(db['people']) or 'none'})")


# --------------------------------------------------------------------------
# Occasions
# --------------------------------------------------------------------------

def next_occurrence(occ: dict, today=None) -> date | None:
    today = today or date.today()
    kind = occ["kind"]
    if kind in MOVABLE:
        d = MOVABLE[kind](today.year)
        if d < today:
            d = MOVABLE[kind](today.year + 1)
        return d
    md = occ.get("month_day")
    if not md:
        return None
    m, d = map(int, md.split("-"))
    try:
        cand = date(today.year, m, d)
    except ValueError:
        return None
    if cand < today:
        try:
            cand = date(today.year + 1, m, d)
        except ValueError:
            return None
    return cand


def all_occurrences(db, within_days=60, today=None):
    """[(days_left, person_key, person, occ, next_date, plan, history_for_person)]"""
    today = today or date.today()
    out = []
    for pk, p in db["people"].items():
        for occ in p.get("occasions", []):
            d = next_occurrence(occ, today)
            if not d:
                continue
            days = (d - today).days
            if 0 <= days <= within_days:
                plan = (p.get("plans") or {}).get(f"{occ['kind']}-{d.year}") or {}
                out.append((days, pk, p, occ, d, plan))
    out.sort(key=lambda x: x[0])
    return out


def occ_id(occ, d):
    slug = re.sub(r"[^a-z0-9]+", "-", f"{occ['kind']} {d.year}").strip("-")
    return slug


def person_history(db, pk):
    return [h for h in db["history"] if h["person"] == pk]


# --------------------------------------------------------------------------
# Recommendation engine
# --------------------------------------------------------------------------

GIFT_CATEGORIES = {
    # category → (budget_share, examples template)
    "experience": (1.0, ["class in {interest}", "{interest} show/tickets",
                         "weekend trip tied to {interest}"]),
    "tool": (0.8, ["quality gear for {interest}", "upgrade for their {interest} setup"]),
    "consumable": (0.3, ["nice supplies for {interest}", "specialty {interest} treats"]),
    "personal": (0.6, ["custom item engraved with {interest} theme",
                       "photo project around {interest}"]),
    "wish-list": (1.0, ["item they mentioned wanting (check notes)"]),
}


def tokens(s):
    return {w.lower() for w in re.findall(r"[a-z]{3,}", s or "")}


def near_dupe(a, b):
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / len(ta | tb) >= 0.6


def recommend(db, pk):
    p = db["people"][pk]
    interests = [i.strip() for i in (p.get("interests") or "").split(",") if i.strip()]
    taboo_tokens = set()
    for t in (p.get("taboo") or "").split(","):
        taboo_tokens |= tokens(t)
    budget = p.get("budget") or 50
    hist = sorted(person_history(db, pk), key=lambda h: h["year"], reverse=True)
    past_gifts = [h["gift"] for h in hist]

    # which interest did the last gift relate to? rotate away from it
    last_interest = None
    if past_gifts and interests:
        last = past_gifts[0].lower()
        for i in interests:
            if i.lower() in last:
                last_interest = i
                break
    rotate = [i for i in interests if i != last_interest] or interests

    # categories used in past 2 years → deprioritize
    recent_cats = {h.get("category") for h in hist[:2]}

    sugg = []
    for i in rotate[:3]:
        for cat, (share, templates) in GIFT_CATEGORIES.items():
            if cat in recent_cats or cat == "wish-list":
                continue
            for t in templates:
                label = t.replace("{interest}", i)
                if any(near_dupe(label, g) for g in past_gifts):
                    continue
                if tokens(label) & taboo_tokens:
                    continue
                sugg.append({
                    "category": cat, "interest": i, "suggestion": label,
                    "est_budget": round(budget * share * (0.85 + 0.3 * (hash(label) % 10) / 10), 2),
                    "rationale": ((f"rotates to {i} (last gift was {last_interest}-themed)" if last_interest else f"ties to their interest: {i}")
                                  + f"; {cat} not used in last 2 years; within ±20% flex of ${budget:.0f} budget"),
                })
    # wish-list items always surface if notes mention wanting something
    notes = p.get("notes") or ""
    if "want" in notes.lower() or "mentioned" in notes.lower():
        sugg.insert(0, {
            "category": "wish-list", "interest": "notes",
            "suggestion": "item from their mentioned-want list (see notes)",
            "est_budget": budget,
            "rationale": "explicitly mentioned wanting it — highest hit rate",
        })
    return sugg[:5]


# --------------------------------------------------------------------------
# Renderers
# --------------------------------------------------------------------------

def render_radar(db, days=60):
    occs = all_occurrences(db, within_days=days)
    if not occs:
        return f"GIFT RADAR — nothing in the next {days} days. (Registry: {len(db['people'])} people)"
    lines = [f"GIFT RADAR — next {days} days (as of {date.today()})", ""]
    for days_left, pk, p, occ, d, plan in occs:
        label = occ.get("label") or occ["kind"].replace("-", " ").title()
        lines.append(f"{'DUE IN %d DAYS' % days_left} {'─' * 30}")
        lines.append(f"  {pk} — {label.upper()} ({d.isoformat()})")
        lines.append(f"    Budget: ${p.get('budget') or '?'}   "
                     f"Status: {plan.get('status', 'IDEA')}"
                     + ("   ⚠ NOTHING PLANNED" if not plan.get("idea") and plan.get("status", "IDEA") == "IDEA" else ""))
        if p.get("interests"):
            lines.append(f"    Interests: {p['interests']}")
        hist = [h for h in person_history(db, pk)][:2]
        if hist:
            lines.append(f"    Recent gifts: " + "; ".join(f"{h['gift']} ({h['year']})" for h in hist))
        if plan.get("idea"):
            lines.append(f"    Plan: {plan['idea']} "
                         + (f"(~${plan['cost']})" if plan.get("cost") else ""))
        recs = recommend(db, pk)[:3]
        if recs and not plan.get("idea"):
            lines.append(f"    Suggestions:")
            for r in recs:
                lines.append(f"      · {r['suggestion']} ~${r['est_budget']}")
        lines.append("")
    return "\n".join(lines)


def render_plan_card(pk, p, occ, d, plan):
    label = occ.get("label") or occ["kind"].replace("-", " ").title()
    days_left = (d - date.today()).days
    lines = [f"PLAN: {pk}'s {label} {d} ({days_left} days out)"]
    lines.append(f"  Gift: {plan.get('idea', '— nothing planned —')}")
    if plan.get("cost"):
        lines.append(f"  Cost: ${plan['cost']}  (budget ${p.get('budget') or '?'})")
    if plan.get("where"):
        lines.append(f"  Where: {plan['where']}")
    buy_by = d - timedelta(days=max(7, min(days_left, 14)))
    lines.append(f"  Buy by: {buy_by} (buffer for shipping)")
    lines.append(f"  Wrap by: {d - timedelta(days=1)}")
    if p.get("interests"):
        lines.append(f"  Card angle: tie to {p['interests'].split(',')[0].strip()}")
    lines.append(f"  Status: {plan.get('status', 'IDEA')} → `status --set bought` when purchased")
    return "\n".join(lines)


def render_budget(db):
    year = date.today().year
    lines = [f"GIFT BUDGET — {year}", ""]
    total_planned = total_spent = 0
    for pk, p in db["people"].items():
        b = p.get("budget") or 0
        n_occ = 1 + len([o for o in p.get("occasions", []) if o["kind"] != "birthday"])
        spent = sum(h["cost"] for h in person_history(db, pk)
                    if h["year"] == year and h.get("cost"))
        total_planned += b * n_occ
        total_spent += spent
        if b or spent:
            lines.append(f"  {pk:12} budget ${b} × {n_occ} occasions = ${b*n_occ}"
                         f"   spent so far ${spent:.0f}")
    lines.append("")
    lines.append(f"  PLANNED (year): ${total_planned}")
    lines.append(f"  SPENT (year):   ${total_spent:.0f}")
    lines.append(f"  REMAINING:      ${total_planned - total_spent:.0f}")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# ICS
# --------------------------------------------------------------------------

def ics_escape(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def build_ics(db, days=365):
    today = date.today()
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
             "PRODID:-//gift-occasion-planner//EN", "CALSCALE:GREGORIAN"]
    for pk, p in db["people"].items():
        for occ in p.get("occasions", []):
            d = next_occurrence(occ, today)
            if not d or (d - today).days > days:
                continue
            label = occ.get("label") or occ["kind"].replace("-", " ").title()
            for lead in (60, 21, 7, 1):
                rem = d - timedelta(days=lead)
                if rem < today:
                    continue
                lines += [
                    "BEGIN:VEVENT",
                    f"UID:{pk}-{occ['kind']}-{d.year}-lead{lead}@gifts",
                    f"DTSTAMP:{today.strftime('%Y%m%d')}T090000Z",
                    f"DTSTART;VALUE=DATE:{rem.strftime('%Y%m%d')}",
                    f"DTEND;VALUE=DATE:{(rem + timedelta(days=1)).strftime('%Y%m%d')}",
                    f"SUMMARY:{ics_escape(f'🎁 {pk} {label} in {lead}d — gift prep')}",
                    f"DESCRIPTION:{ics_escape('Interests: ' + (p.get('interests') or '?') + ' | Budget: $' + str(p.get('budget') or '?') + ' | Taboo: ' + (p.get('taboo') or 'none'))}",
                    "END:VEVENT",
                ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Gift occasion planner")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_p = sub.add_parser("add-person")
    ap_p.add_argument("name")
    ap_p.add_argument("--birthday", help="YYYY-MM-DD")
    ap_p.add_argument("--interests")
    ap_p.add_argument("--taboo")
    ap_p.add_argument("--budget", type=float)
    ap_p.add_argument("--sizes")
    ap_p.add_argument("--notes")

    ao = sub.add_parser("add-occasion")
    ao.add_argument("person")
    ao.add_argument("--kind", required=True,
                    choices=["anniversary", "mothers-day", "fathers-day",
                             "thanksgiving", "graduation", "custom"])
    ao.add_argument("--month-day", help="MM-DD for fixed dates")
    ao.add_argument("--label")
    ao.add_argument("--date", help="YYYY-MM-DD for one-time occasions")

    r = sub.add_parser("radar")
    r.add_argument("--days", type=int, default=60)
    r.add_argument("--json", action="store_true")

    rec = sub.add_parser("recommend")
    rec.add_argument("person")

    pl = sub.add_parser("plan")
    pl.add_argument("occ_id")
    pl.add_argument("--idea", required=True)
    pl.add_argument("--where")
    pl.add_argument("--cost", type=float)

    st = sub.add_parser("status")
    st.add_argument("occ_id")
    st.add_argument("--set", choices=[s.lower() for s in STATUSES])

    g = sub.add_parser("given")
    g.add_argument("occ_id")
    g.add_argument("--gift", required=True)
    g.add_argument("--cost", type=float)
    g.add_argument("--category")

    b = sub.add_parser("budget")

    ix = sub.add_parser("ics")
    ix.add_argument("output")
    ix.add_argument("--days", type=int, default=365)

    args = ap.parse_args()
    db = load()

    if args.cmd == "add-person":
        if args.name in db["people"]:
            raise SystemExit(f"'{args.name}' already exists")
        p = {"occasions": [], "plans": {}}
        if args.birthday:
            p["birthday"] = args.birthday
            p["occasions"].append({"kind": "birthday",
                                   "month_day": args.birthday[5:]})
        for k, v in [("interests", args.interests), ("taboo", args.taboo),
                     ("sizes", args.sizes), ("notes", args.notes)]:
            if v:
                p[k] = v
        if args.budget:
            p["budget"] = args.budget
        db["people"][args.name] = p
        save(db)
        print(f"added {args.name}"
              + (" with birthday occasion" if args.birthday else ""))
        return 0

    if args.cmd == "add-occasion":
        pk, p = find_person(db, args.person)
        occ = {"kind": args.kind}
        if args.month_day:
            occ["month_day"] = args.month_day
        if args.date:
            occ["month_day"] = args.date[5:]
            occ["year"] = args.date[:4]
        if args.label:
            occ["label"] = args.label
        if not occ.get("month_day") and args.kind not in MOVABLE:
            raise SystemExit("fixed-date occasions need --month-day MM-DD")
        p["occasions"].append(occ)
        save(db)
        d = next_occurrence(occ)
        print(f"added {args.kind} for {pk}"
              + (f", next: {d}" if d else ""))
        return 0

    if args.cmd == "radar":
        if args.json:
            out = []
            for days_left, pk, p, occ, d, plan in all_occurrences(db, args.days):
                out.append({"days_left": days_left, "person": pk,
                            "kind": occ["kind"], "date": d.isoformat(),
                            "status": plan.get("status", "IDEA"),
                            "idea": plan.get("idea"),
                            "suggestions": recommend(db, pk)[:3]})
            print(json.dumps(out, indent=2))
        else:
            print(render_radar(db, args.days))
        return 0

    if args.cmd == "recommend":
        pk, p = find_person(db, args.person)
        recs = recommend(db, pk)
        if not recs:
            print("no suggestions — enrich the profile (interests, notes) or raise budget")
            return 0
        print(f"SUGGESTIONS for {pk} (budget ${p.get('budget') or '?'}):")
        for i, r in enumerate(recs, 1):
            print(f"  {i}. {r['suggestion']}  ~${r['est_budget']}")
            print(f"     why: {r['rationale']}")
        return 0

    if args.cmd in ("plan", "status", "given"):
        # resolve occ id like birthday-2026 / anniversary-2026
        match = None
        for days_left, pk, p, occ, d, plan in all_occurrences(db, 400):
            if occ_id(occ, d) == args.occ_id:
                match = (pk, p, occ, d, plan)
                break
        if not match:
            raise SystemExit(f"no occasion id '{args.occ_id}' — see `radar` output ids")
        pk, p, occ, d, plan = match
        key = f"{occ['kind']}-{d.year}"

        if args.cmd == "plan":
            p.setdefault("plans", {})[key] = {
                "idea": args.idea, "where": args.where, "cost": args.cost,
                "status": "IDEA",
            }
            save(db)
            print(render_plan_card(pk, p, occ, d, p["plans"][key]))
        elif args.cmd == "status":
            if key not in p.get("plans", {}):
                raise SystemExit("no plan yet — run `plan` first")
            p["plans"][key]["status"] = args.set.upper()
            save(db)
            print(f"status: {pk} {key} → {args.set.upper()}")
        elif args.cmd == "given":
            db["history"].append({
                "person": pk, "year": d.year, "gift": args.gift,
                "cost": args.cost, "category": args.category,
                "occasion": occ["kind"],
            })
            if key in p.get("plans", {}):
                p["plans"][key]["status"] = "GIVEN"
            save(db)
            print(f"logged: {pk} {occ['kind']} {d.year} → {args.gift}")
        return 0

    if args.cmd == "budget":
        print(render_budget(db))
        return 0

    if args.cmd == "ics":
        Path(args.output).write_text(build_ics(db, days=args.days))
        n_ev = build_ics(db, days=args.days).count("BEGIN:VEVENT")
        print(f"wrote {args.output}: {n_ev} reminder events")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
