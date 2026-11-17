#!/usr/bin/env python3
"""Helper for the AO Job Heartbeat API at https://beat.austinoaksapi.com.

What it does, and what it never does:
  * Python standard library only. Nothing to install.
  * Reads exactly one environment variable, JOB_HEARTBEAT_API_KEY, and never
    prints, logs or writes it. The key is sent only as an Authorization
    header to the one host below. ping, fail and snippet do not use it.
  * Talks to one host only (BASE_URL). No flag or variable changes the host.
    System proxy settings are ignored. HTTP redirects are refused.
  * Writes no files, starts no other programs, and never edits a crontab
    or any other schedule. `snippet` only PRINTS a line for the human.
  * Has no signup, billing, upgrade or payment command.

Commands (all output is JSON on stdout, except `snippet`, which is text):
  account                         plan, email_verified, checks in use / allowed
  list                            the account's checks
  get ID                          one check
  create --name N --period P [--grace G]
                                  one new check; refused if the plan is full
                                  or a check with that name already exists
  delete ID --confirm             cancel a check (only after the human said yes)
  ping ID                         sign of life: run ONLY after the task succeeded
  fail ID                         the task knows it failed: mark it failed now
  events ID [--limit N]           recent late/recovered events + delivery results
  snippet ID                      print (not run) ONE line for the human's own job

Exit codes: 0 ok, 2 bad input, 3 refused (plan full, duplicate name, 402),
4 API or network error, a timeout, or an answer the helper cannot read (state
unknown), 5 API key missing, malformed or not accepted, 6 not counted (a ping
or fail the service answered with dropped=true).
A ping or fail counts only when the service answers HTTP 200 with ok exactly
true and dropped exactly false. Nothing is ever retried or sent twice.
A field the service did not send is shown as null (unknown), never guessed.
"""
import argparse
import http.client
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request

BASE_URL = "https://beat.austinoaksapi.com"   # pinned; there is no override
KEY_ENV = "JOB_HEARTBEAT_API_KEY"
KEY_PREFIX = "ak_"
USER_AGENT = "job-heartbeat-skill/1.0.0"
TIMEOUT_S = 15
MAX_RESPONSE_BYTES = 1024 * 1024

MIN_PERIOD_S = 60
MAX_SECONDS = 2592000          # 30 days: the API's limit for period and grace
MAX_NAME_LEN = 120

KEY_LIKE_RE = re.compile(r"ak_[0-9A-Za-z]{20,}")
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
DURATION_RE = re.compile(r"^(\d+)\s*([smhd]?)$")
UNIT_SECONDS = {"": 1, "s": 1, "m": 60, "h": 3600, "d": 86400}

EXIT_OK, EXIT_USAGE, EXIT_REFUSED, EXIT_API, EXIT_NO_KEY, EXIT_NOT_COUNTED = 0, 2, 3, 4, 5, 6

EMAIL_NOTE = ("Alert email goes only to the account's own confirmed address. An email "
              "delivery with ok=true means the service's mail step reported success; it "
              "does not show that the message reached the Inbox. Alerts to Microsoft, "
              "Outlook and Hotmail addresses have been landing in Junk. Never tell the "
              "human an alert reached them.")


class ToolError(Exception):
    exit_code = EXIT_API
    label = "ERROR"


class UsageError(ToolError):
    exit_code = EXIT_USAGE


class Refused(ToolError):
    exit_code = EXIT_REFUSED
    label = "REFUSED"


class NoKey(ToolError):
    exit_code = EXIT_NO_KEY


class NotCounted(ToolError):
    exit_code = EXIT_NOT_COUNTED
    label = "NOT COUNTED"


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Returning None makes urllib raise HTTPError for any 3xx answer, so a
    redirect can never carry a request (or the key) to another place."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}), _NoRedirect)


# ---- small helpers -----------------------------------------------------------
def _iso(ts):
    if ts is None:
        return None
    try:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(float(ts)))
    except (TypeError, ValueError, OverflowError):
        return None


def _check_id(value):
    value = (value or "").strip().lower()
    if not UUID_RE.match(value):
        raise UsageError("check id must be a UUID like 0b8f5c1e-1111-4222-8333-944455556666")
    return value


