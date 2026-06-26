#!/usr/bin/env python3
import json
import os
import shlex
import subprocess
import sys
import time
import threading
import queue
import urllib.request
import urllib.error
import ssl
import tempfile
from urllib.parse import quote


def _json_out(obj):
    sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def _fail(action, msg, detail=None, code=1):
    out = {"ok": False, "action": action, "error": msg}
    if detail:
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
    p = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
    )
    return p.returncode, p.stdout, p.stderr


def _open_app(app):
    code, out, err = _run(["open", "-a", app])
    if code != 0:
        _fail("open", "Failed to open app", (err or out).strip()[:500])
    _ok("open", {"app": app})


def _open_url(url):
    code, out, err = _run(["open", url])
    if code != 0:
        _fail("open", "Failed to open url", (err or out).strip()[:500])
    _ok("open", {"url": url})


def _open_app_silent(app):
    _run(["open", "-a", app])


def _open_url_silent(url):
    _run(["open", url])


def _osascript(script, argv=None):
    cmd = ["osascript", "-"]
    if argv:
        cmd.extend(argv)
    code, out, err = _run(cmd, input_text=script)
    if code != 0:
        _fail("osascript", "AppleScript failed", (err or out).strip()[:1200])
    return out.strip()


def _osascript_try(script, argv=None):
    cmd = ["osascript", "-"]
    if argv:
        cmd.extend(argv)
    code, out, err = _run(cmd, input_text=script)
    if code != 0:
        return None, (err or out).strip()[:1200]
    return (out or "").strip(), None


def _kv_lines_from_osascript(action, script, argv=None, sep="\t"):
    raw = _osascript(script, argv)
    if raw == "":
        return []
    lines = [l for l in raw.splitlines() if l.strip() != ""]
    out = []
    for l in lines:
        parts = l.split(sep)
        out.append(parts)
    return out


def cmd_open(args):
    app = args.get("app")
    url = args.get("url")
    if app:
        return _open_app(app)
    if url:
        return _open_url(url)
    _fail("open", "Missing app= or url=")


def _confirm_required(action, args):
    v = (args.get("confirm") or "").strip().upper()
    if v == "YES":
        return
    alternatives = []
    if action == "mail.send":
        alternatives = [{"command": "mail.draft", "note": "创建草稿，不发送"}]
    elif action == "calendar.add":
        alternatives = [{"command": "calendar.today", "note": "只读查看今天日程"}]
    elif action == "reminders.add":
        alternatives = [{"command": "reminders.list", "note": "只读查看提醒事项"}]
    elif action == "notes.create":
        alternatives = [{"command": "notes.search", "note": "只读搜索备忘录"}]
    elif action.startswith("freeform."):
        alternatives = [{"command": "freeform.open", "note": "只打开无边记，不修改画板"}]

    out = {
        "ok": False,
        "action": action,
        "needsConfirm": True,
        "error": "Confirmation required",
        "message": "该操作会修改本机应用数据或界面。为避免误操作，需要你显式确认。",
        "howToConfirm": "如继续，请在命令参数中追加 confirm=YES（大写）。",
        "confirmKey": "confirm",
        "confirmRequiredValue": "YES",
        "alternatives": alternatives,
    }
    _json_out(out)
    raise SystemExit(2)


def _permission_hint(err):
    if not err:
        return None
    s = str(err)
    low = s.lower()
    if "not allowed to send keystrokes" in low or "不允许发送按键" in s or "error: 1002" in low:
        return "需要在“系统设置 -> 隐私与安全性 -> 辅助功能/自动化”中允许终端/osascript 控制 System Events 与 Freeform。"
    if "not authorised" in low or "not authorized" in low or "automation" in low or "osa" in low:
        return "需要在“系统设置 -> 隐私与安全性 -> 自动化”中允许终端/osascript 控制相关应用。"
    return None


