#!/usr/bin/env python3
"""
Package Tracker - Core logic
Handles: Kuaidi100 subscribe API, push webhook processing,
         today-delivery detection, Google Calendar sync, local state.

Usage (called by index.ts via execFile):
  python3 tracker_core.py <command> <json_args>

Commands:
  add_tracking      {"number":"...", "com":"auto", "note":"..."}
  handle_push       {"push_body": "<raw json string from kuaidi100 webhook>"}
  sync_calendar     {}
  list_packages     {}
  remove_tracking   {"number":"..."}
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path
from typing import Any

# ── Paths ──────────────────────────────────────────────────────────────────────
STATE_FILE = Path(os.environ.get(
    "TRACKER_STATE_FILE",
    os.path.expanduser("~/.openclaw/workspace/package-tracker-state.json"),
))

# ── Config (injected via env) ──────────────────────────────────────────────────
KUAIDI100_CUSTOMER    = os.environ.get("KUAIDI100_CUSTOMER", "")
KUAIDI100_KEY         = os.environ.get("KUAIDI100_KEY", "")
KUAIDI100_SUB_KEY     = os.environ.get("KUAIDI100_SUB_KEY", KUAIDI100_KEY)   # subscribe uses same key
KUAIDI100_SUB_ENDPOINT = os.environ.get("KUAIDI100_SUB_ENDPOINT",
    "https://poll.kuaidi100.com/poll")
WEBHOOK_URL           = os.environ.get("KUAIDI100_WEBHOOK_URL", "")          # set by plugin at runtime
KUAIDI100_SALT         = os.environ.get("KUAIDI100_SALT", "")
KUAIDI100_SIGNATURE_MODE = os.environ.get("KUAIDI100_SIGNATURE_MODE", "soft").strip().lower()

GCAL_CLIENT_ID     = os.environ.get("GCAL_CLIENT_ID", "")
GCAL_CLIENT_SECRET = os.environ.get("GCAL_CLIENT_SECRET", "")
GCAL_REFRESH_TOKEN = os.environ.get("GCAL_REFRESH_TOKEN", "")
GCAL_CALENDAR_ID   = os.environ.get("GCAL_CALENDAR_ID", "primary")

OFF_WORK_TIME           = os.environ.get("OFF_WORK_TIME", "18:30")
REMINDER_MINUTES_BEFORE = int(os.environ.get("REMINDER_MINUTES_BEFORE", "30"))
TIMEZONE_NAME           = os.environ.get("TIMEZONE_NAME", os.environ.get("TIMEZONE", "Asia/Shanghai"))


# ── State helpers ──────────────────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {"packages": {}}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


# ── Kuaidi100 subscribe API ────────────────────────────────────────────────────
# Docs: https://api.kuaidi100.com/document/subscribeApi
# Sign = MD5(param + key + customer).upper()
# Endpoint: POST https://poll.kuaidi100.com/poll
# Form fields: schema=json, param=<json>, sign=<sign>, key=<customer>

STATE_LABELS = {
    "0": "运输中", "1": "已揽收", "2": "疑难件", "3": "已签收",
    "4": "退签",   "5": "派送中", "6": "退回",   "7": "转投",
    "8": "清关中", "14": "拒签",
}

TODAY_KEYWORDS = [
    "派件", "派送中", "今日达", "今日送", "派送员",
    "已到驿站", "可取件", "到达待取", "等待取件", "正在派件",
]


def md5_upper(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest().upper()


def subscribe_kuaidi100(number: str, com: str, webhook_url: str) -> dict:
    """Subscribe to push updates for a tracking number. Costs 1 quota."""
    if not KUAIDI100_CUSTOMER or not KUAIDI100_KEY:
        return {"error": "missing_kuaidi100_credentials"}
    if not webhook_url:
        return {"error": "missing_webhook_url"}

    # ⚠️ Kuaidi100 subscribe API expects param.key = API secret (授权 key),
    # while the form field `key` is the customer id.
    salt = (KUAIDI100_SALT or "").strip()
    param_obj = {
        "company": com,
        "number":  number,
        "from":    "",
        "to":      "",
        "key":     KUAIDI100_KEY,
        "parameters": {
            "callbackurl": webhook_url,
            # Kuaidi100 callback signature salt. Strongly recommended.
            # If not configured explicitly, we fall back to token-based gate in the callback path.
            "salt":        salt,
            "resultv2":    "1",
            "autoCom":     "1",  # auto detect carrier if com=auto
        },
    }
    param = json.dumps(param_obj, ensure_ascii=False, separators=(",", ":"))
    sign  = md5_upper(param + KUAIDI100_KEY + KUAIDI100_CUSTOMER)

    form = urllib.parse.urlencode({
        "schema": "json",
        "param":  param,
        "sign":   sign,
        "key":    KUAIDI100_CUSTOMER,
    }).encode()

    try:
        req = urllib.request.Request(
            KUAIDI100_SUB_ENDPOINT, data=form,
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


# ── Push payload parser ────────────────────────────────────────────────────────

def is_today_delivery(state: str, traces: list[dict]) -> bool:
    if state == "5":
        return True
    for t in traces[:3]:
        ctx = (t.get("context") or "").lower()
        for kw in TODAY_KEYWORDS:
            if kw.lower() in ctx:
                return True
    return False


def _verify_push_signature(raw: dict) -> tuple[bool, str]:
    """Verify kuaidi100 callback signature when present.

    Per Kuaidi100 doc: when salt is set (or even empty string), callback includes
    `sign` where sign = MD5(param + salt).upper(), and `param` is the JSON payload.

    Our plugin may receive:
      - JSON body (already decoded)
      - form body parsed into dict with `_param_raw` preserved

    Salt comes from env KUAIDI100_SALT.
    """
    salt = (KUAIDI100_SALT or "").strip()
    if salt is None:
        salt = ""

    sig = raw.get("sign") or raw.get("signature") or raw.get("saltSign")
    if not sig:
        # If kuaidi100 didn't include sign, accept (token-in-path still gates ingress)
        return True, "no_signature_in_payload"

    sig_u = str(sig).strip().upper()

    # Best-effort: exact doc rule uses the original `param` string.
    param_raw = raw.get("_param_raw")
    if isinstance(param_raw, str) and param_raw:
        if md5_upper(param_raw + salt) == sig_u:
            return True, "signature_ok:param_raw"
        return False, "signature_mismatch:param_raw"

    # Fallbacks for JSON-only bodies (we don't have the original param string)
    try:
        raw_compact = json.dumps(raw, ensure_ascii=False, separators=(",", ":"))
    except Exception:
        raw_compact = ""
    if raw_compact and md5_upper(raw_compact + salt) == sig_u:
        return True, "signature_ok:raw_compact"

    return False, "signature_mismatch"


def parse_push_payload(raw: dict) -> dict | None:
    """
    Kuaidi100 push body shape:
    {
      "status": "200",
      "message": "ok",
      "lastResult": {
        "com": "shunfeng",
        "nu": "SF...",
        "state": "5",
        "ischeck": "0",
        "data": [{"time":..., "ftime":..., "context":..., "location":...}, ...]
      }
    }
    Returns normalised package dict or None on parse error.
    """
    last = raw.get("lastResult") or {}
    number = last.get("nu") or ""
    if not number:
        return None

    traces = last.get("data") or []
    latest = traces[0] if traces else {}
    state  = str(last.get("state", ""))

    return {
        "number":         number,
        "com":            last.get("com") or "auto",
        "state":          state,
        "state_label":    STATE_LABELS.get(state, "未知"),
        "is_completed":   str(last.get("ischeck", "0")) == "1",
        "today_delivery": is_today_delivery(state, traces),
        "latest_time":    latest.get("ftime") or latest.get("time") or "",
        "latest_context": latest.get("context") or "",
        "updated_at":     _now_utc_iso(),
        "raw_message":    raw.get("message") or "",
    }


# ── Google Calendar ────────────────────────────────────────────────────────────

def gcal_refresh_access_token() -> str:
    if not all([GCAL_CLIENT_ID, GCAL_CLIENT_SECRET, GCAL_REFRESH_TOKEN]):
        raise ValueError("Missing Google Calendar credentials")
    data = urllib.parse.urlencode({
        "client_id":     GCAL_CLIENT_ID,
        "client_secret": GCAL_CLIENT_SECRET,
        "refresh_token": GCAL_REFRESH_TOKEN,
        "grant_type":    "refresh_token",
    }).encode()
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token", data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())["access_token"]


def gcal_list_events(access_token: str, date_str: str) -> list[dict]:
    y, m, d = [int(x) for x in date_str.split("-")]
    tz = _tz()
    time_min = datetime(y, m, d, 0, 0, 0, tzinfo=tz).isoformat(timespec="seconds")
    time_max = datetime(y, m, d, 23, 59, 59, tzinfo=tz).isoformat(timespec="seconds")
    params = urllib.parse.urlencode({
        "timeMin": time_min, "timeMax": time_max,
        "q": "取快递", "singleEvents": "true",
    })
    cal_id = urllib.parse.quote(GCAL_CALENDAR_ID, safe="")
    url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_id}/events?{params}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read()).get("items", [])


def gcal_upsert_event(access_token: str, date_str: str, packages: list[dict]) -> dict:
    hw, hm = OFF_WORK_TIME.split(":")
    tz = _tz()
    off_dt = datetime(
        *[int(x) for x in date_str.split("-")],
        int(hw), int(hm), 0,
        tzinfo=tz,
    )
    start_dt = off_dt - timedelta(minutes=REMINDER_MINUTES_BEFORE)
    end_dt   = start_dt + timedelta(minutes=30)

    def fmt(dt: datetime) -> str:
        return dt.isoformat(timespec="seconds")

    desc_lines = []
    for p in packages:
        tail = p["number"][-4:] if len(p["number"]) >= 4 else p["number"]
        line = f"···{tail} · {p.get('com','?')} · {p.get('state_label','?')}"
        if p.get("note"):
            line += f" · {p['note']}"
        if p.get("latest_context"):
            line += f"\n  {p['latest_context']}"
        desc_lines.append(line)

    body = {
        "summary": f"📦 取快递（{len(packages)}件）",
        "description": "\n".join(desc_lines),
        "start": {"dateTime": fmt(start_dt), "timeZone": "Asia/Shanghai"},
        "end":   {"dateTime": fmt(end_dt),   "timeZone": "Asia/Shanghai"},
        "reminders": {"useDefault": False, "overrides": [{"method": "popup", "minutes": 0}]},
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type":  "application/json",
    }
    cal_id = urllib.parse.quote(GCAL_CALENDAR_ID, safe="")
    existing = gcal_list_events(access_token, date_str)

    if existing:
        event_id = existing[0]["id"]
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_id}/events/{event_id}"
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="PUT")
        action = "updated"
    else:
        url = f"https://www.googleapis.com/calendar/v3/calendars/{cal_id}/events"
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method="POST")
        action = "created"

    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read())
        return {"action": action, "event_id": result.get("id"), "summary": body["summary"]}


# ── Helpers ────────────────────────────────────────────────────────────────────

def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _tz() -> ZoneInfo:
    try:
        return ZoneInfo(TIMEZONE_NAME)
    except Exception:
        # Safe fallback
        return ZoneInfo("Asia/Shanghai")


def _now_local() -> datetime:
    return datetime.now(_tz())


# ── Commands ───────────────────────────────────────────────────────────────────

def cmd_add_tracking(args: dict) -> dict:
    number = (args.get("number") or "").strip()
    if not number:
        return {"error": "number is required"}
    com          = args.get("com") or "auto"
    note         = args.get("note") or ""
    webhook_url  = args.get("webhook_url") or WEBHOOK_URL

    state = load_state()
    if number in state["packages"]:
        return {"status": "already_exists", "number": number,
                "package": state["packages"][number]}

    # Subscribe — costs 1 quota; kuaidi100 will push initial status + all updates
    sub_result = subscribe_kuaidi100(number, com, webhook_url)

    entry: dict = {
        "number": number, "com": com, "note": note,
        "state": "", "state_label": "等待推送",
        "is_completed": False, "today_delivery": False,
        "latest_time": "", "latest_context": "",
        "updated_at": _now_utc_iso(),
        "subscribed": True,
        "subscribe_result": sub_result,
    }

    # Treat non-200 status as subscription failure (still save, user can retry)
    sub_status = str(sub_result.get("returnCode") or sub_result.get("result") or "")
    if sub_result.get("error") or sub_status not in ("", "200", "true"):
        entry["subscribed"] = False
        entry["state_label"] = "订阅失败"

    state["packages"][number] = entry
    save_state(state)
    return {"status": "subscribed" if entry["subscribed"] else "subscribe_failed",
            "package": entry, "subscribe_result": sub_result}


def _parse_push_body(raw_body: str | dict) -> tuple[dict | None, dict | None]:
    """Parse kuaidi100 webhook body.

    Kuaidi100 may POST either:
      1) JSON body: {"status":..., "message":..., "lastResult":...}
      2) application/x-www-form-urlencoded with fields: sign=<...>&param=<json>
         where param JSON contains status/message/lastResult.

    Returns: (push_data, error)
    """
    if isinstance(raw_body, dict):
        return raw_body, None

    text = (raw_body or "").strip()
    if not text:
        return None, {"error": "push_body is required"}

    # Try JSON first
    try:
        return json.loads(text), None
    except json.JSONDecodeError:
        pass

    # Try x-www-form-urlencoded: sign=...&param=...
    try:
        qs = urllib.parse.parse_qs(text, keep_blank_values=True)
        param_raw = (qs.get("param") or [""])[0]
        sign_raw  = (qs.get("sign")  or [""])[0]
        if not param_raw:
            return None, {"error": "unsupported_body_format", "raw": text[:200]}

        param_obj = json.loads(param_raw)
        # Put sign at top-level for our verifier
        if sign_raw:
            param_obj["sign"] = sign_raw
        # Keep original param string for signature verification
        param_obj["_param_raw"] = param_raw
        return param_obj, None
    except Exception as e:
        return None, {"error": f"unsupported_body_format: {e}", "raw": text[:200]}


def cmd_handle_push(args: dict) -> dict:
    """Process a push payload from Kuaidi100 webhook."""
    raw_body = args.get("push_body") or ""

    push_data, parse_err = _parse_push_body(raw_body)
    if parse_err:
        return parse_err

    ok, reason = _verify_push_signature(push_data)

    # Fail-closed option: require signature to be present and valid.
    # We treat "no_signature_in_payload" as failure in strict mode.
    if KUAIDI100_SIGNATURE_MODE == "strict" and (not ok or reason.startswith("no_signature")):
        return {
            "error": "signature_invalid",
            "signature_verified": bool(ok),
            "signature_reason": reason,
        }

    parsed = parse_push_payload(push_data)
    if not parsed:
        return {"error": "could_not_parse_push", "raw": push_data}

    # Attach signature verification status
    parsed["signature_verified"] = bool(ok)
    parsed["signature_reason"]   = reason

    number = parsed["number"]
    state  = load_state()

    # Preserve user note if we already have an entry
    existing = state["packages"].get(number, {})
    parsed["note"]       = existing.get("note", "")
    parsed["subscribed"] = existing.get("subscribed", True)
    state["packages"][number] = parsed
    save_state(state)

    # Auto sync calendar if today delivery
    cal_result = None
    if parsed["today_delivery"] and not parsed["is_completed"]:
        cal_result = _do_sync_calendar(state)

    return {
        "status":      "ok",
        "number":      number,
        "state_label": parsed["state_label"],
        "today_delivery": parsed["today_delivery"],
        "calendar_sync":  cal_result,
    }


def _do_sync_calendar(state: dict) -> dict | None:
    today_str  = _now_local().strftime("%Y-%m-%d")
    today_pkgs = [p for p in state["packages"].values()
                  if p.get("today_delivery") and not p.get("is_completed")]
    if not today_pkgs:
        return {"status": "nothing_to_sync"}
    if not all([GCAL_CLIENT_ID, GCAL_CLIENT_SECRET, GCAL_REFRESH_TOKEN]):
        return {"status": "error", "error": "missing_google_calendar_credentials"}
    try:
        token  = gcal_refresh_access_token()
        result = gcal_upsert_event(token, today_str, today_pkgs)
        return {"status": "ok", "calendar_result": result, "synced_count": len(today_pkgs)}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def cmd_sync_calendar(_args: dict) -> dict:
    state = load_state()
    result = _do_sync_calendar(state)
    return result or {"status": "nothing_to_sync"}


def cmd_list_packages(_args: dict) -> dict:
    state  = load_state()
    pkgs   = list(state["packages"].values())
    today  = [p for p in pkgs if p.get("today_delivery") and not p.get("is_completed")]
    active = [p for p in pkgs if not p.get("is_completed")]
    return {
        "total":          len(pkgs),
        "in_transit":     len(active),
        "today_delivery": len(today),
        "packages":       pkgs,
    }


def cmd_remove_tracking(args: dict) -> dict:
    number = (args.get("number") or "").strip()
    if not number:
        return {"error": "number is required"}
    state = load_state()
    if number not in state["packages"]:
        return {"status": "not_found", "number": number}
    del state["packages"][number]
    save_state(state)
    return {"status": "removed", "number": number}


# ── Entry point ────────────────────────────────────────────────────────────────

COMMANDS: dict[str, Any] = {
    "add_tracking":    cmd_add_tracking,
    "handle_push":     cmd_handle_push,
    "sync_calendar":   cmd_sync_calendar,
    "list_packages":   cmd_list_packages,
    "remove_tracking": cmd_remove_tracking,
}


def main() -> int:
    if len(sys.argv) < 3:
        print(json.dumps({"error": "usage: tracker_core.py <command> <json_args>"}))
        return 1

    command = sys.argv[1]
    try:
        args = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"invalid json args: {e}"}))
        return 1

    handler = COMMANDS.get(command)
    if not handler:
        print(json.dumps({"error": f"unknown command: {command}",
                          "available": list(COMMANDS)}))
        return 1

    result = handler(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
