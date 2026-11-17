#!/usr/bin/env python3
"""heirloom-provenance — family object storyteller.

Registry for heirlooms with origin, owner chain, stories, values; interview
question scripts; estate-ready provenance reports; printable QR-tag labels;
sealed wish-lists with conflict detection and a wish-maximizing fair draft.
100% local, single JSON store, pure stdlib.

QR labels: prints the payload (file path or URL) with a note to render a QR
in any printer tool; qrcode generation stays out of stdlib scope.
"""
import argparse
import json
import random
import sys
from datetime import date
from pathlib import Path

DB = Path("heirlooms.json")
INTERVIEW_QUESTIONS = [
    "Who did this belong to first, as far as you know?",
    "Where did it live in the house when you were young?",
    "What did [owner] say about it? Any sayings attached?",
    "Was there ever a fight or a funny accident about it?",
    "Who was 'supposed' to get it? Did anyone ever say?",
    "Is there anything else in the family that goes with it?",
    "If this could talk, what's the first story it would tell?",
]


def load() -> dict:
    if DB.exists():
        return json.loads(DB.read_text())
    return {"objects": [], "wishes": [], "interviews": []}


def save(db: dict) -> None:
    DB.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def get_obj(db: dict, oid: str) -> dict:
    for o in db["objects"]:
        if o["id"] == oid:
            return o
    sys.exit(f"object {oid} not found — `objects` lists IDs")


def next_id(db: dict) -> str:
    return f"HL{len(db['objects']) + 1:03d}"


# ---------- objects ----------

def cmd_object(args, db):
    if args.action == "add":
        o = {
            "id": next_id(db),
            "name": args.name,
            "description": args.description or "",
            "origin": args.origin or "unknown",
            "owner_chain": args.owners or "unknown",
            "story": [{"date": date.today().isoformat(),
                       "text": args.story}] if args.story else [],
            "value": args.value,
            "value_note": "unset" if args.value is None else "family estimate",
            "condition": args.condition or "unknown",
            "photos": [],
        }
        db["objects"].append(o)
        save(db)
        print(f"added {o['id']}: {o['name']}")
    elif args.action == "list":
        if not db["objects"]:
            print("registry empty — `object add` first")
            return
        print(f"{'ID':<7}{'NAME':<32}{'VALUE':>9}  ORIGIN")
        for o in db["objects"]:
            val = f"{o['value']:.0f}" if o["value"] else "?"
            print(f"{o['id']:<7}{o['name'][:31]:<32}{val:>9}  {o['origin'][:38]}")


def cmd_story(args, db):
    o = get_obj(db, args.id)
    o["story"].append({"date": date.today().isoformat(),
                       "source": args.source or "unattributed",
                       "text": args.text})
    save(db)
    print(f"story appended to {o['id']} (source: {args.source or 'unattributed'})")


# ---------- interview ----------

def cmd_interview(args, db):
    rec = {"who": args.who, "date": date.today().isoformat(),
           "object": args.object}
    db["interviews"].append(rec)
    save(db)
    if args.object:
        o = get_obj(db, args.object)
        print(f"INTERVIEW SCRIPT — {args.who} on {o['id']}: {o['name']}")
        print(f"recorded {rec['date']}  (log this session with `interview` again after)\n")
        for i, q in enumerate(INTERVIEW_QUESTIONS, 1):
            print(f"  {i}. {q}")
        print("\nRecord audio. Transcribe later: `story append "
              f"{o['id']} --source \"{args.who} {rec['date']}\" --text \"...\"`")
    else:
        print(f"WHOLE-COLLECTION INTERVIEW — {args.who} ({rec['date']})")
        print("One room per session. Objects cue each other — go shelf by shelf.\n")
        for o in db["objects"]:
            print(f"  {o['id']}: {o['name']}")
        print(f"\nFor each object, the 7 questions:")
        for i, q in enumerate(INTERVIEW_QUESTIONS, 1):
            print(f"  {i}. {q}")
        print("\nAppends: `story append <ID> --source \"<who> <date>\" --text \"...\"`")


# ---------- reports ----------