def cmd_mail_draft(args, send):
    action = "mail.send" if send else "mail.draft"
    to = args.get("to", "").strip()
    subject = args.get("subject", "")
    body = args.get("body", "")
    cc = _split_csv(args.get("cc", ""))
    bcc = _split_csv(args.get("bcc", ""))
    attachments = _split_csv(args.get("attachments", ""))

    if not to:
        _fail(action, "Missing to=")
    if send:
        _confirm_required(action, args)

    ascript = r'''
on run argv
  set theTo to item 1 of argv
  set theSubject to item 2 of argv
  set theBody to item 3 of argv
  set theCC to item 4 of argv
  set theBCC to item 5 of argv
  set theAttachments to item 6 of argv
  set shouldSend to item 7 of argv

  tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:theSubject, content:theBody & return & return, visible:true}
    tell newMessage
      make new to recipient at end of to recipients with properties {address:theTo}
      if theCC is not "" then
        repeat with a in (paragraphs of theCC)
          if (a as text) is not "" then make new cc recipient at end of cc recipients with properties {address:(a as text)}
        end repeat
      end if
      if theBCC is not "" then
        repeat with a in (paragraphs of theBCC)
          if (a as text) is not "" then make new bcc recipient at end of bcc recipients with properties {address:(a as text)}
        end repeat
      end if
    end tell

    if theAttachments is not "" then
      set parts to paragraphs of theAttachments
      repeat with p in parts
        set fp to (p as text)
        if fp is not "" then
          tell newMessage to make new attachment with properties {file name:fp} at after the last paragraph
        end if
      end repeat
    end if

    activate
    if shouldSend is "YES" then send newMessage
  end tell
end run
'''
    cc_arg = "\n".join(cc)
    bcc_arg = "\n".join(bcc)
    att_arg = "\n".join([os.path.expanduser(a) for a in attachments])
    should_send = "YES" if send else "NO"
    _osascript(ascript, [to, subject, body, cc_arg, bcc_arg, att_arg, should_send])
    _ok(action, {"to": to, "sent": bool(send), "draft": True})


def cmd_mail_unread_count(args):
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
    rows = _kv_lines_from_osascript("mail.unread_list", ascript, [str(limit)])
    items = []
    for r in rows:
        if len(r) < 4:
            continue
        items.append(
            {"id": r[0], "subject": r[1], "from": r[2], "date": r[3]}
        )
    _ok("mail.unread_list", {"items": items, "limit": limit})


def cmd_notes_create(args):
    _confirm_required("notes.create", args)
    title = args.get("title", "").strip()
    body = args.get("body", "")
    folder = args.get("folder", "").strip()
    if not title:
        _fail("notes.create", "Missing title=")

    ascript = r'''
on run argv
  set theTitle to item 1 of argv
  set theBody to item 2 of argv
  set theFolder to item 3 of argv

  tell application "Notes"
    if theFolder is "" then
      set targetFolder to folder 1
    else
      set targetFolder to folder theFolder
    end if
    make new note at targetFolder with properties {name:theTitle, body:theBody}
    activate
  end tell
end run
'''
    _osascript(ascript, [title, body, folder])
    _ok("notes.create", {"title": title, "folder": folder or None})


def cmd_notes_folders(_args):
    ascript = r'''
on run argv
  set outLines to {}
  tell application "Notes"
    repeat with a in accounts
      set aname to name of a as text
      repeat with f in folders of a
        set fname to name of f as text
        set end of outLines to (aname & tab & fname)
      end repeat
    end repeat
  end tell
  return outLines as text
end run
'''
    rows = _kv_lines_from_osascript("notes.folders", ascript, [])
    items = []
    for r in rows:
        if len(r) < 2:
            continue
        items.append({"account": r[0], "folder": r[1]})
    _ok("notes.folders", {"items": items})


def cmd_notes_search(args):
    query = args.get("query", "").strip()
    folder = args.get("folder", "").strip()
    limit = _clamp_limit(args, default=20, max_limit=100)
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
    argv = [query, folder, str(limit)]
    rows = _kv_lines_from_osascript("notes.search", ascript, argv)
    items = []
    for r in rows:
        if len(r) < 3:
            continue
        items.append({"title": r[0], "modified": r[1], "snippet": r[2]})
    _ok("notes.search", {"items": items, "limit": limit, "query": query, "folder": folder or None})


def cmd_reminders_add(args):
    _confirm_required("reminders.add", args)
    lst = args.get("list", "").strip()
    title = args.get("title", "").strip()
    notes = args.get("notes", "")
    due = args.get("due", "").strip()

    if not title:
        _fail("reminders.add", "Missing title=")

    ascript = r'''
on run argv
  set theList to item 1 of argv
  set theTitle to item 2 of argv
  set theNotes to item 3 of argv
  set theDue to item 4 of argv

  tell application "Reminders"
    if theList is "" then
      set targetList to list 1
    else
      set matches to (every list whose name is theList)
      if (count of matches) > 0 then
        set targetList to item 1 of matches
      else
        set targetList to list 1
      end if
    end if
    set props to {name:theTitle}
    if theNotes is not "" then set props to props & {body:theNotes}
    if theDue is not "" then
      set d to date theDue
      set props to props & {due date:d}
    end if
    make new reminder at targetList with properties props
    activate
  end tell
end run
'''
    _osascript(ascript, [lst, title, notes, due])
    _ok("reminders.add", {"list": lst or None, "title": title, "due": due or None})


def cmd_reminders_lists(_args):
    ascript = r'''
on run argv
  tell application "Reminders"
    set outLines to {}
    repeat with l in lists
      set end of outLines to (name of l as text)
    end repeat
  end tell
  return outLines as text
end run
'''
    raw = _osascript(ascript, [])
    lines = [l for l in raw.splitlines() if l.strip() != ""]
    _ok("reminders.lists", {"items": lines})


