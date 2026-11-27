#!/usr/bin/env python3
"""run_checks.py - 9 live, read-only checks of the way into Dispersed 3D that this skill teaches.

These check OUR PATH (the game's public files, the seat page, scripts/call.py and the connector), not a language model.
They never make a seat, never make a move and never submit to the leaderboard: every request is a plain GET of a public
file, plus the connector's read-only tools/list and one_call. One fixed User-Agent. Python 3.8+, standard library only.

  python run_checks.py          run all 9
  python run_checks.py c3 c7    run only those
Exit code 0 = all passed, 1 = at least one failed.
"""
import contextlib
import datetime as dt
import importlib.util
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CALL = os.path.join(HERE, "..", "scripts", "call.py")
GAME = "https://momatio.com/dispersed3d"
MCP = "https://davelalande.com/mcp"
UA = "aa-skill/1 (+https://davelalande.com/skill/) play-dispersed-3d-checks/1.0.0"
LINK_RE = re.compile(r"^https://momatio\.com/dispersed3d/\?watch=[^&]+&at=\d+&call=1#c=[^&]+&by=claude$")

_spec = importlib.util.spec_from_file_location("call", CALL)
call = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(call)
call.UA = UA        # one fixed User-Agent for every request this file makes

_last = [0.0]


def pace():
    wait = 0.5 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()


def get(url):
    """(status, body bytes). A network failure is (0, b'')."""
    pace()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception:
        return 0, b""


def get_json(url):
    s, b = get(url)
    try:
        return s, json.loads(b.decode("utf-8"))
    except ValueError:
        return s, None


def rpc(method, params=None, session=None, version=None, notify=False, rid=1):
    pace()
    payload = {"jsonrpc": "2.0", "method": method}
    if not notify:
        payload["id"] = rid
    if params is not None:
        payload["params"] = params
    headers = {"User-Agent": UA, "Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if session:
        headers["Mcp-Session-Id"] = session
    if version:
        headers["MCP-Protocol-Version"] = version
    req = urllib.request.Request(MCP, data=json.dumps(payload).encode(), method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=45) as r:
        sid = r.headers.get("Mcp-Session-Id") or session
        text = r.read().decode("utf-8").strip()
    if not text:
        return None, sid
    if text.startswith("data:") or text.startswith("event:"):
        found = []
        for ln in text.splitlines():
            if ln.strip().startswith("data:"):
                try:
                    found.append(json.loads(ln.strip()[5:].strip()))
                except ValueError:
                    pass
        return (found[-1] if found else None), sid
    return json.loads(text), sid


def mcp_session():
    msg, sid = rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {},
                                  "clientInfo": {"name": "aa-skill-checks", "version": "1.0.0"}})
    version = ((msg or {}).get("result") or {}).get("protocolVersion") or "2025-03-26"
    rpc("notifications/initialized", session=sid, version=version, notify=True)
    return sid, version


