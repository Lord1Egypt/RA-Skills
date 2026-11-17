#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""github-workflow-integration · PR / push / status CLI over GitHub REST API.

Pure stdlib (urllib). Token comes from env var GITHUB_TOKEN — never stored,
never printed. No OAuth flow: the user mints a PAT on github.com themselves.

Subcommands:
  pr create   --repo owner/repo --title ... --body ... --head branch --base main
  pr list     --repo owner/repo [--state open]
  status      --repo owner/repo --ref <sha-or-branch>
  push-file   --repo owner/repo --path localfile [--repo-path REMOTE] --message ... --branch main

Exit codes: 0 ok / 1 API error / 2 usage error.
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

API = "https://api.github.com"


def token():
    t = os.environ.get("GITHUB_TOKEN", "").strip()
    if not t:
        print("ERROR: env var GITHUB_TOKEN is not set. Mint a classic PAT on "
              "github.com -> Settings -> Developer settings -> Personal access "
              "tokens (classic), tick 'repo', then `export GITHUB_TOKEN=...`",
              file=sys.stderr)
        sys.exit(2)
    return t


def call(method, path, body=None, dry_run=False):
    url = API + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    if dry_run:
        print("[dry-run] %s %s" % (method, url))
        if body is not None:
            print("[dry-run] body keys: %s" % list(body.keys()))
        return {"dry_run": True}
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "github-workflow-integration/1.0")
    req.add_header("Authorization", "Bearer " + token())
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", errors="replace")[:500]
        print("API %s %s -> HTTP %d: %s" % (method, path, e.code, msg), file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print("API %s %s -> network error: %s" % (method, path, e.reason), file=sys.stderr)
        sys.exit(1)


def cmd_pr_create(a):
    body = {"title": a.title, "head": a.head, "base": a.base, "body": a.body or ""}
    r = call("POST", "/repos/%s/pulls" % a.repo, body, a.dry_run)
    if not a.dry_run:
        print("PR #%d opened: %s" % (r["number"], r["html_url"]))
    else:
        print("would open PR head=%s base=%s title=%r" % (a.head, a.base, a.title))


def cmd_pr_list(a):
    r = call("GET", "/repos/%s/pulls?state=%s&per_page=20" % (a.repo, a.state), dry_run=a.dry_run)
    if not a.dry_run:
        if not r:
            print("no %s pull requests" % a.state)
        for pr in r:
            print("#%-4d [%s] %s  (%s <- %s)" % (pr["number"], pr["state"], pr["title"],
                                                  pr["base"]["ref"], pr["head"]["ref"]))


def cmd_status(a):
    r = call("GET", "/repos/%s/commits/%s/status" % (a.repo, a.ref), dry_run=a.dry_run)
    if not a.dry_run:
        print("state=%s  sha=%s  total_checks=%d" % (r["state"], r["sha"], r["total_count"]))
        for c in r.get("statuses", []):
            print("  - [%s] %s %s" % (c["state"], c["context"], c.get("target_url", "")))


def cmd_push_file(a):
    with open(a.path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode("ascii")
    remote_path = a.repo_path or os.path.basename(a.path)
    # 1. blob
    blob = call("POST", "/repos/%s/git/blobs" % a.repo,
                {"content": content_b64, "encoding": "base64"}, a.dry_run)
    if a.dry_run:
        print("would push %s -> %s:%s (branch=%s)" % (a.path, a.repo, remote_path, a.branch))
        return
    blob_sha = blob["sha"]
    # 2. current branch tip
    ref = call("GET", "/repos/%s/git/refs/heads/%s" % (a.repo, a.branch))
    commit_sha = ref["object"]["sha"]
    # 3. current tree
    cur = call("GET", "/repos/%s/git/commits/%s" % (a.repo, commit_sha))
    tree_sha = cur["tree"]["sha"]
    # 4. new tree
    new_tree = call("POST", "/repos/%s/git/trees" % a.repo,
                    {"base_tree": tree_sha,
                     "tree": [{"path": remote_path, "mode": "100644",
                               "type": "blob", "sha": blob_sha}]})
    # 5. new commit
    new_commit = call("POST", "/repos/%s/git/commits" % a.repo,
                      {"message": a.message, "tree": new_tree["sha"], "parents": [commit_sha]})
    # 6. move ref
    call("PATCH", "/repos/%s/git/refs/heads/%s" % (a.repo, a.branch),
         {"sha": new_commit["sha"], "force": False})
    print("pushed %s -> %s:%s  commit=%s" % (a.path, a.repo, remote_path, new_commit["sha"][:8]))


def main():
    ap = argparse.ArgumentParser(
        description="github-workflow-integration · PR/push/status CLI over GitHub REST API (pure stdlib, token from GITHUB_TOKEN)"
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("pr", help="pull request operations")
    sp = p.add_subparsers(dest="sub", required=True)

    pc = sp.add_parser("create")
    pc.add_argument("--repo", required=True, help="owner/repo")
    pc.add_argument("--title", required=True)
    pc.add_argument("--body", default="")
    pc.add_argument("--head", required=True, help="head branch")
    pc.add_argument("--base", default="main")
    pc.add_argument("--dry-run", action="store_true")
    pc.set_defaults(func=cmd_pr_create)

    pl = sp.add_parser("list")
    pl.add_argument("--repo", required=True)
    pl.add_argument("--state", default="open", choices=["open", "closed", "all"])
    pl.add_argument("--dry-run", action="store_true")
    pl.set_defaults(func=cmd_pr_list)

    s = sub.add_parser("status")
    s.add_argument("--repo", required=True)
    s.add_argument("--ref", required=True, help="sha or branch name")
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(func=cmd_status)

    pf = sub.add_parser("push-file")
    pf.add_argument("--repo", required=True)
    pf.add_argument("--path", required=True, help="local file to upload")
    pf.add_argument("--repo-path", help="remote path (default: local basename)")
    pf.add_argument("--message", required=True)
    pf.add_argument("--branch", default="main")
    pf.add_argument("--dry-run", action="store_true")
    pf.set_defaults(func=cmd_push_file)

    a = ap.parse_args()
    a.func(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