def cmd_reminders_list(args):
    lst = args.get("list", "").strip()
    include_completed = (args.get("includeCompleted", "NO").strip() == "YES")
    limit = _clamp_limit(args, default=20, max_limit=100)
    ascript = r'''
on run argv
  set theList to item 1 of argv
  set includeCompleted to item 2 of argv
  set theLimit to (item 3 of argv) as integer
  set outLines to {}

  tell application "Reminders"
    if theList is "" then
      set targetList to list 1
    else
      set matches to (every list whose name is theList)
      if (count of matches) > 0 then
        set targetList to item 1 of matches
      else
        set targetList to list 1
      end if
    end if

    set items to reminders of targetList
    set n to 0
    repeat with r in items
      set isDone to completed of r
      if includeCompleted is "YES" or isDone is false then
        set tName to name of r as text
        set tDone to isDone as text
        set tDue to ""
        try
          set tDue to due date of r as text
        end try
        set end of outLines to (tName & tab & tDone & tab & tDue)
        set n to n + 1
        if n >= theLimit then exit repeat
      end if
    end repeat
  end tell

  return outLines as text
end run
'''
    raw, err = _osascript_try(ascript, [lst, "YES" if include_completed else "NO", str(limit)])
    if err:
        name = (args.get("shortcut") or os.environ.get("MACOS_SUITE_REMINDERS_SHORTCUT") or "").strip()
        if name:
            payload = json.dumps(
                {"list": lst, "limit": limit, "includeCompleted": include_completed},
                ensure_ascii=False,
            )
            out, serr = _run_shortcut(name, input_text=payload)
            if not serr:
                try:
                    data = json.loads(out)
                    _ok("reminders.list", data, {"warning": "Used shortcuts fallback."})
                    return
                except Exception:
                    _ok("reminders.list", {"text": out, "shortcut": name}, {"warning": "Used shortcuts fallback."})
                    return
        _open_app_silent("Reminders")
        _ok("reminders.list", None, {"warning": f"Reminders query failed; opened Reminders app instead. {err}", "openedApp": "Reminders"})
        return
    lines = [l for l in raw.splitlines() if l.strip() != ""]
    rows = [l.split("\t") for l in lines]
    items = []
    for r in rows:
        if len(r) < 3:
            continue
        items.append({"title": r[0], "completed": (r[1] == "true"), "due": r[2] or None})
    _ok("reminders.list", {"list": lst or None, "includeCompleted": include_completed, "limit": limit, "items": items})


def cmd_calendar_add(args):
    _confirm_required("calendar.add", args)
    cal = args.get("calendar", "").strip()
    title = args.get("title", "").strip()
    start = args.get("start", "").strip()
    end = args.get("end", "").strip()
    location = args.get("location", "")
    notes = args.get("notes", "")

    if not title:
        _fail("calendar.add", "Missing title=")
    if not start or not end:
        _fail("calendar.add", "Missing start= or end=")

    ascript = r'''
on run argv
  set theCal to item 1 of argv
  set theTitle to item 2 of argv
  set theStart to item 3 of argv
  set theEnd to item 4 of argv
  set theLocation to item 5 of argv
  set theNotes to item 6 of argv

  set dStart to date theStart
  set dEnd to date theEnd

  tell application "Calendar"
    if theCal is "" then
      set targetCal to calendar 1
    else
      set targetCal to calendar theCal
    end if
    set props to {summary:theTitle, start date:dStart, end date:dEnd}
    if theLocation is not "" then set props to props & {location:theLocation}
    if theNotes is not "" then set props to props & {description:theNotes}
    make new event at targetCal with properties props
    activate
  end tell
end run
'''
    _osascript(ascript, [cal, title, start, end, location, notes])
    _ok("calendar.add", {"calendar": cal or None, "title": title, "start": start, "end": end})


def cmd_calendar_list(args):
    cal = args.get("calendar", "").strip()
    start = args.get("start", "").strip()
    end = args.get("end", "").strip()
    limit = _clamp_limit(args, default=50, max_limit=100)
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
    rows = _kv_lines_from_osascript("calendar.list", ascript, [cal, start, end, str(limit)])
    items = []
    for r in rows:
        if len(r) < 4:
            continue
        items.append({"title": r[0], "start": r[1], "end": r[2], "location": r[3] or None})
    _ok("calendar.list", {"calendar": cal or None, "start": start, "end": end, "limit": limit, "items": items})


def cmd_calendar_today(args):
    now = time.localtime()
    start = time.strftime("%Y-%m-%d 00:00:00", now)
    end = time.strftime("%Y-%m-%d 23:59:59", now)
    cal = args.get("calendar", "").strip()
    limit = _clamp_limit(args, default=50, max_limit=100)
    cmd_calendar_list({"calendar": cal, "start": start, "end": end, "limit": str(limit)})


