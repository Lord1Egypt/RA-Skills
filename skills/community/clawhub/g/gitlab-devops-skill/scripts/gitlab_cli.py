#!/usr/bin/env python3
"""GitLab CLI — a thin wrapper over the GitLab REST API v4.

Connection is read from environment variables (or a JSON config file):

    GITLAB_URL    e.g. https://gitlab.com  (or self-hosted base URL)
    GITLAB_TOKEN  personal/project/group access token (scope: api)

Or put {"url": "...", "token": "..."} in ~/.devops-skills/gitlab.json.

Projects may be referenced by numeric ID or by URL-encoded path
(e.g. "group/subgroup/project"); this CLI URL-encodes paths for you.

Every command prints JSON to stdout and exits non-zero on error.
"""
import argparse
import json
import os
import sys
from urllib.parse import quote

try:
    import requests
except ImportError:
    sys.stderr.write("Missing dependency: pip install requests\n")
    sys.exit(2)

CONFIG_PATH = os.path.expanduser("~/.devops-skills/gitlab.json")
MIN_VERSION = (9, 0, 0)
MIN_VERSION_TEXT = "9.0.0"


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
    url = os.environ.get("GITLAB_URL", cfg.get("url", "https://gitlab.com"))
    token = os.environ.get("GITLAB_TOKEN", cfg.get("token"))
    if not token:
        die("GITLAB_TOKEN is required (env var or ~/.devops-skills/gitlab.json)")
    return {"url": url.rstrip("/"), "token": token}


def request(cfg, method, path, **kwargs):
    headers = {"PRIVATE-TOKEN": cfg["token"], "Content-Type": "application/json"}
    try:
        resp = requests.request(method, cfg["url"] + "/api/v4" + path,
                                headers=headers, timeout=30, **kwargs)
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
    if os.environ.get("GITLAB_SKIP_VERSION_CHECK") or \
            os.environ.get("DEVOPS_SKILLS_SKIP_VERSION_CHECK"):
        return
    data = request(cfg, "GET", "/version")
    version = data.get("version")
    if not version:
        warn(f"could not determine GitLab version; expected GitLab >= {MIN_VERSION_TEXT} with REST API v4")
        return
    detected = parse_version(version)
    if detected < MIN_VERSION:
        die(f"unsupported GitLab version {version}. This skill uses REST API v4 and supports "
            f"GitLab >= {MIN_VERSION_TEXT}; please upgrade GitLab or use an older skill.")


def pid(project):
    """Accept a numeric id or a path; return the URL-encoded segment."""
    return project if project.isdigit() else quote(project, safe="")


def out(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ---- commands ---------------------------------------------------------------

def cmd_list_projects(cfg, args):
    params = {"membership": "true", "per_page": args.limit,
              "order_by": "last_activity_at"}
    if args.search:
        params["search"] = args.search
    data = request(cfg, "GET", "/projects", params=params)
    out([{"id": p["id"], "path": p["path_with_namespace"],
          "url": p["web_url"]} for p in data])


def cmd_get_project(cfg, args):
    p = request(cfg, "GET", f"/projects/{pid(args.project)}")
    out({"id": p["id"], "path": p["path_with_namespace"], "url": p["web_url"],
         "default_branch": p.get("default_branch"),
         "open_issues": p.get("open_issues_count"),
         "visibility": p.get("visibility")})


def cmd_list_issues(cfg, args):
    params = {"state": args.state, "per_page": args.limit}
    data = request(cfg, "GET", f"/projects/{pid(args.project)}/issues", params=params)
    out([{"iid": i["iid"], "title": i["title"], "state": i["state"],
          "assignee": (i.get("assignee") or {}).get("username")} for i in data])


def cmd_create_issue(cfg, args):
    body = {"title": args.title, "description": args.description}
    if args.labels:
        body["labels"] = args.labels
    i = request(cfg, "POST", f"/projects/{pid(args.project)}/issues",
                data=json.dumps(body))
    out({"iid": i["iid"], "title": i["title"], "url": i["web_url"]})


def cmd_list_mrs(cfg, args):
    params = {"state": args.state, "per_page": args.limit}
    data = request(cfg, "GET", f"/projects/{pid(args.project)}/merge_requests",
                   params=params)
    out([{"iid": m["iid"], "title": m["title"], "state": m["state"],
          "source": m["source_branch"], "target": m["target_branch"]} for m in data])


def cmd_create_mr(cfg, args):
    body = {"source_branch": args.source, "target_branch": args.target,
            "title": args.title, "description": args.description}
    m = request(cfg, "POST", f"/projects/{pid(args.project)}/merge_requests",
                data=json.dumps(body))
    out({"iid": m["iid"], "title": m["title"], "url": m["web_url"]})


def cmd_merge_mr(cfg, args):
    m = request(cfg, "PUT",
                f"/projects/{pid(args.project)}/merge_requests/{args.iid}/merge")
    out({"iid": m["iid"], "state": m["state"], "merged_by":
         (m.get("merged_by") or {}).get("username")})


def cmd_list_pipelines(cfg, args):
    params = {"per_page": args.limit}
    if args.ref:
        params["ref"] = args.ref
    data = request(cfg, "GET", f"/projects/{pid(args.project)}/pipelines",
                   params=params)
    out([{"id": p["id"], "status": p["status"], "ref": p["ref"],
          "url": p["web_url"]} for p in data])


def cmd_trigger_pipeline(cfg, args):
    body = {"ref": args.ref}
    p = request(cfg, "POST", f"/projects/{pid(args.project)}/pipeline",
                data=json.dumps(body))
    out({"id": p["id"], "status": p["status"], "ref": p["ref"],
         "url": p["web_url"]})


def build_parser():
    p = argparse.ArgumentParser(description="GitLab REST API v4 CLI")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("list-projects", help="list projects you are a member of")
    s.add_argument("--search", default="")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_list_projects)

    s = sub.add_parser("get-project", help="show a project")
    s.add_argument("project", help="numeric id or group/project path")
    s.set_defaults(func=cmd_get_project)

    s = sub.add_parser("list-issues", help="list project issues")
    s.add_argument("project")
    s.add_argument("--state", default="opened", choices=["opened", "closed", "all"])
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_list_issues)

    s = sub.add_parser("create-issue", help="create an issue")
    s.add_argument("project")
    s.add_argument("--title", required=True)
    s.add_argument("--description", default="")
    s.add_argument("--labels", default="")
    s.set_defaults(func=cmd_create_issue)

    s = sub.add_parser("list-mrs", help="list merge requests")
    s.add_argument("project")
    s.add_argument("--state", default="opened", choices=["opened", "closed", "merged", "all"])
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_list_mrs)

    s = sub.add_parser("create-mr", help="create a merge request")
    s.add_argument("project")
    s.add_argument("--source", required=True)
    s.add_argument("--target", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--description", default="")
    s.set_defaults(func=cmd_create_mr)

    s = sub.add_parser("merge-mr", help="merge a merge request")
    s.add_argument("project")
    s.add_argument("iid")
    s.set_defaults(func=cmd_merge_mr)

    s = sub.add_parser("list-pipelines", help="list pipelines")
    s.add_argument("project")
    s.add_argument("--ref", default="")
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_list_pipelines)

    s = sub.add_parser("trigger-pipeline", help="trigger a pipeline on a ref")
    s.add_argument("project")
    s.add_argument("--ref", required=True)
    s.set_defaults(func=cmd_trigger_pipeline)
    return p


def main():
    args = build_parser().parse_args()
    cfg = load_config()
    ensure_supported_version(cfg)
    args.func(cfg, args)


if __name__ == "__main__":
    main()
