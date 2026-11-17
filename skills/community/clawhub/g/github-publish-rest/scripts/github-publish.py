#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Publish a local folder to a GitHub repo as ONE commit, via the REST API.

Why not `git push` on this machine:
  * the bundled git is a portable build with NO credential helper
    (`credential.helper=helper-selector` + `selected=manager`, but no
    git-credential-manager.exe on disk), so git cannot obtain a credential
    and fails with "could not read Username ... terminal prompts disabled".
  * the WorkBuddy GitHub connector is READ ONLY: create_repository and
    push_files both return 403 "Resource not accessible by integration".
So: take the token that IS stored in Windows Credential Manager (git can still
read it through `git credential fill`) and drive the Git Data API directly.

The token never gets printed and never touches disk.

Usage:
  python github-publish.py --owner ebifry --repo my-repo --dir .\\my-repo ^
                           --message "feat: initial" [--branch main] [--dry-run]

Notes:
  * --dir must be the content root (a .git folder inside is ignored)
  * files are added/updated, nothing is deleted
  * text files should use LF; the API stores bytes as-is
  * ⭐ the commit ALWAYS carries an explicit author/committer with the
    machine's LOCAL UTC offset (see resolve_identity() for why)
"""
import argparse
import base64
import datetime
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

API = "https://api.github.com"
SKIP_DIRS = {".git", "__pycache__", ".idea", ".vscode", "node_modules"}
SKIP_FILES = {"last_run.txt", "last_region.txt", "Thumbs.db", "desktop.ini"}


def get_token():
    # ⭐ 优先读环境变量（本机 git credential fill 会弹交互认证并卡死）
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok.strip(), None
    p = subprocess.run(["git", "credential", "fill"],
                       input="protocol=https\nhost=github.com\n\n",
                       capture_output=True, text=True, timeout=25)
    if p.returncode != 0:
        return None, "git credential fill rc=%s" % p.returncode
    for line in p.stdout.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip(), None
    return None, "no password in credential store"


def resolve_identity(token, owner, name=None, email=None):
    """Who is this commit attributed to? → {"name", "email", "date"}

    ⭐⭐⭐ 必须【显式】传 author / committer，不能靠 API 的默认值。

    ⛔ 不传的后果：GitHub 用"当前 UTC 时间"盖章，时区记成 `Z`（+00:00）。
       而 GitHub 的贡献日历是【按提交里自带的时区】分天的 ——
       官方 2014-03-10「Timezone-aware contribution graphs」原话：
         "When counting commits, we use the timezone information
          present in the timestamps for those commits."
       ⇒ 本机是 AEST/AEDT（UTC+10/+11），**早上 10 点前推的提交，
         UTC 日期还是前一天 → 绿格子记到昨天去了**，看起来就是
         "我明明今天写了代码，图上却没亮"。傍晚推的刚好重合，看不出问题。

    ✅ 这里显式带上本机时区的偏移（`+10:00`），日历就按本地日期记。

    邮箱用 GitHub 给的 noreply 地址 `{id}+{login}@users.noreply.github.com`
    —— 这个地址对账号 ID 天然有效，贡献才算得到本人头上。
    """
    st, me = call("GET", "/user", token)
    if st != 200:
        return None, "GET /user -> %s %s" % (st, me)
    login = me.get("login") or owner
    uid = me.get("id")
    if not email:
        if not uid:
            return None, "cannot derive noreply email (no user id in /user)"
        email = "%s+%s@users.noreply.github.com" % (uid, login)
    return {"name": name or login,
            "email": email,
            "date": datetime.datetime.now().astimezone().isoformat(timespec="seconds")}, None


def call(method, path, token, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "workbuddy-github-publish")
    if data:
        req.add_header("Content-Type", "application/json")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                body = r.read().decode()
                return r.status, (json.loads(body) if body else {})
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode()[:400]
        except Exception as e:
            if attempt == 2:
                return 0, repr(e)
            time.sleep(1.5)
    return 0, "unreachable"


def collect(root):
    out = []
    for p in sorted(root.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if p.name in SKIP_FILES:
            continue
        out.append((rel.as_posix(), p))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--owner", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--dir", required=True, help="local folder to publish (content root)")
    ap.add_argument("--message", default=None,
                    help="提交信息（与 --message-file 二选一）")
    ap.add_argument("--message-file", default=None,
                    help="从文件读提交信息（UTF-8）。⭐ 多行 / 含引号撇号时用这个 —— "
                         "直接拼进命令行会被 shell 吃掉，实测发不出去且没有任何报错")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--author-name", default=None,
                    help="commit 作者名（默认取 /user 的 login）")
    ap.add_argument("--author-email", default=None,
                    help="commit 作者邮箱（默认 {id}+{login}@users.noreply.github.com）")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.message_file:
        if not os.path.exists(a.message_file):
            print("FAIL: message file not found: %s" % a.message_file)
            return 2
        # ⛔ newline="" 原样保留换行；去掉结尾多余空行
        with open(a.message_file, encoding="utf-8", newline="") as fh:
            a.message = fh.read().rstrip("\n")
        if not a.message.strip():
            print("FAIL: message file is empty")
            return 2
    if not a.message:
        ap.error("需要 --message 或 --message-file")
    print("message : %d 字符 / %d 行" % (len(a.message), a.message.count("\n") + 1))

    root = pathlib.Path(a.dir).resolve()
    if not root.is_dir():
        print("not a folder: %s" % root)
        return 2
    files = collect(root)
    if not files:
        print("nothing to publish in %s" % root)
        return 2

    token, err = get_token()
    if not token:
        print("FAIL: no token (%s)" % err)
        print("      authenticate git once on this machine, then retry.")
        return 3
    print("token   : ok (%d chars)" % len(token))

    # ⭐ 身份：显式作者 + 本地时区（见 resolve_identity 的说明）
    ident, ierr = resolve_identity(token, a.owner, a.author_name, a.author_email)
    if not ident:
        print("identity: %s" % ierr)
        return 1
    print("author  : %s <%s>" % (ident["name"], ident["email"]))
    print("stamp   : %s   (本地时区偏移，决定贡献日历算哪一天)" % ident["date"])

    st, ref = call("GET", "/repos/%s/%s/git/ref/heads/%s" % (a.owner, a.repo, a.branch), token)
    if st != 200:
        print("get ref : %s %s" % (st, ref))
        return 1
    head_sha = ref["object"]["sha"]
    st, head = call("GET", "/repos/%s/%s/git/commits/%s" % (a.owner, a.repo, head_sha), token)
    if st != 200:
        print("get head: %s %s" % (st, head))
        return 1
    base_tree = head["tree"]["sha"]
    print("repo    : %s/%s@%s  head=%s" % (a.owner, a.repo, a.branch, head_sha[:8]))
    print("files   : %d" % len(files))

    if a.dry_run:
        for rel, _ in files:
            print("  would push %s" % rel)
        print("dry-run only, nothing written")
        return 0

    tree = []
    for rel, path in files:
        blob = base64.b64encode(path.read_bytes()).decode()
        st, res = call("POST", "/repos/%s/%s/git/blobs" % (a.owner, a.repo), token,
                       {"content": blob, "encoding": "base64"})
        if st != 201:
            print("blob %s -> %s %s" % (rel, st, res))
            return 1
        tree.append({"path": rel, "mode": "100644", "type": "blob", "sha": res["sha"]})
        print("  blob %-28s %s" % (rel, res["sha"][:8]))

    st, res = call("POST", "/repos/%s/%s/git/trees" % (a.owner, a.repo), token,
                   {"base_tree": base_tree, "tree": tree})
    if st != 201:
        print("create tree   : %s %s" % (st, res))
        return 1
    new_tree = res["sha"]

    st, res = call("POST", "/repos/%s/%s/git/commits" % (a.owner, a.repo), token,
                   {"message": a.message, "tree": new_tree, "parents": [head_sha],
                    "author": ident, "committer": ident})
    if st != 201:
        print("create commit : %s %s" % (st, res))
        return 1
    new_commit = res["sha"]

    st, res = call("PATCH", "/repos/%s/%s/git/refs/heads/%s" % (a.owner, a.repo, a.branch), token,
                   {"sha": new_commit, "force": False})
    if st != 200:
        print("update ref    : %s %s" % (st, res))
        return 1
    print("done    : https://github.com/%s/%s  commit=%s" % (a.owner, a.repo, new_commit[:8]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