def cmd_maps_search(args):
    q = args.get("query", "").strip()
    if not q:
        _fail("maps.search", "Missing query=")
    url = "http://maps.apple.com/?q=" + quote(q)
    _open_url(url)


def cmd_maps_directions(args):
    saddr = args.get("saddr", "").strip()
    daddr = args.get("daddr", "").strip()
    mode = args.get("mode", "d").strip() or "d"
    if not daddr:
        _fail("maps.directions", "Missing daddr=")
    parts = []
    if saddr:
        parts.append("saddr=" + quote(saddr))
    parts.append("daddr=" + quote(daddr))
    parts.append("dirflg=" + quote(mode))
    url = "http://maps.apple.com/?" + "&".join(parts)
    _open_url(url)


def cmd_photos_open(_args):
    _open_app("Photos")


def cmd_photos_recent(args):
    limit = _clamp_limit(args, default=20, max_limit=50)
    ascript = r'''
on run argv
  set theLimit to (item 1 of argv) as integer
  set outLines to {}
  tell application "Photos"
    try
      set a to album "Recents"
      set items to media items of a
      set n to count of items
      if n > theLimit then set n to theLimit
      repeat with i from 1 to n
        set m to item i of items
        set tDate to ""
        try
          set tDate to date of m as text
        end try
        set tName to ""
        try
          set tName to name of m as text
        end try
        set tFav to ""
        try
          set tFav to favorite of m as text
        end try
        set end of outLines to (tDate & tab & tName & tab & tFav)
      end repeat
      activate
      return outLines as text
    on error errMsg number errNum
      return ""
    end try
  end tell
end run
'''
    try:
        rows = _kv_lines_from_osascript("photos.recent", ascript, [str(limit)])
    except SystemExit:
        raise
    except Exception:
        rows = []
    if not rows:
        cmd_photos_open({})
        return
    items = []
    for r in rows:
        if len(r) < 3:
            continue
        items.append({"date": r[0] or None, "name": r[1] or None, "favorite": (r[2] == "true")})
    _ok("photos.recent", {"items": items, "limit": limit})


def cmd_freeform_open(_args):
    _open_app("Freeform")


def _freeform_activate():
    _open_app_silent("Freeform")
    _osascript_try('tell application "Freeform" to activate', [])
    time.sleep(0.2)


def _freeform_ui_try(script, argv=None):
    _freeform_activate()
    return _osascript_try(script, argv or [])


def _freeform_new_board(title):
    title = (title or "").strip()
    ascript = r'''
on run argv
  set theTitle to item 1 of argv
  tell application "Freeform" to activate
  delay 0.2
  tell application "System Events"
    tell process "Freeform"
      set frontmost to true
      delay 0.2
      try
        click menu item "New Board" of menu 1 of menu bar item "File" of menu bar 1
      on error
        try
          click menu item "新建画板" of menu 1 of menu bar item "文件" of menu bar 1
        on error
          keystroke "n" using {command down}
        end try
      end try
      delay 0.3
      if theTitle is not "" then
        set the clipboard to theTitle
        keystroke "v" using {command down}
        key code 36
      end if
    end tell
  end tell
  return "ok"
end run
'''
    out, err = _freeform_ui_try(ascript, [title])
    return err


def cmd_freeform_new_board(args):
    _confirm_required("freeform.new_board", args)
    title = args.get("title", "").strip()
    err = _freeform_new_board(title)
    if err:
        extra = {"warning": err, "openedApp": "Freeform"}
        hint = _permission_hint(err)
        if hint:
            extra["hint"] = hint
        _ok("freeform.new_board", None, extra)
        return
    _ok("freeform.new_board", {"title": title or None})


def _freeform_add_text(text):
    text = text or ""
    ascript = r'''
on run argv
  set theText to item 1 of argv
  tell application "Freeform" to activate
  delay 0.2
  tell application "System Events"
    tell process "Freeform"
      set frontmost to true
      delay 0.2
      try
        click menu item "Text Box" of menu 1 of menu bar item "Insert" of menu bar 1
      on error
        try
          click menu item "文本框" of menu 1 of menu bar item "插入" of menu bar 1
        end try
      end try
      delay 0.2
      set the clipboard to theText
      keystroke "v" using {command down}
      delay 0.1
      key code 53
    end tell
  end tell
  return "ok"
end run
'''
    out, err = _freeform_ui_try(ascript, [text])
    return err


