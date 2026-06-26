#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitCode PR 检视意见：拉取未解决行评、回复讨论、修改解决状态。
Python 3.7+，仅标准库。

子命令:
  fetch   需指定 --pr-url（或 --owner/--repo/--number），拉取未解决 diff_comment，写出 JSON
  reply   在指定 discussion 下发表回复（POST）
  resolve 修改检视讨论解决状态（PUT）
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

GITCODE_API_BASE = "https://api.gitcode.com/api/v5"
API_RETRY = 2
API_RETRY_INTERVAL = 2.0


def _init_windows_utf8() -> None:
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass


def _print_json(data: Any, outfile: Optional[str] = None) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if outfile:
        with open(outfile, "w", encoding="utf-8") as f:
            f.write(text)
    try:
        sys.stdout.buffer.write(text.encode("utf-8"))
        sys.stdout.buffer.flush()
    except (AttributeError, OSError):
        print(text, end="")


def get_token(cli_token: Optional[str]) -> Optional[str]:
    if cli_token and cli_token.strip():
        return cli_token.strip()
    t = os.environ.get("GITCODE_TOKEN")
    if t:
        return t.strip()
    if sys.platform == "win32":
        for scope in ("User", "Machine"):
            try:
                out = subprocess.check_output(
                    [
                        "powershell",
                        "-NoProfile",
                        "-Command",
                        "[Environment]::GetEnvironmentVariable('GITCODE_TOKEN','%s')" % scope,
                    ],
                    creationflags=0x08000000,
                    timeout=5,
                    stderr=subprocess.DEVNULL,
                )
                val = out.decode("utf-8", errors="replace").strip()
                if val:
                    return val
            except Exception:
                pass
    return None


def parse_pr_url(url: str) -> Tuple[str, str, int]:
    s = url.strip()
    m = re.search(
        r"gitcode\.com[/:]([^/]+)/([^/]+)/(?:pull|pulls|merge_requests)/(\d+)",
        s,
        re.I,
    )
    if m:
        owner, repo, num = m.group(1), m.group(2), int(m.group(3))
        if repo.endswith(".git"):
            repo = repo[:-4]
        return owner, repo, num
    raise ValueError("无法从 URL 解析 owner/repo/PR 编号: %s" % url)


def _api_url(path: str, query: Optional[Dict[str, Any]] = None) -> str:
    base = GITCODE_API_BASE.rstrip("/") + "/" + path.lstrip("/")
    if query:
        # urlencode 处理 since 中的 + 等
        q = urlencode(
            [(k, v) for k, v in query.items() if v is not None],
            doseq=True,
        )
        return base + "?" + q
    return base


def api_request(
    method: str,
    token: str,
    path: str,
    query: Optional[Dict[str, Any]] = None,
    json_body: Any = None,
) -> Any:
    url = _api_url(path, query)
    headers = {"PRIVATE-TOKEN": token}
    data = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    last_err = None
    for attempt in range(API_RETRY + 1):
        req = Request(url, data=data, method=method, headers=headers)
        try:
            with urlopen(req, timeout=60) as f:
                body = f.read().decode("utf-8")
                if not body.strip():
                    return None
                return json.loads(body)
        except HTTPError as e:
            last_err = e
            if e.code == 429:
                wait = 60
                try:
                    wait = int(e.headers.get("Retry-After", 60))
                except (TypeError, ValueError):
                    pass
                time.sleep(wait)
            elif attempt < API_RETRY:
                time.sleep(API_RETRY_INTERVAL)
            else:
                err_body = ""
                try:
                    err_body = e.read().decode("utf-8", errors="replace")
                except Exception:
                    pass
                raise RuntimeError("HTTP %s %s: %s" % (e.code, url, err_body or str(e))) from e
        except (URLError, OSError) as e:
            last_err = e
            if attempt < API_RETRY:
                time.sleep(API_RETRY_INTERVAL)
            else:
                raise RuntimeError("请求失败 %s: %s" % (url, e)) from e
    raise last_err  # type: ignore


