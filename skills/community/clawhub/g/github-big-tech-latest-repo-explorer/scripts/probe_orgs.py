#!/usr/bin/env python3
"""逐个访问名单中的 GitHub 组织页面，判断：
1. 页面是否可访问（HTTP 200）
2. 页面是否包含「仓库」内容

只做轻量 HTTP GET，不下载完整 HTML。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Tuple

DEFAULT_ORG_CONFIG = Path(__file__).resolve().parent.parent / "references" / "organizations.json"

UA = "github-big-tech-latest-repo-explorer-org-probe/1.0"


def http_get(url: str, timeout: int = 15):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        try:
            return resp.status, dict(resp.headers), resp
        finally:
            # Caller still owns the body via resp.read(); don't close here.
            pass
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers or {}), None
    except urllib.error.URLError as e:
        return None, {"error": str(e.reason)}, None


def normalize_login(value) -> Optional[str]:
    if not isinstance(value, str):
        return None
    s = value.strip().rstrip("/")
    if not s:
        return None
    s = re.sub(r"^https?://", "", s)
    if s.startswith("github.com/"):
        s = s[len("github.com/"):]
    login = s.split("/")[0]
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", login):
        return None
    return login


def load_org_pairs(path: Path) -> List[Tuple[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    pairs: List[Tuple[str, str]] = []
    if isinstance(data, dict) and "organizations" in data and not any(
        isinstance(v, list) for v in data.values()
    ):
        for org in data["organizations"]:
            login = normalize_login(org)
            if login:
                pairs.append(("", login))
    elif isinstance(data, dict):
        for company, urls in data.items():
            for url in urls:
                login = normalize_login(url)
                if login:
                    pairs.append((company, login))
    return pairs


def probe_one(company: str, login: str, max_bytes: int = 500_000) -> dict:
    # GitHub org URLs are case-insensitive: Taobao -> taobao, Alipay -> alipay
    # All anchors in HTML are emitted with the canonical lowercase login.
    login_lc = login.lower()
    profile_url = f"https://github.com/{login}"
    repos_url = f"https://github.com/orgs/{login_lc}/repositories?type=source"
    # 匹配 /<login>/<repo> 这种仓库链接（前面不能是 /orgs/，后面是 ? # 或 "）。
    # 大小写不敏感，因为 URL 路径不分大小写。
    repo_anchor_re = re.compile(
        r'href="(?!/orgs/)/' + re.escape(login_lc) + r"/([A-Za-z0-9._-]+)(?:[?#\"])",
        re.IGNORECASE,
    )

    result: dict = {
        "company": company or None,
        "login": login,
        "profile_url": profile_url,
        "profile_status": None,
        "profile_title": None,
        "repos_url": repos_url,
        "repos_status": None,
        "has_repos": False,
        "evidence": "",
        "error": None,
    }

    try:
        status, _h, resp = http_get(profile_url)
        result["profile_status"] = status
        if resp is not None:
            data = resp.read(max_bytes).decode("utf-8", errors="replace")
            m = re.search(r"<title>([^<]+)</title>", data)
            if m:
                result["profile_title"] = m.group(1).strip()
            anchors = repo_anchor_re.findall(data)
            if anchors:
                result["evidence"] += f"profile:anchors={len(anchors)}"
                result["has_repos"] = True
            if (
                "Pinned repositories" in data
                or "pinned-repos" in data
                or "Pinned Repositories" in data
            ):
                result["evidence"] += "profile:has_pinned;"
    except Exception as e:
        result["error"] = f"profile: {e}"

    try:
        status, _h, resp = http_get(repos_url)
        result["repos_status"] = status
        if resp is not None:
            data = resp.read(max_bytes).decode("utf-8", errors="replace")
            anchors = repo_anchor_re.findall(data)
            if anchors:
                result["evidence"] += f"repos:anchors={len(anchors)}"
                result["has_repos"] = True
            m = re.search(
                r"(\d+)\s+results?\s+for\s+repositories", data
            ) or re.search(
                r"Public repositories\s*</span>\s*<span[^>]*>\s*(\d+)", data
            )
            if m:
                result["evidence"] += f";count={m.group(1)}"
    except Exception as e:
        result["error"] = (result.get("error") or "") + f" repos: {e}"

    if (
        not result["has_repos"]
        and result["profile_status"] == 200
        and "profile:has_pinned" in result["evidence"]
    ):
        result["has_repos"] = True

    return result

def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org-config", type=Path, default=DEFAULT_ORG_CONFIG)
    ap.add_argument("--workers", type=int, default=10)
    args = ap.parse_args(argv)

    pairs = load_org_pairs(args.org_config)
    print(f"# orgs to probe: {len(pairs)}", file=sys.stderr)

    results: list = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(probe_one, c, l) for c, l in pairs]
        for i, f in enumerate(as_completed(futs), 1):
            r = f.result()
            results.append(r)
            print(
                f"[{i}/{len(pairs)}] {r['login']:<32s} profile={r['profile_status']} repos={r['repos_status']} has_repos={r['has_repos']}",
                file=sys.stderr,
            )

    results.sort(key=lambda r: ((r.get("company") or ""), r["login"]))

    has = [r for r in results if r["has_repos"]]
    no_has = [r for r in results if not r["has_repos"]]
    errs = [r for r in results if r["profile_status"] is None and r["repos_status"] is None]

    summary = {
        "total": len(results),
        "with_repos": len(has),
        "without_repos": len(no_has),
        "errors": len(errs),
        "results": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
