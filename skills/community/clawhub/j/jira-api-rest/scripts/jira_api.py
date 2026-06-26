#!/usr/bin/env python3
"""Jira Cloud REST API v3 helper (no external deps).

Goal
----
Provide API coverage for what `jira-cli` can do *and* what it misses (notably edit/delete worklogs).

Auth + config
-------------
- Reads Jira base URL + login + timezone from: ~/.config/.jira/.config.yml
- Reads API token from: ~/.netrc  (machine <hostname>, login <email>, password <api_token>)

Safety
------
- Never prints tokens.
- For destructive operations (delete/edit), you should still get human confirmation at the chat level.

Output
------
- Prints JSON to stdout for all commands.

Commands
--------
Generic:
  - request METHOD /path [--query k=v ...] [--data-json '{...}' | --data-file file.json]

Identity / discovery:
  - me
  - project-list [--max 50]

Search:
  - search-jql "<JQL>" [--fields key,summary,status] [--max 50]

Issues:
  - issue-get ISSUE-KEY [--fields key,summary,status,assignee] [--expand ...]
  - issue-create --project DES --type Task --summary "..." [--description "..."] [--fields-json '{...}']
  - issue-edit ISSUE-KEY [--fields-json '{"fields":{...}}']
  - issue-comment-add ISSUE-KEY --comment "..."
  - issue-transitions ISSUE-KEY
  - issue-transition ISSUE-KEY --id <transitionId>
  - user-search "query" [--max 20]
  - issue-assign ISSUE-KEY --accountId <id>
  - issue-link --type "Relates" --inward DES-1 --outward DES-2

Sprints (Agile API):
  - board-list [--max 50]
  - board-get BOARD_ID
  - sprint-list --board BOARD_ID [--state future|active|closed] [--max 50]
  - sprint-get SPRINT_ID
  - sprint-issues SPRINT_ID [--jql "..."] [--fields key,summary,status] [--max 50]
  - sprint-create --board BOARD_ID --name "..." [--start "YYYY-MM-DD"] [--end "YYYY-MM-DD"]
  - sprint-update SPRINT_ID [--name "..."] [--state future|active|closed] [--start "YYYY-MM-DD"] [--end "YYYY-MM-DD"]

Worklogs:
  - worklog-add ISSUE-KEY "3h 30m" --started "YYYY-MM-DD HH:MM:SS" [--timezone Europe/Madrid] [--comment "..."]
  - worklog-list ISSUE-KEY [--from YYYY-MM-DD] [--to YYYY-MM-DD]
  - worklog-update ISSUE-KEY WORKLOG_ID [--started ...] [--timezone ...] [--timeSpent "..."] [--comment "..."]
                  [--adjustEstimate auto|new|leave] [--newEstimate 0m]
  - worklog-delete ISSUE-KEY WORKLOG_ID [--adjustEstimate auto|new|leave] [--newEstimate 0m]

Notes
-----
- JQL search uses the new endpoint: GET /rest/api/3/search/jql (Atlassian CHANGE-2046).
- Comments for worklog-update use ADF (Atlassian Document Format) minimal structure.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import netrc
import os
import re
import sys
import urllib.parse
import urllib.request

DEFAULT_JIRA_CONFIG = os.path.expanduser("~/.config/.jira/.config.yml")
DEFAULT_NETRC = os.path.expanduser("~/.netrc")


def _read_jira_config(path: str = DEFAULT_JIRA_CONFIG) -> dict:
    server = None
    login = None
    timezone = None
    if not os.path.exists(path):
        raise FileNotFoundError(f"Jira config not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("server:"):
                server = line.split(":", 1)[1].strip()
            elif line.startswith("login:"):
                login = line.split(":", 1)[1].strip()
            elif line.startswith("timezone:"):
                timezone = line.split(":", 1)[1].strip()
    if not server or not login:
        raise RuntimeError(f"Could not read server/login from {path}")
    return {"server": server.rstrip("/"), "login": login, "timezone": timezone or "UTC"}


def _netrc_auth_for_host(hostname: str, netrc_path: str = DEFAULT_NETRC) -> tuple[str, str]:
    if not os.path.exists(netrc_path):
        raise FileNotFoundError(f".netrc not found: {netrc_path}")
    n = netrc.netrc(netrc_path)
    auth = n.authenticators(hostname)
    if not auth:
        raise RuntimeError(f"No netrc entry for host: {hostname}")
    login, _account, password = auth
    if not login or not password:
        raise RuntimeError(f"Invalid netrc entry for host: {hostname}")
    return login, password


def _basic_auth_header(user: str, token: str) -> str:
    raw = f"{user}:{token}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def _http(method: str, url: str, headers: dict, body: dict | None = None) -> tuple[int, dict | None, str]:
    data = None
    headers = dict(headers)
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers.setdefault("Content-Type", "application/json")

    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            text = resp.read().decode("utf-8", errors="replace")
            if not text:
                return status, None, ""
            try:
                return status, json.loads(text), text
            except json.JSONDecodeError:
                return status, None, text
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {err_body[:4000]}") from None


def _parse_date(s: str) -> dt.date:
    return dt.datetime.strptime(s, "%Y-%m-%d").date()


def _started_in_jira_format(started: str, tz: str) -> str:
    # Accept Jira format already
    if re.search(r"T\d\d:\d\d:\d\d\.\d\d\d[+-]\d\d\d\d$", started):
        return started

    # Accept 'YYYY-MM-DD HH:MM:SS'
    naive = dt.datetime.strptime(started, "%Y-%m-%d %H:%M:%S")

    # Use zoneinfo for offset if available.
    try:
        from zoneinfo import ZoneInfo

        z = ZoneInfo(tz)
        local = naive.replace(tzinfo=z)
        offset = local.utcoffset() or dt.timedelta(0)
        sign = "+" if offset >= dt.timedelta(0) else "-"
        total_min = int(abs(offset.total_seconds()) // 60)
        hh, mm = divmod(total_min, 60)
        return naive.strftime("%Y-%m-%dT%H:%M:%S.000") + f"{sign}{hh:02d}{mm:02d}"
    except Exception:
        # Fallback: assume +0000
        return naive.strftime("%Y-%m-%dT%H:%M:%S.000+0000")


def _adf_text(text: str) -> dict:
    return {
        "type": "doc",
        "version": 1,
        "content": [{"type": "paragraph", "content": [{"type": "text", "text": text}]}],
    }


def _print(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


# ---------------- Generic ----------------

def cmd_request(args, cfg):
    server = cfg["server"]
    url = urllib.parse.urljoin(server + "/", args.path.lstrip("/"))
    if args.query:
        q = urllib.parse.urlencode(args.query)
        url += ("&" if "?" in url else "?") + q

    body = None
    if args.data_json:
        body = json.loads(args.data_json)
    elif args.data_file:
        with open(args.data_file, "r", encoding="utf-8") as f:
            body = json.load(f)

    status, j, raw = _http(args.method, url, args.headers, body)
    _print({"status": status, "url": url, "json": j, "raw": raw if (j is None and raw) else None})


# ---------------- Discovery ----------------

def cmd_me(args, cfg):
    server = cfg["server"]
    url = server + "/rest/api/3/myself"
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "me": j, "raw": raw if j is None else None})


def cmd_project_list(args, cfg):
    server = cfg["server"]
    url = server + "/rest/api/3/project/search?maxResults=" + str(args.max)
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "projects": j, "raw": raw if j is None else None})


# ---------------- Search ----------------

def cmd_search_jql(args, cfg):
    server = cfg["server"]
    base = server + "/rest/api/3/search/jql"
    fields = [f.strip() for f in (args.fields or "key,summary,status").split(",") if f.strip()]
    params = {
        "jql": args.jql,
        "maxResults": str(args.max),
        "fields": ",".join(fields),
    }
    url = base + "?" + urllib.parse.urlencode(params)
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "url": url, "result": j, "raw": raw if j is None else None})


# ---------------- Issues ----------------

def cmd_issue_get(args, cfg):
    server = cfg["server"]
    params = {}
    if args.fields:
        params["fields"] = args.fields
    if args.expand:
        params["expand"] = args.expand
    q = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}{q}"
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "issue": j, "raw": raw if j is None else None})


def cmd_issue_create(args, cfg):
    server = cfg["server"]
    url = server + "/rest/api/3/issue"

    fields = {
        "project": {"key": args.project},
        "issuetype": {"name": args.type},
        "summary": args.summary,
    }
    if args.description:
        fields["description"] = _adf_text(args.description)

    if args.fields_json:
        extra = json.loads(args.fields_json)
        # allow user to pass either {"fields":{...}} or just {...}
        if "fields" in extra and isinstance(extra["fields"], dict):
            fields.update(extra["fields"])
        else:
            fields.update(extra)

    body = {"fields": fields}
    status, j, raw = _http("POST", url, args.headers, body)
    _print({"status": status, "created": j, "raw": raw if j is None else None})


def cmd_issue_edit(args, cfg):
    server = cfg["server"]
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}"
    patch = json.loads(args.fields_json)
    status, j, raw = _http("PUT", url, args.headers, patch)
    _print({"status": status, "result": j, "raw": raw if j is None else None})


def cmd_issue_comment_add(args, cfg):
    server = cfg["server"]
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}/comment"
    body = _adf_text(args.comment)
    status, j, raw = _http("POST", url, args.headers, body)
    _print({"status": status, "comment": j, "raw": raw if j is None else None})


def cmd_issue_transitions(args, cfg):
    server = cfg["server"]
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}/transitions"
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "transitions": j, "raw": raw if j is None else None})


def cmd_issue_transition(args, cfg):
    server = cfg["server"]
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}/transitions"
    body = {"transition": {"id": str(args.id)}}
    status, j, raw = _http("POST", url, args.headers, body)
    _print({"status": status, "result": j, "raw": raw if j is None else None})


def cmd_user_search(args, cfg):
    server = cfg["server"]
    params = {
        "query": args.query,
        "maxResults": str(args.max),
    }
    url = server + "/rest/api/3/user/search?" + urllib.parse.urlencode(params)
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "users": j, "raw": raw if j is None else None})


def cmd_issue_assign(args, cfg):
    server = cfg["server"]
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}/assignee"
    body = {"accountId": args.accountId}
    status, j, raw = _http("PUT", url, args.headers, body)
    _print({"status": status, "result": j, "raw": raw if j is None else None})


def cmd_issue_link(args, cfg):
    server = cfg["server"]
    url = server + "/rest/api/3/issueLink"
    body = {
        "type": {"name": args.type},
        "inwardIssue": {"key": args.inward},
        "outwardIssue": {"key": args.outward},
    }
    status, j, raw = _http("POST", url, args.headers, body)
    _print({"status": status, "result": j, "raw": raw if j is None else None})


# ---------------- Sprints / Boards (Agile API) ----------------

def _agile_url(cfg: dict, path: str) -> str:
    return cfg["server"] + "/rest/agile/1.0" + ("/" + path.lstrip("/"))


def cmd_board_list(args, cfg):
    params = {"maxResults": str(args.max)}
    if args.project:
        params["projectKeyOrId"] = args.project
    url = _agile_url(cfg, "/board?") + urllib.parse.urlencode(params)
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "boards": j, "raw": raw if j is None else None})


def cmd_board_get(args, cfg):
    url = _agile_url(cfg, f"/board/{args.board}")
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "board": j, "raw": raw if j is None else None})


def cmd_sprint_list(args, cfg):
    params = {"maxResults": str(args.max)}
    if args.state:
        params["state"] = args.state
    url = _agile_url(cfg, f"/board/{args.board}/sprint?") + urllib.parse.urlencode(params)
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "sprints": j, "raw": raw if j is None else None})


def cmd_sprint_get(args, cfg):
    url = _agile_url(cfg, f"/sprint/{args.sprint}")
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "sprint": j, "raw": raw if j is None else None})


def cmd_sprint_issues(args, cfg):
    fields = [f.strip() for f in (args.fields or "key,summary,status").split(",") if f.strip()]
    params = {
        "maxResults": str(args.max),
        "fields": ",".join(fields),
    }
    if args.jql:
        params["jql"] = args.jql
    url = _agile_url(cfg, f"/sprint/{args.sprint}/issue?") + urllib.parse.urlencode(params)
    status, j, raw = _http("GET", url, args.headers)
    _print({"status": status, "issues": j, "raw": raw if j is None else None})


def _date_to_iso(date_s: str) -> str:
    # input YYYY-MM-DD
    d = dt.datetime.strptime(date_s, "%Y-%m-%d").date()
    # Jira expects ISO datetime; send midnight UTC.
    return dt.datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=dt.timezone.utc).isoformat()


def cmd_sprint_create(args, cfg):
    url = _agile_url(cfg, "/sprint")
    body = {"name": args.name, "originBoardId": int(args.board)}
    if args.start:
        body["startDate"] = _date_to_iso(args.start)
    if args.end:
        body["endDate"] = _date_to_iso(args.end)
    status, j, raw = _http("POST", url, args.headers, body)
    _print({"status": status, "sprint": j, "raw": raw if j is None else None})


def cmd_sprint_update(args, cfg):
    url = _agile_url(cfg, f"/sprint/{args.sprint}")
    body = {}
    if args.name:
        body["name"] = args.name
    if args.state:
        body["state"] = args.state
    if args.start:
        body["startDate"] = _date_to_iso(args.start)
    if args.end:
        body["endDate"] = _date_to_iso(args.end)
    status, j, raw = _http("PUT", url, args.headers, body)
    _print({"status": status, "sprint": j, "raw": raw if j is None else None})


# ---------------- Worklogs ----------------

def cmd_worklog_add(args, cfg):
    server = cfg["server"]
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}/worklog"
    body = {
        "timeSpent": args.time_spent,
        "started": _started_in_jira_format(args.started, args.timezone),
    }
    if args.comment is not None:
        body["comment"] = _adf_text(args.comment)

    status, j, raw = _http("POST", url, args.headers, body)
    _print({"status": status, "worklog": j, "raw": raw if j is None else None})


def cmd_worklog_list(args, cfg):
    server = cfg["server"]
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}/worklog"
    status, j, raw = _http("GET", url, args.headers)

    worklogs = (j or {}).get("worklogs", [])
    if args.from_date or args.to_date:
        d_from = _parse_date(args.from_date) if args.from_date else None
        d_to = _parse_date(args.to_date) if args.to_date else None
        filtered = []
        for w in worklogs:
            started = w.get("started")
            if not started:
                continue
            t = dt.datetime.strptime(started, "%Y-%m-%dT%H:%M:%S.%f%z")
            dd = t.date()
            if d_from and dd < d_from:
                continue
            if d_to and dd > d_to:
                continue
            filtered.append(w)
        worklogs = filtered

    _print({"status": status, "issue": args.issue, "worklogs": worklogs, "raw": raw if j is None else None})


def cmd_worklog_delete(args, cfg):
    server = cfg["server"]
    params = {}
    if args.adjustEstimate:
        params["adjustEstimate"] = args.adjustEstimate
    if args.newEstimate:
        params["newEstimate"] = args.newEstimate
    q = ("?" + urllib.parse.urlencode(params)) if params else ""
    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}/worklog/{urllib.parse.quote(args.worklog_id)}{q}"
    status, j, raw = _http("DELETE", url, args.headers)
    _print({"status": status, "issue": args.issue, "worklogId": args.worklog_id, "json": j, "raw": raw or None})


def cmd_worklog_update(args, cfg):
    server = cfg["server"]
    params = {}
    if args.adjustEstimate:
        params["adjustEstimate"] = args.adjustEstimate
    if args.newEstimate:
        params["newEstimate"] = args.newEstimate
    q = ("?" + urllib.parse.urlencode(params)) if params else ""

    body = {}
    if args.started:
        body["started"] = _started_in_jira_format(args.started, args.timezone)
    if args.timeSpent:
        body["timeSpent"] = args.timeSpent
    if args.comment is not None:
        body["comment"] = _adf_text(args.comment)

    url = server + f"/rest/api/3/issue/{urllib.parse.quote(args.issue)}/worklog/{urllib.parse.quote(args.worklog_id)}{q}"
    status, j, raw = _http("PUT", url, args.headers, body)
    _print({"status": status, "issue": args.issue, "worklogId": args.worklog_id, "result": j, "raw": raw or None})


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument("--jira-config", default=DEFAULT_JIRA_CONFIG)
    p.add_argument("--netrc", default=DEFAULT_NETRC)

    sub = p.add_subparsers(dest="cmd", required=True)

    # request
    r = sub.add_parser("request")
    r.add_argument("method")
    r.add_argument("path")
    r.add_argument("--query", action="append", default=[], metavar="k=v")
    r.add_argument("--data-json")
    r.add_argument("--data-file")

    # discovery
    sub.add_parser("me")
    pl = sub.add_parser("project-list")
    pl.add_argument("--max", type=int, default=50)

    # search
    sj = sub.add_parser("search-jql")
    sj.add_argument("jql")
    sj.add_argument("--fields", default="key,summary,status")
    sj.add_argument("--max", type=int, default=50)

    # issues
    ig = sub.add_parser("issue-get")
    ig.add_argument("issue")
    ig.add_argument("--fields")
    ig.add_argument("--expand")

    ic = sub.add_parser("issue-create")
    ic.add_argument("--project", required=True)
    ic.add_argument("--type", required=True)
    ic.add_argument("--summary", required=True)
    ic.add_argument("--description")
    ic.add_argument("--fields-json")

    ie = sub.add_parser("issue-edit")
    ie.add_argument("issue")
    ie.add_argument("--fields-json", required=True, help='JSON patch. Example: {"fields":{"summary":"..."}}')

    ca = sub.add_parser("issue-comment-add")
    ca.add_argument("issue")
    ca.add_argument("--comment", required=True)

    tr = sub.add_parser("issue-transitions")
    tr.add_argument("issue")

    do = sub.add_parser("issue-transition")
    do.add_argument("issue")
    do.add_argument("--id", required=True)

    us = sub.add_parser("user-search")
    us.add_argument("query")
    us.add_argument("--max", type=int, default=20)

    ia = sub.add_parser("issue-assign")
    ia.add_argument("issue")
    ia.add_argument("--accountId", required=True)

    il = sub.add_parser("issue-link")
    il.add_argument("--type", required=True)
    il.add_argument("--inward", required=True)
    il.add_argument("--outward", required=True)

    # boards / sprints (agile)
    bl = sub.add_parser("board-list")
    bl.add_argument("--max", type=int, default=50)
    bl.add_argument("--project", help="Filter by project key/id (optional)")

    bg = sub.add_parser("board-get")
    bg.add_argument("board")

    sl = sub.add_parser("sprint-list")
    sl.add_argument("--board", required=True)
    sl.add_argument("--state", choices=["future", "active", "closed"])
    sl.add_argument("--max", type=int, default=50)

    sg = sub.add_parser("sprint-get")
    sg.add_argument("sprint")

    si = sub.add_parser("sprint-issues")
    si.add_argument("sprint")
    si.add_argument("--jql")
    si.add_argument("--fields", default="key,summary,status")
    si.add_argument("--max", type=int, default=50)

    sc = sub.add_parser("sprint-create")
    sc.add_argument("--board", required=True)
    sc.add_argument("--name", required=True)
    sc.add_argument("--start", help="YYYY-MM-DD")
    sc.add_argument("--end", help="YYYY-MM-DD")

    su = sub.add_parser("sprint-update")
    su.add_argument("sprint")
    su.add_argument("--name")
    su.add_argument("--state", choices=["future", "active", "closed"])
    su.add_argument("--start", help="YYYY-MM-DD")
    su.add_argument("--end", help="YYYY-MM-DD")

    # worklogs
    wa = sub.add_parser("worklog-add")
    wa.add_argument("issue")
    wa.add_argument("time_spent")
    wa.add_argument("--started", required=True, help="YYYY-MM-DD HH:MM:SS or Jira datetime")
    wa.add_argument("--timezone", default="Europe/Madrid")
    wa.add_argument("--comment")

    wl = sub.add_parser("worklog-list")
    wl.add_argument("issue")
    wl.add_argument("--from", dest="from_date")
    wl.add_argument("--to", dest="to_date")

    wdel = sub.add_parser("worklog-delete")
    wdel.add_argument("issue")
    wdel.add_argument("worklog_id")
    wdel.add_argument("--adjustEstimate", choices=["auto", "new", "leave"])
    wdel.add_argument("--newEstimate")

    wup = sub.add_parser("worklog-update")
    wup.add_argument("issue")
    wup.add_argument("worklog_id")
    wup.add_argument("--started")
    wup.add_argument("--timezone", default="Europe/Madrid")
    wup.add_argument("--timeSpent")
    wup.add_argument("--comment")
    wup.add_argument("--adjustEstimate", choices=["auto", "new", "leave"])
    wup.add_argument("--newEstimate")

    return p


def main(argv: list[str]) -> int:
    p = build_parser()
    args = p.parse_args(argv)

    cfg = _read_jira_config(args.jira_config)
    host = urllib.parse.urlparse(cfg["server"]).hostname
    if not host:
        raise RuntimeError("Could not parse Jira hostname")

    user, token = _netrc_auth_for_host(host, args.netrc)
    args.headers = {
        "Accept": "application/json",
        "Authorization": _basic_auth_header(user, token),
        "User-Agent": "openclaw-skill/jira-api",
    }

    # Parse --query k=v
    if getattr(args, "query", None):
        pairs = []
        for item in args.query:
            if "=" not in item:
                raise SystemExit(f"Invalid --query '{item}', expected k=v")
            k, v = item.split("=", 1)
            pairs.append((k, v))
        args.query = pairs

    cmd = args.cmd

    if cmd == "request":
        cmd_request(args, cfg)
    elif cmd == "me":
        cmd_me(args, cfg)
    elif cmd == "project-list":
        cmd_project_list(args, cfg)
    elif cmd == "search-jql":
        cmd_search_jql(args, cfg)
    elif cmd == "issue-get":
        cmd_issue_get(args, cfg)
    elif cmd == "issue-create":
        cmd_issue_create(args, cfg)
    elif cmd == "issue-edit":
        cmd_issue_edit(args, cfg)
    elif cmd == "issue-comment-add":
        cmd_issue_comment_add(args, cfg)
    elif cmd == "issue-transitions":
        cmd_issue_transitions(args, cfg)
    elif cmd == "issue-transition":
        cmd_issue_transition(args, cfg)
    elif cmd == "user-search":
        cmd_user_search(args, cfg)
    elif cmd == "issue-assign":
        cmd_issue_assign(args, cfg)
    elif cmd == "issue-link":
        cmd_issue_link(args, cfg)
    elif cmd == "board-list":
        cmd_board_list(args, cfg)
    elif cmd == "board-get":
        cmd_board_get(args, cfg)
    elif cmd == "sprint-list":
        cmd_sprint_list(args, cfg)
    elif cmd == "sprint-get":
        cmd_sprint_get(args, cfg)
    elif cmd == "sprint-issues":
        cmd_sprint_issues(args, cfg)
    elif cmd == "sprint-create":
        cmd_sprint_create(args, cfg)
    elif cmd == "sprint-update":
        cmd_sprint_update(args, cfg)
    elif cmd == "worklog-add":
        cmd_worklog_add(args, cfg)
    elif cmd == "worklog-list":
        cmd_worklog_list(args, cfg)
    elif cmd == "worklog-delete":
        cmd_worklog_delete(args, cfg)
    elif cmd == "worklog-update":
        cmd_worklog_update(args, cfg)
    else:
        raise SystemExit("Unknown command")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except Exception as e:
        _print({"error": str(e)})
        raise SystemExit(1)
