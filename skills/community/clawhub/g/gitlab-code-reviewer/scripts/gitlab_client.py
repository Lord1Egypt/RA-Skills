#!/usr/bin/env python3
"""
GitLab API client for MR code review workflow.

Usage:
    python gitlab_client.py fetch-mr <mr_url>
    python gitlab_client.py fetch-diff <mr_url>
    python gitlab_client.py post-comment <mr_url> <file_path> <line> <comment>

Credentials read from ~/.openclaw/credentials/gitlab.json:
    { "token": "glpat-xxx", "host": "https://gitlab.com", "ignore_patterns": [...] }
"""

import json
import sys
import re
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode


CREDS_PATH = Path.home() / ".openclaw" / "credentials" / "gitlab.json"


def load_credentials() -> dict:
    if not CREDS_PATH.exists():
        raise FileNotFoundError(f"Credentials not found at {CREDS_PATH}")
    with open(CREDS_PATH) as f:
        creds = json.load(f)
    if "token" not in creds or "host" not in creds:
        raise ValueError("Credentials must contain 'token' and 'host' fields")
    return creds


def parse_mr_url(url: str) -> tuple[str, str, str]:
    """
    Parse a GitLab MR URL into (host, project_path_encoded, mr_iid).
    Supports:
        https://gitlab.com/group/subgroup/project/-/merge_requests/123
        https://gitlab.example.com/namespace/project/-/merge_requests/456
    Returns (host, url_encoded_project_path, mr_iid).
    """
    pattern = r"(https?://[^/]+)/(.+)/-/merge_requests/(\d+)"
    m = re.match(pattern, url.rstrip("/"))
    if not m:
        raise ValueError(f"Cannot parse MR URL: {url}")
    host = m.group(1)
    project_path = m.group(2)
    mr_iid = m.group(3)
    encoded_path = project_path.replace("/", "%2F")
    return host, encoded_path, mr_iid


def api_get(host: str, token: str, path: str, params: dict | None = None) -> dict | list:
    url = f"{host}/api/v4{path}"
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={"PRIVATE-TOKEN": token, "Content-Type": "application/json"})
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"GitLab API error {e.code} on GET {path}: {body}") from e


def api_post(host: str, token: str, path: str, payload: dict) -> dict:
    url = f"{host}/api/v4{path}"
    data = json.dumps(payload).encode()
    req = Request(url, data=data, headers={
        "PRIVATE-TOKEN": token,
        "Content-Type": "application/json"
    }, method="POST")
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"GitLab API error {e.code} on POST {path}: {body}") from e


def check_token_scope(mr_url: str) -> dict:
    """
    Check whether the configured token has 'api' (write) or only 'read_api' scope.
    Returns {"can_write": bool, "scopes": list[str], "token_name": str}.
    Prints a warning when posting comments will not be possible.
    """
    creds = load_credentials()
    host = creds["host"]
    try:
        info = api_get(host, creds["token"], "/personal_access_tokens/self")
        scopes = info.get("scopes", [])
        can_write = "api" in scopes
        if not can_write:
            print(
                "WARNING: Token scope is read-only (scopes: "
                + ", ".join(scopes)
                + ").\n"
                "Analysis will proceed, but inline comments CANNOT be posted.\n"
                "To enable posting: regenerate the token with scope 'api' at\n"
                "GitLab → User Settings → Access Tokens, then update\n"
                "~/.openclaw/credentials/gitlab.json.",
                file=sys.stderr,
            )
        return {"can_write": can_write, "scopes": scopes, "token_name": info.get("name", "")}
    except RuntimeError as e:
        # Endpoint may not be available on older GitLab versions — treat as unknown.
        print(f"WARNING: Could not verify token scope: {e}", file=sys.stderr)
        return {"can_write": None, "scopes": [], "token_name": ""}


def fetch_mr(mr_url: str) -> dict:
    """Return MR metadata (title, author, source_branch, target_branch, description, state)."""
    creds = load_credentials()
    host, project, iid = parse_mr_url(mr_url)
    data = api_get(host, creds["token"], f"/projects/{project}/merge_requests/{iid}")
    return {
        "iid": data["iid"],
        "title": data["title"],
        "state": data["state"],
        "author": data.get("author", {}).get("username", ""),
        "source_branch": data["source_branch"],
        "target_branch": data["target_branch"],
        "description": data.get("description", ""),
        "web_url": data["web_url"],
        "sha": data["sha"],
    }