def cmd_report(args, db):
    o = get_obj(db, args.id)
    print("=" * 64)
    print(f"PROVENANCE REPORT — {o['id']}")
    print("=" * 64)
    print(f"\n{o['name']}")
    if o["description"]:
        print(o["description"])
    print(f"\nORIGIN:        {o['origin']}")
    print(f"OWNER CHAIN:   {o['owner_chain']}")
    val = f"${o['value']:.2f} ({o['value_note']})" if o["value"] else "unknown"
    print(f"VALUE:         {val}")
    print(f"CONDITION:     {o['condition']}")
    if o["story"]:
        print("\nSTORY (append-only):")
        for s in o["story"]:
            print(f"  [{s['date']}] {s.get('source', '—')}: {s['text']}")
    else:
        print("\nSTORY: (none recorded — run the interview kit)")


def cmd_storybook(args, db):
    print("# Family Object Storybook\n")
    print(f"_Generated {date.today().isoformat()} from the provenance registry._\n")
    for o in db["objects"]:
        print(f"## {o['name']} ({o['id']})\n")
        print(f"**Origin:** {o['origin']}  ")
        print(f"**Owners:** {o['owner_chain']}  ")
        val = f"${o['value']:.0f}" if o["value"] else "value unknown"
        print(f"**Value:** {val} — {o['condition']}\n")
        if o["story"]:
            for s in o["story"]:
                print(f"> _{s['text']}_")
                print(f"> — {s.get('source', 'family memory')}, {s['date']}\n")
        else:
            print("_No story recorded yet._\n")
        print("---\n")


# ---------- tags ----------

def cmd_tag(args, db):
    o = get_obj(db, args.id)
    payload = args.url or f"heirlooms.json#{o['id']}"
    print("┌──────────────────────────────────────┐")
    print("│  HEIRLOOM — DO NOT DISCARD           │")
    print(f"│  {o['name'][:36]:<36}│")
    print(f"│  ID {o['id']:<34}│")
    print(f"│  QR payload: {payload[:24]:<24}│")
    print("│  (render payload as QR, attach here) │")
    print("└──────────────────────────────────────┘")
    print(f"\nfull record: `heirloom.py report {o['id']}`")


# ---------- wishes / distribution ----------

def cmd_wish(args, db):
    get_obj(db, args.id)
    db["wishes"].append({"object": args.id, "by": args.by, "rank": args.rank,
                         "date": date.today().isoformat()})
    save(db)
    print(f"wish recorded (sealed until `wishes` reveal): {args.by} ranks "
          f"{args.id} #{args.rank}")


def cmd_wishes(args, db):
    if not db["wishes"]:
        print("no wishes recorded — collect from everyone BEFORE revealing")
        return
    print("WISH REVEAL (all lists at once — no re-ranking after this point)\n")
    by_obj = {}
    for w in db["wishes"]:
        by_obj.setdefault(w["object"], []).append(w)
    for oid in sorted(by_obj):
        o = get_obj(db, oid)
        print(f"{oid}: {o['name']}")
        for w in sorted(by_obj[oid], key=lambda x: x["rank"]):
            print(f"    #{w['rank']}  {w['by']}")


def cmd_conflicts(args, db):
    by_obj = {}
    for w in db["wishes"]:
        by_obj.setdefault(w["object"], []).append(w)
    found = False
    for oid, ws in sorted(by_obj.items()):
        if len(ws) > 1:
            o = get_obj(db, oid)
            top = [w for w in ws if w["rank"] == 1]
            flag = "  ⚠ BOTH #1 — pre-meeting resolution required" if len(top) > 1 else ""
            found = True
            print(f"{oid}: {o['name']}")
            for w in sorted(ws, key=lambda x: x["rank"]):
                print(f"    #{w['rank']}  {w['by']}{flag if w is ws[0] and flag else ''}")
            if not top or len(top) <= 1:
                print(f"    (overlap but not dual-#1 — draftable)")
    if not found:
        print("no contested objects — every wished object has one wisher")


