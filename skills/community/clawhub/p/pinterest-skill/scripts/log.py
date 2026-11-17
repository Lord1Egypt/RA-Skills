#!/usr/bin/env python3
"""Keep a log of every pin posted (so nothing is repeated) and learn which designs earn clicks.

    python3 scripts/log.py record plan.json                      # add posted pins to pins-log.jsonl
    python3 scripts/log.py results --plan plan.json --metrics metrics.json    # numbers from WoopSocial
    python3 scripts/log.py results --plan plan.json --csv analytics.csv       # numbers from Pinterest Analytics

record: every pin in the plan with a WoopSocial `postId` (set it from posts_create) is appended once
  to pins-log.jsonl next to the plan (or --log), with a fingerprint of its picture. pin_check.py reads
  this log so the same picture never goes to the same link twice.
results: metrics.json is one or more saved responses of WoopSocial's social_account_posts_list.
  The CSV adds what Pinterest Analytics shows, columns (any subset):
  pin,measured,impressions,saves,pin_clicks,outbound_clicks
  (pin = the plan id; measured = YYYY-MM-DD; CSV numbers win; "1.2K" and "1,234" are read, "n/a" is skipped). WoopSocial's `clicks` stand in for
  outbound clicks until the CSV gives the exact number. Every run stores its snapshot in the
  log, so the history grows. Writes results.md.

How it judges, so it doesn't mislead:
- A pin is not judged before day 30: most new pins get almost no impressions in their first days,
  and good ones keep growing for months (judge again at day 90).
- Outbound clicks per 1,000 impressions first (the visit is the point), then saves per 1,000.
- Pins are compared with the other designs for the same link first, then with the account's pins
  of the same format. A best design is named once a link has 3 or more pins past day 30, each
  with at least 1,000 impressions (fewer, and one click decides it).
- Numbers that weren't reported are shown as "not reported", never estimated.
Python 3.9+, standard library only.
"""
import argparse, csv, json, os, re, statistics, sys
from collections import defaultdict
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pinlib as P  # noqa: E402

ALIASES = {"impressions": "impressions", "saves": "saves", "saved": "saves",
           "clicks": "clicks", "outboundclicks": "outbound_clicks", "linkclicks": "outbound_clicks",
           "pinclicks": "pin_clicks", "closeups": "pin_clicks", "comments": "comments", "reactions": "reactions"}
JUDGE_DAY, LATE_DAY = 30, 90
MIN_IMPRESSIONS = 1000     # below this a single click decides the ranking


def cmd_record(a):
    base = os.path.dirname(os.path.abspath(a.plan))
    log = a.log or os.path.join(base, "pins-log.jsonl")
    plan = P.load_plan(a.plan)
    have = {r.get("postId") for r in P.read_log(log) if r.get("type") == "pin"}
    added = 0
    skipped = []
    with open(log, "a", encoding="utf-8") as f:
        for p in plan["pins"]:
            pid = str(p.get("postId") or "")
            if not pid or pid.startswith("<") or pid in have:
                continue
            if str(p.get("status", "")).upper() == "FAILED":
                skipped.append(p.get("id"))
                continue
            acc = plan["accounts"].get(p.get("account"), {})
            url = (plan["links"].get(p.get("link")) or {}).get("url") or p.get("link")
            path = P.resolve(base, p.get("file"))
            f.write(json.dumps({
                "type": "pin", "logged": datetime.now().isoformat(timespec="seconds"),
                "id": p["id"], "postId": p["postId"], "account": p.get("account"),
                "socialAccountId": acc.get("socialAccountId"), "board": p.get("board"),
                "timezone": acc.get("timezone") or plan.get("timezone"),
                "url": url, "link": p.get("link"), "at": p.get("at"), "format": P.fmt_of(p),
                "layout": p.get("layout"), "title": p.get("title"),
                "print": P.media_fingerprint(path) if path and os.path.exists(path) else None,
                "sources": source_prints(plan, base, p, path),
            }, ensure_ascii=False) + "\n")
            added += 1
    print(f"logged {added} new pin(s) to {P.rel(log, os.getcwd())}")
    if skipped:
        print("not logged (status FAILED): " + ", ".join(skipped))


