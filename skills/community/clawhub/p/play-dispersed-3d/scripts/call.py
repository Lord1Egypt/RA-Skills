#!/usr/bin/env python3
"""call.py - make one Call in the free game Dispersed 3D without a browser. Read-only, Python 3.8+, stdlib only.

  call.py today [--date YYYY-MM-DD] [--json]
      The Call for the date (UTC today by default): the situation line and a numbered menu, one decision
      from a checked run. It picks the same turn as the connector's one_call tool (same rule, same day).
      It never prints what the checked AI picked, nor its key, nor its reason.
  call.py link --challenge C --run R --at N --pick KEY --by claude
      Prints the reveal link for your pick, after checking that KEY is on that turn's menu and that the
      turn is a Call turn (call_ok). KEY is the menu key, or the menu number shown by "today".
      --by is one of: claude, chatgpt, grokbot, gemini, perplexity, copilot, other.

It reads https://momatio.com/dispersed3d/api/challenges, .../data/replays/<challenge>/index.json and
.../<run>.calls.json. It makes no seat, makes no move and submits nothing.
Exit code 0 = ok, 1 = could not read or the check failed.
"""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

GAME = "https://momatio.com/dispersed3d"
UA = "aa-skill/1 (+https://davelalande.com/skill/) play-dispersed-3d/1.0.0"
CALL_NAMES = ("claude", "chatgpt", "grokbot", "gemini", "perplexity", "copilot", "other")
# The words the game's Call page never says, plus the season words (copied from the connector's rule).
BANNED = re.compile(r"\b(wrong|fail\w*|mistake\w*|smug|blunder\w*|caught|gotcha|snow\w*|winter\w*|ice|icy|frost\w*|blizzard\w*|sleet|freez\w+|frozen|chains)\b", re.I)
BANNED2 = re.compile(r"\b(snow\w*|winter\w*|cold[\s-]+season)\b", re.I)
MAX_FETCHED = 12
MAX_MISSES = 2
_last = [0.0]


def fetch_json(url):
    """One paced GET. Returns the parsed JSON, or None when it cannot be read."""
    wait = 0.5 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, ValueError, TimeoutError):
        return None


def calls_file(chal, run):
    d = fetch_json("%s/data/replays/%s/%s.calls.json" % (GAME, urllib.parse.quote(str(chal)), urllib.parse.quote(str(run))))
    if isinstance(d, dict) and d.get("format") == "d3-calls-1" and isinstance(d.get("turns"), list):
        return d
    return None


def real_sentence(why):
    w = (why or "").strip()
    return len(w.split()) >= 5 and w[-1:] in "!.?" and not (BANNED.search(w) or BANNED2.search(w))


def pick_turn(d, today, chal):
    """The connector's rule: a hash of the date and challenge over the candidate turns."""
    turns = [t for t in d["turns"] if isinstance(t, dict) and t.get("call_ok") is True and isinstance(t.get("n"), int)
             and isinstance(t.get("menu"), list) and isinstance(t.get("keys"), list) and len(t["menu"]) == len(t["keys"]) >= 2
             and all(isinstance(x, str) for x in t["menu"] + t["keys"])]
    tiers = [[t for t in turns if 2 <= len(t["menu"]) <= 6 and real_sentence(t.get("why"))],
             [t for t in turns if real_sentence(t.get("why"))]]
    for cand in tiers:
        if cand:
            cand = sorted(cand, key=lambda t: t["n"])
            h = int(hashlib.sha256(("%s|%s" % (today, chal)).encode()).hexdigest(), 16)
            return cand[h % len(cand)]
    return None


def run_order(rid):
    try:
        return (1, int(rid))
    except (TypeError, ValueError):
        return (0, 0)


def fix(s):
    """Some lines carry a doubled-up character (A-circumflex before the middle dot). Repair it for reading."""
    try:
        return s.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def find_today(today):
    ch = fetch_json(GAME + "/api/challenges")
    listed = sorted((c for c in ((ch or {}).get("challenges") or []) if c.get("runs", 0) > 0),
                    key=lambda c: c.get("id", ""), reverse=True)
    fetched = 0
    for c in listed:
        idx = fetch_json("%s/data/replays/%s/index.json" % (GAME, urllib.parse.quote(c["id"])))
        runs = [r for r in (idx or {}).get("runs", []) if r.get("finished") and r.get("id") is not None]
        misses = 0
        for r in sorted(runs, key=lambda r: run_order(r["id"]), reverse=True):
            if fetched >= MAX_FETCHED or misses >= MAX_MISSES:
                break
            fetched += 1
            d = calls_file(c["id"], r["id"])
            turn = pick_turn(d, today, c["id"]) if d else None
            misses = 0 if d else misses + 1
            if turn:
                return c["id"], str(r["id"]), d, turn
        if fetched >= MAX_FETCHED:
            break
    return None