def cmd_freeform_add_text(args):
    _confirm_required("freeform.add_text", args)
    text = args.get("text", "")
    err = _freeform_add_text(text)
    if err:
        extra = {"warning": err, "openedApp": "Freeform"}
        hint = _permission_hint(err)
        if hint:
            extra["hint"] = hint
        _ok("freeform.add_text", None, extra)
        return
    _ok("freeform.add_text", {"textLen": len(text)})


def _freeform_add_sticky(text):
    text = text or ""
    ascript = r'''
on run argv
  set theText to item 1 of argv
  tell application "Freeform" to activate
  delay 0.2
  tell application "System Events"
    tell process "Freeform"
      set frontmost to true
      delay 0.2
      try
        click menu item "Sticky Note" of menu 1 of menu bar item "Insert" of menu bar 1
      on error
        try
          click menu item "便笺" of menu 1 of menu bar item "插入" of menu bar 1
        end try
      end try
      delay 0.2
      set the clipboard to theText
      keystroke "v" using {command down}
      delay 0.1
      key code 53
    end tell
  end tell
  return "ok"
end run
'''
    out, err = _freeform_ui_try(ascript, [text])
    return err


def cmd_freeform_add_sticky(args):
    _confirm_required("freeform.add_sticky", args)
    text = args.get("text", "")
    err = _freeform_add_sticky(text)
    if err:
        extra = {"warning": err, "openedApp": "Freeform"}
        hint = _permission_hint(err)
        if hint:
            extra["hint"] = hint
        _ok("freeform.add_sticky", None, extra)
        return
    _ok("freeform.add_sticky", {"textLen": len(text)})


def _freeform_add_shape(en, zh):
    ascript = r'''
on run argv
  set kEn to item 1 of argv
  set kZh to item 2 of argv
  tell application "Freeform" to activate
  delay 0.2
  tell application "System Events"
    tell process "Freeform"
      set frontmost to true
      delay 0.2
      try
        click menu item "Shape" of menu 1 of menu bar item "Insert" of menu bar 1
        delay 0.1
        click menu item kEn of menu 1 of menu item "Shape" of menu 1 of menu bar item "Insert" of menu bar 1
      on error
        try
          click menu item "形状" of menu 1 of menu bar item "插入" of menu bar 1
          delay 0.1
          click menu item kZh of menu 1 of menu item "形状" of menu 1 of menu bar item "插入" of menu bar 1
        end try
      end try
    end tell
  end tell
  return "ok"
end run
'''
    out, err = _freeform_ui_try(ascript, [en, zh])
    return err


def cmd_freeform_add_shape(args):
    _confirm_required("freeform.add_shape", args)
    kind = (args.get("kind", "") or "").strip().lower()
    kind_map = {
        "rectangle": ("Rectangle", "矩形"),
        "circle": ("Circle", "圆形"),
        "line": ("Line", "线条"),
        "arrow": ("Arrow", "箭头"),
    }
    if kind not in kind_map:
        _fail("freeform.add_shape", "Unsupported kind", {"kind": kind, "supported": sorted(kind_map.keys())})
    en, zh = kind_map[kind]
    err = _freeform_add_shape(en, zh)
    if err:
        extra = {"warning": err, "openedApp": "Freeform"}
        hint = _permission_hint(err)
        if hint:
            extra["hint"] = hint
        _ok("freeform.add_shape", None, extra)
        return
    _ok("freeform.add_shape", {"kind": kind})


def cmd_freeform_compose(args):
    _confirm_required("freeform.compose", args)
    fp = (args.get("file", "") or "").strip()
    if not fp:
        _fail("freeform.compose", "Missing file=")
    path = os.path.expanduser(fp)
    try:
        with open(path, "r", encoding="utf-8") as f:
            spec = json.load(f)
    except Exception as e:
        _fail("freeform.compose", "Failed to read JSON file", str(e)[:300])
    title = (spec.get("boardTitle") or "").strip()
    items = spec.get("items") or []
    if not isinstance(items, list):
        _fail("freeform.compose", "items must be an array")

    first_err = _freeform_new_board(title)
    created = {"text": 0, "sticky": 0, "shape": 0}
    warnings = []
    if first_err:
        extra = {"warning": first_err, "openedApp": "Freeform"}
        hint = _permission_hint(first_err)
        if hint:
            extra["hint"] = hint
        _ok("freeform.compose", None, extra)
        return
    for it in items:
        if not isinstance(it, dict):
            continue
        t = (it.get("type") or "").strip().lower()
        if t == "text":
            text = it.get("text") or ""
            err = _freeform_add_text(text)
            if err:
                warnings.append(err)
            else:
                created["text"] += 1
        elif t == "sticky":
            text = it.get("text") or ""
            err = _freeform_add_sticky(text)
            if err:
                warnings.append(err)
            else:
                created["sticky"] += 1
        elif t == "shape":
            kind = it.get("kind") or ""
            k = str(kind).strip().lower()
            kind_map = {
                "rectangle": ("Rectangle", "矩形"),
                "circle": ("Circle", "圆形"),
                "line": ("Line", "线条"),
                "arrow": ("Arrow", "箭头"),
            }
            if k not in kind_map:
                warnings.append(f"Unsupported shape kind: {k}")
                continue
            en, zh = kind_map[k]
            err = _freeform_add_shape(en, zh)
            if err:
                warnings.append(err)
            else:
                created["shape"] += 1
        else:
            warnings.append(f"Skipped unknown item type: {t}")
    extra = {}
    if warnings:
        extra["warning"] = "; ".join(warnings)[:800]
    _ok("freeform.compose", {"boardTitle": title or None, "created": created}, extra)


