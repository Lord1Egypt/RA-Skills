#!/usr/bin/env python3
"""Give every post a time per account, and write the WoopSocial request for each one.

    python3 scripts/schedule.py plan.json --start 2026-11-16
    python3 scripts/schedule.py plan.json --bodies-only      # times already set; just (re)write requests

Feed posts (image, carousel, reel) without a time get one day each, in plan order, one per day per
account by default (--per-day), skipping --skip days. Each account posts at its own `times` in its
own `timezone` (from plan.json; --times and --tz are the defaults for accounts that don't set
them). Stories never take a feed slot: give a Story `"with": {"post": "<feed post id>",
"minutes": -60}` and it goes out that many minutes before (negative) or after the feed post, on
each account.

Writes schedule.md (the table to show the user, with the first-hour notes) and
requests/<post>-<account>.json: the exact body for WoopSocial's posts_validate and posts_create.
Media IDs come from the plan's `mediaIds` / `coverId` (or the target's own, for per-account media).
Needs Python 3.9+ (zoneinfo). On Windows also: pip install tzdata.
"""
import argparse, json, os, shutil, sys
from datetime import date, datetime, timedelta

DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
POST_TYPE = {"image": "POST", "carousel": "POST", "reel": "REEL", "story": "STORY"}
PLACEHOLDER = "12:00"


def zone(name):
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:
        sys.exit(f"time zone '{name}' not found. On Windows run: pip install tzdata. "
                 "Use names like Europe/Madrid or America/New_York.")