def run_call(argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = call.main(argv)
    return code, out.getvalue(), err.getvalue()


STATE = {}


def today_call():
    if "today" not in STATE:
        STATE["date"] = dt.datetime.now(dt.timezone.utc).date().isoformat()
        code, out, err = run_call(["today", "--json", "--date", STATE["date"]])
        STATE["today"] = json.loads(out) if code == 0 else None
        STATE["today_err"] = err
    return STATE["today"]


def c1():
    s, b = get(GAME + "/llms.txt")
    t = b.decode("utf-8", "replace")
    need = ["?ai=1", "D3.ai.state", "/agent/", "dispersed3d_state", "dispersed3d_menu", "dispersed3d_move", "dispersed3d_pack"]
    missing = [n for n in need if n not in t]
    return ([] if s == 200 and not missing else ["status %s, missing %s" % (s, missing)])


def c2():
    s, d = get_json(GAME + "/features.json")
    fa = (d or {}).get("for_agents") or {}
    return [] if s == 200 and fa.get("llms_txt") and fa.get("agent_page") else ["for_agents links missing (status %s)" % s]


def c3():
    s, _ = get(GAME + "/agent/")
    return [] if s == 200 else ["status %s" % s]


def c4():
    s, d = get_json(GAME + "/seat/health")
    return [] if s == 200 and isinstance(d, dict) and d.get("ok") is True else ["status %s, ok=%r" % (s, (d or {}).get("ok"))]


def c5():
    s, d = get_json(GAME + "/api/challenges")
    ch = (d or {}).get("challenges") or []
    return [] if s == 200 and any(c.get("runs", 0) > 0 for c in ch) else ["no challenge with runs (status %s)" % s]


def c6():
    t = today_call()
    if not t:
        return ["call.py today gave nothing: %s" % STATE.get("today_err", "").strip()]
    s, d = get_json("%s/data/replays/%s/%s.calls.json" % (GAME, t["challenge"], t["run"]))
    ok_turns = [x for x in (d or {}).get("turns", []) if x.get("call_ok") is True]
    if s == 200 and (d or {}).get("format") == "d3-calls-1" and ok_turns:
        return []
    return ["calls.json: status %s, format %r, %d call_ok turns" % (s, (d or {}).get("format"), len(ok_turns))]


def c7():
    t = today_call()
    if not t:
        return ["call.py today gave nothing"]
    sid, ver = mcp_session()
    msg, _ = rpc("tools/call", {"name": "one_call", "arguments": {}}, session=sid, version=ver, rid=2)
    res = (msg or {}).get("result") or {}
    obj = res.get("structuredContent")
    if not isinstance(obj, dict):
        for item in res.get("content") or []:
            if item.get("type") == "text":
                try:
                    obj = json.loads(item["text"])
                except ValueError:
                    obj = None
                break
    if not isinstance(obj, dict) or "challenge" not in obj:
        return ["one_call gave no Call: %s" % json.dumps(msg)[:200]]
    m = re.search(r"&at=(\d+)&call=1", (obj.get("how_to_reveal") or {}).get("url_pattern", ""))
    mine = (t["challenge"], str(t["run"]), t["turn"])
    theirs = (obj["challenge"], str(obj["run"]), int(m.group(1)) if m else None)
    if mine != theirs:
        return ["call.py says %s, the connector says %s" % (mine, theirs)]
    if obj.get("same_call_for_everyone_on") != STATE["date"]:
        return ["the connector's day is %s, call.py used %s" % (obj.get("same_call_for_everyone_on"), STATE["date"])]
    return []


def c8():
    t = today_call()
    if not t:
        return ["call.py today gave nothing"]
    code, out, err = run_call(["link", "--challenge", t["challenge"], "--run", t["run"], "--at", str(t["turn"]),
                               "--pick", t["menu"][0]["key"], "--by", "claude"])
    link = out.strip()
    bad = []
    if code != 0 or not LINK_RE.match(link):
        bad.append("link %r (exit %s %s)" % (link, code, err.strip()))
    # the output must never carry what the checked AI picked, its key or its reason
    code2, out2, _ = run_call(["today", "--json", "--date", STATE["date"]])
    for word in ("picked", "pick_key", "\"why\""):
        if word in out2:
            bad.append("call.py today printed %s" % word)
    return bad


def c9():
    sid, ver = mcp_session()
    msg, _ = rpc("tools/list", {}, session=sid, version=ver, rid=3)
    names = {t.get("name") for t in ((msg or {}).get("result") or {}).get("tools", [])}
    missing = [n for n in ("one_call", "game_leaderboard", "trip_status") if n not in names]
    return [] if not missing else ["tools/list is missing %s" % missing]


CHECKS = [("c1", "llms.txt answers 200 and holds ?ai=1, D3.ai.state, /agent/ and the four tool names", c1),
          ("c2", "features.json holds both for_agents links", c2),
          ("c3", "/dispersed3d/agent/ answers 200", c3),
          ("c4", "/dispersed3d/seat/health answers 200", c4),
          ("c5", "/dispersed3d/api/challenges lists a challenge with runs", c5),
          ("c6", "a calls.json reads as d3-calls-1 with a call_ok turn", c6),
          ("c7", "call.py today matches the connector's one_call (challenge, run, turn)", c7),
          ("c8", "call.py link output matches the link pattern and shows no pick", c8),
          ("c9", "the connector's tools/list names one_call, game_leaderboard, trip_status", c9)]


def main():
    want = set(sys.argv[1:])
    passed, failed = 0, []
    for cid, label, fn in CHECKS:
        if want and cid not in want:
            continue
        try:
            problems = fn()
        except Exception as e:
            problems = ["%s: %s" % (type(e).__name__, e)]
        if problems:
            failed.append(cid)
            print("FAIL %s  %s\n     %s" % (cid, label, "; ".join(problems)))
        else:
            passed += 1
            print("PASS %s  %s" % (cid, label))
    print("\n%d passed, %d failed." % (passed, len(failed)))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
