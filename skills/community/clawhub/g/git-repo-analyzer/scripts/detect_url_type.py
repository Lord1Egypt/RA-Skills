#!/usr/bin/env python3
"""Detect the type of a given URL."""
import sys, re, urllib.request, urllib.error

GIT_PATTERNS = [
    r"github\.com/[\w-]+/[\w.-]+",
    r"gitlab\.com/[\w-]+/[\w.-]+",
    r"bitbucket\.org/[\w-]+/[\w.-]+",
    r"gitee\.com/[\w-]+/[\w.-]+",
]

FILE_EXTS = re.compile(r"\.(pdf|md|txt|docx|epub|ipynb)$", re.IGNORECASE)


def analyze(url: str):
    result = {"url": url, "type": "unknown", "domain": ""}
    try:
        result["domain"] = urllib.parse.urlparse(url).hostname or ""
    except Exception:
        pass

    is_git = any(re.search(p, url) for p in GIT_PATTERNS)
    if is_git:
        result["type"] = "git-repo"
        return result

    m = FILE_EXTS.search(url)
    if m:
        result["type"] = "direct-file"
        result["fileExt"] = m.group(1).lower()
        if result["fileExt"] == "pdf":
            result["subtype"] = "pdf"
        else:
            result["subtype"] = "markdown" if result["fileExt"] in ("md", "txt") else "document"
        return result

    # Try HEAD request for content-type
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            ct = resp.headers.get("Content-Type", "")
            if "application/pdf" in ct:
                result["type"] = "direct-file"
                result["subtype"] = "pdf"
                result["fileExt"] = "pdf"
            elif "text/markdown" in ct or "text/plain" in ct:
                result["type"] = "direct-file"
                result["subtype"] = "markdown"
                result["fileExt"] = "md" if "markdown" in ct else "txt"
            else:
                result["type"] = "webpage"
                result["subtype"] = "article"
    except Exception:
        result["type"] = "webpage"
        result["subtype"] = "article"

    return result


if __name__ == "__main__":
    import json, urllib.parse
    url = sys.argv[1] if len(sys.argv) > 1 else ""
    if not url:
        print(json.dumps({"error": "URL required"}), file=sys.stderr)
        sys.exit(1)
    print(json.dumps(analyze(url), ensure_ascii=False))
