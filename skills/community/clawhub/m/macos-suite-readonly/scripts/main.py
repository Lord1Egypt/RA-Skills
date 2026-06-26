#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import threading
import time
import urllib.request
import urllib.error
import ssl
from urllib.parse import quote


def _json_out(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def _fail(action, msg, detail=None, code=1):
    out = {"ok": False, "action": action, "error": msg}
    if detail is not None:
        out["detail"] = detail
    _json_out(out)
    raise SystemExit(code)


def _ok(action, result=None, extra=None):
    out = {"ok": True, "action": action}
    if result is not None:
        out["result"] = result
    if extra:
        out.update(extra)
    _json_out(out)


def _require_darwin():
    if sys.platform != "darwin":
        _fail("init", "This skill only supports macOS (darwin).")


def _parse_kv(argv):
    kv = {}
    for a in argv:
        if "=" not in a:
            _fail("args", f"Bad argument (expected key=value): {a}")
        k, v = a.split("=", 1)
        kv[k.strip()] = v
    return kv


def _split_csv(v):
    if not v:
        return []
    parts = [p.strip() for p in v.split(",")]
    return [p for p in parts if p]


def _clamp_limit(args, default=20, max_limit=100):
    raw = args.get("limit", "")
    if raw == "":
        return default
    try:
        n = int(str(raw).strip())
    except Exception:
        return default
    if n <= 0:
        return default
    if n > max_limit:
        return max_limit
    return n


def _run(cmd, input_text=None):
    p = subprocess.run(cmd, input=input_text, text=True, capture_output=True)
    return p.returncode, p.stdout, p.stderr


def _osascript(script, argv=None):
    cmd = ["osascript", "-"]
    if argv:
        cmd.extend(argv)
    code, out, err = _run(cmd, input_text=script)
    if code != 0:
        _fail("osascript", "AppleScript failed", (err or out).strip()[:1200])
    return (out or "").strip()


def _kv_lines_from_osascript(script, argv=None, sep="\t"):
    raw = _osascript(script, argv)
    if raw == "":
        return []
    lines = [l for l in raw.splitlines() if l.strip() != ""]
    out = []
    for l in lines:
        out.append(l.split(sep))
    return out


def cmd_mail_unread_count(_args):
    ascript = r'''
on run argv
  tell application "Mail"
    set u to count of (messages of inbox whose read status is false)
  end tell
  return u as text
end run
'''
    raw = _osascript(ascript, [])
    try:
        count = int(raw.strip())
    except Exception:
        count = None
    _ok("mail.unread_count", {"count": count})


def cmd_mail_unread_list(args):
    limit = _clamp_limit(args, default=20, max_limit=100)
    ascript = r'''
on run argv
  set theLimit to (item 1 of argv) as integer
  set outLines to {}
  tell application "Mail"
    set msgs to (messages of inbox whose read status is false)
    set n to count of msgs
    if n > theLimit then set n to theLimit
    repeat with i from 1 to n
      set m to item i of msgs
      set theSubject to subject of m as text
      set theSender to sender of m as text
      set theDate to date received of m as text
      set theId to message id of m as text
      set end of outLines to (theId & tab & theSubject & tab & theSender & tab & theDate)
    end repeat
  end tell
  return outLines as text
end run
'''
    rows = _kv_lines_from_osascript(ascript, [str(limit)])
    items = []
    for r in rows:
        if len(r) < 4:
            continue
        items.append({"id": r[0], "subject": r[1], "from": r[2], "date": r[3]})
    _ok("mail.unread_list", {"limit": limit, "items": items})


def cmd_notes_folders(_args):
    ascript = r'''
on run argv
  set outLines to {}
  tell application "Notes"
    repeat with a in accounts
      repeat with f in folders of a
        set end of outLines to ((name of a as text) & tab & (name of f as text))
      end repeat
    end repeat
  end tell
  return outLines as text
end run
'''
    rows = _kv_lines_from_osascript(ascript, [])
    items = []
    for r in rows:
        if len(r) < 2:
            continue
        items.append({"account": r[0], "folder": r[1]})
    _ok("notes.folders", {"items": items})


def cmd_notes_search(args):
    query = args.get("query", "").strip()
    folder = args.get("folder", "").strip()
    limit = _clamp_limit(args, default=10, max_limit=50)
    if not query:
        _fail("notes.search", "Missing query=")
    ascript = r'''
on cleanText(t)
  set t to t as text
  set AppleScript's text item delimiters to {return}
  set t to (text items of t) as text
  set AppleScript's text item delimiters to {linefeed}
  set t to (text items of t) as text
  set AppleScript's text item delimiters to {tab}
  set t to (text items of t) as text
  set AppleScript's text item delimiters to {""}
  return t
end cleanText

on run argv
  set theQuery to item 1 of argv
  set theFolder to item 2 of argv
  set theLimit to (item 3 of argv) as integer
  set outLines to {}
  tell application "Notes"
    set hits to {}
    if theFolder is "" then
      set hits to (every note whose name contains theQuery)
      if (count of hits) is 0 then set hits to (every note whose body contains theQuery)
    else
      set f to folder theFolder
      set hits to (every note of f whose name contains theQuery)
      if (count of hits) is 0 then set hits to (every note of f whose body contains theQuery)
    end if
    set n to count of hits
    if n > theLimit then set n to theLimit
    repeat with i from 1 to n
      set n0 to item i of hits
      set tTitle to my cleanText(name of n0)
      set tMod to modification date of n0 as text
      set tBody to my cleanText(body of n0)
      if (count of characters of tBody) > 160 then set tBody to (text 1 thru 160 of tBody)
      set end of outLines to (tTitle & tab & tMod & tab & tBody)
    end repeat
  end tell
  return outLines as text
end run
'''
    rows = _kv_lines_from_osascript(ascript, [query, folder, str(limit)])
    items = []
    for r in rows:
        if len(r) < 3:
            continue
        items.append({"title": r[0], "modified": r[1], "snippet": r[2]})
    _ok("notes.search", {"query": query, "folder": folder or None, "limit": limit, "items": items})


def _parse_dt(s):
    if not s:
        return None
    return str(s).strip()


def cmd_calendar_list(args):
    cal = args.get("calendar", "").strip()
    start = _parse_dt(args.get("start"))
    end = _parse_dt(args.get("end"))
    limit = _clamp_limit(args, default=50, max_limit=200)
    if not start or not end:
        _fail("calendar.list", "Missing start= or end=")
    ascript = r'''
on cleanText(t)
  set t to t as text
  set AppleScript's text item delimiters to {return}
  set t to (text items of t) as text
  set AppleScript's text item delimiters to {linefeed}
  set t to (text items of t) as text
  set AppleScript's text item delimiters to {tab}
  set t to (text items of t) as text
  set AppleScript's text item delimiters to {""}
  return t
end cleanText

on run argv
  set theCal to item 1 of argv
  set theStart to item 2 of argv
  set theEnd to item 3 of argv
  set theLimit to (item 4 of argv) as integer
  set outLines to {}
  set dStart to date theStart
  set dEnd to date theEnd
  tell application "Calendar"
    if theCal is "" then
      set targetCal to calendar 1
    else
      set matches to (every calendar whose name is theCal)
      if (count of matches) > 0 then
        set targetCal to item 1 of matches
      else
        set targetCal to calendar 1
      end if
    end if
    set evs to (every event of targetCal whose start date >= dStart and start date <= dEnd)
    set n to count of evs
    if n > theLimit then set n to theLimit
    repeat with i from 1 to n
      set e to item i of evs
      set tTitle to my cleanText(summary of e as text)
      set tStart to start date of e as text
      set tEnd to end date of e as text
      set tLoc to ""
      try
        set tLoc to my cleanText(location of e as text)
      end try
      set end of outLines to (tTitle & tab & tStart & tab & tEnd & tab & tLoc)
    end repeat
  end tell
  return outLines as text
end run
'''
    rows = _kv_lines_from_osascript(ascript, [cal, start, end, str(limit)])
    items = []
    for r in rows:
        if len(r) < 4:
            continue
        items.append({"title": r[0], "start": r[1], "end": r[2], "location": r[3] or None})
    _ok("calendar.list", {"calendar": cal or None, "start": start, "end": end, "limit": limit, "items": items})


def cmd_calendar_today(args):
    limit = _clamp_limit(args, default=50, max_limit=200)
    now = time.localtime()
    start = time.strftime("%Y-%m-%d 00:00:00", now)
    end = time.strftime("%Y-%m-%d 23:59:59", now)
    cmd_calendar_list({"calendar": args.get("calendar", ""), "start": start, "end": end, "limit": str(limit)})


_STOCKS_CACHE = {}
_STOCKS_CACHE_LOCK = threading.Lock()


def _http_get(url, timeout=8):
    u = url.strip()
    if not (u.startswith("https://") or u.startswith("http://")):
        _fail("http", "Only http/https URLs are allowed")
    if not (u.startswith("https://qt.gtimg.cn/") or u.startswith("http://qt.gtimg.cn/")):
        _fail("http", "Domain not allowlisted", {"url": u})
    ctx = ssl.create_default_context()
    req = urllib.request.Request(u, headers={"User-Agent": "openclaw-macos-suite-readonly/0.1"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        raw = resp.read(200000)
        ctype = (resp.headers.get("Content-Type") or "").lower()
        if "charset=" in ctype:
            cs = ctype.split("charset=", 1)[1].split(";", 1)[0].strip()
            try:
                return raw.decode(cs, errors="replace")
            except Exception:
                pass
        try:
            return raw.decode("utf-8", errors="strict")
        except Exception:
            try:
                return raw.decode("gb18030", errors="replace")
            except Exception:
                return raw.decode("utf-8", errors="replace")


def _stocks_norm_symbol(sym):
    s = (sym or "").strip()
    if s == "":
        return None
    if s.isdigit():
        if len(s) == 5:
            return "hk" + s
        if len(s) == 6:
            return "sh" + s
    u = s.upper()
    if u.startswith(("SH", "SZ", "HK", "US")) and len(u) > 2:
        return u.lower()
    if u.startswith("^"):
        return u.lower()
    return "us" + u


def _stocks_parse_qt_line(line):
    if "=\"" not in line:
        return None
    head, rest = line.split("=\"", 1)
    sym = head.strip()
    if sym.startswith("v_s_"):
        sym = sym[len("v_s_"):]
    elif sym.startswith("v_"):
        sym = sym[len("v_"):]
    payload = rest.rsplit("\";", 1)[0]
    parts = payload.split("~")
    if len(parts) < 6:
        return None
    name = parts[1] or None
    try:
        price = float(parts[3]) if parts[3] else None
    except Exception:
        price = None
    try:
        change = float(parts[4]) if parts[4] else None
    except Exception:
        change = None
    try:
        change_pct = float(parts[5]) if parts[5] else None
    except Exception:
        change_pct = None
    return {"symbol": sym, "name": name, "price": price, "change": change, "changePct": change_pct, "ts": None, "source": "tencent"}


def _stocks_fetch(symbols):
    syms = [s for s in symbols if s]
    if not syms:
        return []
    joined = ",".join(["s_" + s for s in syms])
    url = "https://qt.gtimg.cn/q=" + quote(joined)
    txt = _http_get(url, timeout=8)
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    out = []
    for l in lines:
        q = _stocks_parse_qt_line(l)
        if q:
            out.append(q)
    return out


def _stocks_get_cached(symbol):
    now = time.time()
    with _STOCKS_CACHE_LOCK:
        it = _STOCKS_CACHE.get(symbol)
        if not it:
            return None
        if now - it["ts"] > 30:
            return None
        return it["data"]


def _stocks_set_cached(symbol, data):
    with _STOCKS_CACHE_LOCK:
        _STOCKS_CACHE[symbol] = {"ts": time.time(), "data": data}


def cmd_stocks_quote(args):
    raw = args.get("symbol", "").strip()
    sym = _stocks_norm_symbol(raw)
    if not sym:
        _fail("stocks.quote", "Missing symbol=")
    cached = _stocks_get_cached(sym)
    if cached:
        _ok("stocks.quote", cached, {"cached": True})
        return
    rows = _stocks_fetch([sym])
    if not rows:
        _ok("stocks.quote", None, {"warning": "No quote returned", "cached": False})
        return
    q = rows[0]
    _stocks_set_cached(sym, q)
    _ok("stocks.quote", q, {"cached": False})


def cmd_stocks_batch(args):
    syms = _split_csv(args.get("symbols", ""))
    norm = []
    for s in syms:
        ns = _stocks_norm_symbol(s)
        if ns:
            norm.append(ns)
    norm = list(dict.fromkeys(norm))[:50]
    if not norm:
        _fail("stocks.batch", "Missing symbols=")
    need = []
    items = []
    for s in norm:
        c = _stocks_get_cached(s)
        if c:
            items.append({"symbol": s, "quote": c, "cached": True})
        else:
            need.append(s)
    if need:
        rows = _stocks_fetch(need)
        by = {r["symbol"]: r for r in rows if r and r.get("symbol")}
        for s in need:
            q = by.get(s)
            if q:
                _stocks_set_cached(s, q)
            items.append({"symbol": s, "quote": q, "cached": False})
    _ok("stocks.batch", {"items": items, "symbols": norm})


def main(argv):
    _require_darwin()
    if len(argv) < 2:
        _fail("init", "Missing command")
    cmd = argv[1].strip()
    args = _parse_kv(argv[2:])
    dispatch = {
        "mail.unread_count": cmd_mail_unread_count,
        "mail.unread_list": cmd_mail_unread_list,
        "calendar.today": cmd_calendar_today,
        "calendar.list": cmd_calendar_list,
        "notes.folders": cmd_notes_folders,
        "notes.search": cmd_notes_search,
        "stocks.quote": cmd_stocks_quote,
        "stocks.batch": cmd_stocks_batch,
    }
    fn = dispatch.get(cmd)
    if not fn:
        _fail("init", "Unknown command", {"command": cmd, "commands": sorted(dispatch.keys())})
    fn(args)


if __name__ == "__main__":
    main(sys.argv)