def _seconds(value, what, low):
    match = DURATION_RE.match(str(value).strip().lower())
    if not match:
        raise UsageError("%s must be a number of seconds, or a number with s, m, h or d "
                         "(for example 300, 15m, 1h, 1d)" % what)
    seconds = int(match.group(1)) * UNIT_SECONDS[match.group(2)]
    if seconds < low or seconds > MAX_SECONDS:
        raise UsageError("%s must be between %d seconds and 30 days" % (what, low))
    return seconds


def default_grace(period_s):
    """The same defaults the service's own sign-up page uses."""
    if period_s <= 300:
        return 60
    if period_s <= 900:
        return 120
    if period_s <= 3600:
        return 300
    if period_s <= 21600:
        return 900
    return 1800


def _load_key():
    key = os.environ.get(KEY_ENV, "").strip()
    if not key:
        raise NoKey("%s is not set. Ask the human to store their API key in that environment "
                    "variable themselves. Never ask them to paste the key into chat." % KEY_ENV)
    if not key.startswith(KEY_PREFIX) or any(c.isspace() for c in key) \
            or not key.isprintable() or len(key) > 200:
        raise NoKey("%s does not look like an AO Job Heartbeat key (they start with %s). "
                    "Nothing was sent. The value is not shown." % (KEY_ENV, KEY_PREFIX))
    return key


def _ping_url(check_id):
    return "%s/ping/%s" % (BASE_URL, check_id)


UNKNOWN = "The state is unknown; do not guess."
TIMED_OUT = ("%s did not answer, or stopped answering, for %d seconds. The request may or may "
             "not have reached the service, so whether it counted is unknown. It was not sent "
             "again.")
NO_RESEND = "Do not send it again automatically or in a loop; tell the human."


def _no_duplicate_keys(pairs):
    """object_pairs_hook: an object that repeats a key is not one clear answer."""
    obj = dict(pairs)
    if len(obj) != len(pairs):
        raise ValueError("duplicate key in a JSON object")
    return obj