def fetch_diff(mr_url: str) -> list[dict]:
    """
    Return list of diffs per changed file.
    Each entry:
        {
          "old_path": str,
          "new_path": str,
          "diff": str,         # unified diff text
          "new_file": bool,
          "deleted_file": bool,
          "renamed_file": bool,
        }
    Tries /diffs first (paginated, 100 per page).
    Falls back to /changes automatically if the server returns HTTP 500.
    """
    creds = load_credentials()
    host, project, iid = parse_mr_url(mr_url)

    all_diffs = []
    page = 1
    use_changes_fallback = False

    while True:
        try:
            if use_changes_fallback:
                data = api_get(
                    host, creds["token"],
                    f"/projects/{project}/merge_requests/{iid}/changes",
                )
                all_diffs = data.get("changes", [])
                break
            else:
                data = api_get(
                    host, creds["token"],
                    f"/projects/{project}/merge_requests/{iid}/diffs",
                    params={"page": page, "per_page": 100},
                )
        except RuntimeError as e:
            if "500" in str(e) and not use_changes_fallback:
                print(
                    "Warning: /diffs returned HTTP 500; retrying via /changes fallback.",
                    file=sys.stderr,
                )
                use_changes_fallback = True
                continue
            raise

        if not data:
            break
        all_diffs.extend(data)
        if len(data) < 100:
            break
        page += 1

    return [
        {
            "old_path": d.get("old_path", ""),
            "new_path": d.get("new_path", ""),
            "diff": d.get("diff", ""),
            "new_file": d.get("new_file", False),
            "deleted_file": d.get("deleted_file", False),
            "renamed_file": d.get("renamed_file", False),
        }
        for d in all_diffs
    ]


def post_inline_comment(mr_url: str, file_path: str, new_line: int, body: str) -> dict:
    """
    Post a single inline comment on a specific file line in the MR diff.
    Uses the Discussions API (position-based diff comments).
    Requires the MR's latest diff SHA.
    Returns the created discussion object.
    """
    creds = load_credentials()
    host, project, iid = parse_mr_url(mr_url)

    mr = fetch_mr(mr_url)
    base_sha_data = api_get(
        host, creds["token"],
        f"/projects/{project}/merge_requests/{iid}/versions"
    )
    if not base_sha_data:
        raise RuntimeError("No diff versions found for this MR")

    latest = base_sha_data[0]
    head_sha = latest["head_commit_sha"]
    base_sha = latest["base_commit_sha"]
    start_sha = latest["start_commit_sha"]

    payload = {
        "body": body,
        "position": {
            "position_type": "text",
            "base_sha": base_sha,
            "start_sha": start_sha,
            "head_sha": head_sha,
            "new_path": file_path,
            "new_line": new_line,
        }
    }
    result = api_post(
        host, creds["token"],
        f"/projects/{project}/merge_requests/{iid}/discussions",
        payload
    )
    return result


def post_bulk_comments(mr_url: str, comments: list[dict]) -> list[dict]:
    """
    Post multiple inline comments.
    comments: list of { "file_path": str, "line": int, "body": str }
    Returns list of results (success or error per comment).
    Stops early on 403 insufficient_scope and prints a clear diagnostic.
    """
    results = []
    for c in comments:
        try:
            r = post_inline_comment(mr_url, c["file_path"], c["line"], c["body"])
            results.append({"status": "ok", "file": c["file_path"], "line": c["line"], "id": r.get("id")})
        except Exception as e:
            err_str = str(e)
            results.append({"status": "error", "file": c["file_path"], "line": c["line"], "error": err_str})
            if "403" in err_str and "insufficient_scope" in err_str:
                print(
                    "\nERROR: Token lacks write scope for posting discussions.\n"
                    "Fix: regenerate the token at GitLab → User Settings → Access Tokens\n"
                    "     and set scope to 'api' (not just 'read_api').\n"
                    "     Update the token in ~/.openclaw/credentials/gitlab.json.",
                    file=sys.stderr,
                )
                # All remaining comments will fail with the same error — skip them.
                for remaining in comments[len(results):]:
                    results.append({
                        "status": "skipped",
                        "file": remaining["file_path"],
                        "line": remaining["line"],
                        "error": "aborted: insufficient token scope",
                    })
                break
    return results


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    # Force UTF-8 on stdout to prevent encoding errors on Windows (cp1252)
    import io as _io
    if hasattr(sys.stdout, "buffer"):
        sys.stdout = _io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    mr_url = sys.argv[2]

    if cmd == "check-token":
        result = check_token_scope(mr_url)
        print(json.dumps(result, indent=2))

    elif cmd == "fetch-mr":
        result = fetch_mr(mr_url)
        print(json.dumps(result, indent=2))

    elif cmd == "fetch-diff":
        result = fetch_diff(mr_url)
        print(json.dumps(result, indent=2))

    elif cmd == "post-comment":
        if len(sys.argv) < 6:
            print("Usage: gitlab_client.py post-comment <mr_url> <file_path> <line> <comment>")
            sys.exit(1)
        file_path = sys.argv[3]
        line = int(sys.argv[4])
        comment = sys.argv[5]
        result = post_inline_comment(mr_url, file_path, line, comment)
        print(json.dumps(result, indent=2))

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