def to_utc(local_iso, tz):
    d = datetime.fromisoformat(local_iso)
    if d.tzinfo is None:
        d = d.replace(tzinfo=zone(tz))
    return d.astimezone(zone("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ")


def refs(files, ids):
    out = []
    for i, m in enumerate(files):
        mid = ids[i] if i < len(ids) and ids[i] else f"<mediaId for {os.path.basename(m)}>"
        out.append({"type": "MEDIA_LIBRARY", "mediaId": mid})
    return out


def body_for(post, target, accounts, tz):
    acc = accounts.get(target.get("account"), {})
    text = target.get("caption") or post.get("caption", "")
    files = target.get("media") or post.get("media", [])
    ids = target.get("mediaIds") or ([] if target.get("media") else post.get("mediaIds", []))
    sa = {"platform": "INSTAGRAM",
          "socialAccountId": acc.get("socialAccountId") or f"<socialAccountId for {target.get('account')}>",
          "postType": POST_TYPE[post["format"]]}
    cover = target.get("cover") or post.get("cover")
    if post["format"] == "reel" and cover:
        cid = target.get("coverId") or (None if target.get("cover") else post.get("coverId"))
        sa["cover"] = {"type": "MEDIA_LIBRARY", "mediaId": cid or "<mediaId for the cover>"}
    if post["format"] == "reel" and post.get("trial"):
        sa["trialParams"] = {"graduationStrategy": post["trial"] if post["trial"] in ("MANUAL", "SS_PERFORMANCE") else "MANUAL"}
    if post["format"] == "story":
        text = ""  # Stories have no caption
    body = {"content": [{"text": text, "media": refs(files, ids)}], "socialAccounts": [sa]}
    if target.get("now"):
        body["schedule"] = {"type": "PUBLISH_NOW"}
    elif target.get("at"):
        body["schedule"] = {"type": "SCHEDULE_FOR_LATER", "scheduledFor": to_utc(target["at"], tz)}
    else:
        body["schedule"] = {"type": "DRAFT"}
    return body


def parse_times(s):
    out = []
    for t in (s if isinstance(s, list) else str(s).split(",")):
        hh, mm = str(t).strip().split(":")
        out.append((int(hh), int(mm)))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan")
    ap.add_argument("--start", help="first day, YYYY-MM-DD (default: tomorrow)")
    ap.add_argument("--times", help="default posting times, local, e.g. 12:30,19:00 (from your Insights)")
    ap.add_argument("--per-day", type=int, default=1, help="feed posts per account per day")
    ap.add_argument("--skip", default="", help="days to skip, e.g. sat,sun")
    ap.add_argument("--stagger", type=int, default=0, help="optional minutes between accounts that share a time zone")
    ap.add_argument("--tz", help="default IANA time zone (default: the plan's timezone)")
    ap.add_argument("--bodies-only", action="store_true")
    a = ap.parse_args()

    base = os.path.dirname(os.path.abspath(a.plan))
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    default_tz = a.tz or plan.get("timezone")
    accounts = plan.get("accounts", {})
    for k, acc in accounts.items():
        if not (acc.get("timezone") or default_tz):
            sys.exit(f"no time zone for account '{k}': set accounts.{k}.timezone or \"timezone\" in plan.json")
        zone(acc.get("timezone") or default_tz)
    tz_of = lambda k: accounts.get(k, {}).get("timezone") or default_tz
    placeholder = False
    posts = plan.get("posts", [])
    by_id = {p.get("id"): p for p in posts}

    if not a.bodies_only:
        def times_of(k):
            nonlocal placeholder
            t = accounts.get(k, {}).get("times") or a.times
            if not t:
                placeholder = True
                t = PLACEHOLDER
            return parse_times(t)

        skip = {s.strip().lower()[:3] for s in a.skip.split(",") if s.strip()}
        start = date.fromisoformat(a.start) if a.start else date.today() + timedelta(days=1)
        cursor = {}  # account -> (day, index within the day)
        for p in posts:
            if p.get("format") == "story":
                continue
            for k, t in enumerate(p.get("targets", [])):
                if t.get("at") or t.get("now"):
                    continue
                acct = t.get("account")
                times = times_of(acct)
                if a.per_day > len(times):
                    sys.exit(f"--per-day {a.per_day} needs at least that many times for account '{acct}'")
                day, idx = cursor.get(acct, (start, 0))
                now = datetime.now(zone(tz_of(acct))).replace(tzinfo=None)
                while True:
                    if DAYS[day.weekday()] in skip or idx >= a.per_day:
                        day, idx = day + timedelta(days=1), 0
                        continue
                    h, m = times[idx]
                    slot = datetime(day.year, day.month, day.day, h, m)
                    if slot > now + timedelta(minutes=20):
                        break
                    idx += 1
                cursor[acct] = (day, idx + 1)
                shared = [x for x in p.get("targets", [])[:k] if tz_of(x.get("account")) == tz_of(acct)]
                slot += timedelta(minutes=a.stagger * len(shared))
                t["at"] = slot.isoformat(timespec="minutes")
        for p in posts:
            if p.get("format") != "story":
                continue
            w = p.get("with") or {}
            ref = by_id.get(w.get("post"))
            for t in p.get("targets", []):
                if t.get("at") or t.get("now"):
                    continue
                rt = next((x for x in (ref or {}).get("targets", []) if x.get("account") == t.get("account") and x.get("at")), None)
                if not rt:
                    sys.exit(f"story {p.get('id')}: set \"with\": {{\"post\": \"<feed post id>\", \"minutes\": -60}} "
                             f"for account {t.get('account')}, or give it an \"at\"")
                t["at"] = (datetime.fromisoformat(rt["at"]) + timedelta(minutes=int(w.get("minutes", -60)))).isoformat(timespec="minutes")
        shutil.copyfile(a.plan, a.plan + ".bak")
        with open(a.plan, "w", encoding="utf-8") as f:
            json.dump(plan, f, indent=1, ensure_ascii=False)

    rdir = os.path.join(base, "requests")
    os.makedirs(rdir, exist_ok=True)
    rows, missing = [], set()
    for p in posts:
        if p.get("format") not in POST_TYPE:
            sys.exit(f"post {p.get('id')}: unknown format {p.get('format')}")
        for t in p.get("targets", []):
            tz = tz_of(t.get("account"))
            body = body_for(p, t, accounts, tz)
            name = f"{p['id']}-{t.get('account', 'account')}.json"
            with open(os.path.join(rdir, name), "w", encoding="utf-8") as f:
                json.dump(body, f, indent=1, ensure_ascii=False)
            if "<" in json.dumps(body):
                missing.add(p["id"])
            cap = "(Story, no caption)" if p["format"] == "story" else (t.get("caption") or p.get("caption", "")).strip().split("\n")[0]
            utc = body["schedule"].get("scheduledFor", "")
            rows.append((utc or "~", t.get("at") or ("now" if t.get("now") else "draft"), tz, p["id"], p["format"],
                         accounts.get(t.get("account"), {}).get("handle", t.get("account")), cap))
    rows.sort()
    lines = ["# Schedule", ""]
    if placeholder:
        lines += ["**The times are a placeholder (12:00 local).** Replace them with the hours your Insights show "
                  "(Professional dashboard > Total followers > Most active times) and run this again.", ""]
    lines += ["| When (account's local time) | Post | Format | Account | First line |", "|---|---|---|---|---|"]
    for _, at, tz, pid, fmt, acc, cap in rows:
        when = at
        try:
            when = datetime.fromisoformat(at).strftime("%a %d %b %H:%M") + f" ({tz.split('/')[-1].replace('_', ' ')})"
        except ValueError:
            pass
        lines.append(f"| {when} | {pid} | {fmt} | {acc} | {cap.replace('|', '/')[:90]} |")
    lines += ["", "## The first hour after each feed post", "",
              "- Be online: reply to every comment in the first hour; replies count as conversation.",
              "- Share the post to your Story from the app with the post sticker (the API can't add stickers), unless a Story is already scheduled for it.",
              "- Pin the comment that answers the most likely question, if there is one.",
              "- Add what's on each post's checklist (alt text, collaborators, location, music, AI label)."]
    with open(os.path.join(base, "schedule.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines[: lines.index("## The first hour after each feed post")]))
    print(f"wrote {len(rows)} request bodies to {rdir} and schedule.md")
    if missing:
        print("Still placeholders (upload the media, put the IDs in mediaIds/coverId, set socialAccountId, "
              "then run again with --bodies-only): " + ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()
