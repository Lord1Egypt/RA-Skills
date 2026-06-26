#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)
LIST_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")
SECRET_FIELD_WITH_VALUE_RE = re.compile(
    r"(?i)\b(?:api[ _-]?key|access[ _-]?key|client[ _-]?secret|refresh[ _-]?token|private[ _-]?key|password|token)\b.{0,24}(?::|=)\s*['\"]?[A-Za-z0-9_\-./+=]{8,}"
)
BEARER_VALUE_RE = re.compile(r"(?i)\bbearer\s+[A-Za-z0-9_\-./+=]{8,}")


def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, False
    data = {}
    current_key = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        list_match = LIST_ITEM_RE.match(line)
        if list_match and current_key:
            data.setdefault(current_key, []).append(list_match.group(1).strip())
            continue
        if ":" not in line:
            current_key = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        current_key = key
        if value == "":
            data[key] = []
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [part.strip().strip('"\'') for part in inner.split(",") if part.strip()]
        elif value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value.strip('"\'')
    return data, True


def strip_frontmatter(text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return text
    return text[match.end():]


def normalized_text_hash(text: str) -> str:
    normalized = strip_frontmatter(text).replace("\r\n", "\n").replace("\r", "\n").strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def looks_sensitive_pending_verification(text: str) -> bool:
    body = strip_frontmatter(text)
    if SECRET_FIELD_WITH_VALUE_RE.search(body):
        return True
    if BEARER_VALUE_RE.search(body):
        return True
    return False


def iter_markdown_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".obsidian", ".git", ".trash", "node_modules"}]
        for filename in filenames:
            if filename.lower().endswith(".md"):
                yield os.path.join(dirpath, filename)


def relpath(path: str, root: str):
    return os.path.relpath(path, root)


def bucket_name(path: str, root: str):
    rel = relpath(path, root)
    parts = rel.split(os.sep)
    return parts[0] if len(parts) > 1 else "."


def main():
    parser = argparse.ArgumentParser(description="Inventory one Obsidian/Markdown vault slice.")
    parser.add_argument("target", help="Folder or note path to inspect")
    args = parser.parse_args()

    root = os.path.abspath(args.target)
    if not os.path.exists(root):
        raise SystemExit(f"Target not found: {root}")

    files = [root] if os.path.isfile(root) else sorted(iter_markdown_files(root))
    if not files:
        raise SystemExit(f"No markdown files found in target: {root}")
    status_counts = Counter()
    doc_kind_counts = Counter()
    missing_status = []
    missing_doc_kind = []
    missing_frontmatter = []
    canonical = []
    by_title = defaultdict(list)
    by_content_hash = defaultdict(list)
    sensitive_candidates = []
    top_level_buckets = Counter()

    for path in files:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
        fm, has_frontmatter = parse_frontmatter(text)
        rel = relpath(path, os.path.dirname(root) if os.path.isfile(root) else root)
        title = os.path.splitext(os.path.basename(path))[0]
        by_title[title.lower()].append(rel)
        by_content_hash[normalized_text_hash(text)].append(rel)
        if not os.path.isfile(root):
            top_level_buckets[bucket_name(path, root)] += 1
        if not has_frontmatter:
            missing_frontmatter.append(rel)
        status = fm.get("status")
        doc_kind = fm.get("doc_kind")
        if status:
            status_counts[str(status)] += 1
        else:
            missing_status.append(rel)
        if doc_kind:
            doc_kind_counts[str(doc_kind)] += 1
        else:
            missing_doc_kind.append(rel)
        if fm.get("canonical") is True or str(fm.get("canonical", "")).lower() == "true":
            canonical.append(rel)
        if looks_sensitive_pending_verification(text):
            sensitive_candidates.append(rel)

    duplicates = {k: v for k, v in by_title.items() if len(v) > 1}
    exact_duplicates = sorted(sorted(paths) for paths in by_content_hash.values() if len(paths) > 1)
    report = {
        "target": root,
        "notes": len(files),
        "status_counts": dict(status_counts),
        "doc_kind_counts": dict(doc_kind_counts),
        "missing_frontmatter": missing_frontmatter,
        "missing_status": missing_status,
        "missing_doc_kind": missing_doc_kind,
        "canonical": canonical,
        "duplicate_titles": duplicates,
        "duplicate_exact_content": exact_duplicates,
        "sensitive_candidates_pending_verification": sensitive_candidates,
        "top_level_buckets": dict(top_level_buckets),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