def cmd_weather_open(_args):
    _open_app("Weather")


def _has_shortcuts():
    return os.path.exists("/usr/bin/shortcuts")


def _run_shortcut(name, input_text=None):
    if not _has_shortcuts():
        return None, "shortcuts CLI not found"
    cmd = ["/usr/bin/shortcuts", "run", name]
    tmp_path = None
    if input_text is not None:
        fd, tmp_path = tempfile.mkstemp(prefix="openclaw-shortcuts-input-", suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(input_text)
        cmd.extend(["--input-path", tmp_path])
    code, out, err = _run(cmd)
    if tmp_path:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
    if code != 0:
        return None, (err or out).strip()[:500]
    return (out or "").strip(), None


def cmd_weather_current(args):
    name = (args.get("shortcut") or os.environ.get("MACOS_SUITE_WEATHER_SHORTCUT") or "").strip()
    if not name:
        _open_app_silent("Weather")
        _ok("weather.current", None, {"warning": "No shortcut configured. Set shortcut=... or env MACOS_SUITE_WEATHER_SHORTCUT.", "openedApp": "Weather"})
        return
    out, err = _run_shortcut(name)
    if err:
        _open_app_silent("Weather")
        _ok("weather.current", None, {"warning": f"Shortcut failed: {err}", "openedApp": "Weather"})
        return
    try:
        data = json.loads(out)
        _ok("weather.current", data)
        return
    except Exception:
        _ok("weather.current", {"text": out, "shortcut": name})


def cmd_clock_open(_args):
    _open_app("Clock")


def cmd_stocks_open(args):
    sym = args.get("symbol", "").strip()
    if not sym:
        _open_app("Stocks")
        return
    url = "stocks://quote?symbol=" + quote(sym)
    _open_url(url)


_STOCKS_CACHE = {}
_STOCKS_CACHE_LOCK = threading.Lock()


def _http_get(url, timeout=8):
    u = url.strip()
    if not (u.startswith("https://") or u.startswith("http://")):
        _fail("http", "Only http/https URLs are allowed")
    if not (
        u.startswith("https://qt.gtimg.cn/")
        or u.startswith("http://qt.gtimg.cn/")
        or u.startswith("https://stooq.com/")
        or u.startswith("http://stooq.com/")
    ):
        _fail("http", "Domain not allowlisted", {"url": u})
    ctx = ssl.create_default_context()
    req = urllib.request.Request(u, headers={"User-Agent": "openclaw-macos-suite/0.1"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        max_bytes = 2000000 if ("stooq.com/" in u) else 200000
        raw = resp.read(max_bytes)
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


def _normalize_symbol(sym):
    s = (sym or "").strip()
    if s == "":
        return None
    s2 = s.replace(" ", "").upper()
    for p in ["SH", "SZ", "HK"]:
        if s2.startswith(p):
            return p.lower() + s2[len(p):]
    if s2.startswith("SH") or s2.startswith("SZ"):
        return s2.lower()
    if s2.startswith("HK"):
        return "hk" + s2[2:]
    if s2.isdigit() and len(s2) == 6:
        if s2.startswith("6"):
            return "sh" + s2
        return "sz" + s2
    if s2.isdigit() and len(s2) == 5:
        return "hk" + s2
    if "." in s2:
        base = s2.split(".", 1)[0]
        if base.isalpha():
            return "us" + base
        return s2
    if s2.isalpha():
        return "us" + s2
    return s2


def _stocks_quote_cached(key):
    with _STOCKS_CACHE_LOCK:
        v = _STOCKS_CACHE.get(key)
        if not v:
            return None
        ts, data = v
        if time.time() - ts > 30:
            del _STOCKS_CACHE[key]
            return None
        return data


def _stocks_quote_set_cache(key, data):
    with _STOCKS_CACHE_LOCK:
        _STOCKS_CACHE[key] = (time.time(), data)


def _parse_float(x):
    try:
        return float(str(x).strip())
    except Exception:
        return None


def _fetch_tencent_simple(code):
    q = "s_" + code
    url = "https://qt.gtimg.cn/q=" + quote(q)
    text = _http_get(url, timeout=8)
    if "~" not in text:
        return None
    try:
        payload = text.split('"', 2)[1]
    except Exception:
        payload = text
    parts = payload.split("~")
    if len(parts) < 6:
        return None
    name = parts[1] or None
    price = _parse_float(parts[3])
    chg = _parse_float(parts[4])
    chg_pct = _parse_float(parts[5])
    return {
        "symbol": code,
        "name": name,
        "price": price,
        "change": chg,
        "changePct": chg_pct,
        "ts": None,
        "source": "tencent",
    }


def _fetch_stooq_daily(sym):
    s = sym.lower()
    if "." not in s:
        s = s + ".us"
    url = "https://stooq.com/q/d/l/?s=" + quote(s) + "&i=d"
    csv = _http_get(url, timeout=10)
    lines = [l.strip() for l in csv.splitlines() if l.strip() != ""]
    if len(lines) < 3:
        return None
    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        cols = line.split(",")
        if len(cols) < 6:
            continue
        rows.append(cols)
    if len(rows) < 2:
        return None
    idx_close = header.index("Close") if "Close" in header else 4
    idx_date = header.index("Date") if "Date" in header else 0
    rows.sort(key=lambda r: r[idx_date])
    last = rows[-1]
    prev = rows[-2]
    price = _parse_float(last[idx_close])
    prev_close = _parse_float(prev[idx_close])
    chg = None
    chg_pct = None
    if price is not None and prev_close is not None and prev_close != 0:
        chg = price - prev_close
        chg_pct = (chg / prev_close) * 100.0
    ts = last[idx_date] if idx_date < len(last) else None
    return {
        "symbol": sym,
        "name": None,
        "price": price,
        "change": chg,
        "changePct": chg_pct,
        "ts": ts,
        "source": "stooq",
    }


def _fetch_stooq_series(sym, days=260):
    s = sym.lower()
    if "." not in s:
        s = s + ".us"
    url = "https://stooq.com/q/d/l/?s=" + quote(s) + "&i=d"
    csv = _http_get(url, timeout=10)
    lines = [l.strip() for l in csv.splitlines() if l.strip() != ""]
    if len(lines) < 2:
        return None
    header = lines[0].split(",")
    idx_date = header.index("Date") if "Date" in header else 0
    idx_open = header.index("Open") if "Open" in header else 1
    idx_high = header.index("High") if "High" in header else 2
    idx_low = header.index("Low") if "Low" in header else 3
    idx_close = header.index("Close") if "Close" in header else 4
    idx_vol = header.index("Volume") if "Volume" in header else 5
    rows = []
    for line in lines[1:]:
        cols = line.split(",")
        if len(cols) <= max(idx_date, idx_open, idx_high, idx_low, idx_close, idx_vol):
            continue
        d = cols[idx_date]
        o = _parse_float(cols[idx_open])
        h = _parse_float(cols[idx_high])
        lo = _parse_float(cols[idx_low])
        c = _parse_float(cols[idx_close])
        v = _parse_float(cols[idx_vol])
        if not d:
            continue
        if c is None:
            continue
        rows.append({"date": d, "open": o, "high": h, "low": lo, "close": c, "volume": v})
    if not rows:
        return None
    rows.sort(key=lambda r: r["date"])
    if days and days > 0 and len(rows) > days:
        rows = rows[-days:]
    first = rows[0]["close"]
    last = rows[-1]["close"]
    chg = None
    chg_pct = None
    if first is not None and last is not None and first != 0:
        chg = last - first
        chg_pct = (chg / first) * 100.0
    return {"symbol": sym, "source": "stooq", "days": days, "items": rows, "from": rows[0]["date"], "to": rows[-1]["date"], "change": chg, "changePct": chg_pct}


def cmd_stocks_history(args):
    sym = args.get("symbol", "").strip()
    if not sym:
        _fail("stocks.history", "Missing symbol=")
    raw_days = (args.get("days") or "").strip()
    raw_range = (args.get("range") or "").strip().lower()
    days = None
    if raw_days:
        try:
            days = int(raw_days)
        except Exception:
            days = None
    if days is None:
        if raw_range in ("1y", "1year", "year"):
            days = 260
        elif raw_range in ("6m", "6mon", "6month"):
            days = 130
        elif raw_range in ("3m", "3mon", "3month"):
            days = 65
        elif raw_range in ("1m", "1mon", "1month"):
            days = 22
        else:
            days = 260
    if days > 2000:
        days = 2000
    norm = _normalize_symbol(sym)
    if not norm:
        _fail("stocks.history", "Bad symbol", {"symbol": sym})
    if norm.startswith(("sh", "sz", "hk")):
        _fail("stocks.history", "History currently supports US tickers via stooq", {"symbol": sym})
    stooq_sym = norm[2:] if norm.startswith("us") else norm
    data = _fetch_stooq_series(stooq_sym, days=days)
    if not data:
        _ok("stocks.history", None, {"warning": "History fetch failed (stooq)."})
        return
    _ok("stocks.history", data)


def cmd_stocks_quote(args):
    sym = args.get("symbol", "").strip()
    if not sym:
        _fail("stocks.quote", "Missing symbol=")
    norm = _normalize_symbol(sym)
    cached = _stocks_quote_cached(norm)
    if cached:
        _ok("stocks.quote", cached, {"cached": True})
        return
    data = None
    if norm.startswith(("sh", "sz", "hk", "us")):
        data = _fetch_tencent_simple(norm)
    else:
        data = _fetch_stooq_daily(norm)
    if not data:
        _open_url_silent("stocks://quote?symbol=" + quote(sym))
        _ok("stocks.quote", None, {"warning": "Quote fetch failed; opened Stocks app instead.", "openedApp": "Stocks"})
        return
    _stocks_quote_set_cache(norm, data)
    _ok("stocks.quote", data, {"cached": False})


def cmd_stocks_batch(args):
    raw = args.get("symbols", "").strip()
    if not raw:
        _fail("stocks.batch", "Missing symbols=")
    syms = _split_csv(raw)
    limit = _clamp_limit({"limit": str(len(syms))}, default=len(syms), max_limit=50)
    syms = syms[:limit]
    qout = queue.Queue()
    threads = []

    def worker(s):
        try:
            norm = _normalize_symbol(s)
            if not norm:
                qout.put({"symbol": s, "ok": False, "error": "bad symbol"})
                return
            cached = _stocks_quote_cached(norm)
            if cached:
                qout.put({"symbol": s, "ok": True, "data": cached, "cached": True})
                return
            if norm.startswith(("sh", "sz", "hk", "us")):
                data = _fetch_tencent_simple(norm)
            else:
                data = _fetch_stooq_daily(norm)
            if not data:
                qout.put({"symbol": s, "ok": False, "error": "fetch failed"})
                return
            _stocks_quote_set_cache(norm, data)
            qout.put({"symbol": s, "ok": True, "data": data, "cached": False})
        except Exception as e:
            qout.put({"symbol": s, "ok": False, "error": str(e)[:120]})

    for s in syms:
        t = threading.Thread(target=worker, args=(s,))
        t.start()
        threads.append(t)
        while sum(1 for tt in threads if tt.is_alive()) >= 5:
            time.sleep(0.05)

    for t in threads:
        t.join(12)

    items = []
    while not qout.empty():
        items.append(qout.get_nowait())
    items.sort(key=lambda x: syms.index(x["symbol"]) if x.get("symbol") in syms else 9999)
    _ok("stocks.batch", {"items": items, "symbols": syms})


def main():
    _require_darwin()
    if len(sys.argv) < 2:
        _fail("init", "Missing command")
    command = sys.argv[1].strip()
    args = _parse_kv(sys.argv[2:])

    dispatch = {
        "open": cmd_open,
        "mail.draft": lambda a: cmd_mail_draft(a, send=False),
        "mail.send": lambda a: cmd_mail_draft(a, send=True),
        "mail.unread_count": cmd_mail_unread_count,
        "mail.unread_list": cmd_mail_unread_list,
        "notes.create": cmd_notes_create,
        "notes.folders": cmd_notes_folders,
        "notes.search": cmd_notes_search,
        "reminders.add": cmd_reminders_add,
        "reminders.lists": cmd_reminders_lists,
        "reminders.list": cmd_reminders_list,
        "calendar.add": cmd_calendar_add,
        "calendar.list": cmd_calendar_list,
        "calendar.today": cmd_calendar_today,
        "maps.search": cmd_maps_search,
        "maps.directions": cmd_maps_directions,
        "photos.open": cmd_photos_open,
        "photos.recent": cmd_photos_recent,
        "freeform.open": cmd_freeform_open,
        "freeform.new_board": cmd_freeform_new_board,
        "freeform.add_text": cmd_freeform_add_text,
        "freeform.add_sticky": cmd_freeform_add_sticky,
        "freeform.add_shape": cmd_freeform_add_shape,
        "freeform.compose": cmd_freeform_compose,
        "weather.open": cmd_weather_open,
        "weather.current": cmd_weather_current,
        "clock.open": cmd_clock_open,
        "stocks.open": cmd_stocks_open,
        "stocks.quote": cmd_stocks_quote,
        "stocks.batch": cmd_stocks_batch,
        "stocks.history": cmd_stocks_history,
    }

    fn = dispatch.get(command)
    if not fn:
        _fail("init", "Unknown command", {"command": command, "known": sorted(dispatch.keys())})
    fn(args)


if __name__ == "__main__":
    main()
