#!/usr/bin/env python3
"""MyGitVerse CLI — repos, issues, pulls for GitVerse (gitverse.ru).
Dependency-free: uses only stdlib (urllib).
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error

BASE_URL = os.environ.get("GITVERSE_BASE_URL", "https://api.gitverse.ru")
ACCEPT = "application/vnd.gitverse.object+json;version=1"


def get_token():
    t = os.environ.get("GITVERSE_TOKEN")
    if not t:
        p = os.path.expanduser("~/.gitverse_token")
        if os.path.exists(p):
            with open(p) as f:
                t = f.read().strip()
    if not t:
        sys.exit("Ошибка: задай GITVERSE_TOKEN или положи токен в ~/.gitverse_token")
    return t


def request(method, path, body=None):
    url = BASE_URL + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + get_token())
    req.add_header("Accept", ACCEPT)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        sys.exit(f"HTTP {e.code}: {detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Сеть: {e.reason}")


def out(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    p = argparse.ArgumentParser(prog="gitverse-skill")
    sub = p.add_subparsers(dest="cmd", required=True)

    # repos
    rp = sub.add_parser("repos", help="Репозитории")
    rsub = rp.add_subparsers(dest="sub", required=True)
    rl = rsub.add_parser("list", help="Список репозиториев")
    rl.add_argument("--org")
    ri = rsub.add_parser("info", help="Инфо о репозитории")
    ri.add_argument("--owner", required=True)
    ri.add_argument("--repo", required=True)

    # issues
    ip = sub.add_parser("issues", help="Issues")
    isub = ip.add_subparsers(dest="sub", required=True)
    il = isub.add_parser("list")
    il.add_argument("--owner", required=True)
    il.add_argument("--repo", required=True)
    il.add_argument("--state", default="all")
    iv = isub.add_parser("view")
    iv.add_argument("--owner", required=True)
    iv.add_argument("--repo", required=True)
    iv.add_argument("--number", type=int, required=True)
    ic = isub.add_parser("create")
    ic.add_argument("--owner", required=True)
    ic.add_argument("--repo", required=True)
    ic.add_argument("--title", required=True)
    ic.add_argument("--body", default="")
    icm = isub.add_parser("comment")
    icm.add_argument("--owner", required=True)
    icm.add_argument("--repo", required=True)
    icm.add_argument("--number", type=int, required=True)
    icm.add_argument("--body", required=True)
    icl = isub.add_parser("close")
    icl.add_argument("--owner", required=True)
    icl.add_argument("--repo", required=True)
    icl.add_argument("--number", type=int, required=True)

    # pulls
    pp = sub.add_parser("pulls", help="Pull Requests")
    psub = pp.add_subparsers(dest="sub", required=True)
    pl = psub.add_parser("list")
    pl.add_argument("--owner", required=True)
    pl.add_argument("--repo", required=True)
    pl.add_argument("--state", default="all")
    pv = psub.add_parser("view")
    pv.add_argument("--owner", required=True)
    pv.add_argument("--repo", required=True)
    pv.add_argument("--number", type=int, required=True)
    pc = psub.add_parser("create")
    pc.add_argument("--owner", required=True)
    pc.add_argument("--repo", required=True)
    pc.add_argument("--title", required=True)
    pc.add_argument("--head", required=True)
    pc.add_argument("--base", required=True)
    pc.add_argument("--body", default="")
    pm = psub.add_parser("merge")
    pm.add_argument("--owner", required=True)
    pm.add_argument("--repo", required=True)
    pm.add_argument("--number", type=int, required=True)

    a = p.parse_args()

    if a.cmd == "repos":
        if a.sub == "list":
            path = f"/orgs/{a.org}/repos" if a.org else "/user/repos"
            out(request("GET", path))
        elif a.sub == "info":
            out(request("GET", f"/repos/{a.owner}/{a.repo}"))
    elif a.cmd == "issues":
        base = f"/repos/{a.owner}/{a.repo}/issues"
        if a.sub == "list":
            q = "" if a.state == "all" else f"?state={a.state}"
            out(request("GET", base + q))
        elif a.sub == "view":
            out(request("GET", f"{base}/{a.number}"))
        elif a.sub == "create":
            out(request("POST", base, {"title": a.title, "body": a.body}))
        elif a.sub == "comment":
            out(request("POST", f"{base}/{a.number}/comments", {"body": a.body}))
        elif a.sub == "close":
            out(request("PATCH", f"{base}/{a.number}", {"state": "closed"}))
    elif a.cmd == "pulls":
        base = f"/repos/{a.owner}/{a.repo}/pulls"
        if a.sub == "list":
            q = "" if a.state == "all" else f"?state={a.state}"
            out(request("GET", base + q))
        elif a.sub == "view":
            out(request("GET", f"{base}/{a.number}"))
        elif a.sub == "create":
            out(request("POST", base, {"title": a.title, "head": a.head, "base": a.base, "body": a.body}))
        elif a.sub == "merge":
            out(request("PUT", f"{base}/{a.number}/merge"))


if __name__ == "__main__":
    main()