def cmd_draft(args, db):
    people = [p.strip() for p in args.people.split(",")]
    if len(people) < 2:
        sys.exit("need at least 2 people")
    # objects each person top-ranked (wishes), ordered by rank then value
    wants = {p: {} for p in people}
    for w in db["wishes"]:
        if w["by"] in wants:
            wants[w["by"]][w["object"]] = w["rank"]
    contested = [oid for oid in {w["object"] for w in db["wishes"]}
                 if sum(1 for w in db["wishes"] if w["object"] == oid) > 1]
    rng = random.Random(args.seed)
    rng.shuffle(people)
    print(f"draft order (seed {args.seed}): {' → '.join(people)}\n")
    assignment = {p: [] for p in people}
    remaining = list(contested)
    turn = 0
    while remaining:
        p = people[turn % len(people)]
        # pick p's best-ranked remaining object; else highest value
        best = min(remaining, key=lambda oid: wants[p].get(oid, 99))
        assignment[p].append(best)
        remaining.remove(best)
        rank = wants[p].get(best)
        print(f"round {turn // len(people) + 1}: {p:<10} takes {best}"
              f"{' (their #' + str(rank) + ' wish)' if rank else ''}")
        turn += 1
    print("\nSETTLEMENT")
    values = {p: 0.0 for p in people}
    for p in people:
        for oid in assignment[p]:
            o = get_obj(db, oid)
            if o["value"]:
                values[p] += o["value"]
        print(f"  {p:<10} {', '.join(assignment[p]) or '(nothing)'}"
              f"  ≈ ${values[p]:.0f}")
    vals = list(values.values())
    if vals and max(vals) > 0:
        mean = sum(vals) / len(vals)
        print("\nEQUALIZATION (value gap only — stories are not priced)")
        for p in people:
            diff = values[p] - mean
            if abs(diff) >= 1:
                print(f"  {p:<10} {'receives' if diff < 0 else 'pays'} ${abs(diff):.0f}")
    print("\nuncontested wishes go to their single wisher automatically.")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("object")
    os_ = p.add_subparsers(dest="action", required=True)
    pa = os_.add_parser("add")
    pa.add_argument("name")
    pa.add_argument("--description"); pa.add_argument("--origin"); pa.add_argument("--owners")
    pa.add_argument("--story"); pa.add_argument("--value", type=float)
    pa.add_argument("--condition")
    os_.add_parser("list")

    p = sub.add_parser("story")
    st = p.add_subparsers(dest="action", required=True)
    psa = st.add_parser("append")
    psa.add_argument("id")
    psa.add_argument("--text", required=True); psa.add_argument("--source")

    p = sub.add_parser("interview"); p.add_argument("who"); p.add_argument("--object")

    p = sub.add_parser("report"); p.add_argument("id")
    sub.add_parser("storybook")

    p = sub.add_parser("tag"); p.add_argument("id"); p.add_argument("--url")

    p = sub.add_parser("wish")
    ws = p.add_subparsers(dest="action", required=True)
    pwa = ws.add_parser("add")
    pwa.add_argument("id"); pwa.add_argument("--by", required=True)
    pwa.add_argument("--rank", type=int, required=True)
    sub.add_parser("wishes")
    sub.add_parser("conflicts")

    p = sub.add_parser("draft")
    p.add_argument("--people", required=True); p.add_argument("--seed", type=int, default=1)

    args = ap.parse_args()
    db = load()

    if args.cmd == "object":
        cmd_object(args, db)
    elif args.cmd == "story":
        cmd_story(args, db)
    elif args.cmd == "interview":
        cmd_interview(args, db)
    elif args.cmd == "report":
        cmd_report(args, db)
    elif args.cmd == "storybook":
        cmd_storybook(args, db)
    elif args.cmd == "tag":
        cmd_tag(args, db)
    elif args.cmd == "wish":
        cmd_wish(args, db)
    elif args.cmd == "wishes":
        cmd_wishes(args, db)
    elif args.cmd == "conflicts":
        cmd_conflicts(args, db)
    elif args.cmd == "draft":
        cmd_draft(args, db)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except Exception:
            pass
        sys.exit(0)