def reveal_base(chal, run, n):
    return "%s/?watch=%s/%s&at=%d&call=1" % (GAME, chal, run, n)


def cmd_today(a):
    today = a.date or dt.datetime.now(dt.timezone.utc).date().isoformat()
    found = find_today(today)
    if not found:
        print("ERROR: no checked run has its Call data published (or it could not be read just now). "
              "That is not the same as none. The leaderboard lists the checked runs: %s/leaderboard/" % GAME, file=sys.stderr)
        return 1
    chal, run, d, t = found
    menu = [{"number": i, "key": k, "label": lb} for i, (k, lb) in enumerate(zip(t["keys"], t["menu"]), 1)]
    place = chal[11:].replace("-", " ").title()
    out = {
        "challenge": chal,
        "run": run,
        "turn": t["n"],
        "place_line": "%s, day %s, %s" % (place, t.get("day"), t.get("clock")),
        "line": fix(t.get("line") or ""),
        "menu": menu,
        "by_must_be_one_of": list(CALL_NAMES),
        "link_pattern": reveal_base(chal, run, t["n"]) + "#c=<key of your pick>&by=<name>",
        "same_call_for_everyone_on": today,
        "how": "Pick one move and give your reason in a line. Then run: call.py link --challenge %s --run %s --at %d --pick <key> --by <your name>" % (chal, run, t["n"]),
        "note": "A checked run, played back. The other AI's answer is shown only after your pick, and neither answer is scored.",
    }
    if a.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    print("One decision from a checked run of Dispersed 3D (%s, run %s, turn %d)." % (chal, run, t["n"]))
    print(out["place_line"])
    print(out["line"])
    for m in menu:
        print("  %d. %s   [key %s]" % (m["number"], fix(m["label"]), m["key"]))
    print("Same Call for everyone on %s (UTC)." % today)
    print(out["how"])
    return 0


def cmd_link(a):
    if a.by not in CALL_NAMES:
        print("ERROR: --by must be one of: %s" % ", ".join(CALL_NAMES), file=sys.stderr)
        return 1
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,120}", a.challenge) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,40}", a.run):
        print("ERROR: that challenge or run is not a name the game uses.", file=sys.stderr)
        return 1
    d = calls_file(a.challenge, a.run)
    if not d:
        print("ERROR: could not read that run's Call data. Could not read; that is not the same as none.", file=sys.stderr)
        return 1
    turn = next((t for t in d["turns"] if isinstance(t, dict) and t.get("n") == a.at), None)
    if not turn:
        print("ERROR: that run has no turn %d." % a.at, file=sys.stderr)
        return 1
    if turn.get("call_ok") is not True:
        print("ERROR: turn %d is not a Call turn (call_ok is not true). Run 'call.py today' for one." % a.at, file=sys.stderr)
        return 1
    keys = turn.get("keys") or []
    key = a.pick
    if key not in keys:
        if re.fullmatch(r"\d{1,3}", key) and 1 <= int(key) <= len(keys):
            key = keys[int(key) - 1]
        else:
            print("ERROR: %r is not a key on that turn's menu." % a.pick, file=sys.stderr)
            return 1
    print("%s#c=%s&by=%s" % (reveal_base(a.challenge, a.run, a.at), key, a.by))
    return 0


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Make one Call in Dispersed 3D (read-only).")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("today")
    s.add_argument("--date", help="YYYY-MM-DD (UTC); default today")
    s.add_argument("--json", action="store_true")
    s = sub.add_parser("link")
    s.add_argument("--challenge", required=True)
    s.add_argument("--run", required=True)
    s.add_argument("--at", required=True, type=int)
    s.add_argument("--pick", required=True)
    s.add_argument("--by", required=True)
    a = p.parse_args(argv)
    return cmd_today(a) if a.cmd == "today" else cmd_link(a)


if __name__ == "__main__":
    sys.exit(main())