def _request(method, path, key=None, body=None):
    """One HTTPS call to BASE_URL. Returns (status, parsed JSON object).

    A success answer (2xx, except an empty 204) must be one complete JSON
    object. Anything else -- empty, cut short, too large, not JSON, a JSON
    list -- raises ToolError (exit 4, state unknown) instead of being read
    as an empty answer. Error answers (4xx/5xx) may have any body."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE_URL + path, data=data, method=method, headers=headers)
    if key is not None:
        req.add_unredirected_header("Authorization", "Bearer " + key)
    declared = None
    try:
        try:
            with _OPENER.open(req, timeout=TIMEOUT_S) as resp:
                status, raw = resp.status, resp.read(MAX_RESPONSE_BYTES + 1)
                declared = resp.getheader("Content-Length")
        except urllib.error.HTTPError as err:
            status = err.code
            try:
                raw = err.read(MAX_RESPONSE_BYTES + 1)
            finally:
                err.close()
    except urllib.error.URLError as err:
        if isinstance(getattr(err, "reason", None), socket.timeout):
            raise ToolError(TIMED_OUT % (BASE_URL, TIMEOUT_S))
        raise ToolError("could not reach %s (%s). Nothing is known about the check's state."
                        % (BASE_URL, getattr(err, "reason", err)))
    except socket.timeout:
        raise ToolError(TIMED_OUT % (BASE_URL, TIMEOUT_S))
    except OSError as err:
        raise ToolError("network error talking to %s (%s). Nothing is known about the "
                        "check's state." % (BASE_URL, err.__class__.__name__))
    except http.client.HTTPException as err:
        raise ToolError("the answer from %s was not valid HTTP (%s). %s"
                        % (BASE_URL, err.__class__.__name__, UNKNOWN))
    if 300 <= status < 400:
        raise ToolError("the service answered with a redirect (HTTP %d); it was not followed"
                        % status)
    parsed = None
    if raw and len(raw) <= MAX_RESPONSE_BYTES:
        try:
            parsed = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys)
        except (ValueError, UnicodeDecodeError, RecursionError):
            parsed = None
    if 200 <= status < 300:
        if status == 204:
            return status, {}
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ToolError("the service's answer (HTTP %d) was larger than %d bytes and was "
                            "not read. %s" % (status, MAX_RESPONSE_BYTES, UNKNOWN))
        # http.client can hand back a body that stopped early without raising,
        # and the part that arrived may still parse as JSON. Never read it.
        if declared is not None and declared.strip() != str(len(raw)):
            raise ToolError("the service's answer (HTTP %d) did not match its declared length "
                            "(Content-Length: %r, %d bytes arrived). %s"
                            % (status, declared, len(raw), UNKNOWN))
        if not isinstance(parsed, dict):
            raise ToolError("the service answered HTTP %d, but the answer was not one complete, "
                            "clear JSON object (empty, cut short, a repeated key or a different "
                            "shape). %s" % (status, UNKNOWN))
        return status, parsed
    return status, parsed if isinstance(parsed, dict) else {}


def _known_bool(value):
    """True or False only when the service said so; None (unknown) otherwise."""
    return value if isinstance(value, bool) else None


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _fail_for(status, body, what):
    """Turn a non-success answer into a clear error. Only reason_code and
    message from the service are shown."""
    reason = body.get("reason_code")
    message = body.get("message")
    detail = " ".join(str(x) for x in (reason, message) if x) or "no details"
    if 200 <= status < 300:
        return ToolError("%s: unexpected success answer (HTTP %d), so the outcome is unknown. "
                         "Check the current state (list or get) before trying again."
                         % (what, status))
    if status == 401:
        return NoKey("the API key was not accepted (HTTP 401). Ask the human to check %s. "
                     "Do not ask them to paste the key." % KEY_ENV)
    if status == 402:
        return Refused("%s refused by the plan (HTTP 402, %s). This skill never upgrades or "
                       "pays. Tell the human; they decide." % (what, detail))
    if status == 404:
        return ToolError("%s: no such check on this account (HTTP 404)" % what)
    if status == 429:
        return ToolError("%s: rate limited (HTTP 429). Wait and try once more later; "
                         "do not loop." % what)
    if status == 400:
        return UsageError("%s: the service rejected the input (%s)" % (what, detail))
    return ToolError("%s failed (HTTP %d, %s)" % (what, status, detail))


def _beat_fail_for(status, body, what, effect):
    """Non-200 answers to ping and fail, which send no key and no body. A 429 is
    refused before the service reads the call, so it did not count (exit 6). A
    404 means no such check. Anything else, including a 5xx that may arrive after
    the call counted, is unknown (exit 4). Nothing is ever sent again."""
    if status == 429:
        return NotCounted("%s was refused as rate limited (HTTP 429), so it did not count: %s. "
                          "It was not sent again. %s" % (what, effect, NO_RESEND))
    if status == 404:
        return ToolError("%s: no such check (HTTP 404), so it did not count. It was not sent "
                         "again. %s" % (what, NO_RESEND))
    reason = body.get("reason_code")
    detail = str(reason) if isinstance(reason, str) and reason else "no details"
    return ToolError("%s: the service answered HTTP %d (%s). Whether it counted is unknown. It "
                     "was not sent again. %s" % (what, status, detail, NO_RESEND))


def _summary(check):
    return {
        "id": check.get("id"),
        "name": check.get("name"),
        "status": check.get("status"),
        "period_s": check.get("period_s"),
        "grace_s": check.get("grace_s"),
        "last_ping_at": _iso(check.get("last_ping_at")),
        "due_at": _iso(check.get("due_at")),
        "miss_count": check.get("miss_count"),
    }


# ---- commands ----------------------------------------------------------------
def _account(key):
    status, body = _request("GET", "/v1/account", key=key)
    if status != 200:
        raise _fail_for(status, body, "account")
    usage = body.get("usage") if isinstance(body.get("usage"), dict) else {}
    limits = body.get("limits") if isinstance(body.get("limits"), dict) else {}
    limit = usage.get("checks_limit", limits.get("max_checks"))
    # The account's email address is in the answer; it is left out on purpose.
    # A missing field stays None (unknown); it is never turned into False or 0.
    return {
        "plan": body.get("plan") if isinstance(body.get("plan"), str) else None,
        "email_verified": _known_bool(body.get("email_verified")),
        "checks_active": (usage.get("checks_active")
                          if _is_int(usage.get("checks_active")) else None),
        "checks_limit": limit if _is_int(limit) else None,
        "webhooks_allowed": _known_bool(limits.get("webhooks")),
        "alert_emails_per_day": (limits.get("emails_per_day")
                                 if _is_int(limits.get("emails_per_day")) else None),
    }


def cmd_account(args):
    out = _account(_load_key())
    if out["email_verified"] is True:
        out["note"] = "Alert email is switched on. " + EMAIL_NOTE
    elif out["email_verified"] is False:
        out["note"] = ("Alert email is OFF until the human opens the confirmation email from "
                       "Job Heartbeat and presses 'Confirm my email' (check Junk too).")
    else:
        out["note"] = ("The service's answer did not say whether the email address is "
                       "confirmed, so whether alert email is on is unknown. Do not guess.")
    unknown = sorted(k for k, v in out.items() if v is None)
    if unknown:
        out["unknown_fields"] = unknown
    return out


def _list_checks(key):
    status, body = _request("GET", "/v1/checks", key=key)
    if status != 200:
        raise _fail_for(status, body, "list")
    checks = body.get("checks")
    if not isinstance(checks, list):
        raise ToolError("list: the service's answer has no list of checks. " + UNKNOWN)
    return [c for c in checks if isinstance(c, dict)]


def cmd_list(args):
    checks = _list_checks(_load_key())
    return {"count": len(checks), "checks": [_summary(c) for c in checks]}


def cmd_get(args):
    check_id = _check_id(args.id)
    status, body = _request("GET", "/v1/checks/" + check_id, key=_load_key())
    if status != 200:
        raise _fail_for(status, body, "get")
    if not isinstance(body.get("id"), str):
        raise ToolError("get: the service's answer does not describe a check. " + UNKNOWN)
    return _summary(body)


def cmd_create(args):
    name = (args.name or "").strip()
    if not name or len(name) > MAX_NAME_LEN:
        raise UsageError("--name must be 1 to %d characters" % MAX_NAME_LEN)
    if not name.isprintable():
        raise UsageError("--name must be plain printable text")
    period_s = _seconds(args.period, "--period", MIN_PERIOD_S)
    grace_s = default_grace(period_s) if args.grace is None else _seconds(args.grace, "--grace", 0)
    key = _load_key()
    if key in name or KEY_LIKE_RE.search(name):
        raise UsageError("--name must not contain an API key. Nothing was sent.")

    account = _account(key)
    used, limit = account["checks_active"], account["checks_limit"]
    if not _is_int(used) or not _is_int(limit):
        raise ToolError("could not read how many checks the plan allows; not creating one")
    if used >= limit:
        raise Refused("the %s plan allows %d checks and %d are in use. No check was created. "
                      "Tell the human. Do not delete a check to make room unless they say so, "
                      "and never upgrade or pay for them." % (account["plan"], limit, used))
    for check in _list_checks(key):
        if str(check.get("name", "")).strip().lower() == name.lower():
            raise Refused("a check named %r already exists (id %s). Reuse it; one check per "
                          "recurring task." % (check.get("name"), check.get("id")))

    status, body = _request("POST", "/v1/checks", key=key,
                            body={"name": name, "period_s": period_s, "grace_s": grace_s})
    if status != 201:
        raise _fail_for(status, body, "create")
    raw_id = body.get("id")
    if not isinstance(raw_id, str) or not UUID_RE.match(raw_id.strip().lower()):
        raise ToolError("create: the service answered HTTP 201 but gave no usable check id, so "
                        "whether a check was created is unknown. Run list before trying again; "
                        "do not create another one blindly.")
    check_id = raw_id.strip().lower()
    out = _summary(body)
    out["ping_url"] = _ping_url(check_id)
    out["fail_url"] = _ping_url(check_id) + "/fail"
    if body.get("ping_url") not in (None, out["ping_url"]):
        out["warning"] = "the service returned a different ping_url; use the one shown here"
    due = body.get("due_at")
    if isinstance(due, (int, float)):
        out["first_ping_due_by"] = _iso(due + grace_s)
    out["checks_in_use_after"] = "%d of %d" % (used + 1, limit)
    out["next"] = ("The check is armed now. Add the ping as the LAST step of the task, after "
                   "its own success checks. If no ping arrives by first_ping_due_by, the "
                   "service records a late event; run events ID to see what was delivered. "
                   "Anyone who has the ping URL can ping this check or mark it failed, which "
                   "sends alert email and uses up the account's daily email allowance, so keep "
                   "it out of public places.")
    return out


def cmd_delete(args):
    check_id = _check_id(args.id)
    if not args.confirm:
        raise UsageError("delete needs --confirm, and only after the human said yes to "
                         "deleting this check")
    status, body = _request("DELETE", "/v1/checks/" + check_id, key=_load_key())
    if status != 204:
        raise _fail_for(status, body, "delete")
    return {"deleted": check_id,
            "note": ("The check is cancelled; its 30-day event log stays readable. Remove the "
                     "ping step from the task too.")}


def _require_counted(body, what, effect):
    """The only answer that counts: HTTP 200 (checked by the caller) whose JSON
    object has ok exactly true and dropped exactly false. A missing, non-boolean
    or unexpected field is 'unknown' (exit 4); dropped=true is 'not counted'
    (exit 6). Neither is retried."""
    if body.get("ok") is not True or not isinstance(body.get("dropped"), bool):
        raise ToolError("%s: the service's answer did not say clearly that the call counted "
                        "(it needs ok=true and dropped=false). Whether it counted is unknown. "
                        "It was not sent again. %s" % (what, NO_RESEND))
    if body.get("dropped"):
        raise NotCounted("%s was dropped by the 10-a-minute limit for this check, so it did not "
                         "count: %s. It was not sent again. %s More than 10 calls a minute "
                         "usually means duplicate pings or a shared URL." % (what, effect, NO_RESEND))


PING_EFFECT = "the deadline did not move"
FAIL_EFFECT = "the check was not marked failed and no late event was recorded"


def _text_or_none(value):
    return value if isinstance(value, str) else None


def cmd_ping(args):
    check_id = _check_id(args.id)
    status, body = _request("GET", "/ping/" + check_id)
    if status != 200:
        raise _beat_fail_for(status, body, "ping", PING_EFFECT)
    _require_counted(body, "ping", PING_EFFECT)
    return {"check_id": check_id, "ok": True, "dropped": False, "counted": True,
            "status": _text_or_none(body.get("status")),
            "recovered": _known_bool(body.get("recovered"))}


FAIL_DELIVERY_NOTE = (
    "This answer does not show whether any alert was sent. Run events ID to see what was "
    "delivered. No email goes out when the address is not confirmed (the email entry shows "
    "skipped=email_unverified) or when the daily email cap is used up (the event has no email "
    "entry at all). ")


def cmd_fail(args):
    check_id = _check_id(args.id)
    status, body = _request("POST", "/ping/" + check_id + "/fail")
    if status != 200:
        raise _beat_fail_for(status, body, "fail", FAIL_EFFECT)
    _require_counted(body, "fail", FAIL_EFFECT)
    event = body.get("event", ())
    if event is not None and not isinstance(event, str):
        raise ToolError("fail: the service's answer does not say whether a late event was "
                        "recorded. " + UNKNOWN)
    recorded = bool(event)
    out = {"check_id": check_id, "status": _text_or_none(body.get("status")), "dropped": False,
           "counted": True, "late_event_recorded": recorded}
    if recorded:
        out["note"] = ("The service recorded a check.late event. " + FAIL_DELIVERY_NOTE
                       + EMAIL_NOTE)
    else:
        out["note"] = ("The check is now marked failed. It was already late or failed, so "
                       "no new late event was recorded and no new alert was started.")
    return out


DELIVERY_FIELDS = ("kind", "ok", "attempts", "skipped", "pending", "status", "error")
EVENT_DATA_FIELDS = ("reason", "late_for_s", "miss_count")
EVENTS_NOTE = (
    "Reading delivery: an email entry with skipped=email_unverified means no email was sent "
    "because the address is not confirmed. An event with no email entry at all means no email "
    "was sent for it, usually because the daily email cap (alert_emails_per_day in account) "
    "was used up. pending=true means delivery has not finished; look again later. A webhook "
    "delivery with ok=true means the webhook answered with a 2xx status. ")


def cmd_events(args):
    check_id = _check_id(args.id)
    status, body = _request("GET", "/v1/checks/%s/events" % check_id, key=_load_key())
    if status != 200:
        raise _fail_for(status, body, "events")
    listed = body.get("events")
    if not isinstance(listed, list):
        raise ToolError("events: the service's answer has no list of events. " + UNKNOWN)
    rows = [e for e in listed if isinstance(e, dict)][: args.limit]
    events = []
    for row in rows:
        delivery = []
        listed_delivery = row.get("delivery")
        for item in listed_delivery if isinstance(listed_delivery, list) else []:
            if isinstance(item, dict):
                delivery.append({k: item[k] for k in DELIVERY_FIELDS if k in item})
        entry = {"type": row.get("type"), "at": _iso(row.get("at")), "delivery": delivery}
        envelope = row.get("envelope")
        event = envelope.get("event") if isinstance(envelope, dict) else None
        data = event.get("data") if isinstance(event, dict) else None
        if isinstance(data, dict):
            entry.update({k: data[k] for k in EVENT_DATA_FIELDS if k in data})
        events.append(entry)
    return {"check_id": check_id, "events": events, "note": EVENTS_NOTE + EMAIL_NOTE}


# Run by the printed line on the job's machine (python3 -I: no local files or
# PYTHON* variables). It reads curl's raw output from a pipe, byte for byte (a
# shell $(...) would drop NUL bytes), then a last line holding curl's exit
# status. Exit 75 if curl failed. Otherwise exit 0 only for HTTP 200 whose body
# (split from the headers at the first blank line and never changed) is strict
# UTF-8 JSON: one object with ok exactly true and dropped exactly false, where
# no object at any depth repeats a key (a repeat stops the check). Anything
# else exits non-zero.
SNIPPET_CHECK = ('import sys,json,re;x,_,c=sys.stdin.buffer.read()[:-1].rpartition(b"\\n");'
                 'c==b"0"or sys.exit(75);h,b=re.split(rb"\\r?\\n\\r?\\n",x,maxsplit=1);'
                 'd=json.loads(b.decode(),object_pairs_hook=lambda p:dict(p)'
                 'if len(dict(p))==len(p)else sys.exit(1));'
                 'sys.exit(h.split()[1:2]!=[b"200"]or type(d)is not dict'
                 ' or d.get("ok")is not True or d.get("dropped")is not False)')

# macOS cron (cron-52) reads a crontab command into a 1000-byte buffer and keeps
# at most 999 bytes, dropping the rest without warning (VERIFIED 2026-10-04:
# the 0x3e8 size in /usr/sbin/cron on this Mac). It counts bytes, not
# characters: a non-ASCII character takes 2 to 4 bytes in UTF-8. Other crons
# may allow more.
CRON_MAX_BYTES = 999
JOB = "your-job-command"


def cmd_snippet(args):
    url = _ping_url(_check_id(args.id))
    # The braces make a line that cron cut short a syntax error, so nothing runs
    # instead of half of it. The job runs once, in its own subshell, so an exit,
    # exec, cd or set -e inside it cannot skip the report. curl -q reads no
    # config file (a ~/.curlrc could add retries). --suppress-connect-headers
    # keeps a proxy's CONNECT answer out of the -i output; curl's manual says it
    # was "Added in 7.54.0" (VERIFIED 2026-10-04, man curl for curl 8.7.1).
    # curl's output goes through a pipe, never through $(...), so the check sees
    # the answer's exact bytes; curl's own exit status follows on a last line.
    # The last step exits with the job's own code if it failed, else with r.
    line = " ".join([
        "{ ( %s ); rc=$?; u=%s; [ $rc -ne 0 ] && u=$u/fail;" % (JOB, url),
        '{ curl -q -sS -m 10 -i --suppress-connect-headers "$u"; c=$?; echo; echo $c; } |',
        "python3 -I -c '%s' 2>/dev/null; r=$?; if [ $r -eq 75 ]; then" % SNIPPET_CHECK,
        'm="NOT SENT or UNKNOWN (see curl error above)"; elif [ $r -ne 0 ]; then r=76;',
        'm="NOT CONFIRMED (dropped, error, unreadable or no python3)"; fi; [ $r -ne 0 ] &&',
        'echo "job-heartbeat: job exit $rc; heartbeat $m" >&2; (exit $((rc?rc:r))); }',
    ])
    budget = CRON_MAX_BYTES - (len(line.encode("utf-8")) - len(JOB))
    return "\n".join([
        "# For the human to add to their own job. This skill does not edit any schedule.",
        "# No API key is needed or included. Replace %s with the job's command." % JOB,
        "# ONE line, used once, in place of the job's current command. It runs the job once.",
        "# Job succeeded: it pings, and exits 0 only if the service answers HTTP 200 with",
        "# ok=true and dropped=false. Job failed: it reports the failure at once and exits",
        "# with the job's own exit code. Nothing is retried or sent twice.",
        "# Exit 75: the job succeeded, but curl failed (timeout, network error, or curl",
        "# missing or too old), so the ping may not have counted. Exit 76: the job succeeded,",
        "# but the ping was not confirmed as counted. If a ping did not count, the check goes",
        "# late at its deadline and the service records a late event. A job that itself",
        "# exits 75 or 76 looks the same; the job-heartbeat message on stderr tells them apart.",
        "# Use ONE command or a script path: no pipe (only the pipe's last command counts),",
        "# no trailing &, and no # comment (a comment stops the whole line from running).",
        "# Your command can be at most %d bytes: macOS cron keeps only %d bytes of a"
        % (budget, CRON_MAX_BYTES),
        "# command, and a line cut short does not run at all. A plain ASCII character is",
        "# 1 byte; others (such as an accented letter) take 2 to 4 bytes. If it is longer,",
        "# put it in a script and use the script's path. In a crontab, escape any % as \\%.",
        "# Needs sh, curl 7.54 or newer (curl's manual), and python3 where the job runs.",
        line,
    ])


# ---- entry point -------------------------------------------------------------
def build_parser():
    parser = argparse.ArgumentParser(
        prog="jobhb.py",
        description="AO Job Heartbeat helper (host pinned to %s)." % BASE_URL)
    sub = parser.add_subparsers(dest="command")
    sub.required = True
    sub.add_parser("account", help="plan, email_verified, checks in use / allowed")
    sub.add_parser("list", help="list checks")
    p = sub.add_parser("get", help="show one check")
    p.add_argument("id")
    p = sub.add_parser("create", help="create one check")
    p.add_argument("--name", required=True, help="1-120 characters; no secrets or personal data")
    p.add_argument("--period", required=True, help="how often the task runs: 300, 15m, 1h, 1d")
    p.add_argument("--grace", default=None, help="how late is still fine (default: by period)")
    p = sub.add_parser("delete", help="cancel a check (needs --confirm)")
    p.add_argument("id")
    p.add_argument("--confirm", action="store_true", help="the human said yes")
    p = sub.add_parser("ping", help="sign of life, only after the task succeeded")
    p.add_argument("id")
    p = sub.add_parser("fail", help="mark the check failed now")
    p.add_argument("id")
    p = sub.add_parser("events", help="recent events and delivery results")
    p.add_argument("id")
    p.add_argument("--limit", type=int, default=10)
    p = sub.add_parser("snippet", help="print a ping line for the human's own job")
    p.add_argument("id")
    return parser


COMMANDS = {"account": cmd_account, "list": cmd_list, "get": cmd_get, "create": cmd_create,
            "delete": cmd_delete, "ping": cmd_ping, "fail": cmd_fail, "events": cmd_events,
            "snippet": cmd_snippet}


def main(argv=None, stdout=None, stderr=None):
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    args = build_parser().parse_args(argv)
    if getattr(args, "limit", None) is not None:
        args.limit = max(1, min(args.limit, 100))
    try:
        result = COMMANDS[args.command](args)
    except ToolError as err:
        stderr.write("%s: %s\n" % (err.label, err))
        return err.exit_code
    if isinstance(result, str):
        stdout.write(result + "\n")
    else:
        stdout.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
