#!/usr/bin/env python3
"""Spread pins over the coming weeks the way Pinterest likes them (a steady trickle, new designs for
a link days apart, seasonal pins well ahead of the moment) and write the WoopSocial request for each.

    python3 scripts/schedule.py plan.json --start 2026-11-16
    python3 scripts/schedule.py plan.json --bodies-only     # times already set; just (re)write requests

Rules (change them in plan.json "rules" or with the flags):
- at most --per-day pins per account per day (default 1; Pinterest rewards consistency, not bursts);
- new pins for the same link at least --gap days apart (default 7), also counting pins in the log;
- a link with a "moment" (a holiday, a launch, a season) gets its pins 90 to 45 days before it
  (`lead_days` changes that); later than that the schedule says so, and a pin that would go live
  after the moment isn't scheduled at all.
Each account posts at its own `times` in its own `timezone`. Pinterest is not hour-sensitive the
way TikTok is; spacing matters far more than the hour, so a placeholder time is fine.

Writes schedule.md (the table to show the user) and requests/<pin>.json: the exact body for
WoopSocial's posts_validate and posts_create. Needs Python 3.9+ (zoneinfo); Windows: pip install tzdata.
"""
import argparse, json, os, sys
from collections import defaultdict
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pinlib as P  # noqa: E402

DEFAULT_TIME = "20:00"
LEAD_MAX, LEAD_MIN = 90, 45


to_utc = P.to_utc


def times_of(acc):
    t = acc.get("times") or [DEFAULT_TIME]
    out = []
    for x in (t if isinstance(t, list) else str(t).split(",")):
        try:
            hh, mm = str(x).strip().split(":")
            hh, mm = int(hh), int(mm)
            assert 0 <= hh < 24 and 0 <= mm < 60
        except (ValueError, AssertionError):
            sys.exit(f"posting time '{x}' must look like 20:30")
        out.append((hh, mm))
    return sorted(out)


