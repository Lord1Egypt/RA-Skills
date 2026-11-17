#!/usr/bin/env python3
"""Jira CLI — a thin, dependency-light wrapper over the Jira REST API.

Auth & connection are read from environment variables (or a JSON config file),
so no secrets ever live in the command line or in this repo:

    JIRA_URL    e.g. https://your-domain.atlassian.net  (or self-hosted base URL)
    JIRA_USER   account email (Cloud) or username (Server/DC)
    JIRA_TOKEN  API token (Cloud) or personal access token (Server/DC)
    JIRA_AUTH   "basic" (default, Cloud: email+token) or "bearer" (Server/DC PAT)

Alternatively put the same keys (lowercased, without the JIRA_ prefix) in
~/.devops-skills/jira.json, e.g. {"url": "...", "user": "...", "token": "..."}.

Every command prints JSON to stdout so the output is easy to parse, and exits
non-zero on error with a human-readable message on stderr.
"""
import argparse
import json
import os
import sys

try:
    import requests
    from requests.auth import HTTPBasicAuth
except ImportError:
    sys.stderr.write("Missing dependency: pip install requests\n")
    sys.exit(2)

CONFIG_PATH = os.path.expanduser("~/.devops-skills/jira.json")
MIN_VERSION = (7, 0, 0)
MIN_VERSION_TEXT = "7.0.0"


def die(msg, code=1):
    sys.stderr.write(f"error: {msg}\n")
    sys.exit(code)


def warn(msg):
    sys.stderr.write(f"warning: {msg}\n")


def parse_version(value):
    nums, cur = [], ""
    for ch in str(value):
        if ch.isdigit():
            cur += ch
        elif cur:
            nums.append(int(cur))
            cur = ""
            if len(nums) == 3:
                break
    if cur and len(nums) < 3:
        nums.append(int(cur))
    return tuple((nums + [0, 0, 0])[:3])


def load_config():
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, encoding="utf-8") as fh:
                cfg = json.load(fh)
        except (OSError, ValueError) as exc:
            die(f"Cannot read config {CONFIG_PATH}: {exc}")
    url = os.environ.get("JIRA_URL", cfg.get("url"))
    user = os.environ.get("JIRA_USER", cfg.get("user"))
    token = os.environ.get("JIRA_TOKEN", cfg.get("token"))
    auth = os.environ.get("JIRA_AUTH", cfg.get("auth", "basic")).lower()
    if not url or not token:
        die("JIRA_URL and JIRA_TOKEN are required (env vars or ~/.devops-skills/jira.json)")
    if auth == "basic" and not user:
        die("JIRA_USER is required for basic auth")
    return {"url": url.rstrip("/"), "user": user, "token": token, "auth": auth}


def request(cfg, method, path, **kwargs):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    auth = None
    if cfg["auth"] == "bearer":
        headers["Authorization"] = f"Bearer {cfg['token']}"
    else:
        auth = HTTPBasicAuth(cfg["user"], cfg["token"])
    try:
        resp = requests.request(method, cfg["url"] + path, headers=headers,
                                auth=auth, timeout=30, **kwargs)
    except requests.RequestException as exc:
        die(f"request failed: {exc}")
    if resp.status_code >= 400:
        die(f"{method} {path} -> HTTP {resp.status_code}: {resp.text[:500]}")
    if resp.text:
        try:
            return resp.json()
        except ValueError:
            return {"raw": resp.text}
    return {}


def ensure_supported_version(cfg):
    if os.environ.get("JIRA_SKIP_VERSION_CHECK") or \
            os.environ.get("DEVOPS_SKILLS_SKIP_VERSION_CHECK"):
        return
    data = request(cfg, "GET", "/rest/api/2/serverInfo")
    deployment = (data.get("deploymentType") or "").lower()
    version = data.get("version") or ".".join(str(x) for x in data.get("versionNumbers", []))
    if deployment == "cloud" and not version:
        return
    if not version:
        warn("could not determine Jira version; expected Jira Cloud or Jira Server/Data Center "
             f">= {MIN_VERSION_TEXT}")
        return
    detected = parse_version(version)
    if detected < MIN_VERSION:
        die(f"unsupported Jira version {version}. This skill supports Jira Cloud and "
            f"Jira Server/Data Center >= {MIN_VERSION_TEXT}; please upgrade Jira or use an older skill.")