def source_prints(plan, base, pin, path):
    """Fingerprints of the photos a pin was made from (render manifest, or the pin's own "sources")."""
    srcs = [P.resolve(base, s) for s in (pin.get("sources") or []) if isinstance(s, str)]
    for mf in plan.get("manifests") or []:
        mp = P.resolve(base, mf)
        try:
            entries = json.load(open(mp, encoding="utf-8")).get("pins", [])
        except Exception:
            continue
        for m in entries:
            spec_dir = os.path.normpath(os.path.join(os.path.dirname(mp), m.get("spec_dir") or ".."))
            if os.path.normpath(P.resolve(spec_dir, m.get("file", ""))) == os.path.normpath(path or ""):
                srcs += [P.resolve(spec_dir, s) for s in m.get("images", [])]
    return [f for f in (P.media_fingerprint(s) for s in srcs if os.path.exists(s)) if f]


def latest(v):
    """WoopSocial gives each metric as snapshots: [{date, collectedAt, value}]. Return (date, value)."""
    if isinstance(v, (int, float)):
        return None, v
    best = None
    for x in v if isinstance(v, list) else []:
        if isinstance(x, dict) and isinstance(x.get("value"), (int, float)):
            d = (x.get("date") or x.get("collectedAt") or "")[:10]
            if best is None or d >= best[0]:
                best = (d, x["value"])
    return best or (None, None)


def norm(k):
    return ALIASES.get(re.sub(r"[^a-z]", "", k.lower()))


def number(v):
    """A number from a CSV cell, or None: accepts 1,234 and 1.2K; skips n/a."""
    t = str(v or "").strip().replace("\u00a0", "").replace(" ", "")
    if not t or t.lower() in ("n/a", "na", "-", "--"):
        return None
    mult = 1
    if t[-1:].lower() in ("k", "m"):
        mult, t = (1000 if t[-1].lower() == "k" else 1_000_000), t[:-1]
    if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", t):
        t = t.replace(",", "")
    elif re.fullmatch(r"\d+,\d+", t):
        t = t.replace(",", ".")
    try:
        return float(t) * mult
    except ValueError:
        return None