def body_for(pin, plan, tz):
    acc = plan["accounts"].get(pin.get("account"), {})
    url, _ = P.link_of(pin, plan["links"])
    board = pin.get("board")
    board_id = (acc.get("boards") or {}).get(board) or f"<board id for '{board}'>"
    mid = (pin.get("mediaIds") or [None])[0] or f"<mediaId for {os.path.basename(pin.get('file', 'file'))}>"
    sa = {"platform": "PINTEREST",
          "socialAccountId": acc.get("socialAccountId") or f"<socialAccountId for {pin.get('account')}>",
          "pinterestBoardId": board_id}
    if pin.get("title"):
        sa["title"] = pin["title"]
    if url:
        sa["link"] = url
    body = {"content": [{"text": pin.get("description", ""), "media": [{"type": "MEDIA_LIBRARY", "mediaId": mid}]}],
            "socialAccounts": [sa]}
    if pin.get("now"):
        body["schedule"] = {"type": "PUBLISH_NOW"}
    elif pin.get("at"):
        body["schedule"] = {"type": "SCHEDULE_FOR_LATER", "scheduledFor": to_utc(pin["at"], tz)}
    else:
        body["schedule"] = {"type": "DRAFT"}
    return body


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan")
    ap.add_argument("--start", help="first day, YYYY-MM-DD (default: tomorrow)")
    ap.add_argument("--per-day", type=int, help="pins per account per day (default 1)")
    ap.add_argument("--gap", type=int, help="days between new pins for the same link (default 7)")
    ap.add_argument("--log", help="pins already posted (default: pins-log.jsonl next to plan.json)")
    ap.add_argument("--bodies-only", action="store_true")
    a = ap.parse_args()

    base = os.path.dirname(os.path.abspath(a.plan))
    plan = P.load_plan(a.plan)
    rules = plan.get("rules") or {}
    per_day = a.per_day or rules.get("per_day") or 1
    gap = a.gap if a.gap is not None else rules.get("link_gap_days", 7)
    default_tz = plan.get("timezone")
    accounts, links, pins = plan["accounts"], plan["links"], plan["pins"]
    for k, acc in accounts.items():
        if not (acc.get("timezone") or default_tz):
            sys.exit(f"no time zone for account '{k}': set accounts.{k}.timezone or \"timezone\" in plan.json")
        P.zone(acc.get("timezone") or default_tz)
    tz_of = lambda k: accounts.get(k, {}).get("timezone") or default_tz
    notes = []
    if not accounts:
        sys.exit("plan.json has no accounts: add one with its time zone and boards (references/plan-json.md)")
    P.check_ids(pins)
    bad = [f"{p['id']}: {err}" for p in pins for err in [P.link_of(p, links)[1]] if err]
    bad += [f"{p['id']}: account '{p.get('account')}' isn't in accounts" for p in pins if p.get("account") not in accounts]
    if bad:
        sys.exit("fix these first (pin_check.py explains more):\n  " + "\n  ".join(bad))
    page = lambda p: P.canonical(P.link_of(p, links)[0])

    if not a.bodies_only:
        try:
            start = date.fromisoformat(a.start) if a.start else date.today() + timedelta(days=1)
        except ValueError:
            sys.exit(f"--start must be a date like 2026-11-16, not {a.start}")
        if start < date.today():
            notes.append(f"--start {start} is in the past; scheduling from today instead")
            start = date.today()
        used = defaultdict(int)            # (account, day) -> pins, including pins already posted
        last_page = {}                     # (account, canonical url) -> last day
        def seen(acct, url, d):
            used[(acct, d)] += 1
            if url:
                last_page[(acct, url)] = max(last_page.get((acct, url), d), d)
        plan_posts = {p.get("postId") for p in pins if p.get("postId")}
        for old in P.read_log(a.log or os.path.join(base, "pins-log.jsonl")):
            d = P.parse_local(old.get("at"), tz_of(old.get("account")))
            if d and old.get("postId") not in plan_posts:
                seen(old.get("account"), P.canonical(old.get("url")), d.date())
        for p in pins:
            d = P.parse_local(p.get("at"), tz_of(p.get("account")))
            if d:
                seen(p.get("account"), page(p), d.date())
        for p in pins:
            if p.get("at") or p.get("now"):
                continue
            acct = p.get("account")
            link = links.get(p.get("link")) if isinstance(p.get("link"), str) else None
            link = link if isinstance(link, dict) else {}
            url = page(p)
            day = start
            if url and (acct, url) in last_page:
                day = max(day, last_page[(acct, url)] + timedelta(days=gap))
            moment = link.get("moment")
            lead = link.get("lead_days") or rules.get("lead_days") or [LEAD_MAX, LEAD_MIN]
            try:
                lead = [int(lead), int(lead) // 2] if isinstance(lead, (int, float, str)) else [int(x) for x in lead[:2]]
                lead_max, lead_min = (lead + [lead[0] // 2])[:2]
            except (TypeError, ValueError, IndexError):
                sys.exit(f"links.{p.get('link')}.lead_days must be [most, fewest] days, like [120, 60]")
            m = None
            if moment:
                try:
                    m = date.fromisoformat(str(moment))
                except ValueError:
                    sys.exit(f"links.{p.get('link')}.moment must be a date like 2026-12-25, not {moment!r}")
                if m <= start:
                    notes.append(f"{p['id']}: the moment {moment} has passed; scheduled as an evergreen pin")
                    m = None
                else:
                    day = max(day, m - timedelta(days=int(lead_max)))
            times = times_of(accounts.get(acct, {}))
            now = datetime.now(P.zone(tz_of(acct))).replace(tzinfo=None)
            while True:
                n = used[(acct, day)]
                if n < per_day:
                    h, mi = times[min(n, len(times) - 1)]
                    slot = datetime(day.year, day.month, day.day, h, mi) + timedelta(minutes=15 * max(0, n - len(times) + 1))
                    if slot >= now + timedelta(minutes=30):
                        break
                day += timedelta(days=1)
            if m and slot.date() >= m:
                notes.append(f"{p['id']} would go live after {moment}, so it isn't scheduled: keep it for next "
                             "year's season, or remove the moment to pin it as evergreen")
                continue
            p["at"] = slot.isoformat(timespec="minutes")
            seen(acct, url, slot.date())
            if m:
                left = (m - slot.date()).days
                if left < int(lead_min):
                    notes.append(f"{p['id']} goes live {left} days before {moment}; seasonal pins do best "
                                 f"{lead_min} to {lead_max} days ahead, so start earlier next time")
        P.save_plan(a.plan, plan)

    rdir = os.path.join(base, "requests")
    os.makedirs(rdir, exist_ok=True)
    keep = {f"{p['id']}.json" for p in pins if p.get("at") or p.get("now")}
    for old in os.listdir(rdir):       # a removed pin must not stay sendable
        if old.endswith(".json") and old not in keep:
            os.remove(os.path.join(rdir, old))
    rows, missing = [], set()
    unscheduled = [p["id"] for p in pins if not (p.get("at") or p.get("now"))]
    for p in pins:
        if not (p.get("at") or p.get("now")):
            continue      # no date, no request: nothing can be sent by mistake
        tz = tz_of(p.get("account"))
        body = body_for(p, plan, tz)
        with open(os.path.join(rdir, f"{p['id']}.json"), "w", encoding="utf-8") as f:
            json.dump(body, f, indent=1, ensure_ascii=False)
        if P.PLACEHOLDER.search(json.dumps(body)):
            missing.add(p["id"])
        rows.append((p.get("at") or "", tz, p))
    rows.sort(key=lambda r: r[0])

    has_times = all(accounts.get(p.get("account"), {}).get("times") for p in pins)
    lines = ["# Pin schedule", ""]
    if not has_times:
        lines += [f"Times are {DEFAULT_TIME} local. On Pinterest the spacing matters far more than the hour; "
                  "change `times` per account if the user's own analytics show a better one.", ""]
    lines += ["| Goes live (local time) | Pin | Board | Link | Title |", "|---|---|---|---|---|"]
    for at, tz, p in rows:
        when = at
        d = P.parse_local(at, tz)
        if d:
            when = d.strftime("%a %d %b %Y %H:%M") + f" ({tz.split('/')[-1].replace('_', ' ')})"
        url = P.link_of(p, links)[0]
        lines.append(f"| {when} | {p['id']} ({P.fmt_of(p)}) | {p.get('board', '')} | {P.domain(url)} | "
                     f"{p.get('title', '').replace('|', '/')} |")
    alts = [p for p in pins if p.get("alt")]
    if alts:
        lines += ["", "## Alt text to add in Pinterest", "",
                  "WoopSocial doesn't send alt text. Once each pin is live: open it, Edit Pin, "
                  "Alt text, paste. It helps people using screen readers and tells Pinterest what the image shows.", ""]
        for p in alts:
            lines.append(f"- **{p['id']}**: {p['alt']}")
    if unscheduled:
        notes.append("not scheduled (no request written): " + ", ".join(unscheduled))
    if notes:
        lines += ["", "## Notes", ""] + [f"- {n}" for n in notes]
    lines += ["", "## After the pins go live", "",
              "- Judge them at day 30 and day 90, not in week 1: most new pins get almost no impressions in their first days.",
              "- Don't delete and re-pin the same picture to the same link; make a new design instead.",
              "- Keep pinning steadily: a few fresh pins a week beat a burst."]
    with open(os.path.join(base, "schedule.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[: lines.index("## After the pins go live")]))
    print(f"wrote {len(rows)} request bodies to {P.rel(rdir, os.getcwd())} and schedule.md")
    if missing:
        print("Still placeholders (upload the media, put the IDs in mediaIds, set socialAccountId and the "
              "board ids, then run again with --bodies-only): " + ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()
