#!/usr/bin/env python3
"""Keep a log of what was posted, and learn from the account's own numbers.

    python3 scripts/log.py record plan.json                 # add posted targets to posts.jsonl
    python3 scripts/log.py results --metrics metrics.json   # rank posts against the account's own posts
    python3 scripts/log.py results --csv insights.csv       # add numbers only the app shows

record: every target in the plan with a WoopSocial `postId` (set it from posts_create) is appended
  once to posts.jsonl next to the plan (or --log).
results: metrics.json is one or more saved responses of WoopSocial's social_account_posts_list.
  insights.csv adds what only Instagram's app shows, columns (any subset):
  post,account,measured,reach,views,shares,saves,likes,comments,follows,avg_watch_s,skip_rate
  (post = the plan id or the post URL; CSV numbers win over WoopSocial's). Writes results.md.

Rules, so it doesn't mislead:
- Rates are per reach (accounts reached). A post without reach is listed but not ranked.
- Posts are only compared within the same format and account; Stories are left out.
- Each post is measured once, at the collected value nearest to day 7 (within days 3 to 14),
  and that measurement is saved in posts.jsonl. So posts from different weeks are compared at
  the same age, and the comparison grows with every run. insights.csv can add a `measured`
  date column (YYYY-MM-DD) for numbers copied by hand.
- A best post is named once a format has 6 or more ranked posts; before that it says so.
- Posting-time advice needs 3+ ranked posts in at least 2 time slots.
Python 3.9+, standard library only.
"""
import argparse, csv, json, os, re, statistics, sys
from datetime import datetime, timezone

RATES = ["shares", "saves", "follows", "comments", "likes"]
ALIASES = {"uniqueimpressions": "reach", "reach": "reach", "impressionsunique": "reach",
           "views": "views", "plays": "views", "videoviews": "views",
           "shares": "shares", "sends": "shares", "saves": "saves", "saved": "saves",
           "likes": "likes", "comments": "comments", "follows": "follows"}
MIN_RANKED = 6


def load_log(path):
    rows = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            rows = [json.loads(x) for x in f if x.strip()]
    return rows


def cmd_record(a):
    base = os.path.dirname(os.path.abspath(a.plan))
    log = a.log or os.path.join(base, "posts.jsonl")
    with open(a.plan, encoding="utf-8") as f:
        plan = json.load(f)
    have = {(r.get("woop_post_id"), r.get("account")) for r in load_log(log)}
    accounts = plan.get("accounts", {})
    added = 0
    with open(log, "a", encoding="utf-8") as f:
        for p in plan.get("posts", []):
            for t in p.get("targets", []):
                if not t.get("postId") or (t["postId"], t.get("account")) in have:
                    continue
                acc = accounts.get(t.get("account"), {})
                cap = t.get("caption") or p.get("caption", "")
                f.write(json.dumps({
                    "logged": datetime.now().isoformat(timespec="seconds"),
                    "post": p.get("id"), "format": p.get("format"),
                    "items": len(t.get("media") or p.get("media", [])),
                    "account": t.get("account"), "handle": acc.get("handle"),
                    "socialAccountId": acc.get("socialAccountId"),
                    "at": t.get("at"), "timezone": acc.get("timezone") or plan.get("timezone"),
                    "first_line": "" if p.get("format") == "story" else cap.strip().split("\n")[0][:200],
                    "hashtags": re.findall(r"#(\w+)", cap), "trial": bool(p.get("trial")),
                    "woop_post_id": t["postId"], "url": t.get("url"),
                }, ensure_ascii=False) + "\n")
                added += 1
    print(f"logged {added} new post(s) to {log}")


def history(v):
    """WoopSocial stores each metric as values collected over time: return [(date or None, value)]."""
    if isinstance(v, (int, float)):
        return [(None, v)]
    out = []
    for x in (v if isinstance(v, list) else []):
        if isinstance(x, (int, float)):
            out.append((None, x))
        elif isinstance(x, dict):
            val = next((x[k] for k in ("value", "count", "total") if isinstance(x.get(k), (int, float))), None)
            if val is not None:
                out.append((x.get("collectedAt") or x.get("date") or x.get("timestamp"), val))
    return out


