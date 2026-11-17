#!/usr/bin/env python3
"""Nexus CLI — a thin wrapper over the Sonatype Nexus Repository 3 REST API.

Connection is read from environment variables (or a JSON config file):

    NEXUS_URL   e.g. https://nexus.example.com
    NEXUS_USER  username
    NEXUS_PASS  password (or token)

Or put {"url": "...", "user": "...", "pass": "..."} in
~/.devops-skills/nexus.json.

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

CONFIG_PATH = os.path.expanduser("~/.devops-skills/nexus.json")
API = "/service/rest/v1"
MIN_VERSION = (3, 0, 0)
MIN_VERSION_TEXT = "3.0.0"


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
    url = os.environ.get("NEXUS_URL", cfg.get("url"))
    user = os.environ.get("NEXUS_USER", cfg.get("user"))
    password = os.environ.get("NEXUS_PASS", cfg.get("pass"))
    if not url or not user or not password:
        die("NEXUS_URL, NEXUS_USER and NEXUS_PASS are required (env vars or ~/.devops-skills/nexus.json)")
    return {"url": url.rstrip("/"), "user": user, "pass": password}


def request(cfg, method, path, **kwargs):
    auth = HTTPBasicAuth(cfg["user"], cfg["pass"])
    try:
        resp = requests.request(method, cfg["url"] + API + path,
                                auth=auth, timeout=60, **kwargs)
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
    if os.environ.get("NEXUS_SKIP_VERSION_CHECK") or \
            os.environ.get("DEVOPS_SKILLS_SKIP_VERSION_CHECK"):
        return
    auth = HTTPBasicAuth(cfg["user"], cfg["pass"])
    try:
        resp = requests.get(cfg["url"] + API + "/status", auth=auth, timeout=30)
    except requests.RequestException as exc:
        die(f"version check failed: {exc}")
    if resp.status_code >= 400:
        die(f"GET /status -> HTTP {resp.status_code}: {resp.text[:500]}")
    server = resp.headers.get("Server", "")
    version = ""
    if "Nexus/" in server:
        version = server.split("Nexus/", 1)[1].split()[0]
    if not version:
        warn(f"could not determine Nexus version; expected Sonatype Nexus Repository 3 >= {MIN_VERSION_TEXT}")
        return
    detected = parse_version(version)
    if detected < MIN_VERSION:
        die(f"unsupported Nexus version {version}. This skill supports Sonatype Nexus Repository "
            f"3 >= {MIN_VERSION_TEXT}; Nexus 2 is not supported.")


def out(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ---- commands ---------------------------------------------------------------

def cmd_list_repos(cfg, args):
    data = request(cfg, "GET", "/repositories")
    out([{"name": r["name"], "format": r["format"], "type": r["type"],
          "url": r.get("url")} for r in data])


def cmd_search(cfg, args):
    params = {}
    if args.repo:
        params["repository"] = args.repo
    if args.name:
        params["name"] = args.name
    if args.format:
        params["format"] = args.format
    data = request(cfg, "GET", "/search", params=params)
    out([{"name": i["name"], "version": i.get("version"),
          "format": i["format"], "repository": i["repository"],
          "id": i["id"]} for i in data.get("items", [])])


def cmd_list_components(cfg, args):
    params = {"repository": args.repo}
    items, token = [], None
    while True:
        if token:
            params["continuationToken"] = token
        data = request(cfg, "GET", "/components", params=params)
        items.extend(data.get("items", []))
        token = data.get("continuationToken")
        if not token or len(items) >= args.limit:
            break
    out([{"name": c["name"], "version": c.get("version"),
          "id": c["id"]} for c in items[:args.limit]])


def cmd_upload_raw(cfg, args):
    if not os.path.isfile(args.file):
        die(f"file not found: {args.file}")
    directory = args.directory.strip("/")
    filename = args.filename or os.path.basename(args.file)
    with open(args.file, "rb") as fh:
        files = {
            "raw.directory": (None, directory),
            "raw.asset1": (filename, fh),
            "raw.asset1.filename": (None, filename),
        }
        auth = HTTPBasicAuth(cfg["user"], cfg["pass"])
        url = f"{cfg['url']}{API}/components"
        try:
            resp = requests.post(url, params={"repository": args.repo},
                                 files=files, auth=auth, timeout=300)
        except requests.RequestException as exc:
            die(f"upload failed: {exc}")
    if resp.status_code >= 400:
        die(f"upload -> HTTP {resp.status_code}: {resp.text[:500]}")
    out({"uploaded": f"{directory}/{filename}", "repository": args.repo})


def cmd_download(cfg, args):
    auth = HTTPBasicAuth(cfg["user"], cfg["pass"])
    try:
        resp = requests.get(args.url, auth=auth, stream=True, timeout=300)
    except requests.RequestException as exc:
        die(f"download failed: {exc}")
    if resp.status_code >= 400:
        die(f"download -> HTTP {resp.status_code}")
    dest = args.output or os.path.basename(args.url.split("?")[0]) or "download.bin"
    with open(dest, "wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
    out({"downloaded": dest, "bytes": os.path.getsize(dest)})


def cmd_delete_component(cfg, args):
    request(cfg, "DELETE", f"/components/{args.id}")
    out({"deleted": args.id})


def build_parser():
    p = argparse.ArgumentParser(description="Sonatype Nexus 3 REST API CLI")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("list-repos", help="list all repositories")
    s.set_defaults(func=cmd_list_repos)

    s = sub.add_parser("search", help="search components/assets")
    s.add_argument("--repo", default="")
    s.add_argument("--name", default="")
    s.add_argument("--format", default="")
    s.set_defaults(func=cmd_search)

    s = sub.add_parser("list-components", help="list components in a repo")
    s.add_argument("--repo", required=True)
    s.add_argument("--limit", type=int, default=100)
    s.set_defaults(func=cmd_list_components)

    s = sub.add_parser("upload-raw", help="upload a file to a raw (hosted) repo")
    s.add_argument("--repo", required=True)
    s.add_argument("--file", required=True)
    s.add_argument("--directory", default="/")
    s.add_argument("--filename", default="")
    s.set_defaults(func=cmd_upload_raw)

    s = sub.add_parser("download", help="download an asset by full URL")
    s.add_argument("url")
    s.add_argument("--output", default="")
    s.set_defaults(func=cmd_download)

    s = sub.add_parser("delete-component", help="delete a component by id")
    s.add_argument("id")
    s.set_defaults(func=cmd_delete_component)
    return p


def main():
    args = build_parser().parse_args()
    cfg = load_config()
    ensure_supported_version(cfg)
    args.func(cfg, args)


if __name__ == "__main__":
    main()