def out(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ---- commands ---------------------------------------------------------------

def cmd_get_issue(cfg, args):
    data = request(cfg, "GET", f"/rest/api/2/issue/{args.key}")
    f = data.get("fields", {})
    out({
        "key": data.get("key"),
        "summary": f.get("summary"),
        "status": (f.get("status") or {}).get("name"),
        "assignee": (f.get("assignee") or {}).get("displayName"),
        "reporter": (f.get("reporter") or {}).get("displayName"),
        "priority": (f.get("priority") or {}).get("name"),
        "type": (f.get("issuetype") or {}).get("name"),
        "description": f.get("description"),
    })


def cmd_search(cfg, args):
    body = {"jql": args.jql, "maxResults": args.limit,
            "fields": ["summary", "status", "assignee"]}
    data = request(cfg, "POST", "/rest/api/2/search", data=json.dumps(body))
    issues = [{
        "key": i.get("key"),
        "summary": i["fields"].get("summary"),
        "status": (i["fields"].get("status") or {}).get("name"),
        "assignee": (i["fields"].get("assignee") or {}).get("displayName"),
    } for i in data.get("issues", [])]
    out({"total": data.get("total"), "issues": issues})


def cmd_create_issue(cfg, args):
    fields = {
        "project": {"key": args.project},
        "summary": args.summary,
        "issuetype": {"name": args.type},
    }
    if args.description:
        fields["description"] = args.description
    if args.assignee:
        fields["assignee"] = {"name": args.assignee}
    data = request(cfg, "POST", "/rest/api/2/issue",
                   data=json.dumps({"fields": fields}))
    out({"created": data.get("key"), "id": data.get("id")})


def cmd_comment(cfg, args):
    data = request(cfg, "POST", f"/rest/api/2/issue/{args.key}/comment",
                   data=json.dumps({"body": args.body}))
    out({"issue": args.key, "comment_id": data.get("id")})


def cmd_transitions(cfg, args):
    data = request(cfg, "GET", f"/rest/api/2/issue/{args.key}/transitions")
    out({"transitions": [{"id": t["id"], "to": t["name"]}
                         for t in data.get("transitions", [])]})


def cmd_transition(cfg, args):
    data = request(cfg, "GET", f"/rest/api/2/issue/{args.key}/transitions")
    match = next((t for t in data.get("transitions", [])
                  if t["name"].lower() == args.to.lower()), None)
    if not match:
        names = ", ".join(t["name"] for t in data.get("transitions", []))
        die(f'no transition "{args.to}". Available: {names}')
    request(cfg, "POST", f"/rest/api/2/issue/{args.key}/transitions",
            data=json.dumps({"transition": {"id": match["id"]}}))
    out({"issue": args.key, "transitioned_to": match["name"]})


def cmd_assign(cfg, args):
    request(cfg, "PUT", f"/rest/api/2/issue/{args.key}/assignee",
            data=json.dumps({"name": args.user}))
    out({"issue": args.key, "assignee": args.user})


def build_parser():
    p = argparse.ArgumentParser(description="Jira REST API CLI")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("get-issue", help="show one issue")
    s.add_argument("key")
    s.set_defaults(func=cmd_get_issue)

    s = sub.add_parser("search", help="search issues by JQL")
    s.add_argument("jql")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("create-issue", help="create an issue")
    s.add_argument("--project", required=True)
    s.add_argument("--type", default="Task")
    s.add_argument("--summary", required=True)
    s.add_argument("--description", default="")
    s.add_argument("--assignee", default="")
    s.set_defaults(func=cmd_create_issue)

    s = sub.add_parser("comment", help="add a comment")
    s.add_argument("key")
    s.add_argument("--body", required=True)
    s.set_defaults(func=cmd_comment)

    s = sub.add_parser("list-transitions", help="list available transitions")
    s.add_argument("key")
    s.set_defaults(func=cmd_transitions)

    s = sub.add_parser("transition", help="move issue to a status by name")
    s.add_argument("key")
    s.add_argument("--to", required=True)
    s.set_defaults(func=cmd_transition)

    s = sub.add_parser("assign", help="assign issue to a user")
    s.add_argument("key")
    s.add_argument("--user", required=True)
    s.set_defaults(func=cmd_assign)
    return p


def main():
    args = build_parser().parse_args()
    cfg = load_config()
    ensure_supported_version(cfg)
    args.func(cfg, args)


if __name__ == "__main__":
    main()