def norm(key):
    return ALIASES.get(re.sub(r"[^a-z]", "", key.lower()))


def read_metrics(path):
    """{(postId, socialAccountId): {metric: [(date, value), ...]}}"""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    for page in (data if isinstance(data, list) else [data]):
        for it in (page.get("socialAccountPosts", []) if isinstance(page, dict) else []):
            vals = out.setdefault((str(it.get("postId")), str(it.get("socialAccountId"))), {})
            for k, v in (it.get("analytics") or {}).items():
                n = norm(k)
                if n:
                    vals.setdefault(n, []).extend(history(v))
    return out


def pick_day7(hist, posted, now):
    """The value collected nearest to day 7 after posting, within days 3 to 14. Returns (value, age) or None."""
    best = None
    for d, v in hist:
        when = parse_dt(d) or now
        age = (when - posted).total_seconds() / 86400 if posted else None
        if age is None or not 3 <= age <= 14:
            continue
        if best is None or abs(age - 7) < abs(best[1] - 7):
            best = (v, age)
    return best


def num(x):
    try:
        return float(str(x).replace(",", "").replace("%", "").strip())
    except ValueError:
        return None


def parse_dt(s):
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def cmd_results(a):
    rows = load_log(a.log)
    if not rows:
        sys.exit(f"no posts in {a.log}; run 'log.py record plan.json' after posting")
    woop = read_metrics(a.metrics) if a.metrics else {}
    csv_rows = []
    if a.csv:
        with open(a.csv, encoding="utf-8-sig") as f:
            csv_rows = list(csv.DictReader(f))
    now = datetime.now(timezone.utc)
    for r in rows:
        posted = parse_dt(r.get("at"))
        meas = dict(r.get("measured") or {})
        for k, hist in woop.get((str(r.get("woop_post_id")), str(r.get("socialAccountId"))), {}).items():
            got = pick_day7(hist, posted, now)
            old = meas.get(k)
            if got and (not old or abs(got[1] - 7) < abs(old["age"] - 7)):
                meas[k] = {"value": got[0], "age": round(got[1], 1)}
        for c in csv_rows:
            key = (c.get("post") or "").strip()
            if key and key in (r.get("post"), r.get("url")) and (not c.get("account") or c["account"].strip() in (r.get("account"), r.get("handle"))):
                mdate = parse_dt(c.get("measured")) or now
                age = round((mdate - posted).total_seconds() / 86400, 1) if posted else 7
                for k in ("reach", "views", "shares", "saves", "likes", "comments", "follows", "avg_watch_s", "skip_rate"):
                    v = num(c.get(k, ""))
                    if v is not None:
                        meas[k] = {"value": v, "age": age}
        r["measured"] = meas
        r["m"] = {k: x["value"] for k, x in meas.items()}
        ages = [x["age"] for k, x in meas.items() if k in ("reach", "shares", "saves")]
        r["age"] = round(sum(ages) / len(ages)) if ages else ((now - posted).days if posted else None)
    # keep the day-7 numbers, so later runs can compare posts from any week
    with open(a.log, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({k: v for k, v in r.items() if k not in ("m", "age", "r", "score")}, ensure_ascii=False) + "\n")

    lines = ["# Results", "",
             "Rates per 1,000 accounts reached; in brackets, x times the median of the same format on the same account.", ""]
    by_acc = {}
    for r in rows:
        if r.get("format") == "story":
            continue
        by_acc.setdefault(r.get("handle") or r.get("account"), []).append(r)
    if not any(r["m"] for r in rows):
        lines.append("No numbers yet. WoopSocial collects them over the first days after posting; "
                     "or copy them from Instagram (Insights) into insights.csv.")
    for acc, items in by_acc.items():
        lines += [f"## {acc}", ""]
        for fmt in ("reel", "carousel", "image"):
            group = [i for i in items if i.get("format") == fmt]
            if not group:
                continue
            ranked, notes = [], []
            for i in group:
                reach = i["m"].get("reach")
                if not i["m"]:
                    notes.append(f"{i['post']}: no numbers yet")
                elif not reach:
                    notes.append(f"{i['post']}: no reach reported, not ranked")
                elif i["age"] is not None and i["age"] < 0:
                    notes.append(f"{i['post']}: not published yet")
                elif i["age"] is not None and i["age"] < 3:
                    notes.append(f"{i['post']}: {i['age']} day(s) old, too new to compare; run this again after day 3")
                elif i["age"] is not None and i["age"] > 14:
                    notes.append(f"{i['post']}: no numbers from days 3 to 14 were collected, so it isn't compared")
                else:
                    i["r"] = {k: i["m"][k] / reach * 1000 for k in RATES if k in i["m"]}
                    ranked.append(i)
            lines.append(f"### {fmt.title()}s ({len(ranked)} ranked of {len(group)})")
            lines.append("")
            if ranked:
                keys = [k for k in RATES if any(k in i["r"] for i in ranked)]
                med = {k: statistics.median([i["r"][k] for i in ranked if k in i["r"]]) for k in keys}
                for i in ranked:
                    # sends, saves and follows per reach: the signals Instagram names for growth
                    parts = [i["r"][k] / med[k] for k in ("shares", "saves", "follows") if k in i["r"] and med.get(k)]
                    i["score"] = sum(parts) / len(parts) if parts else 0
                ranked.sort(key=lambda i: i["score"], reverse=True)
                extra = ["Avg watch", "Skip rate"] if fmt == "reel" else []
                lines.append("| Post | Reach | " + " | ".join(k.title() for k in keys) + "".join(f" | {e}" for e in extra) + " |")
                lines.append("|---|---|" + "---|" * (len(keys) + len(extra)))
                for i in ranked:
                    cells = [f"{i['r'][k]:.1f} ({i['r'][k] / med[k]:.1f}x)" if k in i["r"] and med[k] else "" for k in keys]
                    if fmt == "reel":
                        cells += [f"{i['m']['avg_watch_s']:.1f} s" if "avg_watch_s" in i["m"] else "",
                                  f"{i['m']['skip_rate']:.0f}%" if "skip_rate" in i["m"] else ""]
                    lines.append(f"| {i['post']}: {i['first_line'][:48]} | {int(i['m']['reach'])} | " + " | ".join(cells) + " |")
                lines.append("")
                if len(ranked) >= MIN_RANKED:
                    lines.append(f"Best {fmt} on sends, saves and follows: **{ranked[0]['post']}**. "
                                 "Make the next one closer to it and change one thing at a time.")
                else:
                    lines.append(f"Too few {fmt}s to call a winner ({len(ranked)} of the {MIN_RANKED} needed). Keep posting and compare again.")
                if fmt == "reel" and not any("avg_watch_s" in i["m"] for i in ranked):
                    lines.append("Reels are judged mostly on watch time: copy average watch time and skip rate from each Reel's Insights into insights.csv.")
                if not any("follows" in i["m"] for i in ranked):
                    lines.append("Follows per post are only in the app (post Insights); add them to insights.csv to rank on growth.")
            for n in notes:
                lines.append(f"- {n}")
            lines.append("")
        slots = {}
        for i in items:
            if "score" not in i:
                continue
            d = datetime.fromisoformat(i["at"])
            band = "morning" if d.hour < 12 else "afternoon" if d.hour < 17 else "evening"
            slots.setdefault(f"{'weekday' if d.weekday() < 5 else 'weekend'} {band}", []).append(i["score"])
        good = {k: v for k, v in slots.items() if len(v) >= 3}
        if len(good) >= 2:
            best = max(good, key=lambda k: statistics.median(good[k]))
            lines.append("Posting time (median score, 1.0 = typical): " + ", ".join(
                f"{k} {statistics.median(v):.2f} ({len(v)})" for k, v in sorted(good.items())) + f". Best so far: **{best}**.")
        else:
            lines.append("Posting time: not enough data yet (3+ ranked posts in at least 2 time slots). "
                         "Until then, use the hours Insights shows your followers are most active.")
        lines.append("")
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("plan")
    r.add_argument("--log")
    s = sub.add_parser("results")
    s.add_argument("--log", default="posts.jsonl")
    s.add_argument("--metrics")
    s.add_argument("--csv")
    s.add_argument("--out", default="results.md")
    a = ap.parse_args()
    (cmd_record if a.cmd == "record" else cmd_results)(a)


if __name__ == "__main__":
    main()
