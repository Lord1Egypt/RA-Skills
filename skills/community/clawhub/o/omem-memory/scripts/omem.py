#!/usr/bin/env python3
"""OMEM client for the OpenClaw skill. Python stdlib only, on purpose: every
line is auditable, there is nothing to install, and the only network calls go
to the OMEM server YOU configured, never anywhere else.

Environment:
  OMEM_BASE_URL  your omem-server (default http://127.0.0.1:8787)
  OMEM_API_KEY   printed on the server's first run (omem_sk_...)
  OMEM_PROJECT   project id (proj_...)
  OMEM_AGENT     the agent identity this skill writes as (default: openclaw)

Commands (all print JSON):
  remember --about X --claim Y [--note "evidence text"]
  believes --about X --claim Y
  recall   [--about X] [--as-of ISO] [--limit N]
  why      --id ASSERTION_ID
  conflicts
  observe  --text "..." [--source S]
  learn    --text "..." [--about X] [--source S]
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("OMEM_BASE_URL", "http://127.0.0.1:8787").rstrip("/")
KEY = os.environ.get("OMEM_API_KEY", "")
PROJECT = os.environ.get("OMEM_PROJECT", "")
AGENT = os.environ.get("OMEM_AGENT", "openclaw")


def req(method, path, body=None, tolerate=False):
    url = BASE + path
    if PROJECT:
        url += ("&" if "?" in url else "?") + "project=" + PROJECT
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KEY}"})
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        if tolerate:
            return None
        detail = e.read().decode(errors="replace")[:300]
        print(json.dumps({"error": f"HTTP {e.code}", "detail": detail}))
        sys.exit(1)


def main():
    p = argparse.ArgumentParser(prog="omem")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("remember")
    s.add_argument("--about", required=True)
    s.add_argument("--claim", required=True)
    s.add_argument("--note", default="")

    s = sub.add_parser("believes")
    s.add_argument("--about", required=True)
    s.add_argument("--claim", required=True)

    s = sub.add_parser("recall")
    s.add_argument("--about", default="")
    s.add_argument("--as-of", dest="as_of", default="")
    s.add_argument("--limit", type=int, default=10)

    s = sub.add_parser("why")
    s.add_argument("--id", required=True)

    sub.add_parser("conflicts")

    s = sub.add_parser("observe")
    s.add_argument("--text", required=True)
    s.add_argument("--source", default="openclaw")

    s = sub.add_parser("learn")
    s.add_argument("--text", required=True)
    s.add_argument("--about", default="")
    s.add_argument("--source", default="openclaw")

    a = p.parse_args()

    if a.cmd == "remember":
        # Mirror the SDK's auto_create: the agent and subject entity are
        # ensured first so a first-time remember works; "already exists"
        # responses are tolerated silently.
        req("POST", "/v1/agents", {"id": AGENT, "kind": "system"}, tolerate=True)
        req("POST", "/v1/entities", {"id": a.about, "type": "thing"}, tolerate=True)
        body = {"agent": AGENT, "subjects": [a.about], "proposition": a.claim,
                "assertion_time": "now", "because": []}
        if a.note:
            body["label"] = a.note
        out = req("POST", "/v1/assertions", body)
    elif a.cmd == "believes":
        out = req("POST", "/v1/queries/proposition-state",
                  {"subjects": [a.about], "proposition": a.claim})
    elif a.cmd == "recall":
        body = {"limit": a.limit}
        if a.about:
            body["about"] = a.about
        if a.as_of:
            body["as_of"] = a.as_of
        out = req("POST", "/v1/recall", body)
    elif a.cmd == "why":
        out = req("GET", f"/v1/assertions/{a.id}/why")
    elif a.cmd == "conflicts":
        out = req("GET", "/v1/memory/conflicts")
    elif a.cmd == "observe":
        out = req("POST", "/v1/observe",
                  {"agent": AGENT, "interaction": {"text": a.text},
                   "source": a.source})
    elif a.cmd == "learn":
        body = {"agent": AGENT, "text": a.text, "source": a.source}
        if a.about:
            body["about"] = a.about
        out = req("POST", "/v1/learn", body)
    else:
        p.error("unknown command")
        return

    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