def fetch_all_pr_comments(
    token: str, owner: str, repo: str, number: int
) -> List[Dict[str, Any]]:
    all_c: List[Dict[str, Any]] = []
    page = 1
    per_page = 100
    while True:
        chunk = api_request(
            "GET",
            token,
            "/repos/%s/%s/pulls/%s/comments"
            % (quote(owner, safe=""), quote(repo, safe=""), number),
            query={
                "comment_type": "diff_comment",
                "per_page": per_page,
                "page": page,
                "direction": "asc",
                "view": "all",
            },
        )
        if not isinstance(chunk, list) or not chunk:
            break
        all_c.extend(chunk)
        if len(chunk) < per_page:
            break
        page += 1
    return all_c


def comment_sort_key(c: Dict[str, Any]) -> int:
    for k in ("line", "original_line", "start_line", "position"):
        v = c.get(k)
        if v is not None:
            try:
                return int(v)
            except (TypeError, ValueError):
                pass
    return 0


def build_by_file(items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    by_file: Dict[str, List[Dict[str, Any]]] = {}
    for it in items:
        path = it.get("diff_file") or it.get("path") or "(unknown)"
        by_file.setdefault(str(path), []).append(it)
    for path in by_file:
        by_file[path].sort(key=comment_sort_key, reverse=True)
    return by_file


def cmd_fetch(args: argparse.Namespace) -> int:
    token = get_token(args.token)
    if not token:
        sys.stderr.write("缺少 Token：请设置环境变量 GITCODE_TOKEN 或使用 --token\n")
        return 2

    owner, repo, number = parse_pr_url(args.pr_url)
    pr_detail = api_request(
        "GET",
        token,
        "/repos/%s/%s/pulls/%s" % (quote(owner, safe=""), quote(repo, safe=""), number),
    )
    comments = fetch_all_pr_comments(token, owner, repo, number)
    # False / 缺省视为未解决；仅 resolved 为真时排除
    unresolved = [c for c in comments if not c.get("resolved")]

    indexed: List[Dict[str, Any]] = []
    for i, c in enumerate(unresolved, start=1):
        row = dict(c)
        row["seq"] = i
        did = row.get("discussion_id") or row.get("discussionId")
        if did is not None:
            row["discussion_id"] = did
        indexed.append(row)

    by_file = build_by_file(indexed)
    missing_did = [x["seq"] for x in indexed if not x.get("discussion_id")]
    warnings: List[str] = []
    if missing_did:
        warnings.append(
            "以下 seq 缺少 discussion_id，无法使用 reply/resolve：%s" % missing_did
        )
    payload: Dict[str, Any] = {
        "schema_version": 1,
        "owner": owner,
        "repo": repo,
        "pr_number": number,
        "pr_html_url": (pr_detail or {}).get("html_url"),
        "pr_title": (pr_detail or {}).get("title"),
        "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "unresolved_diff_comments": indexed,
        "by_file": by_file,
        "stats": {
            "total_diff_comments": len(comments),
            "unresolved_count": len(indexed),
        },
    }
    if warnings:
        payload["warnings"] = warnings

    out_path = args.output
    if out_path:
        _print_json(payload, outfile=out_path)
        sys.stderr.write("已写入: %s\n" % os.path.abspath(out_path))
    else:
        _print_json(payload)
    return 0


def cmd_reply(args: argparse.Namespace) -> int:
    token = get_token(args.token)
    if not token:
        sys.stderr.write("缺少 Token\n")
        return 2
    ctx = _load_context(args.context)
    owner = ctx["owner"]
    repo = ctx["repo"]
    number = int(ctx["pr_number"])
    did = args.discussion_id
    if not did:
        seq = args.seq
        if seq is None:
            sys.stderr.write("需要 --discussion-id 或 --seq\n")
            return 2
        for c in ctx.get("unresolved_diff_comments") or []:
            if int(c.get("seq", -1)) == int(seq):
                did = c.get("discussion_id")
                break
        if not did:
            sys.stderr.write("找不到 seq=%s 对应的 discussion_id\n" % seq)
            return 2
    body = args.body
    if args.body_file:
        with open(args.body_file, encoding="utf-8") as f:
            body = f.read()
    if body is None:
        sys.stderr.write("需要 --body 或 --body-file\n")
        return 2

    path = "/repos/%s/%s/pulls/%s/discussions/%s/comments" % (
        quote(owner, safe=""),
        quote(repo, safe=""),
        number,
        quote(str(did), safe=""),
    )
    result = api_request("POST", token, path, json_body={"body": body})
    _print_json(result or {"ok": True})
    return 0


def cmd_resolve(args: argparse.Namespace) -> int:
    token = get_token(args.token)
    if not token:
        sys.stderr.write("缺少 Token\n")
        return 2
    ctx = _load_context(args.context)
    owner = ctx["owner"]
    repo = ctx["repo"]
    number = int(ctx["pr_number"])
    did = args.discussion_id
    if not did:
        seq = args.seq
        if seq is None:
            sys.stderr.write("需要 --discussion-id 或 --seq\n")
            return 2
        for c in ctx.get("unresolved_diff_comments") or []:
            if int(c.get("seq", -1)) == int(seq):
                did = c.get("discussion_id")
                break
        if not did:
            sys.stderr.write("找不到 seq=%s 对应的 discussion_id\n" % seq)
            return 2

    # 官方：PUT .../pulls/:number/comments/discussions/:id
    path = "/repos/%s/%s/pulls/%s/comments/discussions/%s" % (
        quote(owner, safe=""),
        quote(repo, safe=""),
        number,
        quote(str(did), safe=""),
    )
    body = {"resolved": bool(args.resolved)}
    result = api_request("PUT", token, path, json_body=body)
    _print_json(result or {"ok": True})
    return 0


def _load_context(path: str) -> Dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    _init_windows_utf8()
    p = argparse.ArgumentParser(description="GitCode PR 检视意见工具")
    p.add_argument("--token", help="覆盖 GITCODE_TOKEN")
    sub = p.add_subparsers(dest="cmd", required=True)

    pf = sub.add_parser("fetch", help="拉取未解决行评上下文 JSON（仅支持 PR 链接）")
    pf.add_argument(
        "--pr-url",
        required=True,
        help="GitCode PR 页面完整 URL（唯一方式，路径含 pull/pulls/merge_requests）",
    )
    pf.add_argument(
        "--output",
        "-o",
        help="写出 JSON 路径（推荐，便于后续 reply/resolve）",
    )
    pf.set_defaults(func=cmd_fetch)

    pr = sub.add_parser("reply", help="在讨论下回复")
    pr.add_argument("--context", "-c", required=True, help="fetch 生成的 JSON 路径")
    pr.add_argument("--discussion-id", help="讨论 ID（与 --seq 二选一）")
    pr.add_argument("--seq", type=int, help="上下文中的序号 seq")
    pr.add_argument("--body", help="回复正文")
    pr.add_argument("--body-file", help="从文件读正文")
    pr.set_defaults(func=cmd_reply)

    pv = sub.add_parser("resolve", help="修改讨论解决状态")
    pv.add_argument("--context", "-c", required=True, help="fetch 生成的 JSON 路径")
    pv.add_argument("--discussion-id", help="讨论 ID")
    pv.add_argument("--seq", type=int, help="序号 seq")
    pv.add_argument(
        "--resolved",
        type=int,
        default=1,
        choices=(0, 1),
        help="1=已解决 0=未解决",
    )
    pv.set_defaults(func=cmd_resolve)

    args = p.parse_args()
    try:
        return int(args.func(args))
    except RuntimeError as e:
        sys.stderr.write("%s\n" % e)
        return 1
    except ValueError as e:
        sys.stderr.write("%s\n" % e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
