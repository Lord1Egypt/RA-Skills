#!/usr/bin/env python3
"""Jenkins CLI — a thin wrapper over the Jenkins remote API.

Connection is read from environment variables (or a JSON config file):

    JENKINS_URL    e.g. https://jenkins.example.com
    JENKINS_USER   username
    JENKINS_TOKEN  API token (User → Configure → API Token)

Or put {"url": "...", "user": "...", "token": "..."} in
~/.devops-skills/jenkins.json.

POST actions (build, enable/disable) automatically fetch a CSRF crumb when the
instance has CSRF protection enabled. Job names may include folders, e.g.
"team/app/main"; the CLI builds the correct /job/.../job/... path for you.

Every command prints JSON to stdout and exits non-zero on error.
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

CONFIG_PATH = os.path.expanduser("~/.devops-skills/jenkins.json")
MIN_VERSION = (2, 60, 0)
MIN_VERSION_TEXT = "2.60.0"


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
    url = os.environ.get("JENKINS_URL", cfg.get("url"))
    user = os.environ.get("JENKINS_USER", cfg.get("user"))
    token = os.environ.get("JENKINS_TOKEN", cfg.get("token"))
    if not url or not user or not token:
        die("JENKINS_URL, JENKINS_USER and JENKINS_TOKEN are required (env vars or ~/.devops-skills/jenkins.json)")
    return {"url": url.rstrip("/"), "user": user, "token": token}


def job_path(name):
    """Turn "folder/job/sub" into "/job/folder/job/job/job/sub"."""
    return "".join(f"/job/{seg}" for seg in name.strip("/").split("/"))


def auth(cfg):
    return HTTPBasicAuth(cfg["user"], cfg["token"])


def ensure_supported_version(cfg):
    if os.environ.get("JENKINS_SKIP_VERSION_CHECK") or \
            os.environ.get("DEVOPS_SKILLS_SKIP_VERSION_CHECK"):
        return
    try:
        resp = requests.get(cfg["url"] + "/api/json", auth=auth(cfg), timeout=30)
    except requests.RequestException as exc:
        die(f"version check failed: {exc}")
    if resp.status_code >= 400:
        die(f"GET /api/json -> HTTP {resp.status_code}: {resp.text[:300]}")
    version = resp.headers.get("X-Jenkins", "")
    if not version:
        warn(f"could not determine Jenkins version; expected Jenkins >= {MIN_VERSION_TEXT}")
        return
    detected = parse_version(version)
    if detected < MIN_VERSION:
        die(f"unsupported Jenkins version {version}. This skill supports Jenkins >= "
            f"{MIN_VERSION_TEXT}; please upgrade Jenkins or use an older skill.")


def get_crumb(cfg):
    try:
        resp = requests.get(cfg["url"] + "/crumbIssuer/api/json",
                            auth=auth(cfg), timeout=30)
    except requests.RequestException as exc:
        die(f"crumb request failed: {exc}")
    if resp.status_code == 404:
        return {}  # CSRF protection disabled
    if resp.status_code >= 400:
        return {}
    data = resp.json()
    return {data["crumbRequestField"]: data["crumb"]}


def request(cfg, method, path, expect_json=True, headers=None, **kwargs):
    hdrs = headers or {}
    if method.upper() == "POST":
        hdrs.update(get_crumb(cfg))
    try:
        resp = requests.request(method, cfg["url"] + path, auth=auth(cfg),
                                headers=hdrs, timeout=60, **kwargs)
    except requests.RequestException as exc:
        die(f"request failed: {exc}")
    if resp.status_code >= 400:
        die(f"{method} {path} -> HTTP {resp.status_code}: {resp.text[:300]}")
    if not expect_json:
        return resp
    if resp.text:
        try:
            return resp.json()
        except ValueError:
            return {"raw": resp.text}
    return {}


def out(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ---- commands ---------------------------------------------------------------

def cmd_list_jobs(cfg, args):
    data = request(cfg, "GET", "/api/json?tree=jobs[name,color,url]")
    out([{"name": j["name"], "status": j.get("color"), "url": j.get("url")}
         for j in data.get("jobs", [])])


def cmd_job_info(cfg, args):
    path = job_path(args.name) + "/api/json"
    data = request(cfg, "GET", path)
    out({
        "name": data.get("name"),
        "buildable": data.get("buildable"),
        "color": data.get("color"),
        "last_build": (data.get("lastBuild") or {}).get("number"),
        "last_success": (data.get("lastSuccessfulBuild") or {}).get("number"),
        "last_failure": (data.get("lastFailedBuild") or {}).get("number"),
        "url": data.get("url"),
    })


def cmd_build(cfg, args):
    params = {}
    for kv in args.param or []:
        if "=" not in kv:
            die(f"--param expects KEY=VALUE, got: {kv}")
        k, v = kv.split("=", 1)
        params[k] = v
    if params:
        path = job_path(args.name) + "/buildWithParameters"
        resp = request(cfg, "POST", path, expect_json=False, params=params)
    else:
        path = job_path(args.name) + "/build"
        resp = request(cfg, "POST", path, expect_json=False)
    out({"job": args.name, "queued": True,
         "queue_url": resp.headers.get("Location")})


def cmd_build_status(cfg, args):
    num = args.number or "lastBuild"
    path = job_path(args.name) + f"/{num}/api/json"
    data = request(cfg, "GET", path)
    out({
        "job": args.name,
        "number": data.get("number"),
        "building": data.get("building"),
        "result": data.get("result"),
        "duration_ms": data.get("duration"),
        "url": data.get("url"),
    })


def cmd_console(cfg, args):
    num = args.number or "lastBuild"
    path = job_path(args.name) + f"/{num}/consoleText"
    resp = request(cfg, "GET", path, expect_json=False)
    text = resp.text
    if args.tail and args.tail > 0:
        text = "\n".join(text.splitlines()[-args.tail:])
    sys.stdout.write(text + "\n")


def cmd_enable(cfg, args):
    request(cfg, "POST", job_path(args.name) + "/enable", expect_json=False)
    out({"job": args.name, "enabled": True})


def cmd_disable(cfg, args):
    request(cfg, "POST", job_path(args.name) + "/disable", expect_json=False)
    out({"job": args.name, "disabled": True})


def build_parser():
    p = argparse.ArgumentParser(description="Jenkins remote API CLI")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("list-jobs", help="list top-level jobs")
    s.set_defaults(func=cmd_list_jobs)

    s = sub.add_parser("job-info", help="show a job summary")
    s.add_argument("name", help='job name, folders allowed e.g. "team/app"')
    s.set_defaults(func=cmd_job_info)

    s = sub.add_parser("build", help="trigger a build")
    s.add_argument("name")
    s.add_argument("--param", action="append", help="KEY=VALUE (repeatable)")
    s.set_defaults(func=cmd_build)

    s = sub.add_parser("build-status", help="status of a build (default last)")
    s.add_argument("name")
    s.add_argument("--number", default="")
    s.set_defaults(func=cmd_build_status)

    s = sub.add_parser("console", help="print console log of a build")
    s.add_argument("name")
    s.add_argument("--number", default="")
    s.add_argument("--tail", type=int, default=0, help="only last N lines")
    s.set_defaults(func=cmd_console)

    s = sub.add_parser("enable", help="enable a job")
    s.add_argument("name")
    s.set_defaults(func=cmd_enable)

    s = sub.add_parser("disable", help="disable a job")
    s.add_argument("name")
    s.set_defaults(func=cmd_disable)
    return p


def main():
    args = build_parser().parse_args()
    cfg = load_config()
    ensure_supported_version(cfg)
    args.func(cfg, args)


if __name__ == "__main__":
    main()