def cmd_results(a):
    log = a.log
    if not log and a.plan:
        log = os.path.join(os.path.dirname(os.path.abspath(a.plan)), "pins-log.jsonl")
    log = log or "pins-log.jsonl"
    if not os.path.exists(log):
        sys.exit(f"no pin log at {log}: pass --plan plan.json (the log sits next to it) or --log")
    rows = P.read_log(log)
    pins = {r["postId"]: r for r in rows if r.get("type") == "pin" and r.get("id")}
    by_id = {r.get("id"): r for r in pins.values() if r.get("id")}
    snaps = []
    if a.metrics:
        try:
            with open(a.metrics, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            sys.exit(f"can't read {a.metrics}: {e}. Save the social_account_posts_list response as JSON")
        for page in data if isinstance(data, list) else [data]:
            for it in page.get("socialAccountPosts", []) if isinstance(page, dict) else []:
                pin = pins.get(str(it.get("postId"))) if isinstance(it, dict) else None
                if not pin:
                    continue
                vals, when = {}, None
                for k, v in (it.get("analytics") or {}).items():
                    n = norm(k)
                    if n:
                        d, val = latest(v)
                        if val is not None:
                            vals[n] = val
                            when = max(when or d or "", d or "")
                if vals:
                    snaps.append({"type": "snapshot", "postId": pin["postId"], "measured": when or date.today().isoformat(),
                                  "source": "woopsocial", **vals})
    if a.csv:
        with open(a.csv, encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                pin = by_id.get((r.get("pin") or "").strip())
                if not pin:
                    print(f"note: CSV row '{r.get('pin')}' matches no logged pin id", file=sys.stderr)
                    continue
                vals = {}
                for k, v in r.items():
                    n = norm(k or "")
                    if n:
                        x = number(v)
                        if x is not None:
                            vals[n] = x
                        elif str(v or "").strip():
                            print(f"note: '{v}' in {k} for {r.get('pin')} isn't a number; skipped", file=sys.stderr)
                snaps.append({"type": "snapshot", "postId": pin["postId"], "measured": (r.get("measured") or date.today().isoformat())[:10],
                              "source": "csv", **vals})
    seen = {(r.get("postId"), r.get("measured"), r.get("source")) for r in rows if r.get("type") == "snapshot"}
    snaps = [s for s in snaps if (s["postId"], s["measured"], s["source"]) not in seen]
    if snaps:
        with open(log, "a", encoding="utf-8") as f:
            for s in snaps:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        rows += snaps

    # newest snapshot per pin; CSV beats WoopSocial on the same day
    now = {}
    for s in (r for r in rows if r.get("type") == "snapshot"):
        k = s["postId"]
        rank = (s.get("measured", ""), s.get("source") == "csv")
        if k not in now or rank >= now[k][0]:
            merged = dict(now[k][1]) if k in now and now[k][1].get("measured") == s.get("measured") else {}
            merged.update(s)
            now[k] = (rank, merged)

    table = []
    for pid, pin in pins.items():
        s = now.get(pid, (None, {}))[1]
        posted = P.parse_local(pin.get("at"), pin.get("timezone"))
        measured = s.get("measured")
        try:
            age = (date.fromisoformat(str(measured)[:10]) - posted.date()).days if posted and measured else None
        except ValueError:
            age = None
        imp = s.get("impressions")
        rate = lambda k: round(1000 * s[k] / imp, 1) if imp and s.get(k) is not None else None
        key = "outbound_clicks" if s.get("outbound_clicks") is not None else "clicks"
        table.append({"pin": pin, "age": age, "imp": imp, "out": s.get(key), "saves": s.get("saves"),
                      "out_k": rate(key), "saves_k": rate("saves"), "src": "" if key == "outbound_clicks" else "*"})

    lines = ["# Pin results", "", f"Judged from day {JUDGE_DAY}; looked at again at day {LATE_DAY}. "
             "Outbound clicks per 1,000 impressions first, then saves per 1,000. "
             "* = WoopSocial's click count; add Pinterest Analytics' outbound clicks in the CSV for the exact number.", ""]
    groups = defaultdict(list)
    for t in table:
        groups[t["pin"].get("url") or "(no link)"].append(t)
    fmt = lambda v: "not reported" if v is None else (f"{v:,.0f}" if isinstance(v, (int, float)) and v == int(v) else str(v))
    for url, ts in groups.items():
        lines += [f"## {url}", "", "| Pin | Format | Age (days) | Impressions | Outbound clicks | per 1,000 | Saves | per 1,000 |",
                  "|---|---|---|---|---|---|---|---|"]
        ready = [t for t in ts if t["age"] is not None and t["age"] >= JUDGE_DAY and (t["imp"] or 0) >= MIN_IMPRESSIONS]
        ready.sort(key=lambda t: (t["out_k"] or 0, t["saves_k"] or 0), reverse=True)
        early = [t for t in ts if t not in ready]
        for t in ready + early:
            lines.append(f"| {t['pin']['id']} | {t['pin'].get('format') or ''} | {fmt(t['age'])} | {fmt(t['imp'])} | "
                         f"{fmt(t['out'])}{t['src'] if t['out'] is not None else ''} | {fmt(t['out_k'])} | {fmt(t['saves'])} | {fmt(t['saves_k'])} |")
        lines.append("")
        if len(ready) >= 3:
            top = ready[0]
            lines.append(f"Best design for this link so far: **{top['pin']['id']}** ({top['pin'].get('layout') or top['pin'].get('format')}). "
                         "Make the next pins for this link in the same direction with a new picture, and try that layout on other links.")
        elif ready:
            lines.append(f"{len(ready)} pin(s) past day {JUDGE_DAY} with {MIN_IMPRESSIONS:,}+ impressions: too few to name a best design (needs 3).")
        else:
            lines.append(f"No pin for this link is past day {JUDGE_DAY} with {MIN_IMPRESSIONS:,}+ impressions yet. Don't delete or redo anything; keep adding fresh pins and check again later.")
        lines.append("")
    acct = [t for t in table if t["age"] is not None and t["age"] >= JUDGE_DAY and (t["imp"] or 0) >= MIN_IMPRESSIONS and t["out_k"] is not None]
    if len(acct) >= 6:
        med = statistics.median(t["out_k"] for t in acct)
        lines += [f"Account median: {med} outbound clicks per 1,000 impressions across {len(acct)} pins past day {JUDGE_DAY}.", ""]
    out = os.path.join(os.path.dirname(os.path.abspath(log)), "results.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"wrote {P.rel(out, os.getcwd())}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("plan")
    r.add_argument("--log")
    s = sub.add_parser("results")
    s.add_argument("--metrics")
    s.add_argument("--csv")
    s.add_argument("--plan", help="plan.json; the log next to it is used")
    s.add_argument("--log", help="the pin log (default: next to --plan, else ./pins-log.jsonl)")
    a = ap.parse_args()
    {"record": cmd_record, "results": cmd_results}[a.cmd](a)


if __name__ == "__main__":
    main()
