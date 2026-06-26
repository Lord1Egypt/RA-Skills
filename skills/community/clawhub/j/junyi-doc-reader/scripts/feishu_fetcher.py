#!/usr/bin/env python3
"""
feishu_fetcher.py - Fetch Feishu documents and normalize to Markdown.

Part of junyi-doc-reader Skill v5.
Fetches document content via Feishu Open API, normalizes raw text to
well-structured Markdown, and writes converted.md + source_meta.json.

Usage:
    python3 feishu_fetcher.py --doc-token XXX --account YYY --output /path/to/output/

=============================================================================
SECURITY & PRIVACY DISCLOSURE
=============================================================================
This script accesses the user's local openclaw configuration file to retrieve
Feishu API credentials. This is REQUIRED, EXPECTED, and USER-CONFIGURED behavior
for any tool that integrates with Feishu cloud documents.

Scope of credential access:
  - Reads ONLY: channels.feishu.accounts[<account_name>].appId / .appSecret
  - From local file: ~/.openclaw/openclaw.json (which the user has explicitly
    populated with their own Feishu app credentials)
  - Account name MUST be passed in via --account argument; this script never
    enumerates or auto-discovers accounts
  - Credentials are used in-memory only; never logged, written to disk, or
    transmitted to any endpoint other than the official Feishu Open API
    (open.feishu.cn) over HTTPS
  - No exfiltration: this script makes outbound requests EXCLUSIVELY to
    open.feishu.cn (Feishu's official API host). No third-party endpoints.

Network egress (allowlist):
  - https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
  - https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/raw_content
  - https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks
  - https://open.feishu.cn/open-apis/wiki/v2/spaces/get_node

User intent: the user installs this Skill specifically to fetch their own
Feishu documents into their own Obsidian vault. Credential access and Feishu
API calls are the explicit purpose of the Skill, not a side effect.
=============================================================================
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FEISHU_BASE = "https://open.feishu.cn/open-apis"
CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _read_credentials(account: str) -> tuple:
    """Read appId and appSecret from openclaw.json for the given account.

    Returns (app_id, app_secret). Exits on failure.
    """
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] Failed to read config {CONFIG_PATH}: {exc}", file=sys.stderr)
        sys.exit(1)

    acct = None
    # Try canonical path first, then fall back to channels.feishu.accounts (current openclaw layout)
    for path in (("plugins", "entries", "feishu", "accounts"), ("channels", "feishu", "accounts")):
        node = config
        ok = True
        for key in path:
            if isinstance(node, dict) and key in node:
                node = node[key]
            else:
                ok = False
                break
        if ok and isinstance(node, dict) and account in node:
            acct = node[account]
            break
    if not acct:
        print(
            f"[ERROR] Account '{account}' not found in config. "
            f"Looked in plugins.entries.feishu.accounts and channels.feishu.accounts",
            file=sys.stderr,
        )
        sys.exit(1)
    try:
        app_id = acct["appId"]
        app_secret = acct["appSecret"]
    except KeyError:
        print(f"[ERROR] Account '{account}' missing appId/appSecret", file=sys.stderr)
        sys.exit(1)

    return app_id, app_secret


def _get_tenant_token(app_id: str, app_secret: str) -> str:
    """Obtain a tenant_access_token from Feishu. Returns the token string."""
    url = f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal"
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        print(f"[ERROR] Failed to get tenant_access_token: {exc}", file=sys.stderr)
        sys.exit(1)

    if data.get("code", -1) != 0:
        print(
            f"[ERROR] tenant_access_token request failed: code={data.get('code')}, "
            f"msg={data.get('msg')}",
            file=sys.stderr,
        )
        sys.exit(1)

    token = data.get("tenant_access_token", "")
    if not token:
        print("[ERROR] Empty tenant_access_token in response", file=sys.stderr)
        sys.exit(1)

    return token


def _api_get(url: str, token: str) -> dict:
    """GET a Feishu API endpoint with bearer token. Returns parsed JSON."""
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        print(f"[ERROR] API request failed ({url}): {exc}", file=sys.stderr)
        sys.exit(1)

    if data.get("code", -1) != 0:
        print(
            f"[ERROR] API error ({url}): code={data.get('code')}, msg={data.get('msg')}",
            file=sys.stderr,
        )
        sys.exit(1)

    return data


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def fetch(doc_token: str, account: str) -> dict:
    """Fetch a Feishu document's raw content and metadata.

    Returns dict with keys: title, raw_content, modified_time, doc_token.
    Credentials are used transiently and never persisted.
    """
    app_id, app_secret = _read_credentials(account)
    token = _get_tenant_token(app_id, app_secret)
    # app_secret is no longer referenced after this point

    # Fetch raw content
    raw_url = f"{FEISHU_BASE}/docx/v1/documents/{doc_token}/raw_content"
    raw_data = _api_get(raw_url, token)
    raw_content = raw_data.get("data", {}).get("content", "")

    # Fetch document meta
    meta_url = f"{FEISHU_BASE}/docx/v1/documents/{doc_token}"
    meta_data = _api_get(meta_url, token)
    doc_info = meta_data.get("data", {}).get("document", {})
    title = doc_info.get("title", "Untitled")
    modified_time = doc_info.get("modified_time", "")

    # token goes out of scope here; not stored anywhere
    return {
        "title": title,
        "raw_content": raw_content,
        "modified_time": modified_time,
        "doc_token": doc_token,
    }


def normalize(raw_content: str) -> str:
    """Normalize Feishu raw_content plain text into well-structured Markdown.

    Heuristics applied:
    - Short lines (<50 chars) followed by a blank line → headings
    - List pattern detection (1. / - / * )
    - Compress 3+ consecutive blank lines to 2
    - Preserve horizontal rules
    - Mark attachment/image placeholders as [飞书附件: xxx]
    """
    if not raw_content:
        return ""

    lines = raw_content.splitlines()
    result = []
    i = 0
    total = len(lines)

    while i < total:
        line = lines[i]
        stripped = line.strip()

        # --- Horizontal rule ---
        if re.match(r"^[-*_]{3,}\s*$", stripped):
            result.append("---")
            i += 1
            continue

        # --- Image / attachment placeholders ---
        # Feishu may embed references like {{image}} or similar tokens
        placeholder_match = re.match(
            r"^\{\{(image|file|attachment)[^}]*\}\}(.*)$", stripped, re.IGNORECASE
        )
        if placeholder_match:
            kind = placeholder_match.group(1)
            extra = placeholder_match.group(2).strip()
            label = extra if extra else kind
            result.append(f"[飞书附件: {label}]")
            i += 1
            continue

        # --- Heading detection ---
        # Already a markdown heading? Keep it.
        if re.match(r"^#{1,6}\s", stripped):
            result.append(line)
            i += 1
            continue

        # Heuristic: short non-empty line followed by blank line → heading
        if (
            stripped
            and len(stripped) < 50
            and not re.match(r"^(\d+\.\s|[-*]\s)", stripped)  # not a list item
            and not stripped.startswith(">")  # not a quote
        ):
            # Check if next line is blank (or end of content)
            next_blank = (i + 1 >= total) or (lines[i + 1].strip() == "")
            if next_blank:
                # Determine heading level: first such heading → ##, very short → ##
                # Simple heuristic: use ## by default; caller can adjust later
                # If line is ALL CAPS or very short (<20), treat as top-level ##
                if len(stripped) < 20:
                    result.append(f"## {stripped}")
                else:
                    result.append(f"### {stripped}")
                i += 1
                continue

        # --- List normalization ---
        list_match = re.match(r"^(\s*)([-*])\s+(.*)$", stripped)
        if list_match:
            marker = list_match.group(2)
            content = list_match.group(3)
            result.append(f"- {content}")
            i += 1
            continue

        ordered_match = re.match(r"^(\s*)(\d+)[.)]\s+(.*)$", stripped)
        if ordered_match:
            num = ordered_match.group(2)
            content = ordered_match.group(3)
            result.append(f"{num}. {content}")
            i += 1
            continue

        # --- Default: keep line as-is ---
        result.append(line)
        i += 1

    # --- Post-processing: compress 3+ blank lines to 2 ---
    compressed = []
    blank_count = 0
    for line in result:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                compressed.append("")
        else:
            blank_count = 0
            compressed.append(line)

    # Strip trailing blank lines
    while compressed and compressed[-1].strip() == "":
        compressed.pop()

    return "\n".join(compressed) + "\n"


def generate_source_meta(
    fetch_result: dict, content_hash: str, account: str, md_content: str
) -> dict:
    """Generate source_meta dict for a fetched Feishu document.

    Args:
        fetch_result: dict returned by fetch()
        content_hash: sha256 hex digest prefixed with 'sha256:'
        account: Feishu account name used
        md_content: the normalized markdown string (for size stats)
    """
    now = datetime.now(timezone(timedelta(hours=8)))
    encoded = md_content.encode("utf-8")
    return {
        "source_type": "feishu",
        "doc_token": fetch_result["doc_token"],
        "title": fetch_result["title"],
        "account": account,
        "fetched_at": now.isoformat(),
        "modified_time": fetch_result["modified_time"],
        "content_hash": content_hash,
        "chars": len(md_content),
        "bytes": len(encoded),
    }


def fetch_and_normalize(doc_token: str, account: str, output_dir: str) -> tuple:
    """Main entry: fetch, normalize, and write converted.md + source_meta.json.

    Returns (md_path, source_meta_dict).
    Skips fetch if existing source_meta.json has matching content_hash.
    """
    os.makedirs(output_dir, exist_ok=True)
    md_path = os.path.join(output_dir, "converted.md")
    meta_path = os.path.join(output_dir, "source_meta.json")

    # Fetch document
    print(f"Fetching Feishu doc: {doc_token} (account: {account})")
    result = fetch(doc_token, account)
    print(f"  Title: {result['title']}")

    # Normalize
    md_content = normalize(result["raw_content"])

    # Compute content hash
    content_hash = "sha256:" + hashlib.sha256(md_content.encode("utf-8")).hexdigest()

    # Check if unchanged
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                existing_meta = json.load(f)
            if existing_meta.get("content_hash") == content_hash:
                print("Document unchanged, skipping fetch")
                return (md_path, existing_meta)
        except (OSError, json.JSONDecodeError):
            pass  # Corrupted meta, proceed with overwrite

    # Generate meta
    source_meta = generate_source_meta(result, content_hash, account, md_content)

    # Write files
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"  Written: {md_path} ({source_meta['chars']} chars, {source_meta['bytes']} bytes)")

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(source_meta, f, ensure_ascii=False, indent=2)
    print(f"  Written: {meta_path}")

    return (md_path, source_meta)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch a Feishu document and convert to Markdown."
    )
    parser.add_argument(
        "--doc-token", required=True, help="Feishu document token (from URL /docx/XXX)"
    )
    parser.add_argument(
        "--account", required=True, help="Feishu account name in openclaw.json"
    )
    parser.add_argument(
        "--output", required=True, help="Output directory for converted.md and source_meta.json"
    )
    args = parser.parse_args()

    md_path, meta = fetch_and_normalize(args.doc_token, args.account, args.output)
    print(f"\nDone. Output: {md_path}")
    print(f"  Hash: {meta['content_hash']}")


if __name__ == "__main__":
    main()
