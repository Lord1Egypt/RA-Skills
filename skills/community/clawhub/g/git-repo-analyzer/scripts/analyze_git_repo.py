#!/usr/bin/env python3
"""Analyze a Git repository and detect its subtype (skill, paper, function, unknown)."""
import sys, re, json, os, urllib.request, urllib.error, subprocess, tempfile

GIT_RE = re.compile(r"https?://(github|gitlab|bitbucket|gitee)\.[^/]+/([\w-]+)/([\w.-]+)")

def fetch_api_files(platform: str, owner: str, repo: str):
    repo = repo.replace(".git", "")
    headers = {}
    if platform == "github":
        url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
    elif platform == "gitlab":
        path = urllib.parse.quote(f"{owner}/{repo}", safe="")
        url = f"https://gitlab.com/api/v4/projects/{path}/repository/tree"
        token = os.environ.get("GITLAB_TOKEN")
        if token:
            headers["PRIVATE-TOKEN"] = token
    else:
        return None

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list):
                return [f.get("name", f.get("path", "")) for f in data]
            return []
    except Exception:
        return None


def detect_subtype(file_names):
    has_skill_md = "SKILL.md" in file_names
    has_paper = any(re.search(r"paper|thesis|article|\.pdf$|docs/.*\.md$", f, re.I) for f in file_names)
    has_docs = "docs" in file_names or any(f.lower().endswith(".md") for f in file_names)
    has_code = any(re.search(r"\.(py|js|ts|rs|go|java|cpp|c|h|rb|php)$", f, re.I) for f in file_names)

    if has_skill_md:
        return "skill"
    if has_paper or (has_docs and not has_code):
        return "paper"
    if has_code:
        return "function"
    return "unknown"


def analyze(url: str):
    match = GIT_RE.match(url)
    if not match:
        return {"error": "Invalid Git URL"}
    platform, owner, repo = match.groups()

    files = fetch_api_files(platform, owner, repo)
    if files is None:
        # Fallback to git ls-remote / shallow clone
        files = []

    subtype = detect_subtype(files) if files else "unknown"

    return {
        "url": url,
        "type": "git-repo",
        "subtype": subtype,
        "domain": platform,
        "owner": owner,
        "repo": repo.replace(".git", ""),
        "files": files or [],
    }


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    if not url:
        print(json.dumps({"error": "URL required"}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(analyze(url), ensure_ascii=False))
